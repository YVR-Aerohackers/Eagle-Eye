from datetime import datetime
import cv2
import os
import shutil


class FileProcessor:
    def __init__(self, base_output_dir, camera_id=None):
        self.base_output_dir = base_output_dir
        self.camera_id = camera_id
        self.out = None

    def set_camera_id(self, camera_id):
        self.camera_id = camera_id

    def _generate_filename(self, prefix, extension):
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{current_time}.{extension}"

    def save_image(self, frame, image_prefix="image"):
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
        if self.out is not None:
            self.out.write(frame)

    def release_video_writer(self):
        if self.out is not None:
            self.out.release()

    def rename_file(self, old_path, new_name):
        if not os.path.exists(old_path):
            print(f"File not found: {old_path}")
            return
        dir_name = os.path.dirname(old_path)
        new_path = os.path.join(dir_name, new_name)
        shutil.move(old_path, new_path)
