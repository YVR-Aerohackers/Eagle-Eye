class RecipientManager:
    def __init__(self, recipients_file):
        self.recipients_file = recipients_file

    def get_recipients(self):
        try:
            with open(self.recipients_file, "r") as file:
                recipients = file.read().splitlines()
            return recipients
        except FileNotFoundError:
            print(f"Recipients file not found: {self.recipients_file}")
            return []
