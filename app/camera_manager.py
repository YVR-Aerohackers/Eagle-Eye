import cv2
from object_detector import ObjectDetector
from file_processor import FileProcessor
import queue
import config
import threading


class CameraManagerFactory:
    @staticmethod
    def create_camera_manager(use_multithreading=True):
        if use_multithreading:
            return MultithreadedCameraManager()
        else:
            return SingleThreadedCameraManager()


class BaseCameraManager:
    def __init__(self):
        self.camera = None
        self.camera_id = None

    def connect_camera(self, camera_id):
        try:
            self.camera = cv2.VideoCapture(int(camera_id))
            if not self.camera.isOpened():
                raise Exception(f"Cannot open camera {camera_id}")
            self.camera_id = camera_id
            return True
        except Exception as e:
            print(f"Error connecting to camera: {str(e)}")
            self.camera = None
            self.camera_id = None
            return False

    def disconnect_camera(self):
        if self.camera:
            self.camera.release()
            self.camera = None
            self.camera_id = None

    def is_camera_connected(self):
        return self.camera is not None

    def get_camera_id(self):
        return self.camera_id

    def capture_frame(self):
        if self.camera:
            ret, frame = self.camera.read()
            if ret:
                return frame
        return None

    def start_live_stream(self):
        raise NotImplementedError

    def stop_live_stream(self):
        raise NotImplementedError


class SingleThreadedCameraManager(BaseCameraManager):
    def start_live_stream(self):
        try:
            if not self.is_camera_connected():
                if not self.connect_camera(self.camera_id):
                    raise Exception("Failed to connect to camera")
            object_detector = ObjectDetector()
            file_processor = FileProcessor(config.OUT_LIVE_DIR, self.camera_id)
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    print("Lost connection to camera. Attempting to reconnect...")
                    self.disconnect_camera()
                    if not self.connect_camera(self.camera_id):
                        print("Failed to reconnect to camera")
                        break  # Exit the loop if reconnection fails
                    continue  # Reconnection successful, continue streaming
                detections = object_detector.detect_objects(
                    frame, self.camera_id, config.OUT_LIVE_DIR
                )
                file_processor.write_frame(frame)
                cv2.imshow(f"Live Stream - Camera {self.camera_id}", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        except Exception as e:
            print(f"Error during live stream: {str(e)}")
        finally:
            if self.camera:
                self.camera.release()
                self.camera = None
            cv2.destroyAllWindows()
            cv2.waitKey(1)

    def stop_live_stream(self):
        pass


class MultithreadedCameraManager(BaseCameraManager):
    def __init__(self):
        super().__init__()
        self.streaming = threading.Event()
        self.frame_queue = queue.Queue()

    def start_live_stream(self):
        self.streaming.set()
        self.frame_thread = threading.Thread(target=self._frame_loop)
        self.frame_thread.start()

    def _frame_loop(self):
        try:
            if not self.is_camera_connected():
                if not self.connect_camera(self.camera_id):
                    raise Exception("Failed to connect to camera")
            object_detector = ObjectDetector()
            file_processor = FileProcessor(config.OUT_LIVE_DIR, self.camera_id)
            while self.streaming.is_set():
                ret, frame = self.camera.read()
                if not ret:
                    print("Lost connection to camera. Attempting to reconnect...")
                    self.disconnect_camera()
                    if not self.connect_camera(self.camera_id):
                        print("Failed to reconnect to camera")
                        break  # Exit the loop if reconnection fails
                    continue  # Reconnection successful, continue streaming
                detections = object_detector.detect_objects(
                    frame, self.camera_id, config.OUT_LIVE_DIR
                )
                file_processor.write_frame(frame)
                self.frame_queue.put(frame)
        except Exception as e:
            print(f"Error during frame loop: {str(e)}")
        finally:
            self.streaming.clear()
            if self.camera:
                self.camera.release()
                self.camera = None

    def display_frames(self):
        while self.streaming.is_set():
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                if frame is not None:
                    cv2.imshow(f"Live Stream - Camera {self.camera_id}", frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        self.stop_live_stream()
                        break
        cv2.destroyAllWindows()
        cv2.waitKey(1)

    def stop_live_stream(self):
        self.streaming.clear()
        if (
            self.frame_thread.is_alive()
            and self.frame_thread != threading.current_thread()
        ):
            self.frame_thread.join()
