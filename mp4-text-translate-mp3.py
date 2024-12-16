# for run .\translate310\Scripts\activate
# pip install langchain-google-genai
# pip install langchain

from moviepy import VideoFileClip
import whisper
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# Function to convert MP4 to MP3
def convert_video_to_audio(video_path, audio_output_path):
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_output_path, codec='libmp3lame')
        print(f"Audio extracted and saved as: {audio_output_path}")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

# Function to transcribe MP3 to text
def transcribe_mp3_to_text(mp3_path):
    try:
        model = whisper.load_model("base")  # Whisper model (tiny, base, small, etc.)
        if not os.path.exists(mp3_path):
            raise FileNotFoundError(f"Audio file not found: {mp3_path}")
        print("Transcribing audio... This may take a moment.")
        result = model.transcribe(mp3_path)
        return result['text']
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return None

# Function to translate text to a desired language
def translate_text(input_text, desired_language):
    try:
        summary_prompt = """
        You are a translator. Translate the given input text into the desired language:
        
        Input Text: {input-text}
        Desired Language: {desired-language}
        """
        prompt_template = PromptTemplate(input_variables=['input-text', 'desired-language'], template=summary_prompt)
        llm = ChatGoogleGenerativeAI(
            model = 'gemini-1.5-flash',
            api_key = 'AIzaSyBsk9teXzKWVHeOKHN_PbVBAVZ3CI5oV5k'   # Set your API key in the environment
        )
        chain = prompt_template | llm | StrOutputParser()
        response = chain.invoke({"input-text": input_text, "desired-language": desired_language})
        return response
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return None

if __name__ == "__main__":
    # Step 1: Convert MP4 to MP3
    video_file = input("Enter the path to the MP4 video file: ")
    audio_file_name = input("Enter the name for the MP3 audio file (without extension): ") + ".mp3"
    convert_video_to_audio(video_file, audio_file_name)

    # Step 2: Transcribe MP3 to text
    transcription = transcribe_mp3_to_text(audio_file_name)
    if transcription:
        print("\nTranscription Result:\n")
        print(transcription)

        # Step 3: Translate text to desired language
        desired_language = input("\nEnter the desired language for translation: ")
        translated_text = translate_text(transcription, desired_language)
        if translated_text:
            print("\nTranslated Text:\n")
            print(translated_text)


# text to speech convert (mp3) converter
from gtts import gTTS
import playsound
import os

def text_to_speech_gtts(text, language='hi', output_file='output.mp3'):
    try:
        # Convert text to speech
        tts = gTTS(text=text, lang=language, slow=False)
        # Save to a file
        tts.save(output_file)
        print(f"Audio saved as {output_file}. Playing now...")
        # Play the audio file
        playsound.playsound(output_file)
    except Exception as e:
        print("Error:", e)

# Example usage
text = translated_text
text_to_speech_gtts(text)
