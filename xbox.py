import signal
import motor
from xbox360controller import Xbox360Controller


def on_button_pressed(button):
    print('Button {0} was pressed'.format(button.name))


def on_button_released(button):
    print('Button {0} was released'.format(button.name))


def on_axis_moved(axis):
    motor.writeNumber(int(round(500*abs(axis.x))))
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))


try:
    with Xbox360Controller(1, axis_threshold=0.3) as controller:
        print("this is running")
        print(controller.info())
        # Button A events
        controller.button_a.when_pressed = on_button_pressed
        controller.button_a.when_released = on_button_released

        # Left and right axis move event
        controller.axis_l.when_moved = on_axis_moved
        controller.axis_r.when_moved = on_axis_moved
        controller.hat.when_moved = on_axis_moved


        signal.pause()
except KeyboardInterrupt:
    pass
