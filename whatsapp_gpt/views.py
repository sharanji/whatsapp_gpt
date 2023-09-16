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
        self.access_token = "EAAMAp6fxdaEBO5l3oDBe9c8mdZBavxRDvlmWh2L2mAz2ZBiZAs0KEflDwlO8pb5MyZBA821fTZBbqXqVIs1B0HY7COj15FZBAkEZAkC8WxswWzJ5XNNdeEIwaMc3M01CanZCoAKmpxBalnwNNQtK1U8IADPOvV8VkwOWZBFud2KpQmSzjO2xZAkdlhLXQxNerD4l43KjFM8nYvSq9dc0L289gZDD"

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

                # r = messenger.reply_to_message(
                #     message_id=message_id, message=answer, recipient_id=user_number
                # )

                return Response(getUserinput)
        return Response("Bad Request", status=200)
