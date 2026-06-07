import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_smtp_config():
    host = os.getenv("SMTP_HOST", "email") # Defaults to local Mailpit container
    port = int(os.getenv("SMTP_PORT", "1025"))
    user = os.getenv("SMTP_USER", "")
    password = os.getenv("SMTP_PASSWORD", "")
    sender = os.getenv("SMTP_SENDER", "noreply@somarwal.edu")
    return host, port, user, password, sender

def send_email(to_email: str, subject: str, html_content: str) -> bool:
    host, port, user, password, sender = get_smtp_config()
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email

    part = MIMEText(html_content, "html")
    msg.attach(part)

    try:
        with smtplib.SMTP(host, port) as server:
            if port in [465, 587]:
                server.starttls()
            if user and password:
                server.login(user, password)
            server.sendmail(sender, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
        return False

def send_whatsapp(to_phone: str, message: str) -> bool:
    token = os.getenv("WHATSAPP_TOKEN")
    phone_id = os.getenv("WHATSAPP_PHONE_ID")
    
    if not token or not phone_id:
        print(f"WhatsApp credentials not found. Simulated message to {to_phone}: {message}")
        return True
        
    url = f"https://graph.facebook.com/v17.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": message}
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending WhatsApp to {to_phone}: {e}")
        return False
