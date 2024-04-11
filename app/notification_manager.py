import os

from email_sender import EmailSender
from sms_sender import SmsSender
from recipient_manager import RecipientManager
import config


class NotificationManager:
    """
    NotificationManager class to send notifications to recipients via email or SMS

    Attributes:
    - email_sender (EmailSender): The email sender to send emails
    - sms_sender (SmsSender): The SMS sender to send SMS messages
    - recipient_manager (RecipientManager): The recipient manager to get the list of recipients

    Methods:
    - read_report_content(report_path): Reads the content of the report file
    - format_content_as_html(content, report_content): Formats the content and report as HTML
    - send_notifications(report_path): Sends notifications to recipients with the report attached
    """

    def __init__(self):
        """
        Initializes the NotificationManager with the required services

        @param email_sender (EmailSender): The email sender to send emails
        @param sms_sender (SmsSender): The SMS sender to send SMS messages
        @param recipient_manager (RecipientManager): The recipient manager to get the list of recipients
        """
        self.email_sender = EmailSender()
        self.sms_sender = SmsSender()
        self.recipient_manager = RecipientManager(config.RECIPIENTS_FILE)

    def read_report_content(self, report_path):
        """
        Reads the content of the report file

        @param report_path (str): The path of the report file
        @return (str): The content of the report file
        """
        try:
            with open(report_path, "r") as file:
                return file.read()
        except IOError as e:
            print(f"Error reading report file: {str(e)}")
            return None

    def format_content_as_html(self, content, report_content):
        """
        Formats the content and report as HTML

        @param content (str): The content of the notification
        @param report_content (str): The content of the report
        @return (str): The formatted content as HTML
        """
        html_content = f"<p>{content}</p><br><br><pre>{report_content}</pre>"
        return html_content

    def send_notifications(self, report_path):
        """
        Sends notifications to recipients with the report attached

        @param report_path (str): The path of the report file
        """
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
