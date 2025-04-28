from flask import Flask, render_template, request, send_file
import librosa
import noisereduce as nr
import numpy as np
import scipy.signal as signal
import soundfile as sf
from pydub import AudioSegment
from pydub.effects import compress_dynamic_range
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
PROCESSED_FILE = "processed_audio.wav"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')  # It will load index.html from same folder

@app.route('/process', methods=['POST'])
def process_audio():
    if 'audio_file' not in request.files:
        return "No file uploaded", 400

    file = request.files['audio_file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Load audio
    y, sr = librosa.load(file_path, sr=None, mono=True)

    # Noise reduction
    y_denoised = nr.reduce_noise(y=y, sr=sr, prop_decrease=1.0)

    # High-pass filter
    nyquist = 0.5 * sr
    low_cutoff = 150
    b, a = signal.butter(4, low_cutoff / nyquist, btype='high')
    y_filtered = signal.filtfilt(b, a, y_denoised)

    # Normalize
    y_normalized = librosa.util.normalize(y_filtered)
    y_int16 = np.int16(y_normalized * 32767)

    # Convert to AudioSegment
    y_audio = AudioSegment(
        y_int16.tobytes(),
        frame_rate=sr,
        sample_width=2,
        channels=1
    )

    # Compression
    y_compressed_audio = compress_dynamic_range(y_audio, threshold=-20.0, ratio=2.0)
    y_compressed = np.array(y_compressed_audio.get_array_of_samples(), dtype=np.float32) / 32768.0

    # Save final output
    sf.write(PROCESSED_FILE, y_compressed, sr)
    return send_file(PROCESSED_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
