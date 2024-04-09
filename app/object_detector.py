from roboflow import Roboflow
import cv2
import os
import config
from datetime import datetime


class ObjectDetector:
    def __init__(self):
        self.model = self._load_model()

    def detect_objects(self, frame, camera_id, media_out):
        print(f"Camera {camera_id}: Detecting objects...")
        detections = []
        predictions = self.model.predict(frame, confidence=40, overlap=30).json()[
            "predictions"
        ]

        for prediction in predictions:
            x, y, w, h = map(
                int,
                (
                    prediction["x"],
                    prediction["y"],
                    prediction["width"],
                    prediction["height"],
                ),
            )
            label = prediction["class"]
            confidence = prediction["confidence"]
            detections.append(
                {"bbox": (x, y, w, h), "label": label, "confidence": confidence}
            )
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{label}: {confidence:.2f}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2,
            )

        # Generate output path based on media type
        output_path = self.generate_output_path(camera_id, media_out)
        cv2.imwrite(output_path, frame)
        return detections

    def generate_output_path(self, camera_id, media_type):
        # Generate directory and filename based on media type
        if media_type == config.OUT_IMG_DIR:
            output_dir = os.path.join(config.OUT_IMG_DIR, str(camera_id))
        elif media_type == config.OUT_MOV_DIR:
            output_dir = os.path.join(config.OUT_MOV_DIR, str(camera_id))
        elif media_type == config.OUT_LIVE_DIR:
            output_dir = os.path.join(config.OUT_LIVE_DIR, str(camera_id))
        else:
            raise ValueError("Invalid media type")

        os.makedirs(output_dir, exist_ok=True)
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
        return os.path.join(output_dir, filename)

    def _load_model(self):
        rf = Roboflow(api_key=config.ROBOFLOW_API_KEY)
        project = rf.workspace().project(config.ROBOFLOW_PROJECT)
        model = project.version(config.ROBOFLOW_MODEL).model
        return model
