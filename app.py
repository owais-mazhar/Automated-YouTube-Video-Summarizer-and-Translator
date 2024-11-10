import os
import streamlit as st
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.audio import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from gtts import gTTS
from langchain_openai import OpenAI
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from deep_translator import GoogleTranslator
import re
from datetime import datetime

# Set OpenAI API Key (replace 'YOUR_API_KEY' with your actual key)
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_KEY"

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-title {
        font-size: 20px;
        color: #1E88E5;
        margin-bottom: 10px;
    }
    .highlight {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
    }
    .button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app setup
st.markdown('<h1 class="main-title">YouTube Video Summarizer and Translator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Enter a YouTube URL to summarize its content, translate to Urdu, and listen to the translation.</p>', unsafe_allow_html=True)

# User input for YouTube URL
url = st.text_input("Enter YouTube URL:")

# Display video thumbnail if URL is provided
def get_video_id(url):
    video_id_match = re.search(r'(?<=v=)[^&#]+', url)
    if not video_id_match:
        video_id_match = re.search(r'(?<=be/)[^&#]+', url)
    return video_id_match.group(0) if video_id_match else None

video_id = get_video_id(url)
if video_id:
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"
    st.image(thumbnail_url, caption="YouTube Video Thumbnail", use_column_width=True)

# Load and process the video when button is clicked
if st.button("Process Video", key="process_video"):
    if url and video_id:
        save_dir = "youtube/"
        os.makedirs(save_dir, exist_ok=True)

        # Load and process video content
        loader = GenericLoader(
            YoutubeAudioLoader([url], save_dir),
            OpenAIWhisperParser()
        )
        
        try:
            docs = loader.load()
            doc_content = docs[0].page_content
            
            # Prompt template for summarization
            combine_prompt_template = """
            You will be given points and any important details of a text in bullet points.
            Your goal is to provide a final summary of the main topics and key findings.
            The summary should be clear, concise, and informative to help grasp the main content of the video.
            ```{text}```
            FINAL SUMMARY:
            """
            combine_prompt = PromptTemplate(input_variables=["text"], template=combine_prompt_template)
            
            # Summarize function
            def summarize_pdf(text, chunk_size, chunk_overlap, combine_prompt):
                llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)
                docs_raw_text = [text]
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                docs_chunks = text_splitter.create_documents(docs_raw_text)
                chain = load_summarize_chain(llm, chain_type="map_reduce", combine_prompt=combine_prompt)
                summary = chain.invoke(docs_chunks, return_only_outputs=True)
                return summary['output_text']
            
            # Generate summary
            st.write("Summarizing content...")
            summarized_text = summarize_pdf(doc_content, 1000, 20, combine_prompt)
            st.markdown('<div class="highlight"><h3>Summarized Text:</h3></div>', unsafe_allow_html=True)
            st.write(summarized_text)
            
            # Translate summary to Urdu
            st.write("Translating summary to Urdu...")
            translated_text = GoogleTranslator(source='en', target='ur').translate(summarized_text)
            st.markdown('<div class="highlight"><h3>Translated Text (Urdu):</h3></div>', unsafe_allow_html=True)
            st.write(translated_text)
            
            # Convert translated text to audio
            st.write("Converting translation to audio...")
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            audio_path = os.path.join(save_dir, f"output_audio_{video_id}_{timestamp}.mp3")
            tts = gTTS(text=translated_text, lang='ur')
            tts.save(audio_path)
            
            # Play audio in Streamlit
            with open(audio_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid YouTube URL.")
