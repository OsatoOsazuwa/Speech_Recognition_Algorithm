import os
import streamlit as st
import wave
import json
import speech_recognition as sr
import whisper
from pydub import AudioSegment
import io

# Initialize Whisper model
def load_whisper_model():
    try:
        model = whisper.load_model("base")  # You can change the model size (e.g., "small", "medium", "large")
        return model
    except Exception as e:
        st.error(f"❌ Failed to load Whisper model: {str(e)}")
        return None

# Function to transcribe audio using Whisper
def transcribe_with_whisper(audio_file):
    model = load_whisper_model()
    if model is None:
        return "❌ Could not load Whisper model."

    # Convert audio file to the format Whisper expects (16kHz WAV)
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)

    # Save the audio to a temporary file
    temp_file = "temp_audio.wav"
    audio.export(temp_file, format="wav")

    # Perform transcription with Whisper
    result = model.transcribe(temp_file)
    return result["text"].capitalize()

# Function to transcribe audio using Google API
def transcribe_with_google(audio_file):
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_file) as source:
            st.info("🔄 Processing uploaded file with Google...")  # Update for better clarity
            audio_text = recognizer.record(source)

        text = recognizer.recognize_google(audio_text)
        return text.capitalize()

    except sr.UnknownValueError:
        return "❌ Could not understand the audio."
    except sr.RequestError:
        return "❌ Could not request results from Google, check your internet connection."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Streamlit UI
def main():
    st.set_page_config(page_title="Speech Recognition App", layout="centered")
    st.title("🗣️ Speech Recognition App")
    st.write("🎙️ Upload an audio file to transcribe.")

    st.sidebar.header("⚙️ Settings")
    api = st.sidebar.selectbox("🛠️ Choose API", ["Google", "Whisper"], index=0)

    uploaded_file = st.file_uploader("📂 Upload an audio file", type=["wav", "mp3"])

    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/wav")

        if api == "Whisper":
            text = transcribe_with_whisper(uploaded_file)
        elif api == "Google":
            text = transcribe_with_google(uploaded_file)

        st.subheader("📝 Transcription:")
        st.write(text)

        if text and "❌" not in text:
            st.download_button("📥 Download Transcription", text, file_name="transcription.txt")

if __name__ == "__main__":
    main()
