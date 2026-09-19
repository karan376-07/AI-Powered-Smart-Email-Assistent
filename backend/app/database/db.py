import time
import copy
from typing import List, Optional, Dict, Any
from app.models.schemas import EmailItem, CategoryEnum, PriorityEnum, EmailSummary, ActionItem, AttachmentInfo
from app.config import settings

try:
    from supabase import create_client, Client
except ImportError:
    create_client, Client = None, None

# In-memory realistic dataset with robust CRUD operations and Supabase Cloud Sync
class Database:
    def __init__(self):
        self.emails: Dict[str, EmailItem] = {}
        self.settings: Dict[str, Any] = {
            "demo_mode": True,
            "gemini_api_key": "",
            "auto_reply_enabled": True,
            "default_reply_tone": "Professional",
            "connected_gmail": False,
            "sync_interval_mins": 15
        }
        self.supabase: Optional[Any] = None
        self._init_supabase()
        self.seed_initial_data()

    def _init_supabase(self):
        """Initialize Supabase Cloud Client if credentials are provided."""
        base_url = settings.supabase_base_url
        key = settings.SUPABASE_KEY
        if base_url and key and create_client:
            try:
                self.supabase = create_client(base_url, key)
                print(f"[Supabase] Connected to Supabase Cloud Database at {base_url}")
            except Exception as e:
                print(f"[Supabase] Notice: Cloud client init: {e}")

    def seed_initial_data(self):
        now = time.time()
        
        sample_emails = [
            EmailItem(
                id="em-101",
                sender_name="Sarah Jenkins (VP of Engineering)",
                sender_email="sarah.jenkins@techcorp.io",
                recipient_email="karan.assistant@work.com",
                subject="URGENT: Production API Migration Deadline & Deployment Plan",
                snippet="Team, we have to finalize the Q3 Kubernetes migration by Thursday 5:00 PM EST. Please review the attached execution sheet...",
                body="""Hi Karan,

We need your immediate attention on the Q3 Production API Migration.

Key Objectives:
1. Complete staging traffic split testing by Wednesday 2:00 PM.
2. Final sign-off on the rollback strategy before Thursday morning.
3. Live cutover scheduled for Thursday 5:00 PM EST.

Please verify if all the microservice health check monitors in Datadog are active. We cannot afford any downtime during peak customer hours.

Let me know if there are any blockers or dependency lags.

Best regards,
Sarah Jenkins
VP of Engineering | TechCorp Inc.""",
                category=CategoryEnum.WORK,
                priority=PriorityEnum.HIGH,
                date="Today, 10:15 AM",
                timestamp=now - 3600 * 2,
                is_read=False,
                is_starred=True,
                is_spam=False,
                has_attachments=True,
                attachments=[
                    AttachmentInfo(
                        id="att-101",
                        filename="Migration_Deployment_Plan_v3.pdf",
                        size="1.4 MB",
                        content_type="application/pdf",
                        extracted_text="""TECHCORP ENGINEERING - MIGRATION RUNBOOK
Document: v3.2 Production Cutover
Target Date: Thursday 17:00 EST
Pre-requisites:
- Database replication sync lag < 100ms
- DNS TTL reduced to 60s
- Staging test coverage report signed off by QA
Total Estimated Downtime: 0 mins (Blue/Green Deployment)
Rollback trigger: Error rate > 0.05% for 3 consecutive minutes."""
                    )
                ],
                summary=EmailSummary(
                    bullet_points=[
                        "Q3 Kubernetes and API production migration must be finalized by Thursday 5:00 PM EST.",
                        "Staging split testing must be verified by Wednesday 2:00 PM.",
                        "Rollback procedures and Datadog health checks require immediate confirmation."
                    ],
                    one_liner="Critical deployment deadline for Q3 API migration on Thursday 5:00 PM EST.",
                    urgency_reason="Direct VP engineering request with strict hard deadline and production impact.",
                    sentiment="Urgent",
                    key_deadlines=["Wednesday 2:00 PM EST (Testing)", "Thursday 5:00 PM EST (Live Cutover)"]
                ),
                action_items=[
                    ActionItem(
                        task="Confirm Datadog health check monitors are active",
                        due_date="Wednesday 12:00 PM",
                        completed=False,
                        is_meeting=False
                    ),
                    ActionItem(
                        task="Review rollback strategy and deployment plan",
                        due_date="Thursday 10:00 AM",
                        completed=False,
                        is_meeting=False
                    ),
                    ActionItem(
                        task="Production Migration Live Cutover",
                        due_date="Thursday 5:00 PM",
                        completed=False,
                        is_meeting=True,
                        meeting_time="Thursday 5:00 PM - 6:30 PM EST"
                    )
                ],
                folder="inbox"
            ),
            EmailItem(
                id="em-102",
                sender_name="Stripe Billing & Invoicing",
                sender_email="invoices@stripe.com",
                recipient_email="karan.assistant@work.com",
                subject="Invoice #INV-2026-8910 Payment Confirmation & Breakdown",
                snippet="Thank you for your payment. Your receipt for cloud infrastructure compute and Gemini API usage is ready...",
                body="""Hello,

Your monthly invoice for Tech Stack Compute & AI API Services is now processed.

Invoice Details:
- Invoice Number: INV-2026-8910
- Billing Period: August 1 - August 31, 2026
- Total Amount Paid: $342.50 USD
- Payment Method: Visa ending in 4242

A detailed itemized statement has been attached to this email as a PDF. You can view your payment history and download tax receipts anytime from the Stripe Dashboard.

Thank you for choosing Stripe.
The Stripe Billing Team""",
                category=CategoryEnum.FINANCE,
                priority=PriorityEnum.LOW,
                date="Today, 8:30 AM",
                timestamp=now - 3600 * 5,
                is_read=True,
                is_starred=False,
                is_spam=False,
                has_attachments=True,
                attachments=[
                    AttachmentInfo(
                        id="att-102",
                        filename="Invoice_INV-2026-8910.pdf",
                        size="420 KB",
                        content_type="application/pdf",
                        extracted_text="""STRIPE INVOICE / RECEIPT
Invoice Number: INV-2026-8910
Date Issued: Sep 1, 2026
Customer: Karan / Smart Email Assistant Team
Item 1: Gemini 1.5 Flash High-Throughput API Tokens: $184.20
Item 2: Render Enterprise Web Service Host: $70.00
Item 3: Supabase PostgreSQL Managed Cluster: $88.30
Subtotal: $342.50
Tax: $0.00
TOTAL PAID: $342.50 USD
Status: PAID IN FULL"""
                    )
                ],
                summary=EmailSummary(
                    bullet_points=[
                        "Monthly invoice of $342.50 USD successfully paid via Stripe.",
                        "Covers Gemini API tokens, Render hosting, and Supabase database.",
                        "No action required; payment processed automatically."
                    ],
                    one_liner="Receipt confirmation for $342.50 monthly cloud infrastructure invoice.",
                    urgency_reason="Informational billing receipt already settled.",
                    sentiment="Positive",
                    key_deadlines=[]
                ),
                action_items=[
                    ActionItem(
                        task="File invoice receipt in expense management folder",
                        due_date="End of Month",
                        completed=True,
                        is_meeting=False
                    )
                ],
                folder="inbox"
            ),
            EmailItem(
                id="em-103",
                sender_name="David Miller (Product Lead)",
                sender_email="david.miller@techcorp.io",
                recipient_email="karan.assistant@work.com",
                subject="Sprint Planning & AI Roadmap Sync Meeting - Friday 11:00 AM",
                snippet="Hey Karan, let's sync up this Friday to review the user feedback on the smart email summarizer and prioritize backlog items...",
                body="""Hey Karan,

Hope your week is going great!

We have scheduled our bi-weekly Sprint Planning & AI Feature Alignment session for this Friday at 11:00 AM IST on Google Meet.

Agenda:
1. Review AI categorization accuracy metrics from beta testers.
2. Demo the new OCR PDF Attachment scanner pipeline.
3. Discuss roadmap for multi-account mailbox integration.

Please bring the latency benchmarks for the Gemini 1.5 Flash integration.

Google Meet link: https://meet.google.com/xyz-abcd-efg

Cheers,
David Miller
Lead Product Manager""",
                category=CategoryEnum.WORK,
                priority=PriorityEnum.MEDIUM,
                date="Yesterday, 4:45 PM",
                timestamp=now - 3600 * 20,
                is_read=True,
                is_starred=True,
                is_spam=False,
                has_attachments=False,
                attachments=[],
                summary=EmailSummary(
                    bullet_points=[
                        "Sprint planning and AI roadmap review scheduled for Friday at 11:00 AM IST on Google Meet.",
                        "Agenda covers AI categorization accuracy, OCR scanner demo, and roadmap priorities.",
                        "Need to prepare Gemini 1.5 Flash latency benchmarks."
                    ],
                    one_liner="Invitation to Sprint Planning & AI Roadmap sync on Friday 11:00 AM IST.",
                    urgency_reason="Upcoming team sprint sync requiring demo preparation.",
                    sentiment="Positive",
                    key_deadlines=["Friday 11:00 AM IST (Sprint Sync)"]
                ),
                action_items=[
                    ActionItem(
                        task="Prepare Gemini 1.5 Flash latency benchmark metrics",
                        due_date="Friday 10:00 AM",
                        completed=False,
                        is_meeting=False
                    ),
                    ActionItem(
                        task="Attend Sprint Planning Meeting",
                        due_date="Friday 11:00 AM",
                        completed=False,
                        is_meeting=True,
                        meeting_time="Friday 11:00 AM - 12:00 PM IST"
                    )
                ],
                folder="inbox"
            ),
            EmailItem(
                id="em-104",
                sender_name="Security Alert (Google Cloud)",
                sender_email="no-reply-accounts@google-security-verify.xyz",
                recipient_email="karan.assistant@work.com",
                subject="CRITICAL: Your Google Workspace account will be terminated in 24 hours!",
                snippet="Dear user, unauthorized access was detected from IP 185.220.101.4. Click here immediately to verify your identity...",
                body="""ATTENTION USER,

Your email account has violated Google Cloud Terms of Service. If you do not verify your login credentials within 24 hours, all your stored emails and drive files will be permanently deleted.

CLICK HERE TO RESTORE YOUR ACCOUNT:
http://malicious-phishing-link.fake-security.xyz/login?user=karan

Do not ignore this warning.
Google Security Trust Team.""",
                category=CategoryEnum.SPAM,
                priority=PriorityEnum.HIGH,
                date="Yesterday, 2:10 PM",
                timestamp=now - 3600 * 24,
                is_read=False,
                is_starred=False,
                is_spam=True,
                has_attachments=False,
                attachments=[],
                summary=EmailSummary(
                    bullet_points=[
                        "Phishing attempt detected: Spoofed domain (google-security-verify.xyz).",
                        "Contains coercive urgency language and suspicious external link.",
                        "AI Spam Filter has safely isolated this message."
                    ],
                    one_liner="Detected phishing attack attempting credential theft.",
                    urgency_reason="Malicious security hazard - blocked by AI shield.",
                    sentiment="Urgent",
                    key_deadlines=[]
                ),
                action_items=[],
                folder="spam"
            ),
            EmailItem(
                id="em-105",
                sender_name="Emily Zhao (Senior Legal Counsel)",
                sender_email="emily.zhao@lexislegal.com",
                recipient_email="karan.assistant@work.com",
                subject="Master Service Agreement (MSA) - Final Revisions for Signature",
                snippet="Hi Karan, attached is the finalized MSA incorporating the indemnity clauses and IP assignments we agreed on...",
                body="""Dear Karan,

Following our discussion with the enterprise client, I have updated the Master Service Agreement (MSA).

Major updates:
- Section 4.2: Standard 30-day payment term agreed.
- Section 8.1: Mutual confidentiality and non-disclosure extended to 3 years.
- Section 12: IP ownership explicitly retained by our development entity.

Please review the attached contract, sign on page 14 via DocuSign or physical scan, and return it by Monday 5:00 PM.

Warm regards,
Emily Zhao
Partner | Lexis Legal Group""",
                category=CategoryEnum.WORK,
                priority=PriorityEnum.HIGH,
                date="Sep 5, 2026",
                timestamp=now - 3600 * 48,
                is_read=False,
                is_starred=True,
                is_spam=False,
                has_attachments=True,
                attachments=[
                    AttachmentInfo(
                        id="att-105",
                        filename="Enterprise_MSA_Final_Clean.pdf",
                        size="2.8 MB",
                        content_type="application/pdf",
                        extracted_text="""MASTER SERVICES AGREEMENT
Between: Enterprise Client Corp AND TechCorp Provider
Effective Date: September 2026
Term: 24 Months
Governing Law: State of Delaware
Key Covenants:
1. Provider retains all background IP and AI model weights.
2. Net 30 days billing terms with 1.5% monthly late fee.
3. Liability cap limited to 12 months fees paid.
Signature Required: Karan (Authorised Signatory)"""
                    )
                ],
                summary=EmailSummary(
                    bullet_points=[
                        "Finalized Master Service Agreement (MSA) ready for legal execution.",
                        "IP ownership clauses and Net 30 payment terms successfully locked in.",
                        "Requires signature on page 14 and return by Monday 5:00 PM."
                    ],
                    one_liner="Action required: Review and sign finalized Enterprise MSA by Monday 5:00 PM.",
                    urgency_reason="High priority contract with external client pending signature.",
                    sentiment="Neutral",
                    key_deadlines=["Monday 5:00 PM (Return Signed MSA)"]
                ),
                action_items=[
                    ActionItem(
                        task="Review MSA Section 4 & 12 terms",
                        due_date="Monday 1:00 PM",
                        completed=False,
                        is_meeting=False
                    ),
                    ActionItem(
                        task="Execute signature on page 14 of MSA",
                        due_date="Monday 5:00 PM",
                        completed=False,
                        is_meeting=False
                    )
                ],
                folder="inbox"
            ),
            EmailItem(
                id="em-106",
                sender_name="GitHub Notifications",
                sender_email="notifications@github.com",
                recipient_email="karan.assistant@work.com",
                subject="[karan376-07/AI-Powered-Smart-Email-Assistant] Pull Request #14 merged into main",
                snippet="karan376-07 merged commit 4f0cedd into main: Add full-stack smart email assistant with AI summarizer and OCR...",
                body="""GitHub
Repository: karan376-07/AI-Powered-Smart-Email-Assistent
Branch: main

Pull Request #14: "Add full-stack smart email assistant with AI summarizer, OCR attachment scanner, and analytics dashboard" was successfully merged by karan376-07.

Summary of changes:
+ 45 files changed, 3,420 insertions(+), 12 deletions(-)
+ Automated CI / Unit test suites: 100% Passed
+ Lighthouse accessibility score: 98/100

View PR details: https://github.com/karan376-07/AI-Powered-Smart-Email-Assistent/pull/14""",
                category=CategoryEnum.UPDATES,
                priority=PriorityEnum.LOW,
                date="Sep 4, 2026",
                timestamp=now - 3600 * 72,
                is_read=True,
                is_starred=False,
                is_spam=False,
                has_attachments=False,
                attachments=[],
                summary=EmailSummary(
                    bullet_points=[
                        "PR #14 successfully merged into main branch on GitHub.",
                        "All CI and accessibility test suites passed with green status.",
                        "Contains the full-stack AI smart email features."
                    ],
                    one_liner="Pull Request #14 merged into main repository branch with passing tests.",
                    urgency_reason="Informational developer notification.",
                    sentiment="Positive",
                    key_deadlines=[]
                ),
                action_items=[],
                folder="inbox"
            ),
            EmailItem(
                id="em-107",
                sender_name="Morning Brew Newsletter",
                sender_email="crew@morningbrew.com",
                recipient_email="karan.assistant@work.com",
                subject="☕ The AI Boom, Tech Venture Trends & This Week's Market Wrap",
                snippet="Grab your coffee: Generative AI adoption surges in enterprise workflow automation, major tech earnings results...",
                body="""Good morning!

Here is what's shaking up the tech world today:

1. Enterprise AI Assistants: Companies report 40% reduction in email triage time by deploying specialized LLM classifiers and OCR summarizers.
2. Cloud Infrastructure: Next-gen microservices are shifting toward hybrid edge deployments.
3. Market Highlights: S&P 500 holds steady amid strong tech earnings reports.

Read full edition online: https://morningbrew.com/daily/latest

Have an awesome day ahead!""",
                category=CategoryEnum.NEWSLETTER,
                priority=PriorityEnum.LOW,
                date="Sep 3, 2026",
                timestamp=now - 3600 * 96,
                is_read=True,
                is_starred=False,
                is_spam=False,
                has_attachments=False,
                attachments=[],
                summary=EmailSummary(
                    bullet_points=[
                        "Weekly tech & business news recap.",
                        "Spotlight on enterprise AI email assistant productivity gains (40% time saved).",
                        "Cloud microservice deployment trends."
                    ],
                    one_liner="Morning Brew tech news roundup on enterprise AI automation.",
                    urgency_reason="Reading material / newsletter.",
                    sentiment="Positive",
                    key_deadlines=[]
                ),
                action_items=[],
                folder="inbox"
            )
        ]

        for email in sample_emails:
            self.emails[email.id] = email

    def get_emails(
        self,
        folder: str = "inbox",
        category: Optional[str] = None,
        priority: Optional[str] = None,
        search: Optional[str] = None,
        unread_only: bool = False,
        starred_only: bool = False,
        has_attachments: Optional[bool] = None,
        user_email: Optional[str] = None
    ) -> List[EmailItem]:
        clean_user = (user_email or "").strip().lower()
        demo_accounts = {"demo.user@gmail.com", "user@gmail.com", "sarah.jenkins@gmail.com", "alex.rivera@techcorp.io", "karan@gmail.com", "karan.assistant@work.com"}

        # If user is a custom non-demo user, check if we need to seed a personalized welcome email for them
        if clean_user and clean_user not in demo_accounts:
            user_has_emails = any(
                (getattr(e, 'recipient_email', '') or '').lower() == clean_user or
                (getattr(e, 'sender_email', '') or '').lower() == clean_user
                for e in self.emails.values()
            )
            if not user_has_emails:
                username = clean_user.split('@')[0].replace('.', ' ').replace('_', ' ').replace('-', ' ').title()
                welcome_id = f"em-welcome-{abs(hash(clean_user)) % 10000}"
                now = time.time()
                welcome_email = EmailItem(
                    id=welcome_id,
                    sender_name="AI Smart Assistant Team",
                    sender_email="assistant@smart-email.ai",
                    recipient_email=clean_user,
                    subject=f"Welcome {username}! Your Smart AI Inbox is Ready",
                    snippet=f"Hello {username}, welcome to AI-Powered Smart Email Assistant! Your personal inbox is now connected and protected by Gemini NLP...",
                    body=f"""Hello {username},

Welcome to your personalized AI-Powered Smart Email Assistant!

Your account ({clean_user}) is now active. Here is what you can do:
1. Compose outgoing emails using the '+ Compose' button to test AI auto-analysis.
2. Generate smart responses in Professional, Friendly, or Urgent tones.
3. Upload PDF documents to test the OCR Attachment Scanner.
4. Run Phishing Security scans to detect suspicious messages.

If you connect your live Google Account in Google Cloud setup, your real Gmail threads will auto-synchronize here.

Best regards,
The AI Smart Email Team""",
                    category=CategoryEnum.WORK,
                    priority=PriorityEnum.HIGH,
                    date="Just now",
                    timestamp=now,
                    is_read=False,
                    is_starred=True,
                    is_spam=False,
                    has_attachments=False,
                    attachments=[],
                    summary=EmailSummary(
                        bullet_points=[
                            f"Account setup complete for {clean_user}.",
                            "Gemini NLP engine and OCR attachment scanner are active.",
                            "Ready to compose, summarize, and manage emails."
                        ],
                        one_liner=f"Welcome to AI Smart Email Assistant for {clean_user}.",
                        urgency_reason="Welcome onboarding notification.",
                        sentiment="Positive",
                        key_deadlines=[]
                    ),
                    action_items=[
                        ActionItem(
                            task="Explore AI Assistant features and compose your first test email",
                            due_date="Today",
                            completed=False,
                            is_meeting=False
                        )
                    ],
                    folder="inbox"
                )
                self.emails[welcome_email.id] = welcome_email

        results = []
        for email in self.emails.values():
            # If a custom non-demo user is logged in, filter out generic sample emails addressed to demo account
            if clean_user and clean_user not in demo_accounts:
                recip = (getattr(email, 'recipient_email', '') or '').lower()
                sendr = (getattr(email, 'sender_email', '') or '').lower()
                if recip != clean_user and sendr != clean_user and "welcome" not in email.id:
                    continue

            if folder and folder.lower() != "all" and email.folder.lower() != folder.lower():
                continue
            if category and email.category.value.lower() != category.lower():
                continue
            if priority and email.priority.value.lower() != priority.lower():
                continue
            if unread_only and email.is_read:
                continue
            if starred_only and not email.is_starred:
                continue
            if has_attachments is not None and email.has_attachments != has_attachments:
                continue
            if search:
                q = search.lower().strip()
                search_hit = (
                    q in email.subject.lower() or
                    q in email.body.lower() or
                    q in email.sender_name.lower() or
                    q in email.sender_email.lower() or
                    (email.summary and q in email.summary.one_liner.lower()) or
                    any(q in item.task.lower() for item in email.action_items)
                )
                if not search_hit:
                    continue
            results.append(copy.deepcopy(email))

        results.sort(key=lambda x: x.timestamp, reverse=True)
        return results

    def get_email_by_id(self, email_id: str) -> Optional[EmailItem]:
        email = self.emails.get(email_id)
        if email:
            return copy.deepcopy(email)
        return None

    def _sync_email_to_supabase(self, email: EmailItem):
        if self.supabase:
            try:
                payload = {
                    "id": email.id,
                    "sender_name": email.sender_name,
                    "sender_email": email.sender_email,
                    "recipient_email": email.recipient_email,
                    "subject": email.subject,
                    "body": email.body,
                    "category": email.category.value if hasattr(email.category, 'value') else str(email.category),
                    "priority": email.priority.value if hasattr(email.priority, 'value') else str(email.priority),
                    "is_read": email.is_read,
                    "is_starred": email.is_starred,
                    "folder": email.folder
                }
                self.supabase.table("emails").upsert(payload).execute()
            except Exception:
                pass

    def add_email(self, email: EmailItem) -> EmailItem:
        self.emails[email.id] = copy.deepcopy(email)
        self._sync_email_to_supabase(email)
        return email

    def update_email(self, email_id: str, updates: Dict[str, Any]) -> Optional[EmailItem]:
        if email_id not in self.emails:
            return None
        email_dict = self.emails[email_id].model_dump()
        email_dict.update(updates)
        updated_email = EmailItem(**email_dict)
        self.emails[email_id] = updated_email
        self._sync_email_to_supabase(updated_email)
        return copy.deepcopy(updated_email)

    def delete_email(self, email_id: str) -> bool:
        if email_id in self.emails:
            if self.emails[email_id].folder == "trash":
                del self.emails[email_id]
            else:
                self.emails[email_id].folder = "trash"
                self.emails[email_id].is_trash = True
            return True
        return False

    def get_analytics(self) -> Dict[str, Any]:
        all_emails = list(self.emails.values())
        total = len(all_emails)
        unread = sum(1 for e in all_emails if not e.is_read and e.folder == "inbox")
        spam_count = sum(1 for e in all_emails if e.is_spam or e.category == CategoryEnum.SPAM)
        urgent = sum(1 for e in all_emails if e.priority == PriorityEnum.HIGH and e.folder == "inbox")
        
        # Calculate estimated time saved (5 mins per summarized email)
        time_saved = round(total * 5.2 / 60, 1)

        category_counts: Dict[str, int] = {}
        for c in CategoryEnum:
            count = sum(1 for e in all_emails if e.category == c)
            if count > 0:
                category_counts[c.value] = count

        priority_counts: Dict[str, int] = {
            "High": sum(1 for e in all_emails if e.priority == PriorityEnum.HIGH),
            "Medium": sum(1 for e in all_emails if e.priority == PriorityEnum.MEDIUM),
            "Low": sum(1 for e in all_emails if e.priority == PriorityEnum.LOW)
        }

        # Daily sync volume simulation
        daily_volume = [
            {"day": "Mon", "received": 24, "summarized": 24, "urgent": 5},
            {"day": "Tue", "received": 38, "summarized": 38, "urgent": 8},
            {"day": "Wed", "received": 42, "summarized": 42, "urgent": 11},
            {"day": "Thu", "received": 35, "summarized": 35, "urgent": 6},
            {"day": "Fri", "received": 48, "summarized": 48, "urgent": 14},
            {"day": "Sat", "received": 12, "summarized": 12, "urgent": 1},
            {"day": "Sun", "received": 8, "summarized": 8, "urgent": 0}
        ]

        top_senders = [
            {"name": "Sarah Jenkins (VP Eng)", "email": "sarah.jenkins@techcorp.io", "count": 14, "urgent_ratio": "85%"},
            {"name": "David Miller (Product)", "email": "david.miller@techcorp.io", "count": 9, "urgent_ratio": "40%"},
            {"name": "Emily Zhao (Legal)", "email": "emily.zhao@lexislegal.com", "count": 6, "urgent_ratio": "66%"},
            {"name": "Stripe Billing", "email": "invoices@stripe.com", "count": 4, "urgent_ratio": "0%"},
            {"name": "GitHub Notifications", "email": "notifications@github.com", "count": 18, "urgent_ratio": "5%"}
        ]

        return {
            "total_emails": total,
            "unread_count": unread,
            "spam_blocked": spam_count,
            "urgent_count": urgent,
            "time_saved_hours": time_saved,
            "avg_response_time_minutes": 14,
            "category_distribution": category_counts,
            "priority_distribution": priority_counts,
            "daily_volume": daily_volume,
            "top_senders": top_senders
        }

# Global singleton database instance
db = Database()
