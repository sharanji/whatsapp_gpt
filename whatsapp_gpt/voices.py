import speech_recognition as sr
import pyttsx3
from pydub import AudioSegment

# audio2 = sr.AudioFile("D:\django\whatsapp_gpt\whatsapp_gpt\sample.wav")

# with audio2 as source:
#     audio = r.record(source)

# MyText = r.recognize_google(audio)
# MyText = MyText.lower()

# print("Did you say ", MyText)
from rest_framework.response import Response
import os
from django.conf import settings
from django.http import HttpResponse, Http404
import requests
import subprocess


class ProcessAudio:
    def getTextfromAudio(self, messenger, jsonData, access_token):
        audio = messenger.get_audio(jsonData)
        audio_id, mime_type = audio["id"], audio["mime_type"]
        audio_url = messenger.query_media_url(audio_id)
        audio_filename = messenger.download_media(
            audio_url, mime_type, file_path="audios"
        )
        # response = requests.request(
        #     "GET",
        #     audio_url,
        #     headers={"Authorization": f"Bearer {access_token}"},
        #     data={},
        # )
        # media_file = open(f"audios/{audio_id}.wav", "wb")
        # media_file.write(response.content)
        # media_file.close()

        # Initialize the recognizer
        r = sr.Recognizer()

        subprocess.run(
            f"ffmpeg -i audios/865375815144174.mp3 audios/wav/865375815144174.wav",
            shell=True,
        )
        # sound = AudioSegment.from_mp3("audios/865375815144174.mp3")
        # sound.export("audios/wav/865375815144174.wav", format="wav")

        audio_file = sr.AudioFile(f"audios/865375815144174.mp3")
        # audio_file = sr.AudioFile(f"audios/{audio_id}.wav")
        with audio_file as source:
            recorded_audio = r.record(source)
        extracted_text = r.recognize_google(recorded_audio)

        return extracted_text
