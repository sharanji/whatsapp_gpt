from typing import Any
from rest_framework.response import Response
import openai
from rest_framework.views import APIView
from heyoo import WhatsApp
import requests
from .api_key import *
from .voices import ProcessAudio


class OpenAIGPTView(APIView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.OPENAI_API_KEY = OPENAI_API_KEY
        self.fb_version = "v15.0"
        self.phone_id = "918610711834"
        self.sender_id = "116480298220877"
        self.access_token = "EAAMAp6fxdaEBO6WH9AVnbf9Q4KaASUjh6OCPXeBoEqZAidsWN7OqEOxcMSGaHwGrT1DddDnxLqNAa3Tg37GSMZA0RZCRXIKwQo8jCwMTtMXouSH9S7ots8XPOwG4lmNTWS94yT8FZA5p5iFOz9oChZC4CAU167zZCbJ9vyyZCiMuNPYMBUwGp7ZADm6G7QdAs2OnqrCLuPD1uaK1Jto80j4ZD"

    def get(self, request):
        answer = "hello boss"
        messenger = WhatsApp(self.access_token, phone_number_id=self.sender_id)
        r = messenger.send_message(answer, self.phone_id)

        return Response(answer)

    def post(self, request):
        if (
            "object" in request.data
            and request.data["object"] == "whatsapp_business_account"
        ):
            messenger = WhatsApp(self.access_token, phone_number_id=self.sender_id)
            changed_field = messenger.changed_field(request.data)
            if changed_field == "messages":
                message_type = messenger.get_message_type(request.data)
                if message_type == "audio":
                    getUserinput = ProcessAudio().getTextfromAudio(
                        messenger, jsonData=request.data, access_token=self.access_token
                    )

                elif message_type == "text":
                    getUserinput = messenger.get_message(request.data)

                message_id = messenger.get_message_id(request.data)
                user_number = messenger.get_mobile(request.data)

                # input = getUserinput
                # openai.api_key = self.OPENAI_API_KEY
                # completion = openai.ChatCompletion.create(
                #     model="gpt-3.5-turbo", messages=[{"role": "user", "content": input}]
                # )
                # answer = completion["choices"][0]["message"]["content"]
                answer = "Hello! How can I assist you today?"

                if message_type == "audio":
                    return ProcessAudio().sendSpeechresponse(
                        answer, messenger, message_id, user_number
                    )

                r = messenger.reply_to_message(
                    message_id=message_id, message=answer, recipient_id=user_number
                )

                return Response(message_type)
        return Response("Bad Request", status=200)
