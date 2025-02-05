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

def transcribe_speech(api, language):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        audio_text = recognizer.listen(source, timeout=10)
        st.info("⏳ Transcribing...")

        try:
            if api == "Google":
                lang_code = {"English": "en-US", "French": "fr-FR", "Spanish": "es-ES"}[language]
                text = recognizer.recognize_google(audio_text, language=lang_code)
                return text.capitalize()
            
            elif api == "Vosk":
                model_path = VOSK_MODELS[language]
                model = Model(model_path)
                rec = KaldiRecognizer(model, 16000)

                wav_data = audio_text.get_wav_data()

                # Convert to audio using pydub and resample to 16kHz if necessary
                audio = AudioSegment.from_wav(io.BytesIO(wav_data))
                audio = audio.set_frame_rate(16000)  # Resample to 16kHz
                audio = audio.set_channels(1)  # Mono channel
                audio = audio.set_sample_width(2)  # 16-bit sample width

                # Save the resampled audio to a temporary file
                audio.export("temp_audio.wav", format="wav")
                st.info("✅ WAV file saved and resampled to 16kHz.")

                # Process the WAV file with Vosk
                with wave.open("temp_audio.wav", "rb") as wav_file:
                    while True:
                        data = wav_file.readframes(4000)
                        if len(data) == 0:
                            break
                        if rec.AcceptWaveform(data):
                            text = json.loads(rec.Result())["text"]
                            return text

                # Final result after the stream ends
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
    st.title("🗣️ Enhanced Speech Recognition App")
    st.write("🎙️ Click 'Start Recording' and speak.")

    # Sidebar settings
    st.sidebar.header("⚙️ Settings")

    # Select Speech Recognition API
    api = st.sidebar.selectbox("🛠️ Choose API", ["Google", "Vosk"], index=0)

    # Select Language
    language = st.sidebar.selectbox("🌍 Select Language", ["English", "French", "Spanish"], index=0)

    # Start & Pause Buttons
    if st.button("🎤 Start Recording"):
        text = transcribe_speech(api, language)
        st.subheader("📝 Transcription:")
        st.write(text)

        if text and "❌" not in text:
            st.download_button("📥 Download Transcription", text, file_name="transcription.txt")

    pause_state = st.sidebar.checkbox("⏸️ Pause Speech Recognition")
    if pause_state:
        time.sleep(5)
        st.sidebar.success("Recognition Paused. Resume when ready.")

if __name__ == "__main__":
    main()
