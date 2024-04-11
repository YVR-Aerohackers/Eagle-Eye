import cv2
import os
import config


class InputProcessor:
    """
    InputProcessor class with static methods to process input data (image, video, or directory)

    Attributes:
    - None

    Methods:
    - process_image(image_path): Processes an image file and returns a list of frames
    - process_video(video_path): Processes a video file and returns a list of frames
    - process_directory(directory_path): Processes a directory and returns a list of frames
    """

    @staticmethod
    def process_image(image_path):
        """
        Processes an image file and returns a list of frames

        @param image_path (str): The path of the image file
        @return (list): A list containing the image frame
        """
        image = cv2.imread(image_path)
        return [image] if image is not None else []

    @staticmethod
    def process_video(video_path):
        """
        Processes a video file and returns a list of frames

        @param video_path (str): The path of the video file
        @return (list): A list containing the video frames
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception(f"Cannot open video: {video_path}")

        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

        cap.release()
        return frames

    @staticmethod
    def process_directory(directory_path):
        """
        Processes a directory and returns a list of frames.
        Each file in the directory is processed as an image or video file.

        @param directory_path (str): The path of the directory
        @return (list): A list containing the frames from the directory
        """
        frames = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                    frames.append(InputProcessor.process_image(file_path))
                elif filename.lower().endswith((".mp4", ".avi")):
                    frames.extend(InputProcessor.process_video(file_path))
        return frames
