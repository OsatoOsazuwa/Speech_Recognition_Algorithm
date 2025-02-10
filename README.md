# 🗣️ Enhanced Speech Recognition App

This is a speech recognition web app built using **Streamlit** and **Vosk/Google API** for real-time transcription. The app allows users to upload an audio file in .wav format and receive live transcription of their speech in multiple languages. It supports both **Google's Speech-to-Text API** and **Vosk**, an offline speech recognition model.

## Table of Contents
1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Download Vosk Models](#download-vosk-models)
4. [Usage](#usage)
5. [Running the App](#running-the-app)
6. [Future Improvements](#future-improvements)
7. [Troubleshooting](#troubleshooting)
8. [Contributing](#contributing)

## Features
- 🎙️ **Real-Time Speech Recognition**: Upload an audio file and get the transcription instantly.
- 🌍 **Multi-Language Support**: Supports English, French, and Spanish for transcription.
- 🛠️ **Choice of API**: Users can choose between **Google Speech-to-Text** and **Vosk** for transcription.
- 📥 **Download Transcription**: Once the transcription is completed, you can download the text file.
- ⏸️ **Pause/Resume Functionality**: The app allows you to pause the speech recognition process and resume later.

## Tech Stack
- **Frontend**: Streamlit (for web app interface)
- **Backend**: Python
- **Speech Recognition APIs**: 
  - Google Speech-to-Text (requires internet)
  - Vosk (Offline Model, supports multiple languages)
- **Audio Processing**: 
  - `pydub` for resampling audio to 16kHz if required


## Installation

### Prerequisites
Before running the app, you need to install the required libraries. You can install them using `pip`:

```bash
pip install -r requirements.txt
```
### Download Vosk Models
Download the required Vosk models for English, French, or Spanish from the Vosk GitHub or directly from this link.

- English: [vosk-model-small-en-us-0.15](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip)
- French: [vosk-model-small-fr-0.22](https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip)
- Spanish: [vosk-model-small-es-0.42](https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip)
  
Once downloaded, extract the models and point the app to the model directory.

## Usage
- Start Recording: Click the "🎤 Start Recording" button and start speaking.
- Choose Recognition API: You can select between Google or Vosk.
- Select Language: Choose from English, French, or Spanish.
- Download Transcription: After the transcription is done, click the "📥 Download Transcription" button to download the text file.

## Running the App
To run the app locally, use the following command:
```bash
streamlit speech_recognition_app.py
```
This will launch the app in your default web browser.

## Future Improvements
- 🌐 Add more languages for speech recognition.
- 🔒 Enhance offline capabilities with Vosk for more robust and accurate results.
- 🎨 Improve the UI/UX for a better user experience.

## Troubleshooting
- Audio Playback is Slow: Ensure your microphone is correctly set to record at 16kHz. If necessary, the app will resample the audio before transcription.
- Error with API: Make sure you have internet access for Google API, and the Vosk models are correctly installed for offline transcription.

## Contributing
Feel free to fork the repository and submit pull requests if you have improvements, fixes, or feature requests!




