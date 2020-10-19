console.log(document.URL)
var socket = io.connect();
        var connected = false;
        var updateInterval = 300;
        var time = new Date;
        const start = Date.now();
        var time_remaining = 0;
        var rangeValues = 0;
        var canvas = null;
        var ctx = null;
        var img = null;

        function send_connect() {
            console.log("Sending connected mech message");
            socket.emit('connectMech');
        }

        function update() {
            socket.emit('updateMech');
        }

        function restart() {
            socket.emit('restart')
        }

        function powerOff() {
            socket.emit('powerOff')
        }

        function getTime() {
            socket.emit('getTime', Date.now());
        }


        socket.on('firstConnect', function (data) {
            time_remaining = data;
            var intervalID = setInterval(updateTime, 1000);
            function updateTime() {
                            update()
            }


        });

        socket.on('updateMech', function (updateData) {
            var connection_data = updateData[0]
                var keys = Object.keys(connection_data)

                for(var key in keys){
                    var x = keys[key];
                    if(["Load Cell","Heater","Drill Rpm","System Draw","Flow","Pressure"].includes(x)){
                        document.getElementById(x).innerText = connection_data[x];

                    }
                    else if(x === "Positions") {
                        document.getElementById('Z Position').innerText = (parseInt(connection_data[x][2]) / 100).toString();
                        document.getElementById('drill-slider').value = (100 - (parseInt(connection_data[x][2])));
                        document.getElementById('Z-position Text').innerText = (parseInt(connection_data[x][2]) / 100).toString();
                        ctx.clearRect(0, 0, 500, 300)
                        ctx.drawImage(img, 200 - parseInt(connection_data[x][0]), 140 - parseInt(connection_data[x][1]), 30, 30);
                        ctx.beginPath();
                        var index = 0;
                        var hole_data = updateData[1];
                        while (index < hole_data.length) {

                            var x_coord = hole_data[index][0];
                            var y_coord = hole_data[index][1];
                            if (x_coord > -1) {
                                console.log(x_coord);
                                ctx.beginPath();
                                ctx.arc(x_coord, y_coord, 20, 0, 2 * Math.PI);
                                ctx.stroke();
                                ctx.strokeText(index.toString(), x_coord-3, y_coord+2);
                            }
                            index++;
                        }
                    }
                    else if(x === "Water Collected"){
                        document.getElementById('Water Collected').innerText = (parseFloat(connection_data[x])/100).toString();

                    }
                    else if(x === "Drill Rpm"){

                    }
                    else if(x === "Extractor"){
                        if(connection_data[x][0] !== 0){
                            document.getElementById(x).style = "background-color: green";
                        }
                        else{
                            document.getElementById(x).style = "background-color: red";
                        }
                    }
                    else{
                        if(connection_data[x][0] < 0){
                            document.getElementById(x).style = "background-color: green";
                        }
                        else if (connection_data[x][0] > 0){
                            document.getElementById(x).style = "background-color: green";
                        }
                        else{
                            document.getElementById(x).style = "background-color: red";
                        }
                    }

                }


        });

        function drawImage() {
            canvas = document.getElementById("drill-position");
        ctx = canvas.getContext("2d");
        img = document.getElementById("red-x")
/*    ctx.drawImage(img, 200, 140, 30, 30);
    ctx.beginPath();

    ctx.arc(100, 75, 20, 0, 2 * Math.PI);
    ctx.stroke();

    ctx.strokeText("1", 97, 77);
    ctx.beginPath();
    ctx.arc(280, 175, 20, 0, 2 * Math.PI);
    ctx.stroke();
    ctx.strokeText("2", 280, 177);*/
    send_connect()


}
var intervalID = setInterval(updateRunTime, 1000);
        function updateRunTime() {
                            time_remaining-=1
            document.getElementById("time-remaining").innerHTML = "Time remaining: " + secondsToMinutesAndSeconds(time_remaining);

            }
function millisToMinutesAndSeconds(millis) {
  var minutes = Math.floor(millis / 60000);
  var seconds = ((millis % 60000) / 1000).toFixed(0);
  return minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
}
function secondsToMinutesAndSeconds(secs) {
  var minutes = Math.floor(secs / 60);
  var seconds = (secs % 60).toFixed(0);
  if (minutes < 0){
      minutes = "??"
  }
  if (seconds < 0){
      seconds = 0
  }
  return minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
}