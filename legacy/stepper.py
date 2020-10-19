import time
from threading import Timer
import RPi.GPIO as gpio

class AudioRecording:
    def __init__(self, pin, interval):
        self.output = 0
        self.pin = pin
        self.interval = interval
        self.run_motor_interval = Timer(self.interval, self.run_motor)

    def run_motor(self):

        self.run_motor_interval.start()


gpio.setmode(gpio.BCM)
gpio.setup(24, gpio.OUT)