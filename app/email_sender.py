from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import base64
import os
import config


class EmailSender:
    """
    EmailSender class to send emails using the SendGrid API

    Attributes:
    - sendgrid_api_key (str): The SendGrid API key to authenticate the user
    - sender_email (str): The email address of the sender

    Methods:
    - __init__(self): Initializes the EmailSender with the required SendGrid API key and sender email
    - send_email(self, subject, content, recipient): Sends an email with the given subject, content, and recipient
    """

    def __init__(self):
        """
        Initializes the EmailSender with the required SendGrid API key and sender email

        @param sendgrid_api_key (str): The SendGrid API key to authenticate the user
        @param sender_email (str): The email address of the sender
        """
        self.sendgrid_api_key = config.SENDGRID_API_KEY
        self.sender_email = config.SENDER_EMAIL

    def send_email(self, subject, content, recipient):
        """
        Sends an email with the given subject, content, and recipient

        @param subject (str): The subject of the email
        @param content (str): The content of the email
        @param recipient (str): The email address of the recipient
        """
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
