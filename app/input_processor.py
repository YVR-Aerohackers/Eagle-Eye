import cv2
import os
import config


class InputProcessor:
    @staticmethod
    def process_image(image_path):
        image = cv2.imread(image_path)
        return [image] if image is not None else []

    @staticmethod
    def process_video(video_path):
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
        frames = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                    frames.append(InputProcessor.process_image(file_path))
                elif filename.lower().endswith((".mp4", ".avi")):
                    frames.extend(InputProcessor.process_video(file_path))
        return frames
