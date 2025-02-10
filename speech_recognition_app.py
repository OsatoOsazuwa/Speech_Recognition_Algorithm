import os
import streamlit as st
import wave
import json
import speech_recognition as sr
from pydub import AudioSegment
import io

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

# Function to transcribe audio using Sphinx
def transcribe_with_sphinx(audio_file):
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file) as source:
            st.info("🔄 Processing uploaded file with Sphinx...")  # Update for better clarity
            audio_text = recognizer.record(source)

        text = recognizer.recognize_sphinx(audio_text)
        return text.capitalize()

    except sr.UnknownValueError:
        return "❌ Could not understand the audio."
    except sr.RequestError:
        return "❌ Could not request results from Sphinx."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Streamlit UI
def main():
    st.set_page_config(page_title="Speech Recognition App", layout="centered")
    st.title("🗣️ Speech Recognition App")
    st.write("🎙️ Upload an audio file to transcribe.")

    st.sidebar.header("⚙️ Settings")
    api = st.sidebar.selectbox("🛠️ Choose API", ["Google", "Sphinx"], index=0)

    uploaded_file = st.file_uploader("📂 Upload an audio file", type=["wav", "mp3"])

    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/wav")

        if api == "Sphinx":
            text = transcribe_with_sphinx(uploaded_file)
        elif api == "Google":
            text = transcribe_with_google(uploaded_file)

        st.subheader("📝 Transcription:")
        st.write(text)

        if text and "❌" not in text:
            st.download_button("📥 Download Transcription", text, file_name="transcription.txt")

if __name__ == "__main__":
    main()
