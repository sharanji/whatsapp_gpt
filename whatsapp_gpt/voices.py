import speech_recognition as sr
import pydub

from rest_framework.response import Response
import os
from django.conf import settings
from django.http import HttpResponse, Http404
import requests
import subprocess


class ProcessAudio:
    def convert_ogg_to_wav(self, path, dest):
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
