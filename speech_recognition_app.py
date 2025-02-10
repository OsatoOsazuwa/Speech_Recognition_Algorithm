import streamlit as st
import speech_recognition as sr
import io
from pydub import AudioSegment

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
    api = st.sidebar.selectbox("🛠️ Choose API", ["Google"], index=0)
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
