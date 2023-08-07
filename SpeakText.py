import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    engine.setProperty("pause_between_sentences", 0.5)
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak("Hello Doctor Gamo. What's up today? what about shuriken - a winner?")
