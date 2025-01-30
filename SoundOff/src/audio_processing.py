import librosa
import socket
import numpy as np 
import time

# ESP8266 server IP and port
ESP_IP = '192.168.1.41'  # ESP IP address
ESP_PORT = 12345  # ESP Port

# Function to process audio and return vibration data
def process_audio():
    # ---- Step 3: Load Audio File ----
    audio_file = "music/audio60.wav"

    try:
        y, sr = librosa.load(audio_file, sr=None, mono=True)
    except Exception as e:
        print(f"Audio Load Error: {str(e)}")
        return

    # ---- Step 4: Estimate BPM & Filter Frequencies ----
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(tempo) if isinstance(tempo, (int, float)) else 120

    # Apply band-pass filter (20-150 Hz)
    def bandpass_filter(signal, sr, lowcut=20, highcut=150):
        fft = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal), 1/sr)
        mask = (freqs > lowcut) & (freqs < highcut)
        filtered_fft = fft * mask
        return np.fft.ifft(filtered_fft).real

    y_filtered = bandpass_filter(y, sr)

    # ---- Step 5: Compute Weighted RMS Per Beat ----
    rms_energy = librosa.feature.rms(y=y_filtered)[0]

    weighted_rms = []
    for i in range(len(beats) - 1):
        start, end = beats[i], beats[i + 1]
        rms_segment = rms_energy[start:end]
        weight = (rms_segment ** 2).mean()
        weighted_rms.append(weight)

    # ---- Step 6: Normalize Vibration Intensity ----
    if len(weighted_rms) > 0:
        vibration_data = np.interp(weighted_rms, (min(weighted_rms), max(weighted_rms)), (0, 255))
        vibration_data = [int(val) for val in vibration_data]
    else:
        vibration_data = [0] * 10  # Default to 0 intensity if no data

    # ---- Step 7: Send Data to ESP8266 over socket ----
    try:
        # Create socket connection to ESP8266
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ESP_IP, ESP_PORT))

        # Send vibration data to ESP8266
        for value in vibration_data:
            client_socket.send(f"{value}\n".encode())
            time.sleep(0.05)

        client_socket.send(b"DATA_END\n")  # Signal ESP that data is complete
        client_socket.close()
    except Exception as e:
        print(f"Socket Error: {str(e)}")
