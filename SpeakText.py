import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    engine.setProperty("pause_between_sentences", 0.1)
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak("Why not he's a good driver")
