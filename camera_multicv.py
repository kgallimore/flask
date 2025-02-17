import cv2
import time
import threading
from base_multicam import CameraEvent


class BaseCamera(object):
    thread = {}  # background thread that reads frames from camera
    frame = {}  # current frame is stored here by background thread
    last_access = {}  # time of last client access to the camera
    event = {}
    video_source = 0
    run = True

    def __init__(self, device=None):
        """Start the background camera thread if it isn't running yet."""
        self.unique_name = "{dev}".format(dev=device)
        BaseCamera.event[self.unique_name] = CameraEvent()
        if self.unique_name not in BaseCamera.thread:
            BaseCamera.thread[self.unique_name] = None
        if BaseCamera.thread[self.unique_name] is None:
            BaseCamera.last_access[self.unique_name] = time.time()

            # start background frame thread
            BaseCamera.thread[self.unique_name] = threading.Thread(target=self._thread,
                                                                   args=(self.unique_name,))
            BaseCamera.thread[self.unique_name].start()

            # wait until frames are available
            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        """Return the current camera frame."""
        BaseCamera.last_access[self.unique_name] = time.time()

        # wait for a signal from the camera thread
        BaseCamera.event[self.unique_name].wait()
        BaseCamera.event[self.unique_name].clear()

        return BaseCamera.frame[self.unique_name]

    @classmethod
    def _thread(cls, unique_name):
        """Camera background thread."""
        print('Starting camera thread')
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame[unique_name] = frame
            BaseCamera.event[unique_name].set()  # send signal to clients
            time.sleep(0)

            # if there hasn't been any clients asking for frames in
            # the last 5 seconds then stop the thread
            if time.time() - BaseCamera.last_access[unique_name] > 5 or BaseCamera.run is False:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity')
                break
        BaseCamera.thread[unique_name] = None

    @staticmethod
    def set_video_source(source):
        BaseCamera.video_source = source

    @staticmethod
    def set_run(run):
        BaseCamera.run = run

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(BaseCamera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while BaseCamera.run:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            if img is not None:
                yield cv2.imencode('.jpg', img)[1].tobytes()
