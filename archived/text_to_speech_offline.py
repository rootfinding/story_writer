import pyttsx3

def speak_text_offline(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()