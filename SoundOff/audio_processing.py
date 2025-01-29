import librosa
import numpy as np
import serial
import time

# ---- Step 1: Load Audio File ----
print("🔄 Loading audio file...")
audio_file = "audio60.wav"
y, sr = librosa.load(audio_file, sr=None, mono=True)
print(f"✅ Audio loaded: {sr} Hz sample rate, {len(y)} samples total.")

# ---- Step 2: Estimate BPM & Filter Frequencies ----
print("🎵 Estimating BPM and filtering frequencies...")
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
bpm = float(tempo) if isinstance(tempo, (int, float)) else 120  # Fix: Ensure scalar value
print(f"⚡ Estimated BPM: {bpm:.2f} BPM")

# Apply band-pass filter (20-150 Hz) to isolate beats
def bandpass_filter(signal, sr, lowcut=20, highcut=150):
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), 1/sr)
    mask = (freqs > lowcut) & (freqs < highcut)
    filtered_fft = fft * mask
    return np.fft.ifft(filtered_fft).real

y_filtered = bandpass_filter(y, sr)

# ---- Step 3: Compute Weighted RMS Per Beat ----
print("⚙️ Calculating weighted RMS per beat...")
rms_energy = librosa.feature.rms(y=y_filtered)[0]
beat_frames = librosa.frames_to_time(beats, sr=sr)

weighted_rms = []
for i in range(len(beats) - 1):
    start, end = beats[i], beats[i + 1]
    rms_segment = rms_energy[start:end]
    weight = (rms_segment ** 2).mean()  # Square weights for stronger beats
    weighted_rms.append(weight)
    print(f"📊 Beat {i+1}: Weighted RMS = {weight:.5f}")

# ---- Step 4: Normalize Vibration Intensity ----
print("📏 Normalizing intensity for vibration...")
vibration_data = np.interp(weighted_rms, (min(weighted_rms), max(weighted_rms)), (0, 255))

# ---- Step 5: Setup Serial Communication ----
print("🔌 Setting up serial connection...")
ser = serial.Serial('COM4', 115200, timeout=1)
time.sleep(2)
print("✅ Serial connection established.")

# ---- Step 6: Start Vibration ----
print("🚀 Sending START command...")
ser.write(b"START\n")  # Start vibration
time.sleep(1)  # Allow ESP to process

# ---- Step 7: Send Data to ESP ----
print("📡 Sending vibration data in sync with beats:")
for i, value in enumerate(vibration_data):
    ser.write(b"START\n")  # Keep sending start command to ensure it's vibrating
    print(f"⏳ Beat {i+1} → Sent Value: {int(value)}")
    time.sleep(60 / bpm)  # Sync with BPM

# ---- Step 8: Stop Vibrations ----
print("🛑 Sending STOP command...")
ser.write(b"STOP\n")  # Stop vibration
time.sleep(1)
ser.close()
print("✅ All data sent. Vibration stopped.")
