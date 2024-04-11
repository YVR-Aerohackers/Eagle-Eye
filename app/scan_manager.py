from input_processor import InputProcessor
from object_detector import ObjectDetector
from datetime import datetime
import config
import os
import cv2


class ScanManager:
    """
    ScanManager class is responsible for running media scans using the InputProcessor and ObjectDetector classes.
    This class is used to process input data (images, videos, or directories) and detect objects in the frames.

    Attributes:
    - input_processor (InputProcessor): The input processor to process input data
    - object_detector (ObjectDetector): The object detector to detect objects in frames
    - camera_manager (CameraManager): The camera manager to capture frames from the camera

    Methods:
    - __init__(self, camera_manager): Initializes the ScanManager with the given camera_manager
    - run_scan(self, input_type, input_path): Runs a manual scan on the given input (image, video, or directory path)
    - run_auto_scan(self): Runs an automatic scan by capturing a frame from the connected camera
    """

    def __init__(self, camera_manager):
        """
        Initializes the ScanManager with the given camera_manager

        @param camera_manager (CameraManager): The camera manager to use for capturing frames
        """
        self.input_processor = InputProcessor()
        self.object_detector = ObjectDetector()
        self.camera_manager = camera_manager

    def run_scan(self, input_type, input_path):
        """
        Runs a manual scan on the given input (image, video, or directory path)

        @param input_type (str): The type of input to process (1: Image, 2: Video, 3: Directory)
        @param input_path (str): The path of the input to process
        @return (tuple): A tuple containing the detections and output paths
        """
        if input_type == "1":  # If the input type is Image
            input_data = self.input_processor.process_image(input_path)
        elif input_type == "2":  # If the input type is Video
            input_data = self.input_processor.process_video(input_path)
        elif input_type == "3":  # If the input type is Directory
            input_data = self.input_processor.process_directory(input_path)
        else:
            raise ValueError("Invalid input type")

        camera_id = self.camera_manager.get_camera_id()
        detections = []
        output_paths = []

        # Process each frame to detect objects
        for frame in input_data:
            frame_detections, output_path = self.object_detector.detect_objects(
                frame, camera_id, config.OUT_IMG_DIR
            )
            detections.extend(frame_detections)  # Add the detected objects to the list
            output_paths.append(
                output_path
            )  # Add the output path of the .jpg file to the list

        return detections, output_paths

    def run_auto_scan(self):
        """
        Runs an automatic scan by capturing a frame from the connected camera

        @return (tuple): A tuple containing the detections and output paths
        """
        camera_id = self.camera_manager.get_camera_id()
        if camera_id is None:
            raise ValueError("No camera connected")

        frame = self.camera_manager.capture_frame()
        if frame is None:
            raise Exception("Failed to capture frame from camera")

        # Save the captured frame to the input folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_dir = os.path.join(config.IN_IMG_DIR, str(camera_id))
        os.makedirs(input_dir, exist_ok=True)
        input_path = os.path.join(input_dir, f"{timestamp}.jpg")
        cv2.imwrite(input_path, frame)

        # Run the scan on the captured frame
        return self.run_scan("1", input_path)
