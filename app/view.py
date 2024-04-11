class View:
    """
    View class for the application to display messages and get input from the user

    Methods:
    - display_menu(): Displays the main menu options
    - get_camera_id(): Gets the camera ID from the user
    - get_input_type(): Gets the input type from the user
    - display_camera_connected(camera_id): Displays a message that the camera is connected
    - display_camera_connection_error(camera_id): Displays an error message for camera connection
    - display_scan_complete(): Displays a message that the scan is complete
    - display_report_saved(report_path): Displays a message that the report is saved
    - display_no_report_available(): Displays a message that no report is available
    - display_report_sent(): Displays a message that the report is sent
    - display_error_message(message): Displays an error message
    - display_invalid_choice(): Displays a message for an invalid choice
    """

    @staticmethod
    def display_menu():
        """
        Displays the main menu options

        @return (str): The choice selected by the user
        """
        print(
            "\n\t===================================="
            "\n\t··········· YVR Eagle-Eye ··········"
            "\n\t===================================="
            "\n\t[ 1.] ·· Connect Camera"
            "\n\t[ 2.] ·· Run Auto Scan"
            "\n\t[ 3.] ·· Run Manual Scan"
            "\n\t[ 4.] ·· Send Report to Staff"
            "\n\t[ 5.] ·· View Live Stream"
            "\n\t[ 6.] ·· Exit"
            "\n\t====================================\n"
        )
        return input("Enter your choice: ")

    @staticmethod
    def get_camera_id():
        """
        Gets the camera ID from the user

        @return (str): The camera ID entered by the user
        """
        return input("Enter the camera ID (default 0): ")

    @staticmethod
    def get_input_type():
        """
        Gets the input type from the user

        @return (str): The input type selected by the user
        """
        print(
            "\n\t===================================="
            "\n\t··········· Process Input ··········"
            "\n\t===================================="
            "\n\t[ 1.] ·· Image"
            "\n\t[ 2.] ·· Video"
            "\n\t[ 3.] ·· Directory"
            "\n\t[ 4.] ·· Cancel"
            "\n\t====================================\n"
        )
        return input("Enter input type: ")

    @staticmethod
    def display_camera_connected(camera_id):
        """
        Displays a message that the camera is connected

        @param camera_id (str): The camera ID
        """
        print(f"Camera {camera_id} connected successfully.")

    @staticmethod
    def display_camera_connection_error(camera_id):
        """
        Displays an error message for camera connection

        @param camera_id (str): The camera ID
        """
        print(f"Error connecting to camera {camera_id}.")

    @staticmethod
    def display_scan_complete():
        """
        Displays a message that the scan is complete

        @param camera_id (str): The camera ID
        """
        print("Scan completed successfully.")

    @staticmethod
    def display_report_saved(report_path):
        """
        Displays a message that the report is saved

        @param report_path (str): The path of the saved report
        """
        print(f"Report saved at: {report_path}")

    @staticmethod
    def display_no_report_available():
        """
        Displays a message that no report is available
        """
        print("No report available to send.")

    @staticmethod
    def display_report_sent():
        """
        Displays a message that the report is sent
        """
        print("Report sent to staff.")

    @staticmethod
    def display_error_message(message):
        """
        Displays an error message

        @param message (str): The error message
        """
        print(f"Error: {message}")

    @staticmethod
    def display_invalid_choice():
        """
        Displays a message for an invalid choice
        """
        print("Invalid choice. Please try again.")
