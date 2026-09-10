import sys
import os
import asyncio
from datetime import datetime, timedelta, timezone

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
from app.database.connection import SupabaseCollection
from app.services.gmail import generate_mock_emails

async def seed():
    url = settings.SUPABASE_URL
    key = settings.effective_supabase_key
    if not url or not key:
        print("[ERR] SUPABASE_URL or SUPABASE_KEY is missing in settings!")
        return

    print(f"[Supabase Seeder] Connecting to {url}...")
    user_email = "demo@example.com"

    # 1. Users
    users_col = SupabaseCollection("users", url, key)
    user_doc = {
        "email": user_email,
        "name": "Demo User",
        "picture": "https://lh3.googleusercontent.com/a/default-user=s96-c",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await users_col.insert_one(user_doc)
    print("[OK] Seeded users table")

    # 2. Emails
    emails_col = SupabaseCollection("emails", url, key)
    raw_emails = generate_mock_emails(user_email)

    for email in raw_emails:
        # Add classification & AI summary fields if not present
        if "category" not in email:
            email["category"] = "Work"
        if "priority" not in email:
            email["priority"] = "High"
        if "summary" not in email:
            email["summary"] = {
                "key_points": [email.get("subject", "")],
                "action_required": False,
                "urgency_level": "Medium"
            }
        await emails_col.insert_one(email)
    print(f"[OK] Seeded {len(raw_emails)} sample emails into emails table")

    # 3. Settings
    settings_col = SupabaseCollection("settings", url, key)
    settings_doc = {
        "_id": "default_settings",
        "user_email": user_email,
        "theme": "light",
        "language": "en",
        "auto_reply_enabled": True,
        "default_reply_tone": "Professional",
        "notification_settings": {
            "urgent": True,
            "boss": True,
            "reminders": True,
            "deadlines": True
        },
        "critical_contacts": ["boss@company.com", "manager@company.com", "hr@company.com"]
    }
    await settings_col.insert_one(settings_doc)
    print("[OK] Seeded settings table")

    # 4. Notifications
    notif_col = SupabaseCollection("notifications", url, key)
    notifs = [
        {
            "_id": "notif_001",
            "user_email": user_email,
            "title": "Urgent Email Detected",
            "message": "High-priority message received from VP Engineering.",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "is_read": False
        },
        {
            "_id": "notif_002",
            "user_email": user_email,
            "title": "Meeting Scheduled",
            "message": "Mandatory Cybersecurity Training tomorrow at 10:00 AM.",
            "timestamp": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
            "is_read": True
        }
    ]
    for n in notifs:
        await notif_col.insert_one(n)
    print(f"[OK] Seeded {len(notifs)} items into notifications table")

    # 5. Analytics
    analytics_col = SupabaseCollection("analytics", url, key)
    analytics_doc = {
        "_id": "api_usage",
        "user_email": user_email,
        "gemini_calls": 142,
        "gmail_calls": 384,
        "ocr_calls": 24,
        "total_users": 1,
        "error_count": 2,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }
    await analytics_col.insert_one(analytics_doc)
    print("[OK] Seeded analytics table")

    # 6. Logs
    logs_col = SupabaseCollection("logs", url, key)
    log_doc = {
        "_id": "log_001",
        "user_email": user_email,
        "action": "SYSTEM_SEED",
        "details": "Initial Supabase cloud database seeding executed successfully.",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    await logs_col.insert_one(log_doc)
    print("[OK] Seeded logs table")

    print("\n[SUCCESS] ALL TABLES SUCCESSFULLY SEEDED ON SUPABASE DATABASE!")

if __name__ == "__main__":
    asyncio.run(seed())
