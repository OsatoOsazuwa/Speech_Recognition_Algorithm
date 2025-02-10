import streamlit as st
import speech_recognition as sr
import wave
import json
from vosk import Model, KaldiRecognizer
import time
from pydub import AudioSegment
import io

# Define paths to Vosk models
VOSK_MODELS = {
    "English": "vosk-model-small-en-us-0.15",
    "French": "vosk-model-small-fr-0.22",
    "Spanish": "vosk-model-small-es-0.42"
}

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
            model_path = VOSK_MODELS[language]
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

def main():
    st.set_page_config(page_title="Speech Recognition App", layout="centered")
    st.title("🗣️ Speech Recognition App")
    st.write("🎙️ Upload an audio file to transcribe.")

    st.sidebar.header("⚙️ Settings")
    api = st.sidebar.selectbox("🛠️ Choose API", ["Google", "Vosk"], index=0)
    language = st.sidebar.selectbox("🌍 Select Language", ["English", "French", "Spanish"], index=0)

    uploaded_file = st.file_uploader("📂 Upload an audio file", type=["wav", "mp3"])

    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/wav")
        text = transcribe_audio_file(uploaded_file, api, language)
        st.subheader("📝 Transcription:")
        st.write(text)

        if text and "❌" not in text:
            st.download_button("📥 Download Transcription", text, file_name="transcription.txt")

if __name__ == "__main__":
    main()
