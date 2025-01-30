from flask import Flask
import subprocess
import librosa
import numpy as np
import serial
import time

app = Flask(__name__)

# Open serial connection to ESP8266
ser = serial.Serial('COM4', 115200, timeout=1)  # Adjust COM port if needed
time.sleep(2)  # Allow time for initialization
ser.write(b"Port found \n")

# Function to process audio and return vibration data
def process_audio():
    # ---- Step 3: Load Audio File ----
    audio_file = "music/audio60.wav"
    ser.write(b"Loading audio file...\n")

    try:
        y, sr = librosa.load(audio_file, sr=None, mono=True)
        ser.write(f"Audio loaded: {sr} Hz sample rate, {len(y)} samples total.\n".encode())
    except Exception as e:
        ser.write(f"Audio Load Error: {str(e)}\n".encode())
        ser.close()
        exit(1)

    # ---- Step 4: Estimate BPM & Filter Frequencies ----
    ser.write(b"Estimating BPM and filtering frequencies...\n")

    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(tempo) if isinstance(tempo, (int, float)) else 120
    ser.write(f"Estimated BPM: {bpm:.2f} BPM\n".encode())

    # Apply band-pass filter (20-150 Hz)
    def bandpass_filter(signal, sr, lowcut=20, highcut=150):
        fft = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal), 1/sr)
        mask = (freqs > lowcut) & (freqs < highcut)
        filtered_fft = fft * mask
        return np.fft.ifft(filtered_fft).real

    y_filtered = bandpass_filter(y, sr)

    # ---- Step 5: Compute Weighted RMS Per Beat ----
    ser.write(b"Calculating weighted RMS per beat...\n")
    rms_energy = librosa.feature.rms(y=y_filtered)[0]

    weighted_rms = []
    for i in range(len(beats) - 1):
        start, end = beats[i], beats[i + 1]
        rms_segment = rms_energy[start:end]
        weight = (rms_segment ** 2).mean()
        weighted_rms.append(weight)
        ser.write(f"Beat {i+1}: Weighted RMS = {weight:.5f}\n".encode())

    # ---- Step 6: Normalize Vibration Intensity ----
    ser.write(b"Normalizing intensity for vibration...\n")
    vibration_data = np.interp(weighted_rms, (min(weighted_rms), max(weighted_rms)), (0, 255))
    vibration_data = [int(val) for val in vibration_data]  # Convert to int

    # ---- Step 7: Send Data to ESP8266 ----
    ser.write(b"Sending vibration data to ESP8266...\n")
    ser.write(b"DATA_START\n")  # Signal ESP that data is starting
    time.sleep(0.5)

    for value in vibration_data:
        ser.write(f"{value}\n".encode())  # Send each vibration intensity value
        time.sleep(0.05)  # Avoid buffer overflow

    ser.write(b"DATA_END\n")  # Signal ESP that data is complete
    ser.write(b"All vibration data sent.\n")

    # ---- Step 8: Finish Process ----
    ser.write(b"Vibration sync complete. Stopping vibration...\n")
    ser.close()

# Flask endpoint to trigger the audio processing
@app.route('/play', methods=['POST'])
def play():
    process_audio()  # Run the audio processing script
    return "Python script started", 200

if __name__ == "__main__":
    app.run(host="192.168.1.86", port=5000)
