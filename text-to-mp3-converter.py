from gtts import gTTS
import playsound
import os

def text_to_speech_gtts(text, language='en', output_file='output.mp3'):
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
text = "ಹಲೋ, TOT ಮತ್ತು ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆಯ ಜಗತ್ತಿಗೆ ಸ್ವಾಗತ. ಒಟ್ಟಿಗೆ ಅದ್ಭುತವಾದ ವಿಷಯಗಳನ್ನು ರಚಿಸೋಣ."
text_to_speech_gtts(text)
