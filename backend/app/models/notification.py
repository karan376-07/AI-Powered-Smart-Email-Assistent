from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

class SystemNotification(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_email: str
    email_id: Optional[str] = None
    type: str # "urgent", "boss", "meeting", "payment", "deadline", "interview"
    title: str
    message: str
    is_read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
