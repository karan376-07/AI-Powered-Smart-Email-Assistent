import os
import base64
import logging
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.config import settings
from app.models.email import EmailItem, AttachmentInfo, AISummary

logger = logging.getLogger("smart_email_assistant")

def get_gmail_service(credentials_dict: Dict[str, Any]):
    """Creates a Gmail API service instance."""
    try:
        creds = Credentials.from_authorized_user_info(credentials_dict)
        return build('gmail', 'v1', credentials=creds)
    except Exception as e:
        logger.error(f"Failed to create Gmail service: {e}")
        return None

async def fetch_emails_from_gmail(user_email: str, credentials_dict: Dict[str, Any], max_results: int = 20) -> List[Dict[str, Any]]:
    """Fetches list of emails from Gmail API and parses them."""
    service = get_gmail_service(credentials_dict)
    if not service:
        return []
    
    try:
        results = service.users().messages().list(userId='me', maxResults=max_results).execute()
        messages = results.get('messages', [])
        
        parsed_emails = []
        for msg in messages:
            msg_id = msg['id']
            # Fetch full message
            msg_data = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            parsed = parse_gmail_message(msg_data, user_email)
            if parsed:
                parsed_emails.append(parsed)
                
        return parsed_emails
    except HttpError as error:
        logger.error(f"Gmail API error occurred: {error}")
        return []
    except Exception as e:
        logger.error(f"General error fetching Gmail: {e}")
        return []

def parse_gmail_message(msg_data: Dict[str, Any], user_email: str) -> Optional[Dict[str, Any]]:
    """Helper to parse raw Gmail API response structure."""
    try:
        msg_id = msg_data['id']
        thread_id = msg_data['threadId']
        payload = msg_data.get('payload', {})
        headers = payload.get('headers', [])
        
        # Extract headers
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), '(No Subject)')
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown Sender')
        date_str = next((h['value'] for h in headers if h['name'].lower() == 'date'), '')
        
        # Parse sender
        sender_name = sender
        sender_email = sender
        if '<' in sender and '>' in sender:
            parts = sender.split('<')
            sender_name = parts[0].strip()
            sender_email = parts[1].replace('>', '').strip()
            
        # Parse date
        try:
            # Use email utils or fallback
            from email.utils import parsedate_to_datetime
            date_dt = parsedate_to_datetime(date_str)
        except Exception:
            date_dt = datetime.now(timezone.utc)
            
        # Parse body
        body_snippet = msg_data.get('snippet', '')
        body_full = ""
        attachments = []
        
        # Extract parts
        parts = [payload]
        while parts:
            part = parts.pop(0)
            if part.get('parts'):
                parts.extend(part.get('parts'))
            
            # Text body
            if part.get('mimeType') == 'text/plain' and part.get('body', {}).get('data'):
                body_data = part['body']['data']
                body_full += base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
            elif part.get('mimeType') == 'text/html' and not body_full and part.get('body', {}).get('data'):
                body_data = part['body']['data']
                # basic decode, text extraction can clean it
                body_full += base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
                
            # Attachment info
            if part.get('filename') and part.get('body', {}).get('attachmentId'):
                attachments.append({
                    "filename": part['filename'],
                    "content_type": part['mimeType'],
                    "size": part['body'].get('size', 0),
                    "id": part['body']['attachmentId']
                })
                
        if not body_full:
            body_full = body_snippet or "No readable text content."
            
        return {
            "_id": msg_id,
            "thread_id": thread_id,
            "user_email": user_email,
            "sender_name": sender_name,
            "sender_email": sender_email,
            "subject": subject,
            "date": date_dt,
            "body_snippet": body_snippet,
            "body_full": body_full,
            "is_read": False,
            "attachments": attachments
        }
    except Exception as e:
        logger.error(f"Error parsing message: {e}")
        return None

