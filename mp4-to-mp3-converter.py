# .\translate310\Scripts\activate for activate vertual envirenmaent
# pip install moviepy
# c:\users\adilr\anaconda3\python.exe .\mp4-to-mp3-converter.py
#  python mp4-to-mp3-converter.py
from moviepy import VideoFileClip

def convert_video_to_audio(video_path, audio_output_path):
    """
    Converts an MP4 video file to an MP3 audio file.
    
    Parameters:
        video_path (str): Path to the input MP4 video file.
        audio_output_path (str): Path to save the output MP3 audio file.
    """
    try:
        # Load the video file
        video = VideoFileClip(video_path)
        
        # Extract audio and save it as an MP3 file
        video.audio.write_audiofile(audio_output_path, codec='libmp3lame') 
        print(f"Audio extracted and saved as: {audio_output_path}")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

if __name__ == "__main__":
    # Input video file path
    video_file = "sample_video.mp4"  # Replace with your video file path
    
    # Output audio file path
    audio_file = "output_audio.mp3"  # Specify the desired output MP3 file path
    
    # Convert the video to audio
    convert_video_to_audio(video_file, audio_file)