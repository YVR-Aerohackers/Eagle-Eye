from view import View
from camera_manager import CameraManagerFactory
from scan_manager import ScanManager
from report_manager import ReportManager
from notification_manager import NotificationManager
from file_explorer import FileExplorer
from datetime import datetime


class Controller:
    def __init__(self):
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
        self.new_scan = not self.new_scan

    def _camera_connected(self):
        return True if self.camera_manager.get_camera_id() else False

    def run(self):
        while True:
            choice = self.view.display_menu()
            if choice == "1":
                self.connect_camera()
            elif choice == "2":
                self.run_manual_scan()
            elif choice == "3":
                self.send_report_to_staff()
            elif choice == "4":
                self.view_live_stream()
            elif choice == "5":
                break
            else:
                self.view.display_invalid_choice()

    def connect_camera(self):
        camera_id = self.view.get_camera_id()
        if self.camera_manager.connect_camera(camera_id):
            self.view.display_camera_connected(camera_id)
        else:
            self.view.display_camera_connection_error(camera_id)

    def run_manual_scan(self):
        try:
            input_type = self.view.get_input_type()
            if input_type == "1":
                input_path = self.file_explorer.select_image()
            elif input_type == "2":
                input_path = self.file_explorer.select_video()
            elif input_type == "3":
                input_path = self.file_explorer.select_directory()
            else:
                raise ValueError("Invalid input type")

            detections, output_paths = self.scan_manager.run_scan(
                input_type, input_path
            )

            if not detections:
                self.view.display_error_message("No detections made.")
                return

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = self.report_manager.save_detections(
                detections, timestamp, output_paths
            )
            self.view.display_scan_complete()
            self._toggle_new_scan() if not self.new_scan else None
        except Exception as e:
            self.view.display_error_message(str(e))

    def send_report_to_staff(self):
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
        try:
            if not self._camera_connected():
                raise ValueError("No camera connected")
            self.camera_manager.start_live_stream()
            self.camera_manager.display_frames()
        except Exception as e:
            self.view.display_error_message(str(e))
