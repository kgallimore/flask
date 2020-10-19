# Warning! The Analog input MUST NOT be over 3.3V!
import csv
import os
import shutil
import threading
import time
import states
from importlib import import_module

from flask import Flask, render_template, Response, send_from_directory, request
from flask_socketio import SocketIO, emit

try:
    import RPi.GPIO as gpio
    import smbus2 as smbus
    import motor

    test_environment = False
except (ImportError, RuntimeError):
    test_environment = True

current_values = {
    "output0": 0
}
interval = 0
motor_output = 0
motor_direction = 0
relay_stop = 23
if not os.path.exists('storage'):
    os.makedirs('storage')
current_state = [0, 0]
states_dictionary = states.states_dictionary
constraints = {"Load Cell": [0,160], "Positions": [[0,500], [0,300], [0,100]], "Heater": [20,200], "System Draw": [5,900], "Extractor": [0,40],
              "Pump": [0, 0, 0, 0], "Drill": [[0,1000], [0,1]], "Stepper 1": [[-100, 100],[0,1]], "Stepper 2": [[-100, 100],[0,1]], "Stepper 3": [[-100, 100],[0,1]],
              "Stepper 4": [[-100, 100],[0,1]], "Stepper 5": [[-100, 100],[0,1]], "Flow": [0,50], "Pressure": [0,50], "Water Collected": [0,99999]}
hole_positions = [[-1,-1],[350,150]]

if not test_environment:
    import adc
    import git

    bus = smbus.SMBus(1)
    address = 0x04
    is_run_motor = False

    latest_sensor_readings = [[], [], []]
    gpio.cleanup()
    gpio.setmode(gpio.BOARD)
    gpio.setup(relay_stop, gpio.IN)

    csv_filename = '/home/pi/Desktop/flask/storage/readings.' + time.strftime("%H.%M.%S", time.localtime()) + '.csv'


    def update_recent_readings():
        readings_array = bus.read_i2c_block_data(address, 0, 4)
        for x in range(0, 3):
            if len(latest_sensor_readings[x]) < 200:
                latest_sensor_readings[x] += [readings_array[x]]
            else:
                latest_sensor_readings[x].pop(0)
                latest_sensor_readings[x] += [readings_array[x]]
        with open(csv_filename, 'a') as writeFile:
            csv_writer = csv.writer(writeFile)
            csv_writer.writerow([readings_array[0], readings_array[1], readings_array[2], readings_array[3],
                                 time.strftime("%H:%M:%S", time.localtime())])
        if running_status:
            threading.Timer(.3, update_recent_readings).start()
        else:
            print("Closing files, exiting threads", flush=True)
            writeFile.close()


    def update_recent_readings_adc():
        for x in range(0, 3):
            if len(latest_sensor_readings[x]) < 200:
                latest_sensor_readings[x] += [adc.read(x)]
            else:
                latest_sensor_readings[x].pop(0)
                latest_sensor_readings[x] += [adc.read(x)]
        with open(csv_filename, 'a') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow([adc.read(1), adc.read(2), adc.read(3), time.strftime("%H:%M:%S", time.localtime())])
        if running_status:
            threading.Timer(.3, update_recent_readings).start()
        else:
            print("Closing files, exiting threads", flush=True)
            writeFile.close()

