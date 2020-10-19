// Socketio javascript library
// <script src="/static/js/socket.io.js"></script>

// Sets up socketio variable
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Emits first connect attempt to alert server of new connection
socket.emit('connect');

//Requests server for update
socket.emit('update');

// Retrieves the sent update in an array
socket.on('randint', function (data) {
    // data[x] = current reading of sensor x
});

// Tells server to update from github and restart
socket.emit('restart');

//Stops some running functions to try and ensure clean shutdown
socket.emit('powerOff');

//To test for latency
socket.emit('getTime', Date.now());

// Emit a value for adc output, must be an int between 0 and 255
socket.emit('adjustValue', value);

// Receive adc output change value, comes in as an int
socket.on('rangeUpdate', function (data) {
    //data = int
});

// Receives a dictionary of initial connection data
socket.on('firstConnect', function (connection_data) {
    //connection_data['current_output'] = Current adc output
    //connection_data['sensor_readings'] = A 2D array of up to 200 most recent readings from the three sensors
    //connection_data['sensor_readings'][x] = Up to 20 most recent readings of sensor x
});