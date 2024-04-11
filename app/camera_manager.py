import cv2
from object_detector import ObjectDetector
from file_processor import FileProcessor
import queue
import config
import threading


class CameraManagerFactory:
    """
    CameraManagerFactory is a factory class that creates instances of the CameraManager class.
    Allows for the creation of either a SingleThreadedCameraManager or a MultithreadedCameraManager.

    The multithreaded option is ideal for live streaming multiple cameras simultaneously.

    TODO: Optimize multi-threading to isolate READ/WRITE operations and live stream display operations.
    """

    @staticmethod
    def create_camera_manager(use_multithreading=True):
        """
        Creates an instance of the CameraManager class based on the use_multithreading flag.
        Default is to use multithreading.

        @param use_multithreading (bool): Flag to determine whether to use multithreading
        @return (CameraManager): An instance of the CameraManager class
        """
        if use_multithreading:
            return MultithreadedCameraManager()
        else:
            return SingleThreadedCameraManager()


class BaseCameraManager:
    """
    BaseCameraManager is an abstract class that defines the interface for a CameraManager.
    The CameraManager class is responsible for connecting to a camera, capturing frames, and streaming live video.

    Attributes:
    - camera (cv2.VideoCapture): The camera object
    - camera_id (str): The camera ID

    Methods:
    - connect_camera(self, camera_id): Connects to the camera with the given camera ID
    - disconnect_camera(self): Disconnects from the camera
    - is_camera_connected(self): Checks if the camera is connected
    - get_camera_id(self): Gets the camera ID
    - capture_frame(self): Captures a frame from the camera
    - start_live_stream(self): Starts the live video stream from the camera
    - stop_live_stream(self): Stops the live video stream from the camera
    """

    def __init__(self):
        """
        Initializes the BaseCameraManager with default values for the camera and camera ID.
        """
        self.camera = None
        self.camera_id = None

    def connect_camera(self, camera_id):
        """
        Connects to the camera with the given camera ID.

        @param camera_id (str): The camera ID
        @return (bool): True if the connection was successful, False otherwise
        """
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
        """
        Disconnects from the camera.

        @return (bool): True if the disconnection was successful, False otherwise
        """
        if self.camera:
            self.camera.release()
            self.camera = None
            self.camera_id = None

    def is_camera_connected(self):
        """
        Checks if the camera is connected.

        @return (bool): True if the camera is connected, False otherwise
        """
        return self.camera is not None

    def get_camera_id(self):
        """
        Gets the camera ID.

        @return (str): The camera ID
        """
        return self.camera_id

    def capture_frame(self):
        """
        Captures a frame from the camera.

        @return (np.array): The captured frame
        """
        if self.camera:
            ret, frame = self.camera.read()
            if ret:
                return frame
        return None

    def start_live_stream(self):
        """
        Starts the live video stream from the camera.
        This method should be implemented by the derived classes.
        """
        raise NotImplementedError

    def stop_live_stream(self):
        """
        Stops the live video stream from the camera.
        This method should be implemented by the derived classes.
        """
        raise NotImplementedError


class SingleThreadedCameraManager(BaseCameraManager):
    """
    SingleThreadedCameraManager is a concrete class that extends the BaseCameraManager class.
    The SingleThreadedCameraManager class is responsible for streaming live video from a single camera.
    The live video stream is displayed in a window using OpenCV.

    Attributes:
    - None

    Methods:
    - start_live_stream(self): Starts the live video stream from the camera
    - stop_live_stream(self): Stops the live video stream from the camera
    """

    def start_live_stream(self):
        """
        Starts the live video stream from the camera.
        The live video stream is displayed in a window using OpenCV.
        """
        try:
            if not self.is_camera_connected():
                if not self.connect_camera(self.camera_id):
                    raise Exception("Failed to connect to camera")
            object_detector = ObjectDetector()
            file_processor = FileProcessor(config.OUT_LIVE_DIR, self.camera_id)
            while True:  # Loop stores frames in the queue while streaming
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
    """
    MultithreadedCameraManager is a concrete class that extends the BaseCameraManager class.
    The MultithreadedCameraManager class is responsible for streaming live video from a single camera using multiple threads.
    Ideally, this class should be used for live streaming multiple cameras simultaneously.

    The attempt was to separate the frame capture and object detection processes from the live video display process.
    However, the current implementation does not fully isolate the processes.
    """

    def __init__(self):
        """
        Initializes the MultithreadedCameraManager with a streaming event and a frame queue.

        @param streaming (threading.Event): The streaming event
        @param frame_queue (queue.Queue): The frame queue
        """
        super().__init__()
        self.streaming = threading.Event()  # Event to control streaming
        self.frame_queue = queue.Queue()  # Queue to store frames

    def start_live_stream(self):
        """
        Starts the live video stream from the camera using multiple threads.
        """
        self.streaming.set()
        self.frame_thread = threading.Thread(target=self._frame_loop)
        self.frame_thread.start()

    def _frame_loop(self):
        """
        Utility method to capture frames from the camera and detect objects in the frames.
        Stores streamed frames in a queue for display.

        For demonstration purposes, the live video stream is displayed in a window using OpenCV.
        The current implementation does not fully isolate the frame capture and object detection processes from the live video display process.
        """
        try:
            if not self.is_camera_connected():
                if not self.connect_camera(self.camera_id):
                    raise Exception("Failed to connect to camera")
            object_detector = ObjectDetector()
            file_processor = FileProcessor(config.OUT_LIVE_DIR, self.camera_id)
            while (
                self.streaming.is_set()
            ):  # Loop stores frames in the queue while streaming
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
        """
        Displays the streamed frames in a window using OpenCV.

        The display_frames method should be optimized for live streaming multiple cameras simultaneously.
        """
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
        """
        Stops the live video stream from the camera.
        """
        self.streaming.clear()
        if (
            self.frame_thread.is_alive()
            and self.frame_thread != threading.current_thread()
        ):
            self.frame_thread.join()
