import speech_recognition as sr
import datetime

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # recognize speech using Google Speech Recognition
        speech_text = recognizer.recognize_google(audio)
        print("You said: " + speech_text)
    except:
        print("I didn't understand what you said.")

def append_to_file(speech_text):
    now = datetime.datetime.now()
    date_and_time = now.strftime("%Y-%m-%d_%H-%M-%S")

    with open("speech.txt", "a") as f:
        f.write(f"{date_and_time}: {speech_text}\n")

if __name__ == "__main__":
    speech_text = recognize_speech()
    append_to_file(speech_text)
