# Automated YouTube Video Summarizer and Translator

This project is a YouTube video summarizer and translator that utilizes OpenAI's GPT-3 for summarizing video content and Google Translator for translation. It also converts the translated text into an audio file using Google Text-to-Speech (gTTS) and plays it back in the app.

## Features

- **Video Summarization**: Upload a YouTube URL, and the app will summarize the video content using OpenAI's GPT-3 model.
- **Translation**: Translates the summary into Urdu using Google Translator.
- **Audio Output**: Converts the translated summary into an audio file using Google Text-to-Speech (gTTS) and plays it in the app.
- **Video Thumbnail**: Displays the thumbnail of the YouTube video once the URL is entered.

## Requirements

- Python 3.x
- `streamlit` for the web interface
- `langchain` and `langchain_community` for document processing
- `gTTS` for text-to-speech conversion
- `deep-translator` for translation
- `openai` for utilizing OpenAI models

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/owais-mazhar/youtube-video-summarizer.git
   cd youtube-video-summarizer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API Key:
   You will need to set your OpenAI API Key to use the GPT-3 model. Replace the placeholder in the code with your actual key:
   ```python
   os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

5. Open the app in your browser at `http://localhost:8501`.

## How it Works

1. **Input**: Users input a YouTube URL in the text box.
2. **Video Thumbnail**: The app automatically extracts and displays the thumbnail of the video.
3. **Summarization**: The app processes the video's audio content and generates a summary using OpenAI's GPT-3 model.
4. **Translation**: The summary is translated into Urdu using the Google Translator API.
5. **Audio**: The translated text is converted into audio using Google Text-to-Speech (gTTS), and the audio file is played back in the app.

## Example

### Input:
- A YouTube video URL, such as `https://www.youtube.com/watch?v=RguM2VAg44w`.

### Output:
- A summarized version of the video in English.
- The summary translated into Urdu.
- Audio playback of the translated summary.

## Notes

- Ensure that you have a valid OpenAI API Key for GPT-3 access.
- The video summarization relies on extracting audio from YouTube, so the video must have clear audio for best results.
- The translation is done via Google Translator, so make sure you're connected to the internet.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for the GPT-3 model.
- Google for the Text-to-Speech (gTTS) API and Translator.
- Streamlit for the web app framework.
```

### Key Sections Explained:
- **Project Description**: Overview of what the app does.
- **Features**: A list of key features of the project.
- **Installation**: Step-by-step guide to set up the project locally.
- **How it Works**: Explanation of the user flow and the technology stack.
- **Example**: A simple use case showing the input and expected output.
- **Notes**: Special requirements or considerations for running the app.
- **License and Acknowledgments**: Licensing information and thanks to the tools/APIs used in the project.