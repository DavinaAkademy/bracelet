from flask import Flask, request, jsonify, render_template
from time import sleep
import sounddevice as sd
import numpy as np
from websocket import create_connection
from threading import Thread
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Set the FLASK_ENV configuration
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')

# Configuration from environment variables
ESP32_SERVER = os.getenv('ESP32_SERVER', '192.168.1.41')
ESP32_PORT = os.getenv('ESP32_PORT', '80')
DEFAULT_POWER_FACTOR = float(os.getenv('DEFAULT_POWER_FACTOR', '4.0'))

# Print all environment variables in development mode
if app.config['ENV'] == 'development':
    logger.info(f"ESP32_SERVER: {ESP32_SERVER}")
    logger.info(f"ESP32_PORT: {ESP32_PORT}")
    logger.info(f"DEFAULT_POWER_FACTOR: {DEFAULT_POWER_FACTOR}")

# Global variables
run_stream = False
ws = None
stream_thread = None
audio_stream = None
power_factor = DEFAULT_POWER_FACTOR

@app.route('/')
def index():
    api_url = os.getenv('API_URL', 'http://127.0.0.1:5000')
    return render_template('index.html', api_url=api_url)

@app.route("/start")
def start():
    global run_stream, stream_thread, power_factor
    
    new_factor = request.args.get('factor', type=float)
    if new_factor is not None:
        power_factor = new_factor
        logger.info(f"Power factor set to {power_factor}")
    
    if not run_stream:
        run_stream = True
        stream_thread = Thread(target=stream_audio)
        stream_thread.daemon = True
        stream_thread.start()
        logger.info(f"Started streaming with power factor {power_factor}")
        return jsonify({
            "status": "success",
            "message": "Stream started",
            "config": {
                "power_factor": power_factor,
                "esp32_server": f"{ESP32_SERVER}:{ESP32_PORT}"
            }
        })
    
    return jsonify({
        "status": "warning",
        "message": "Stream already running",
        "config": {
            "power_factor": power_factor,
            "esp32_server": f"{ESP32_SERVER}:{ESP32_PORT}"
        }
    })

@app.route("/stop")
def stop():
    global run_stream, audio_stream
    run_stream = False
    if audio_stream:
        audio_stream.stop()
    logger.info("Stopped streaming")
    return jsonify({
        "status": "success",
        "message": "Stream stopped"
    })

def audio_callback(indata, frames, time, status):
    global ws
    global power_factor
    if not run_stream:
        return
        
    volume_norm = np.linalg.norm(indata) * 10
    scaled_value = np.power(volume_norm, power_factor) / 100
    mapped_value = np.clip(125 + (scaled_value * 5), 125, 255)
    hex_value = format(int(mapped_value), '02x')
    
    try:
        ws.send("#" + hex_value)
        logger.debug(f"Sent value: {int(mapped_value)} (hex: #{hex_value})")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")

def stream_audio():
    global run_stream, ws, audio_stream 
    try:
        ws = create_connection(f"ws://{ESP32_SERVER}:{ESP32_PORT}")
        logger.info(f"Connected to WebSocket at ws://{ESP32_SERVER}:{ESP32_PORT}")
        
        audio_stream = sd.InputStream(callback=audio_callback)
        audio_stream.start()
        logger.info("Audio stream started")
        
        while run_stream:
            sleep(0.1)
    except Exception as e:
        logger.error(f"Stream error: {str(e)}")
    finally:
        if audio_stream:
            audio_stream.stop()
            audio_stream.close()
            logger.info("Audio stream closed")
        if ws:
            try:
                ws.send("#00")
                ws.close()
                logger.info("WebSocket connection closed")
            except Exception as e:
                logger.error(f"Error closing WebSocket: {str(e)}")
        run_stream = False

if __name__ == '__main__':
    logger.info(f"Starting server with ESP32 at {ESP32_SERVER}:{ESP32_PORT}")
