import os
import streamlit as st
import torch
import whisper
from gtts import gTTS
from deep_translator import GoogleTranslator
from pydub import AudioSegment

# Ensure ffmpeg is configured for pydub
AudioSegment.converter = "ffmpeg"

# Streamlit app setup
st.title("YouTube Video Summarizer and Translator")
st.write("Enter a YouTube URL to summarize its content, translate to Urdu, and listen to the translation.")

# User input for YouTube URL
url = st.text_input("Enter YouTube URL:", "https://www.youtube.com/watch?v=5lNQdVJs3pg")

# Function to transcribe audio using openai-whisper
def transcribe_audio(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")
    
    model = whisper.load_model("base")  # Choose the desired model size
    result = model.transcribe(file_path)
    return result["text"]

# Load and process the video when button is clicked
if st.button("Process Video"):
    if url:
        try:
            # Simulate audio download for testing
            audio_path = "sample_audio.mp3"  # Replace with actual audio path after download

            # Ensure the audio file exists
            if not os.path.exists(audio_path):
                st.error(f"Audio file not found: {audio_path}")
            else:
                # Convert MP3 to WAV if needed
                wav_path = "sample_audio.wav"
                audio = AudioSegment.from_file(audio_path)
                audio.export(wav_path, format="wav")

                # Transcribe the audio
                st.write("Transcribing audio...")
                transcription = transcribe_audio(wav_path)
                st.subheader("Transcribed Text:")
                st.write(transcription)

                # Translate transcription to Urdu
                st.write("Translating transcription to Urdu...")
                translated_text = GoogleTranslator(source='en', target='ur').translate(transcription)
                st.subheader("Translated Text (Urdu):")
                st.write(translated_text)

                # Convert translated text to audio
                st.write("Converting translation to audio...")
                tts = gTTS(text=translated_text, lang='ur')
                translated_audio_path = "output_audio.mp3"
                tts.save(translated_audio_path)

                # Play audio in Streamlit
                audio_file = open(translated_audio_path, "rb")
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")
                audio_file.close()

        except FileNotFoundError as fnf_error:
            st.error(f"File error: {fnf_error}")
        except RuntimeError as rt_error:
            st.error(f"Runtime error during transcription: {rt_error}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid YouTube URL.")
