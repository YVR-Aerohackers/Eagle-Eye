from twilio.rest import Client
import config


class SmsSender:
    def __init__(self):
        self.account_sid = config.TWILIO_ACCOUNT_SID
        self.auth_token = config.TWILIO_AUTH_TOKEN
        self.twilio_number = config.TWILIO_PHONE_NUMBER

    def send_sms(self, content, recipient):
        try:
            client = Client(self.account_sid, self.auth_token)
            message = client.messages.create(
                body=content, from_=self.twilio_number, to=recipient
            )
            print(f"SMS sent. Message SID: {message.sid}")
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
