import speech_recognition as sr
import pydub
from gtts import gTTS


from django.http import FileResponse
import requests
from heyoo import WhatsApp
from rest_framework.response import Response
import socket


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

    def sendSpeechresponse(self, message, messenger: WhatsApp, message_id, user_number):
        language = "en"
        myobj = gTTS(text=message, lang=language, slow=False)
        myobj.save(f"static/{message_id}.mp3")

        r = messenger.send_audio(
            audio=f"http://52.14.141.153:8000/static/{message_id}.mp3",
            recipient_id=user_number,
        )

        return Response(f"http://52.14.141.153:8000/static/{message_id}.mp3")
