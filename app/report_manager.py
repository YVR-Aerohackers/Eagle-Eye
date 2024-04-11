import os
from datetime import datetime
import config


class ReportManager:
    """
    ReportManager class to manage and save reports of detections

    Attributes:
    - reports_directory (str): The path to the reports directory

    Methods:
    - format_report_content(detections, timestamp, output_paths, camera_id=None): Formats the report content with the given detections, timestamp, output paths, and camera ID
    - save_detections(detections, timestamp, output_paths, camera_id=None): Saves the detections to a report file with the given timestamp, output paths, and camera ID
    - get_latest_report(): Gets the path of the latest report file
    """

    def __init__(self):
        """
        Initializes the ReportManager with the reports directory
        """
        self.reports_directory = config.REPORTS_DIR
        os.makedirs(self.reports_directory, exist_ok=True)

    def format_report_content(
        self, detections, timestamp, output_paths, camera_id=None
    ):
        """
        Formats the report content with the given detections, timestamp, output paths, and camera ID

        @param detections (list): A list of detections
        @param timestamp (str): The timestamp of the report
        @param output_paths (list): A list of output paths
        @param camera_id (str): The camera ID
        @return (str): The formatted report content
        """
        output_paths_str = "\n".join(f"- {path}" for path in output_paths)
        detections_str = "\n".join(
            f"Label: {det['label']}, Confidence: {det['confidence']}, Bounding Box: {det['bbox']}"
            for det in detections
        )
        report_content = (
            "YVR Eagle-Eye Report\n"
            "====================\n\n"
            f"Camera ID: {camera_id}\n"
            f"Timestamp: {timestamp}\n"
            "Output Paths:\n"
            f"{output_paths_str}\n\n"
            "Detections:\n"
            f"{detections_str}\n"
        )
        return report_content

    def save_detections(self, detections, timestamp, output_paths, camera_id=None):
        """
        Saves the detections to a report file with the given timestamp, output paths, and camera ID

        @param detections (list): A list of detections
        @param timestamp (str): The timestamp of the report
        @param output_paths (list): A list of output paths
        @param camera_id (str): The camera ID
        """
        report_filename = f"report_{timestamp}.txt"
        report_path = os.path.join(self.reports_directory, report_filename)

        report_content = self.format_report_content(
            detections, timestamp, output_paths, camera_id
        )
        print("Saving report...")
        print(f"\n{report_content}")
        with open(report_path, "w") as file:
            file.write(report_content)

        return report_path

    def get_latest_report(self):
        """
        Gets the path of the latest report file

        @return (str): The path of the latest report file
        """
        report_files = os.listdir(self.reports_directory)
        if not report_files:
            return None

        latest_report = max(
            report_files,
            key=lambda x: os.path.getctime(os.path.join(self.reports_directory, x)),
        )
        return os.path.join(self.reports_directory, latest_report)
