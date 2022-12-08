import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)
# engine.setProperty('voice', "com.apple.speech.synthesis.voice.Fred")

with sr.Microphone() as source:
    print('listening...')
    voice = listener.listen(source)
    # command = listener.recognize_sphinx(voice,language = "en-US")
    command = listener.recognize_vosk(voice,language = "zh-CN")
    print(command)


for voice in voices:  
    if "zh_CN" in voice.languages:
        print(voice.id)
        engine.setProperty('voice', voice.id)
        engine.setProperty("rate", 90)
        engine.say(command)
        engine.runAndWait()
        engine.stop()