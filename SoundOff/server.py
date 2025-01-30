from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/play', methods=['POST'])
def play():
    subprocess.Popen(["python", "C:/Users/LENOVO/OneDrive - KERNEX/Bureau/bracelet/SoundOff/src/audio_processing.py"])
    return "Python script started", 200

if __name__ == "__main__":
    app.run(host="192.168.1.86", port=5000)
