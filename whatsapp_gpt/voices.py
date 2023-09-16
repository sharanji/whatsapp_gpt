import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()

audio2 = sr.AudioFile("D:\django\whatsapp_gpt\whatsapp_gpt\sample.wav")

with audio2 as source:
    audio = r.record(source)

MyText = r.recognize_google(audio)
MyText = MyText.lower()

print("Did you say ", MyText)
