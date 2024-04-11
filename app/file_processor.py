from datetime import datetime
import cv2
import os
import shutil


class FileProcessor:
    """
    FileProcessor class to handle file operations

    Attributes:
    - base_output_dir (str): The base output directory to save files
    - camera_id (int): The camera ID to use for saving files
    - out (cv2.VideoWriter): The video writer object

    Methods:
    - set_camera_id(camera_id): Sets the camera ID to use for saving files
    - _generate_filename(prefix, extension): Generates a filename with the given prefix and extension
    - save_image(frame, image_prefix="image"): Saves the given frame as an image with the given prefix
    - start_video_writer(frame_width, frame_height, fps=20.0, video_prefix="video"): Starts a video writer with the given parameters
    - write_frame(frame): Writes the given frame to the video writer
    - release_video_writer(): Releases the video writer
    - rename_file(old_path, new_name): Renames the file at the old path with the new name
    """

    def __init__(self, base_output_dir, camera_id=None):
        """
        Initializes the FileProcessor with the given base_output_dir and camera_id

        @param base_output_dir (str): The base output directory to save files
        @param camera_id (int): The camera ID to use for saving files
        """
        self.base_output_dir = base_output_dir
        self.camera_id = camera_id
        self.out = None

    def set_camera_id(self, camera_id):
        """
        Sets the camera ID to use for saving files

        @param camera_id (int): The camera ID to use for saving files
        """
        self.camera_id = camera_id

    def _generate_filename(self, prefix, extension):
        """
        Generates a filename with the given prefix and extension

        @param prefix (str): The prefix of the filename
        @param extension (str): The extension of the filename
        @return (str): The generated filename
        """
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{current_time}.{extension}"

    def save_image(self, frame, image_prefix="image"):
        """
        Saves the given frame as an image with the given prefix

        @param frame (numpy.ndarray): The frame to save as an image
        @param image_prefix (str): The prefix of the image filename
        """
        if self.camera_id is not None:
            image_dir = os.path.join(self.base_output_dir, str(self.camera_id))
        else:
            image_dir = self.base_output_dir
        os.makedirs(image_dir, exist_ok=True)
        image_filename = self._generate_filename(image_prefix, "jpg")
        cv2.imwrite(os.path.join(image_dir, image_filename), frame)

    def start_video_writer(
        self, frame_width, frame_height, fps=20.0, video_prefix="video"
    ):
        """
        Starts a video writer with the given parameters

        @param frame_width (int): The width of the video frame
        @param frame_height (int): The height of the video frame
        @param fps (float): The frames per second of the video
        @param video_prefix (str): The prefix of the video filename
        """
        if self.camera_id is not None:
            video_dir = os.path.join(self.base_output_dir, str(self.camera_id))
        else:
            video_dir = self.base_output_dir
        os.makedirs(video_dir, exist_ok=True)
        video_filename = self._generate_filename(video_prefix, "avi")
        video_path = os.path.join(video_dir, video_filename)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.out = cv2.VideoWriter(video_path, fourcc, fps, (frame_width, frame_height))

    def write_frame(self, frame):
        """
        Writes the given frame to the video writer

        @param frame (numpy.ndarray): The frame to write to the video writer
        """
        if self.out is not None:
            self.out.write(frame)

    def release_video_writer(self):
        """
        Releases the video writer
        """
        if self.out is not None:
            self.out.release()

    def rename_file(self, old_path, new_name):
        """
        Renames the file at the old path with the new name

        @param old_path (str): The path of the file to rename
        @param new_name (str): The new name of the file
        """
        if not os.path.exists(old_path):
            print(f"File not found: {old_path}")
            return
        dir_name = os.path.dirname(old_path)
        new_path = os.path.join(dir_name, new_name)
        shutil.move(old_path, new_path)
