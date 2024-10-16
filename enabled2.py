import speech_recognition as sr

from enabled import text_to_speech


#from enabled import text_to_speech


def get_voice_command():
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening for your voice command...")

        # Adjust for ambient noise to improve recognition in noisy environments
        recognizer.adjust_for_ambient_noise(source)

        # Listen for the voice command
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Processing...")

            # Recognize speech using Google Web Speech API
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command

        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service: {e}")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for a phrase.")
            return None

# Test the function by calling it
if __name__ == "__main__":
    command = get_voice_command()
    if command:
        text_to_speech("Today is a good day")
        print(f"Voice Command: {command}")
