import cv2
import time
import pyttsx3
from gradio_client import Client, handle_file
import tempfile
import os

# Initialize the TTS engine
engine = pyttsx3.init()


# Function to convert text to speech
def text_to_speech(text):
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 15 )  # Slows down the speech

    # You can adjust the volume (optional)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 1.0)  # Maximum volume

    # You can set the voice type (optional, male/female)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


# Initialize the Gradio client
client = Client("vikhyatk/moondream2")


# Function to process the image and get a description
def process_image(image_path):
    result = client.predict(
        img=handle_file(image_path),
        prompt="Describe this image.",
        api_name="/answer_question"
    )
    return result


def main():
    # Set up the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        # Save the frame as a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_file_path = temp_file.name
            cv2.imwrite(temp_file_path, frame)

        # Process the image using Gradio API
        description = process_image(temp_file_path)
        print(f"Description: {description}")

        # Convert the description to speech
        text_to_speech(description)

        # Clean up the temporary file
        os.remove(temp_file_path)

        # Wait for 10 seconds before capturing the next image

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