else:
    import random

    csv_filename = os.getcwd() + '\\storage\\readings.' + time.strftime("%H.%M.%S", time.localtime()) + '.csv'
    latest_sensor_readings = [[200], [200], [200]]
    mechanical_readings = {"Load Cell": 0, "Positions": [0, 0, 0], "Heater": 0, "System Draw": 0, "Extractor": 0,
              "Pump": [0, 0, 0, 0], "Drill": [0, 0], "Stepper 1": [0, 0], "Stepper 2": [0, 0], "Stepper 3": [0, 0],
              "Stepper 4": [0, 0], "Stepper 5": [0, 0], "Flow": 0, "Pressure": 0, "Water Collected": 0}
    time_remain = time.time()+(15*60)


    def update_recent_readings():
        for x in range(0, 3):
            if len(latest_sensor_readings[x]) < 200:
                latest_sensor_readings[x] += [
                    max(random.randint(latest_sensor_readings[x][-1] - 5, latest_sensor_readings[x][-1] + 5), 0)]
            else:
                latest_sensor_readings[x].pop(0)
                latest_sensor_readings[x] += [
                    max(random.randint(latest_sensor_readings[x][-1] - 5, latest_sensor_readings[x][-1] + 5), 0)]
        with open(csv_filename, 'a') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(
                [max(random.randint(latest_sensor_readings[0][-1] - 5, latest_sensor_readings[0][-1] + 5), 0),
                 max(random.randint(latest_sensor_readings[1][-1] - 5, latest_sensor_readings[1][-1] + 5), 0),
                 max(random.randint(latest_sensor_readings[2][-1] - 5, latest_sensor_readings[2][-1] + 5), 0),
                 time.strftime("%H:%M:%S", time.localtime())])
        if running_status:
            threading.Timer(.3, update_recent_readings).start()
        else:
            print("Closing files, exiting threads", flush=True)
            writeFile.close()
        # check_state_change()
        for x in mechanical_readings:
            if x == "Water Collected":
                mechanical_readings["Water Collected"] = mechanical_readings["Water Collected"] + random.randint(0, 1)
            elif isinstance(mechanical_readings[x],int):
                tempint = mechanical_readings[x] + random.randint(-5, 5)
                if tempint < constraints[x][0]:
                    tempint = constraints[x][0]
                if tempint > constraints[x][1]:
                    tempint = constraints[x][1]
                mechanical_readings[x] = tempint
            elif x != "Pump":
                for y in range(0, len(mechanical_readings[x])):
                    tempint = mechanical_readings[x][y] + random.randint(-2, 2)
                    if tempint < constraints[x][y][0]:
                        tempint = constraints[x][y][0]
                    if tempint > constraints[x][y][1]:
                        tempint = constraints[x][y][1]
                    mechanical_readings[x][y] = tempint

with open(csv_filename, 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(["Sensor One", "Sensor Two", "Sensor Three", "Time"])
    writeFile.close()


def gen(camera):
    while running_status:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.set_run(False)


def emergency_stop(reason):
    print("Emergency stop!", flush=True)
    emit('EmergencyStop', 'Manual Stop')


def check_state_change():
    need_change = True
    current_state_name = current_state[0]
    current_state_number = current_state[1]
    current_state_pointer = states_dictionary[current_state_name][current_state_number]
    if current_state_pointer is not -1:
        threading.Timer(current_state_pointer["time"], change_state).start()
    else:
        for i in range(len(latest_sensor_readings)):
            wanted_reading = current_state_pointer["sensors"][i]
            if wanted_reading is not -1 and current_state_pointer["accetpableDifference"] < abs(
                    latest_sensor_readings[i][-1] - wanted_reading):
                need_change = False
                break
        if need_change:
            change_state()


def change_state():
    if current_state[1] + 1 < len(states_dictionary[current_state[0]]):
        current_state[1] += 1
        change_state()
    else:
        current_state[0] += 1
    adjustMotorValue(states_dictionary[current_state[0]][current_state[1]]["motors"][0])


# Initialize flask variables
app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app)
running_status = True


@app.route('/')
def index():
    client_ip = request.environ['REMOTE_ADDR'][:3]
    if str(client_ip[:3]) == "192" or str(client_ip) == "127.0.0.1":
        print("Local Request", flush=True)
        return render_template('charts.html')
    else:
        return render_template('charts.html')


@app.route('/mechanical')
def mechanical():
    return render_template('mechanical.html')


"""
@app.route('/video')
def video_feed():
    return Response(gen(Camera(0)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
"""


@app.route('/cameras')
def cameras():
    client_ip = request.environ['REMOTE_ADDR'][:3]
    if str(client_ip[:3]) == "192" or str(client_ip) == "127.0.0.1":
        return render_template('cameras.html')
    else:
        return render_template('404.html')


