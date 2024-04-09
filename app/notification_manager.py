import os

from email_sender import EmailSender
from sms_sender import SmsSender
from recipient_manager import RecipientManager
import config


class NotificationManager:
    def __init__(self):
        self.email_sender = EmailSender()
        self.sms_sender = SmsSender()
        self.recipient_manager = RecipientManager(config.RECIPIENTS_FILE)

    def read_report_content(self, report_path):
        try:
            with open(report_path, "r") as file:
                return file.read()
        except IOError as e:
            print(f"Error reading report file: {str(e)}")
            return None

    def format_content_as_html(self, content, report_content):
        html_content = f"<p>{content}</p><br><br><pre>{report_content}</pre>"
        return html_content

    def send_notifications(self, report_path):
        subject = "Airport Monitoring Report"
        content = "Please find the attached airport monitoring report."
        report_content = self.read_report_content(report_path)

        if report_content is None:
            print("No report content found. Notifications not sent.")
            return

        html_content = self.format_content_as_html(content, report_content)

        recipients = self.recipient_manager.get_recipients()
        for recipient in recipients:
            if "@" in recipient:
                self.email_sender.send_email(subject, html_content, recipient)
            else:
                self.sms_sender.send_sms(report_content, recipient)
