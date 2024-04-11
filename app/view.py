class View:
    @staticmethod
    def display_menu():
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
        return input("Enter the camera ID (default 0): ")

    @staticmethod
    def get_input_type():
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
        print(f"Camera {camera_id} connected successfully.")

    @staticmethod
    def display_camera_connection_error(camera_id):
        print(f"Error connecting to camera {camera_id}.")

    @staticmethod
    def display_scan_complete():
        print("Scan completed successfully.")

    @staticmethod
    def display_report_saved(report_path):
        print(f"Report saved at: {report_path}")

    @staticmethod
    def display_no_report_available():
        print("No report available to send.")

    @staticmethod
    def display_report_sent():
        print("Report sent to staff.")

    @staticmethod
    def display_error_message(message):
        print(f"Error: {message}")

    @staticmethod
    def display_invalid_choice():
        print("Invalid choice. Please try again.")
