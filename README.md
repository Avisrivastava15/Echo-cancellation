# 🎵Echo-cancellation Web App
 
This is a simple web application built using Flask and Python that allows users to upload an audio file, remove echo and noise, and download the cleaned, enhanced version of the audio.

**🚀Features**
Upload an audio file through a clean UI
Perform Noise Reduction and High-Pass Filtering
Dynamic Range Compression for better audio quality
Download the processed, echo-cancelled audio file
Simple, lightweight, and fast

Built with Flask, Librosa, Pydub, and Scipy

** 🛠️ Tech Stack**
**Backend**: Python, Flask
**Audio Processing:** Librosa, Noisereduce, Scipy, Pydub
**Frontend:** HTML5, CSS3, JavaScript
**Deployment:** Local Server (Flask)

**echo-cancellation-app/**
│
├── app.py                  # Flask application
├── templates/
│   └── index.html           # Main UI (HTML)
├── static/
│   ├── images/              # Images used in the frontend
│   └── style.css             # Styling for the web page
│             
├── uploads/                 # Temporarily stores uploaded audio files
├── processed_audio.wav      # Output file (generated after processing)
└── README.md                # Project documentation

**How It Works**
User uploads an audio file.
The backend processes it:
Noise is reduced using noisereduce.
A high-pass filter is applied to cut off low-frequency noise.
The audio is normalized and compressed for better clarity.
The processed audio file is made available for download.

**Required libraries :** pip install flask librosa noisereduce scipy pydub soundfile
**Run the flask app:** python app.py
**Access the app:** Open your browser and go to: http://127.0.0.1:5000/


**Notes**
Make sure you have ffmpeg installed (required by pydub).
Keep all your static assets (CSS, images) inside the static/ folder.
Temporary uploaded files are saved inside the uploads/ folder.

**🧹 Future Improvements**
Add real-time audio playback after processing
Allow batch uploads and batch echo cancellation
Improve frontend styling (mobile responsiveness)

Deploy the app on a cloud platform (e.g., Heroku, Render)

**🙌 Acknowledgements**
Flask Documentation
Librosa Documentation
Noisereduce Library
Pydub Documentation

