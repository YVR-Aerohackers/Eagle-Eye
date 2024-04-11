class RecipientManager:
    """
    RecipientManager class to manage the list of recipients

    Attributes:
    - recipients_file (str): The path to the recipients file

    Methods:
    - get_recipients(): Returns the list of recipients from the recipients file
    """

    def __init__(self, recipients_file):
        """
        Initializes the RecipientManager with the given recipients file

        @param recipients_file (str): The path to the recipients file
        """
        self.recipients_file = recipients_file

    def get_recipients(self):
        """
        Gets the list of recipients from the recipients file

        @return (list): A list of recipients
        """
        try:
            with open(self.recipients_file, "r") as file:
                recipients = file.read().splitlines()
            return recipients
        except FileNotFoundError:
            print(f"Recipients file not found: {self.recipients_file}")
            return []