async def send_gmail_reply(credentials_dict: Dict[str, Any], thread_id: str, to: str, subject: str, body: str):
    """Sends a reply to a thread using real Gmail API."""
    service = get_gmail_service(credentials_dict)
    if not service:
        raise Exception("Could not initialize Gmail client.")
        
    try:
        from email.mime.text import MIMEText
        # Ensure subject starts with Re:
        if not subject.lower().startswith("re:"):
            subject = f"Re: {subject}"
            
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        message['threadId'] = thread_id
        
        raw_msg = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        send_result = service.users().messages().send(userId='me', body={'raw': raw_msg, 'threadId': thread_id}).execute()
        return send_result
    except Exception as e:
        logger.error(f"Gmail reply failed: {e}")
        raise e

def generate_mock_emails(user_email: str) -> List[Dict[str, Any]]:
    """Generates a rich, realistic list of simulated emails for Demo/Mock Mode."""
    now = datetime.now(timezone.utc)
    
    mock_data = [
        {
            "_id": "msg_001",
            "thread_id": "thread_001",
            "user_email": user_email,
            "sender_name": "Marcus Vance (CEO)",
            "sender_email": "ceo@company.com",
            "subject": "URGENT: Q3 Roadmap Alignment and Smart Email Project Release Status",
            "date": now - timedelta(hours=1),
            "body_snippet": "Hi Team, I need an urgent update on the Smart Email project status before our board meeting tomorrow morning...",
            "body_full": """Hi Team,

I need an urgent update on the Smart Email project release status before our board meeting tomorrow morning.
Specifically, I would like to know:
1. Is the Gmail OAuth 2.0 flow fully verified?
2. What is the current token consumption rate for the Gemini summarizer?
3. Are the loading skeletons and charts optimized for mobile screens?

Please submit a detailed progress report to my office tomorrow by 9:00 AM.
Also, let's schedule a alignment sync meeting tomorrow at 4:00 PM in the executive boardroom to discuss budget extensions.

Best,
Marcus Vance
Chief Executive Officer""",
            "is_read": False,
            "attachments": []
        },
        {
            "_id": "msg_002",
            "thread_id": "thread_002",
            "user_email": user_email,
            "sender_name": "University Portal",
            "sender_email": "assignments@university.edu",
            "subject": "CS-504: Final Term Project Submission Portal Open",
            "date": now - timedelta(hours=3),
            "body_snippet": "Dear Student, The final project submission folder for CS-504: Smart Applications is now open. Deadline is...",
            "body_full": """Dear Student,

The final project submission portal for CS-504: Intelligent Systems and Web Applications is now open.
Please ensure you upload your code bundle, database setup script, and PDF documentation guide before the deadline.

Deadline: Friday, July 17, 2026 at 11:59 PM.
Late submissions will receive a 10% penalty per day.

Make sure you run unit tests and verify OAuth tokens before submitting.

Sincerely,
Academic Administration Group""",
            "is_read": True,
            "attachments": []
        },
        {
            "_id": "msg_003",
            "thread_id": "thread_003",
            "user_email": user_email,
            "sender_name": "Chase Bank Alerts",
            "sender_email": "bank-alerts@chase.com",
            "subject": "Credit Card Minimum Payment Reminder - Statement Ending 06/2026",
            "date": now - timedelta(hours=8),
            "body_snippet": "Dear Customer, This is a reminder that your minimum payment of $45.00 for statement ending 06/2026 is due...",
            "body_full": """Dear Customer,

This is a reminder that your credit card minimum payment of $45.00 (Total statement balance: $450.00) is due soon.
Please schedule a payment to avoid late fees.

Payment Due Date: July 20, 2026
Account Ending: *1004

Thank you for choosing Chase.
Customer Security Team""",
            "is_read": False,
            "attachments": []
        },
        {
            "_id": "msg_004",
            "thread_id": "thread_004",
            "user_email": user_email,
            "sender_name": "Alex Smith",
            "sender_email": "alexsmith@engineers.com",
            "subject": "Application for Senior Full-Stack Developer Position - Resume Attached",
            "date": now - timedelta(days=1),
            "body_snippet": "Hi Hiring Team, I am writing to apply for the Senior Developer role. I have attached my resume for your review...",
            "body_full": """Hi Hiring Team,

I am writing to express my interest in the Senior Full-Stack Developer position at your company.
I have over 4 years of experience working with React, FastAPI, Node, and MongoDB. I specialize in building responsive SaaS dashboards and integrating Generative AI APIs.

I have attached my PDF resume containing detailed highlights of my professional accomplishments.
Looking forward to speaking with you.

Best regards,
Alex Smith
+1-555-0199""",
            "is_read": False,
            "attachments": [
                {
                    "filename": "Alex_Smith_Resume.pdf",
                    "content_type": "application/pdf",
                    "size": 48294,
                    "id": "att_resume_01"
                }
            ]
        },
        {
            "_id": "msg_005",
            "thread_id": "thread_005",
            "user_email": user_email,
            "sender_name": "Amazon Orders",
            "sender_email": "amazon-orders@amazon.com",
            "subject": "Your Amazon.com order #114-9428-2049 has shipped!",
            "date": now - timedelta(days=1, hours=4),
            "body_snippet": "Hello! Your package is on the way. Tracking details: UPS #1Z999AA10123. Estimated delivery date...",
            "body_full": """Hello,

Your package containing 'Ultra-Slim Mechanical Keyboard (Tactile Browns)' and 'USB-C Desktop Sync Hub' has been shipped and is on the way!
Carrier: UPS
Tracking Number: 1Z999AA10123456789
Estimated Delivery Date: Wednesday, July 15, 2026

We hope you enjoy your purchase!
Amazon Logistics Support""",
            "is_read": True,
            "attachments": []
        },
        {
            "_id": "msg_006",
            "thread_id": "thread_006",
            "user_email": user_email,
            "sender_name": "Megasaver Promotions",
            "sender_email": "promos@megasaverdeals.com",
            "subject": "FLAT 50% OFF! Mega Summer Deal Extravaganza Ends Tonight!",
            "date": now - timedelta(days=2),
            "body_snippet": "Get ready for the biggest deals of the year. Flat 50% discount on all electronics, shirts, shoes, and home accessories...",
            "body_full": """EXCLUSIVE OFFER: SUMMER EXTRAVAGANZA!

For the next 12 hours ONLY, get a flat 50% discount storewide!
Use code SUMMER50 at checkout.
Buy designer watches, mechanical parts, shoes, gaming keyboards, and home gadgets at half-price.

Don't wait! Clearance ends tonight at midnight.
Unsubscribe from these emails by clicking here.""",
            "is_read": True,
            "attachments": []
        },
        {
            "_id": "msg_007",
            "thread_id": "thread_007",
            "user_email": user_email,
            "sender_name": "Security Group (HR)",
            "sender_email": "hr@company.com",
            "subject": "Mandatory Annual Cybersecurity Compliance Training Session",
            "date": now - timedelta(days=3),
            "body_snippet": "Hello Employees, This is a reminder that the annual Cybersecurity Compliance training session must be completed...",
            "body_full": """Hello Employees,

This is a reminder that our annual mandatory Cybersecurity Compliance training session is scheduled.
We will cover OAuth safety, phishing detection, key password hygiene, and proper API key storage guidelines.

Meeting Date: Thursday, July 16, 2026 at 10:00 AM (Virtual Zoom Link will follow).
Please confirm your attendance.

Regards,
Human Resources Group""",
            "is_read": True,
            "attachments": []
        },
        {
            "_id": "msg_008",
            "thread_id": "thread_008",
            "user_email": user_email,
            "sender_name": "International Mega Jackpot",
            "sender_email": "jackpot-notification@cheapdeals.ru",
            "subject": "WINNER! You won the $1,000,000 lottery cash prize bonus!!! Wire details now",
            "date": now - timedelta(days=4),
            "body_snippet": "CONGRATULATIONS! You have been selected as the grand winner of the 2026 Mega Jackpot Promo. Double bitcoin...",
            "body_full": """CONGRATULATIONS!!!

You have been selected as the winner of the 2026 International Mega Jackpot Promotion!
Your email address has won a grand cash bonus of $1,000,000.00 USD.

To claim your prize, please double your bitcoin balance by sending a deposit to our wallet, or reply with your bank details:
- Full Name
- Bank Name
- Account Number
- Routing Transit Number

Wire details must be received immediately or the prize will be forfeited.
Jackpot Operations Representative""",
            "is_read": False,
            "attachments": []
        }
    ]
    
    return mock_data
