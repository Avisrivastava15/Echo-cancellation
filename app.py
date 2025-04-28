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

# The route for rendering the main page (UI)
@app.route('/')
def index():
    return render_template('index.html')  # Make sure you have a proper HTML file (index.html)

# Route to handle the file upload and process it
@app.route('/process', methods=['POST'])
def process_file():
    # Ensure the uploads directory exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    # Check if the user has uploaded a file
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Save the uploaded file to a temporary location
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    try:
        # Process the audio (same code as you already have)
        y, sr = librosa.load(file_path, sr=None, mono=True)   #sr-> sample rate

        # Apply noise reduction
        y_denoised = nr.reduce_noise(y=y, sr=sr, prop_decrease=1.0) #sr-> sample rate

        # Apply a high-pass filter
        nyquist = 0.5 * sr
        low_cutoff = 150
        b, a = signal.butter(4, low_cutoff / nyquist, btype='high')
        y_filtered = signal.filtfilt(b, a, y_denoised)

        # Normalize and convert to 16-bit PCM
        y_normalized = librosa.util.normalize(y_filtered)
        y_int16 = np.int16(y_normalized * 32767)
        y_audio = AudioSegment(y_int16.tobytes(), frame_rate=sr, sample_width=2, channels=1)

        # Apply compression
        y_compressed_audio = compress_dynamic_range(y_audio, threshold=-20.0, ratio=2.0)
        y_compressed = np.array(y_compressed_audio.get_array_of_samples(), dtype=np.float32) / 32768.0

        # Save the processed audio
        output_file = "processed_audio.wav"
        sf.write(output_file, y_compressed, sr)

        # Return the processed file for download
        return send_file(output_file, as_attachment=True)

    except Exception as e:
        # In case something goes wrong, return the error message
        return f"An error occurred during processing: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
