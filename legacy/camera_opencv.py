import cv2
from legacy.base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = 0
    run = True

    def __init__(self, src):
        self.video_source = src
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def set_run(run):
        Camera.run = run

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while Camera.run:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
