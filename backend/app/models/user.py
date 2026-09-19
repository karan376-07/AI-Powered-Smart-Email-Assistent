from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

class UserSettings(BaseModel):
    theme: str = "dark"
    language: str = "en"
    notifications_enabled: bool = True
    critical_contacts: List[str] = ["boss@company.com", "manager@company.com", "ceo@company.com"]
    categories_custom_rules: Dict[str, List[str]] = Field(default_factory=dict)

class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    email: EmailStr
    name: str
    picture: Optional[str] = None
    google_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    settings: UserSettings = Field(default_factory=UserSettings)
    gmail_credentials: Optional[Dict[str, Any]] = None # stores refresh token and scope access