@app.route('/feed/<device>')
def multi_video_feed(device):
    """Video streaming route. Put this in the src attribute of an img tag."""
    client_ip = request.environ['REMOTE_ADDR'][:3]
    if str(client_ip[:3]) == "192" or str(client_ip) == "127.0.0.1":
        camera_stream = import_module('camera_multicv').BaseCamera
        camera_stream.set_video_source(int(device))
        return Response(gen(camera_stream(int(device))),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return render_template('404.html')


@app.route('/csv/')
def send_sensor_data():
    try:
        return send_from_directory('./', csv_filename, as_attachment=True)
    except Exception as e:
        return str(e)


@socketio.on('connectMech')
def connectMechanical():
    print("User connected Mechanical", flush=True)
    # print(current_values['output0'], flush=True)
    emit('firstConnect', int(time_remain-time.time()))


@socketio.on('updateMech')
def connectMechanical():
    emit('updateMech', [mechanical_readings,hole_positions])


# @socketio.on('connect')
# def adjustValue():
#     print("User connected Charts", flush=True)
#     # print(current_values['output0'], flush=True)
#     emit('firstConnect', {"sensor_readings": latest_sensor_readings, "current_output": current_values['output0']})

@socketio.on('update')
def updateInt():
    if not test_environment:
        emit('randint', [adc.read(0), adc.read(1), adc.read(2)])
    else:
        emit('randint', [max(random.randint(latest_sensor_readings[0][-1] - 5, latest_sensor_readings[0][-1] + 5), 0),
                         max(random.randint(latest_sensor_readings[1][-1] - 5, latest_sensor_readings[1][-1] + 5), 0),
                         max(random.randint(latest_sensor_readings[2][-1] - 5, latest_sensor_readings[2][-1] + 5), 0)])


@socketio.on('adjustValue0')
def adjustValue(value):
    current_values['output0'] = value
    if not test_environment:
        adc.write(value)
    emit('rangeUpdate0', value, broadcast=True)


@socketio.on('adjustValue1')
def adjustValue(value):
    emit('rangeUpdate1', value, broadcast=True)


@socketio.on('adjustMotorValue')
def adjustMotorValue(value):
    """global interval, is_run_motor
    value = int(value)
    if value <= 20:
        value = 0
    interval = value
    if not is_run_motor and interval > 0:
        is_run_motor = True
        run_motor()
    print(interval, flush=True)"""
    value = int(value)
    if value <= 20:
        value = 0
    motor.writeNumber(value)
    print(motor.readNumber(), flush=True)


@socketio.on('swtichMotorDirection')
def swtichMotorDirection(direction):
    pass


@socketio.on('switchState')
def swtichMotorDirection(state):
    current_state = state


@socketio.on('restart')
def updateInt():
    """Downloads and replaces any new files from github repo"""
    global running_status
    running_status = False
    adc.running_status = False
    app.logger.warning("Updating")
    if os.path.isdir('./temp/'):
        shutil.rmtree('./temp')
    git.Repo.clone_from('https://github.com/kgallimo/flask.git', './temp')
    for f in os.listdir('./temp/'):
        if os.path.isfile(f) and f is not '.gitignore':
            app.logger.info("Moving " + str(f))
            shutil.move(os.path.join('./temp/', f), os.path.join('./', f))
        elif os.path.isdir(f) and f is not '.git':
            app.logger.info("In directory: " + f)
            for rf in os.listdir('./temp/' + f):
                app.logger.info('./temp/' + str(f) + str(rf))
                if os.path.isfile('./temp/' + f + '/' + rf):
                    app.logger.info("Moving " + str(rf))
                    shutil.move(os.path.join('./temp/' + f, rf), os.path.join('./' + f, rf))
    shutil.rmtree('./temp')
    running_status = True
    adc.running_status = True


@socketio.on('getTime')
def updateInt(data):
    """Test code to test Latency"""
    emit('timestamp', data)


@socketio.on('powerOff')
def powerOff():
    """Prepare Shutdown"""
    global running_status
    running_status = False


if not test_environment:
    gpio.add_event_detect(relay_stop, gpio.RISING)
    gpio.add_event_callback(relay_stop, emergency_stop)

update_recent_readings()

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
    except KeyboardInterrupt:
        if not test_environment:
            adc.destroy()
        exit(0)
