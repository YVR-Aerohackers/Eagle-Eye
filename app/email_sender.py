from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import base64
import os
import config


class EmailSender:
    def __init__(self):
        self.sendgrid_api_key = config.SENDGRID_API_KEY
        self.sender_email = config.SENDER_EMAIL

    def send_email(self, subject, content, recipient):
        try:
            sg = SendGridAPIClient(self.sendgrid_api_key)
            message = Mail(
                from_email=self.sender_email,
                to_emails=recipient,
                subject=subject,
                html_content=content,
            )
            response = sg.send(message)
            print(f"Email sent. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending email: {str(e)}")
