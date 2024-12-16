import whisper  # OpenAI's Whisper library for speech-to-text processing
import os       # For file handling (optional)

# Load the Whisper model
# Options: tiny, base, small, medium, large
# Choose based on system capability and speed requirements
model = whisper.load_model("base")

def transcribe_mp3_to_text(mp3_path):
    try:
        # Check if the file exists
        if not os.path.exists(mp3_path):
            raise FileNotFoundError(f"Audio file not found: {mp3_path}")

        # Perform transcription
        print("Transcribing audio... This may take a moment.")
        result = model.transcribe(mp3_path)
        print(result)
        # Return the transcribed text
        return result['text']
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return None

if __name__ == "__main__":
    # Input MP3 file path
    audio_file="C:/Users/adilr/OneDrive/Desktop/infosys_sprinboard/sir_code/output_audio.mp3"  # Replace with your MP3 file path
    
    
    # Transcribe the MP3 audio to text
    transcription = transcribe_mp3_to_text(audio_file)
    
    # Print the transcription result
    if transcription:
        print("\nTranscription:\n")
        print(transcription)

















"""
    Transcribes speech from an MP3 file to text using Whisper.
    
    Parameters:
        mp3_path (str): Path to the MP3 audio file.
        
    Returns:
        str: Transcribed text.
    """