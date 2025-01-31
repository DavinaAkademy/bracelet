# 🎵 SoundOFF Project:

## 📖 Overview
This project was conceived by a group of students from the ITAKADEMY STUDENTS program. The project aims to provide a unique and innovative solution for individuals with hearing impairments to experience music through vibrations. The project is designed to be a personalized and adaptive experience, tailored to the individual's unique needs and preferences.

## 🏗️ Project Architecture
The project is divided into three main components:

1. The SoundOFF Bracelet: This is the main component of the project, designed to be worn by individuals with hearing impairments.

2. The SoundOFF ESP32 Server: This is the server component that runs on the ESP32 microcontroller. It is responsible for streaming audio data to the SoundOFF Bracelet and providing real-time feedback to the user.

3. The SoundOFF Flask API: This is the API component that runs on the Flask server. It is responsible for handling user requests and providing data to the SoundOFF ESP32 Server.

It is designed to be worn on the wrist and is equipped with a microphone and a buzzer. The buzzer is used to generate vibrations that correspond to the music being played, allowing individuals with hearing impairments to experience the music through touch.

It uses PlatformIO to build the ESP32 Server and Flask API, and Flask to handle user requests.

## 🛠️ Technical Requirements
- PlatformIO
- Flask
- Python
- ESP32 Server
- Microphone  

## How to run:

1. Clone the repository to your local machine.
2. Open the project in PlatformIO.
3. Build and upload the ESP32 Server.
4. Run the Flask API.
5. Connect the SoundOFF Bracelet to the ESP32 Server.
    - Connect the ESP32 Server to the WiFi network.
    - Configure the ESP32 Server to run on the correct port : via virtual environment.
6. Test the project by playing music through the SoundOFF Bracelet. 


## Attention:
On this clone, I've inserted a folder names "esp" that contains the platformio.ini file and the main.cpp file.
But to make it work, you need to install PlatformIO extension for VSCode and to choose from platformio the board you want to use.
In there, you can copy the main.cpp and the platformio.ini file so you can have the dependencies and the configurations.








------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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


