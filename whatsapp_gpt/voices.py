import speech_recognition as sr
import pyttsx3
import soundfile as sf
import numpy as np
from scipy.io import wavfile
import pydub
import ffmpeg

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
    def convert_ogg_to_wav(self, path, dest):
        pydub.AudioSegment.ffmpeg = ffmpeg.__path__
        song = pydub.AudioSegment.from_ogg(path)
        song.export(dest, format="wav")

    def getTextfromAudio(self, messenger, jsonData, access_token):
        audio = messenger.get_audio(jsonData)
        audio_id, mime_type = audio["id"], audio["mime_type"]
        audio_url = messenger.query_media_url(audio_id)
        audio_filename = messenger.download_media(
            audio_url, mime_type, file_path="audios"
        )
        response = requests.request(
            "GET",
            audio_url,
            headers={"Authorization": f"Bearer {access_token}"},
            data={},
        )
        media_file = open(f"audios/{audio_id}.ogg", "wb")
        media_file.write(response.content)
        media_file.close()

        self.convert_ogg_to_wav(f"audios/{audio_id}.ogg", f"audios/wav/{audio_id}.wav")

        # # Initialize the recognizer
        r = sr.Recognizer()
        audio_file = sr.AudioFile(f"audios/wav/{audio_id}.wav")
        with audio_file as source:
            recorded_audio = r.record(source)
        extracted_text = r.recognize_google(recorded_audio)

        return extracted_text
