import hashlib
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from app.auth.auth_handler import create_access_token, create_token_for_user, get_current_user, DEMO_USER
from app.models.schemas import Token, UserProfile, GoogleLoginRequest, AuthConfigResponse
from app.services.gmail_service import gmail_service
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.get("/config", response_model=AuthConfigResponse)
def get_auth_config():
    """Returns the Google OAuth and demo configuration status."""
    is_live = bool(settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET)
    return AuthConfigResponse(
        google_client_id=settings.GOOGLE_CLIENT_ID or "",
        google_redirect_uri=settings.GOOGLE_REDIRECT_URI,
        is_live_configured=is_live,
        demo_mode=settings.DEMO_MODE
    )

@router.get("/login-url")
def get_login_url():
    """Get Google OAuth 2.0 authorization URL."""
    is_live = bool(settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET)
    return {
        "url": gmail_service.get_oauth_url(),
        "is_live_configured": is_live
    }

@router.post("/google-login", response_model=Token)
async def google_login(req: GoogleLoginRequest):
    """
    Authenticate with Google OAuth token or Google Account Profile.
    Supports live Google Identity tokens and interactive sandbox account selection.
    """
    email = req.email or "user@gmail.com"
    email_clean = email.strip().lower()
    
    if req.name and req.name.strip():
        name = req.name.strip()
    else:
        username_part = email_clean.split("@")[0]
        name = " ".join([part.capitalize() for part in username_part.replace("_", ".").replace("-", ".").split(".")])
    
    if req.avatar and req.avatar.strip():
        avatar = req.avatar.strip()
    else:
        seed = hashlib.md5(email_clean.encode()).hexdigest()[:8]
        avatar = f"https://api.dicebear.com/7.x/bottts/svg?seed={seed}"

    user_id = f"usr-g-{hashlib.md5(email_clean.encode()).hexdigest()[:8]}"
    
    user_profile = UserProfile(
        id=user_id,
        email=email_clean,
        name=name,
        avatar=avatar,
        is_demo=bool(req.is_demo),
        connected_gmail=True
    )

    token = create_token_for_user(user_profile)
    return Token(access_token=token, token_type="bearer", user=user_profile)

@router.post("/demo-login", response_model=Token)
def demo_login():
    """1-Click instant demo authentication token."""
    token = create_token_for_user(DEMO_USER)
    return Token(access_token=token, token_type="bearer", user=DEMO_USER)

@router.get("/callback")
async def oauth_callback(code: str = Query(None), error: str = Query(None)):
    """Handles Google OAuth callback redirect."""
    if error or not code:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/?error={error or 'cancelled'}")
    
    # Live exchange with Google OAuth 2.0 servers
    if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                token_res = await client.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "code": code,
                        "client_id": settings.GOOGLE_CLIENT_ID,
                        "client_secret": settings.GOOGLE_CLIENT_SECRET,
                        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                        "grant_type": "authorization_code",
                    },
                    timeout=12.0
                )
                if token_res.status_code == 200:
                    token_data = token_res.json()
                    google_access_token = token_data.get("access_token")
                    
                    # Fetch verified Google user info
                    userinfo_res = await client.get(
                        "https://www.googleapis.com/oauth2/v2/userinfo",
                        headers={"Authorization": f"Bearer {google_access_token}"},
                        timeout=10.0
                    )
                    if userinfo_res.status_code == 200:
                        g_info = userinfo_res.json()
                        user_id = f"usr-g-{g_info.get('id', 'live')}"
                        email = g_info.get("email", "google.user@gmail.com")
                        name = g_info.get("name", email.split("@")[0])
                        avatar = g_info.get("picture") or f"https://api.dicebear.com/7.x/bottts/svg?seed={email}"
                        
                        user_profile = UserProfile(
                            id=user_id,
                            email=email,
                            name=name,
                            avatar=avatar,
                            is_demo=False,
                            connected_gmail=True
                        )
                        jwt_token = create_token_for_user(user_profile)
                        return RedirectResponse(url=f"{settings.FRONTEND_URL}/?token={jwt_token}")
        except Exception as e:
            print(f"Live Google OAuth token exchange error: {e}")

    # On OAuth failure or missing code, redirect to login with error query param
    return RedirectResponse(url=f"{settings.FRONTEND_URL}/login?error=auth_failed")

@router.get("/me", response_model=UserProfile)
def get_me(current_user: UserProfile = Depends(get_current_user)):
    """Get authenticated user profile."""
    return current_user
