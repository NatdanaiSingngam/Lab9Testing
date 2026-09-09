"""External dependency — จะถูก Mock ใน test."""

class EmailService:
    def send(self, to: str, subject: str, body: str = "") -> bool:
        print(f"Sending email to {to}: {subject}")
        return True


def send_welcome_email(to: str, email_service: EmailService) -> bool:
    """ส่งอีเมลต้อนรับ — รับ email_service แบบ DI เพื่อให้ Mock ได้"""
    return email_service.send(to=to, subject="Welcome to Campus Eats", body="Hello!")
