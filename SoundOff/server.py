from flask import Flask, render_template
import socket
import subprocess  # Used to run the external audio processing script

app = Flask(__name__)

# ESP8266 server IP and port
ESP_IP = '192.168.1.41'
ESP_PORT = 12345

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/play', methods=['GET'])
def play():
    try:

         # Create a socket connection to the ESP8266
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ESP_IP, ESP_PORT))

        # Run the audio processing script and capture its output
        result = subprocess.run(['python', 'src/audio_processing.py'], capture_output=True, text=True)
        vibration_data = result.stdout.strip()  # Strip any extra whitespace or newline

        print(f"Vibration data from audio processing: {vibration_data}")  # Log the data

        if not vibration_data.isdigit():
            return "Error: Invalid vibration data", 500
        
        # Send the vibration data received from the audio processing script
        client_socket.sendall(f"{vibration_data}\n".encode())
        client_socket.close()
        
        return f"Vibration triggered with intensity {vibration_data}!", 200
    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == '__main__':
    app.run(host='192.168.1.86', port=5000)
