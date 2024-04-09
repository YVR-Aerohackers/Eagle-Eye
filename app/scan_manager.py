from input_processor import InputProcessor
from object_detector import ObjectDetector
from datetime import datetime
import config
import os


class ScanManager:
    def __init__(self, camera_manager):
        self.input_processor = InputProcessor()
        self.object_detector = ObjectDetector()
        self.camera_manager = camera_manager

    def run_scan(self, input_type, input_path):
        # This part should handle the processing based on input type
        if input_type == "1":  # If the input type is Image
            input_data = self.input_processor.process_image(input_path)
        elif input_type == "2":  # If the input type is Video
            input_data = self.input_processor.process_video(input_path)
        elif input_type == "3":  # If the input type is Directory
            input_data = self.input_processor.process_directory(input_path)
        else:
            raise ValueError("Invalid input type")

        camera_id = self.camera_manager.get_camera_id()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        detections = []
        output_paths = []

        for frame in input_data:
            frame_detections = self.object_detector.detect_objects(
                frame, camera_id, config.OUT_IMG_DIR
            )
            detections.extend(frame_detections)
            output_path = os.path.join(config.OUT_IMG_DIR, f"{timestamp}.jpg")
            output_paths.append(output_path)

        return detections, output_paths
