import os
from datetime import datetime
import config


class ReportManager:
    def __init__(self):
        self.reports_directory = config.REPORTS_DIR
        os.makedirs(self.reports_directory, exist_ok=True)

    def format_report_content(self, detections, timestamp, output_paths):
        output_paths_str = "\n".join(f"- {path}" for path in output_paths)
        detections_str = "\n".join(
            f"Label: {det['label']}, Confidence: {det['confidence']}, Bounding Box: {det['bbox']}"
            for det in detections
        )
        report_content = (
            f"Timestamp: {timestamp}\n"
            "Output Paths:\n"
            f"{output_paths_str}\n\n"
            "Detections:\n"
            f"{detections_str}\n"
        )
        return report_content

    def save_detections(self, detections, timestamp, output_paths):
        report_filename = f"report_{timestamp}.txt"
        report_path = os.path.join(self.reports_directory, report_filename)

        report_content = self.format_report_content(detections, timestamp, output_paths)
        print("Saving report...")
        print(f"\n{report_content}")
        with open(report_path, "w") as file:
            file.write(report_content)

        return report_path

    def get_latest_report(self):
        report_files = os.listdir(self.reports_directory)
        if not report_files:
            return None

        latest_report = max(
            report_files,
            key=lambda x: os.path.getctime(os.path.join(self.reports_directory, x)),
        )
        return os.path.join(self.reports_directory, latest_report)
