#  pip install moviepy pydub pyttsx3

from moviepy import VideoFileClip, AudioFileClip
from pydub import AudioSegment
import os

 
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
    main()
