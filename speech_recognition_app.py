import streamlit as st
import speech_recognition as sr
import wave
import json
import os
import requests
import zipfile
import io
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer

# Vosk model download URLs (official sources)
VOSK_MODEL_URLS = {
    "English": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
    "French": "https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip",
    "Spanish": "https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip"
}

# Local storage path for models
MODEL_DIR = "vosk_models"

# Function to download and extract the Vosk model if not found
def download_vosk_model(language):
    model_path = os.path.join(MODEL_DIR, f"vosk-model-small-{language.lower()}")
    
    if not os.path.exists(model_path):
        st.info(f"📥 Downloading {language} model, please wait...")
        os.makedirs(MODEL_DIR, exist_ok=True)
        
        url = VOSK_MODEL_URLS[language]
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(response.content), "r") as zip_ref:
                zip_ref.extractall(MODEL_DIR)
            st.success(f"✅ {language} model downloaded successfully!")
        else:
            st.error("❌ Model download failed. Check your internet connection.")
    
    return model_path

# Function to transcribe uploaded audio
def transcribe_audio_file(audio_file, api, language):
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_file) as source:
            st.info("🔄 Processing uploaded file...")
            audio_text = recognizer.record(source)

        if api == "Google":
            lang_code = {"English": "en-US", "French": "fr-FR", "Spanish": "es-ES"}[language]
            text = recognizer.recognize_google(audio_text, language=lang_code)
            return text.capitalize()

        elif api == "Vosk":
            model_path = download_vosk_model(language)
            model = Model(model_path)
            rec = KaldiRecognizer(model, 16000)

            wav_data = audio_text.get_wav_data()
            audio = AudioSegment.from_wav(io.BytesIO(wav_data))
            audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)

            audio.export("temp_audio.wav", format="wav")

            with wave.open("temp_audio.wav", "rb") as wav_file:
                while True:
                    data = wav_file.readframes(4000)
                    if len(data) == 0:
                        break
                    if rec.AcceptWaveform(data):
                        text = json.loads(rec.Result())["text"]
                        return text

            text = json.loads(rec.FinalResult())["text"]
            return text.capitalize()

        else:
            return "❌ Selected API is not available."

    except sr.UnknownValueError:
        return "❌ Could not understand the audio."
    except sr.RequestError:
        return "❌ Could not request results, check your internet connection."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Streamlit UI
def main():
    st.set_page_config(page_title="Speech Recognition App", layout="centered")
    st.title("🗣️ Speech Recognition App")
    st.write("🎙️ Upload an audio file to transcribe.")

    st.sidebar.header("⚙️ Settings")
    api = st.sidebar.selectbox("🛠️ Choose API", ["Google", "Vosk"], index=0)
    language = st.sidebar.selectbox("🌍 Select Language", ["English", "French", "Spanish"], index=0)

    uploaded_file = st.file_uploader("📂 Upload an audio file", type=["wav"])

    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/wav")
        text = transcribe_audio_file(uploaded_file, api, language)
        st.subheader("📝 Transcription:")
        st.write(text)

        if text and "❌" not in text:
            st.download_button("📥 Download Transcription", text, file_name="transcription.txt")

if __name__ == "__main__":
    main()
