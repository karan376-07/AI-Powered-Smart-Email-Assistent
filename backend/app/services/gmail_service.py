import time
import random
from typing import List, Dict, Any, Optional
from app.config import settings
from app.models.schemas import EmailItem, CategoryEnum, PriorityEnum, EmailSummary, ActionItem, AttachmentInfo
from app.database.db import db
from app.services.gemini_service import gemini_service

class GmailService:
    @property
    def client_id(self):
        return settings.GOOGLE_CLIENT_ID

    @property
    def client_secret(self):
        return settings.GOOGLE_CLIENT_SECRET

    @property
    def redirect_uri(self):
        return settings.GOOGLE_REDIRECT_URI

    def get_oauth_url(self) -> str:
        """Returns Google OAuth 2.0 authorization URL."""
        if not self.client_id:
            # Return demo callback URL
            return f"{settings.FRONTEND_URL}/login?demo_auth=true"
        
        scopes = [
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"
        ]
        scope_str = "%20".join(scopes)
        return (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={self.client_id}&"
            f"redirect_uri={self.redirect_uri}&"
            f"response_type=code&"
            f"scope={scope_str}&"
            f"access_type=offline&"
            f"prompt=consent"
        )

    async def sync_inbox(self) -> Dict[str, Any]:
        """Simulates or fetches real new incoming emails and runs AI pipelines."""
        now = time.time()
        
        # Batch of dynamic incoming emails to simulate inbox updates
        incoming_pool = [
            {
                "sender_name": "DevOps Watchdog Alert",
                "sender_email": "alerts@datadoghq.com",
                "subject": "ALERT: High Memory Utilization on Primary Redis Cluster (92%)",
                "body": """Datadog Monitor Alert:
Cluster: prod-redis-cluster-01
Metric: memory.used_percent > 90% (Current: 92.4%)
Threshold: 90% breached for 5 minutes.

Please investigate connection pool saturation or scale Redis cache nodes immediately.""",
                "category": CategoryEnum.WORK,
                "priority": PriorityEnum.HIGH,
                "has_att": False,
                "att": []
            },
            {
                "sender_name": "Amazon Business Orders",
                "sender_email": "auto-confirm@amazon.com",
                "subject": "Order Confirmed: Ergonomic Workstation Monitor & USB-C Dock",
                "body": """Hello Karan,

Your purchase order #408-9821245-1102914 has been confirmed.
Estimated Delivery: Tomorrow by 8:00 PM.

Item: 34-inch Curved UltraWide Monitor (4K HDR)
Total: $549.99 USD
Tracking Link: https://amazon.com/orders/track/4089821245""",
                "category": CategoryEnum.UPDATES,
                "priority": PriorityEnum.LOW,
                "has_att": True,
                "att": [
                    AttachmentInfo(
                        id=f"att-{random.randint(1000, 9999)}",
                        filename="Amazon_Order_Receipt_40898.pdf",
                        size="310 KB",
                        content_type="application/pdf",
                        extracted_text="AMAZON ORDER RECEIPT\nOrder #408-9821245-1102914\nTotal: $549.99 USD\nDelivery: Tomorrow 8:00 PM\nPayment: Master Card ending in 1904"
                    )
                ]
            },
            {
                "sender_name": "Alex Rivera (Frontend Tech Lead)",
                "sender_email": "alex.rivera@techcorp.io",
                "subject": "Design Review: AI Email Assistant Dark Mode & Glassmorphism UI",
                "body": """Hi Karan,

I just finished testing the Vite + React frontend for our AI Smart Email Assistant! The Framer Motion animations and dark glass UI look super slick.

Quick questions:
1. Should we add keyboard shortcuts (like 'J' and 'K' for email navigation)?
2. The OCR attachment scanner component is working great. Can we add a sample document preview button for demo testers?

Let's do a quick 10-minute huddle at 3:30 PM today if you're free.

Best,
Alex""",
                "category": CategoryEnum.WORK,
                "priority": PriorityEnum.MEDIUM,
                "has_att": False,
                "att": []
            }
        ]

        # Pick one to add if not already in DB
        added_count = 0
        for sample in incoming_pool:
            email_id = f"em-{abs(hash(sample['subject'])) % 10000}"
            if email_id not in db.emails:
                # Run AI analysis on incoming email
                ai_analysis = await gemini_service.analyze_and_summarize_email(
                    subject=sample["subject"],
                    body=sample["body"],
                    sender=sample["sender_name"]
                )
                
                new_email = EmailItem(
                    id=email_id,
                    sender_name=sample["sender_name"],
                    sender_email=sample["sender_email"],
                    subject=sample["subject"],
                    snippet=sample["body"][:120] + "...",
                    body=sample["body"],
                    category=sample["category"],
                    priority=sample["priority"],
                    date="Just now",
                    timestamp=now,
                    is_read=False,
                    is_starred=False,
                    has_attachments=sample["has_att"],
                    attachments=sample["att"],
                    summary=EmailSummary(
                        bullet_points=ai_analysis.get("bullet_points", [sample["subject"]]),
                        one_liner=ai_analysis.get("one_liner", sample["subject"]),
                        urgency_reason=ai_analysis.get("urgency_reason"),
                        sentiment=ai_analysis.get("sentiment", "Neutral"),
                        key_deadlines=ai_analysis.get("deadlines", [])
                    ),
                    action_items=[
                        ActionItem(
                            task=item["task"],
                            due_date=item.get("due_date"),
                            completed=False,
                            is_meeting=item.get("is_meeting", False),
                            meeting_time=item.get("meeting_time")
                        ) for item in ai_analysis.get("action_items", [])
                    ],
                    folder="inbox"
                )
                db.add_email(new_email)
                added_count += 1
                break

        return {
            "status": "success",
            "synced_emails_count": added_count,
            "message": f"Inbox sync completed. {added_count} new email(s) processed and analyzed by AI."
        }

gmail_service = GmailService()
