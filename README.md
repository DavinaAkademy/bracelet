TODO
Change wifi ssid and password for esp server in main.cpp
source the python virtual environment : source ~/Desktop/WorkSpace/School/bracelet/bracelet/SoundOff/.venv/bin/activate
API_URL=http://127.0.0.1:5000 ESP32_SERVER=192.168.1.41 flask run



Plat-> represents the ESP, this with the extension of Platform.io, makes us develop and send the code to the platform.

User -> makes a call to the python
The PY -> opens a websocket server to the esp

Here we have a bidrectional communication between the python server and the esp server.
The python server sends the hex value to the esp server, which then sets the buzzer to that value.

The ESP aknowledges on the socket.

The communication stops when the user calls the stop command.

We chose a webscoket so we can have a low latency communication since we are dealing real time data.


main.cpp: its the esp code
app.py: its a flask api so we can communicate with the end client
