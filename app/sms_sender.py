from twilio.rest import Client
import config


class SmsSender:
    """
    SmsSender class to send SMS messages using Twilio API

    Attributes:
    - account_sid (str): The Twilio account SID
    - auth_token (str): The Twilio authentication token
    - twilio_number (str): The Twilio phone number

    Methods:
    - send_sms(content, recipient): Sends an SMS message with the given content to the recipient
    """

    def __init__(self):
        """
        Initializes the SmsSender with the required Twilio account SID, authentication token, and phone number
        """
        self.account_sid = config.TWILIO_ACCOUNT_SID
        self.auth_token = config.TWILIO_AUTH_TOKEN
        self.twilio_number = config.TWILIO_PHONE_NUMBER

    def send_sms(self, content, recipient):
        """
        Sends an SMS message with the given content to the recipient

        @param content (str): The content of the SMS message
        @param recipient (str): The phone number of the recipient
        """
        try:
            client = Client(self.account_sid, self.auth_token)
            message = client.messages.create(
                body=content, from_=self.twilio_number, to=recipient
            )
            print(f"SMS sent. Message SID: {message.sid}")
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
