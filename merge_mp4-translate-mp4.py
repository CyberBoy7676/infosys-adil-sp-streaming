# for run .\translate310\Scripts\activate
# pip install langchain-google-genai
# pip install langchain

from moviepy import VideoFileClip
import whisper
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from gtts import gTTS
import playsound 
from moviepy import VideoFileClip, AudioFileClip
from pydub import AudioSegment

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

# step 4: function text to speech converter
def text_to_speech_gtts(text, language='hi', output_file='output.mp3'):
    try:
        # Convert text to speech
        tts = gTTS(text=text, lang=language, slow=False)
        # Save to a file
        tts.save(output_file)
        print(f"Audio saved as {output_file}. Playing now...")
        # Play the audio file
        # playsound.playsound(output_file)
    except Exception as e:
        print("Error:", e)

# step 5
# audio added into video 

# Function to adjust audio speed to match video duration
def adjust_audio_speed(audio_file, target_duration, output_file="adjusted_audio.mp3"):
    """
    Adjust the speed of an audio file to match the given target duration.
    :param audio_file: Path to the input audio file.
    :param target_duration: Target duration in seconds.
    :param output_file: Path to the output audio file.
    :return: Path to the adjusted audio file.
    """
    audio = AudioSegment.from_file(audio_file)
    current_duration = audio.duration_seconds
    speed_factor = current_duration / target_duration

    # Adjust speed
    adjusted_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * speed_factor)
    }).set_frame_rate(audio.frame_rate)

    adjusted_audio.export(output_file, format="mp3")
    return output_file


# Function to replace audio in the original video with the adjusted audio
def replace_audio_in_video(original_video_path, adjusted_audio_path, output_video_path):
    """
    Replace the audio in the original video with the adjusted audio.
    :param original_video_path: Path to the original video file.
    :param adjusted_audio_path: Path to the adjusted audio file.
    :param output_video_path: Path to save the final video file.
    :return: Path to the final video file.
    """
    video = VideoFileClip(original_video_path)
    adjusted_audio = AudioFileClip(adjusted_audio_path)
    video_with_new_audio = video.with_audio(adjusted_audio)
    video_with_new_audio.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    return output_video_path


def main():
    # Take user input for file paths
    video_file = input("Enter the video file name (with extension): ")
    audio_file = input("Enter the audio file name (with extension): ")
    output_video_file = input("Enter the name for the output video file (with extension): ")

    if not os.path.exists(video_file) or not os.path.exists(audio_file):
        print("Error: One or both files do not exist. Please check the file paths.")
        return

    # Load video to determine duration
    video = VideoFileClip(video_file)
    video_duration = video.duration

    # Adjust the audio speed to match the video duration
    print("Adjusting audio speed to match video duration...")
    adjusted_audio_file = adjust_audio_speed(audio_file, video_duration)

    # Replace the original video audio with the adjusted audio
    print("Replacing audio in the video...")
    final_video = replace_audio_in_video(video_file, adjusted_audio_file, output_video_file)

    print(f"Final video with adjusted audio has been saved as {final_video}")



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
    #  step 4: send data text to speech convert.
    text = translated_text
    text_to_speech_gtts(text)
    # step 5:
    main()


