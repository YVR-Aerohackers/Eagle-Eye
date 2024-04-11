from view import View
from camera_manager import CameraManagerFactory
from scan_manager import ScanManager
from report_manager import ReportManager
from notification_manager import NotificationManager
from file_explorer import FileExplorer
from datetime import datetime
import config


class Controller:
    """
    Controller class to manage the flow of the application

    Attributes:
    - view (View): The view to display messages and get user input
    - camera_manager (CameraManager): The camera manager to connect to and capture frames from a camera
    - scan_manager (ScanManager): The scan manager to process input data and detect objects
    - report_manager (ReportManager): The report manager to save and send reports
    - notification_manager (NotificationManager): The notification manager to send notifications
    - file_explorer (FileExplorer): The file explorer to select input files
    - new_scan (bool): A flag to indicate if a new scan has been made

    Methods:
    - __init__(self): Initializes the Controller with the required managers and services
    - _toggle_new_scan(self): Toggles the new_scan flag to indicate if a new scan has been made
    - _camera_connected(self): Checks if a camera is connected
    - run(self): Runs the main loop of the application
    - connect_camera(self): Connects to a camera based on the camera ID obtained from the view
    - run_auto_scan(self): Runs an automatic scan by capturing a frame from the connected camera
    - run_manual_scan(self): Runs a manual scan by processing the input type and path selected by the user
    - send_report_to_staff(self): Sends the latest report to staff members
    - view_live_stream(self): Views the live stream from the connected camera
    """

    def __init__(self):
        """
        Initializes the Controller with the required managers and services
        """
        self.view = View()
        self.camera_manager = CameraManagerFactory.create_camera_manager(
            use_multithreading=True
        )
        self.scan_manager = ScanManager(self.camera_manager)
        self.report_manager = ReportManager()
        self.notification_manager = NotificationManager()
        self.file_explorer = FileExplorer()
        self.new_scan = False

    def _toggle_new_scan(self):
        """
        Toggles the new_scan flag to indicate if a new scan has been made
        """
        self.new_scan = not self.new_scan

    def _camera_connected(self):
        """
        Checks if a camera is connected

        @return (bool): True if a camera is connected, False otherwise
        """
        return True if self.camera_manager.get_camera_id() else False

    def run(self):
        """
        Runs the main loop of the application
        """
        while True:
            choice = self.view.display_menu()
            if choice == "1":
                self.connect_camera()
            elif choice == "2":
                self.run_auto_scan()
            elif choice == "3":
                self.run_manual_scan()
            elif choice == "4":
                self.send_report_to_staff()
            elif choice == "5":
                self.view_live_stream()
            elif choice == "6":
                break
            else:
                self.view.display_invalid_choice()

    def connect_camera(self):
        """
        Connects to a camera based on the camera ID obtained from the view.
        Displays a message on the view based on the success or failure of the connection.
        """
        camera_id = (
            self.view.get_camera_id() or "0"
        )  # Fallback to default camera ID if None

        camera_urls = {
            "1": config.NETWORK_CAMERA_IP_1,
            "2": config.NETWORK_CAMERA_IP_2,
        }
        camera_url = camera_urls.get(
            camera_id, camera_id
        )  # Use camera_id itself if not in map

        try:
            if self.camera_manager.connect_camera(camera_url):
                self.view.display_camera_connected(camera_id)
            else:
                self.view.display_camera_connection_error(camera_id)
        except Exception as e:
            self.view.display_camera_connection_error(camera_id)

    def run_auto_scan(self):
        """
        Runs an automatic scan by capturing a frame from the connected camera

        @return (tuple): A tuple containing the detections and output paths
        """
        try:
            detections, output_paths = self.scan_manager.run_auto_scan()
            if detections:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                camera_id = self.camera_manager.get_camera_id()
                report_path = self.report_manager.save_detections(
                    detections, timestamp, output_paths, camera_id
                )
                self.notification_manager.send_notifications(report_path)
                self.view.display_report_sent()
            else:
                self.view.display_error_message("No detections made.")
        except Exception as e:
            self.view.display_error_message(str(e))

    def run_manual_scan(self):
        """
        Runs a manual scan by processing the input type and path selected by the user

        @return (tuple): A tuple containing the detections and output paths
        """
        try:
            while True:
                input_type = self.view.get_input_type()
                if input_type == "1":
                    input_path = self.file_explorer.select_image()
                elif input_type == "2":
                    input_path = self.file_explorer.select_video()
                elif input_type == "3":
                    input_path = self.file_explorer.select_directory()
                elif input_type == "4":  # Cancel
                    break
                else:
                    print("Invalid input type")

            detections, output_paths = self.scan_manager.run_scan(
                input_type, input_path
            )

            if not detections:
                self.view.display_error_message("No detections made.")
                return

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            camera_id = self.camera_manager.get_camera_id()
            report_path = self.report_manager.save_detections(
                detections, timestamp, output_paths, camera_id=camera_id
            )
            self.view.display_scan_complete()
            self._toggle_new_scan() if not self.new_scan else None
        except Exception as e:
            self.view.display_error_message(str(e))

    def send_report_to_staff(self):
        """
        Sends the latest report to staff members

        @return (str): The path of the latest report
        """
        try:
            if not self.new_scan:
                raise ValueError("No new scan has been made")

            report_path = self.report_manager.get_latest_report()
            if report_path:
                self.notification_manager.send_notifications(report_path)
                self.view.display_report_sent()
                self._toggle_new_scan() if self.new_scan else None
            else:
                self.view.display_no_report_available()
        except Exception as e:
            self.view.display_error_message(str(e))

    def view_live_stream(self):
        """
        Views the live stream from the connected camera

        @return (None)
        """
        try:
            if not self._camera_connected():
                raise ValueError("No camera connected")
            self.camera_manager.start_live_stream()
            self.camera_manager.display_frames()
        except Exception as e:
            self.view.display_error_message(str(e))
