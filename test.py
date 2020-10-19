import mainframe as gui
import wx
import motor
import time
import xboxi2c
try:
    import RPi.GPIO as gpio
    test_environment = False
    from xbox360controller import Xbox360Controller
except (ImportError, RuntimeError):
    test_environment = True


class MainFrame(gui.MainFrame):
    # constructor
    def __init__(self, parent):
        # initialize parent class
        gui.MainFrame.__init__(self, parent)

    def run_control(self, event):
        try:
            print(event)
            values = xboxi2c.get_values(joy)
            self.x_speed.Value = values[0]
            self.y_speed = values[]
        except Exception:
            print(Exception)


def scale_number(number):
    return int(round(254 * abs(number)))


def run_control():
    toggleon = False
    while joy.Guide() != 1:
        if joy.Start() == 1:
            toggleon = not toggleon
            motor.writeBlock([0, 0, 0, 0, 0, 0])
            time.sleep(1)
        if toggleon:
            motor_one_dir, motor_two_dir, motor_three_dir = 1, 1, 1
            if joy.leftX() > 0:
                motor_one_dir = 0
            if joy.leftY() > 0:
                motor_two_dir = 0
            if joy.rightY() > 0:
                motor_three_dir = 0
            motor_speeds = [scale_number(joy.leftX()), scale_number(joy.leftY()), scale_number(joy.rightY())]
            motor.writeBlock(
                [motor_one_dir, motor_speeds[0], motor_two_dir, motor_speeds[1], motor_three_dir, motor_speeds[2]])


joy = xbox.Joystick()
app = wx.App(False)
frame = MainFrame(None)
frame.Show(True)
app.MainLoop()
while True:
    frame.y_speed.Value = xboxi2c.get_values(joy)[0]