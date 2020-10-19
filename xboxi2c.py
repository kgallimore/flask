import xbox
import motor
import time


def scale_number(number):
    return int(round(254 * abs(number)))

def get_values(joy):
    return [scale_number(joy.leftX()), scale_number(joy.leftY()), scale_number(joy.rightY())]

# Instantiate the controller
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

