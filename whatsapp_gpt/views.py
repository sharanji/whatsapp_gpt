from typing import Any
from rest_framework.response import Response
import openai
from rest_framework.views import APIView
from heyoo import WhatsApp
import requests


class OpenAIGPTView(APIView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.OPENAI_API_KEY = "****************"
        self.fb_version = "v15.0"
        self.phone_id = "918610711834"
        self.sender_id = "116480298220877"
        self.access_token = "EAAMAp6fxdaEBOZBcVNIJyZBcIArWceedWtontTyMOS1e4tIDTA5knC9ghvEkxKF3jsFmKtASFCtZAcKmCRW4KaP082Y9oU03pTpnrIZCirJqKiJ23krHlTBoFJCtJLFwUUQhE5YkhtKdbiUDyt15ZAZCfzo6ODPZChX8RAZCNKHcJG6bCr53CtVn7XI9sN2UmZA7RrJB9GA8ZCmPwDhi7Ue1QZD"

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
            getUserinput = messenger.get_message(request.data)
            message_id = messenger.get_message_id(request.data)
            user_number = messenger.get_mobile(request.data)

            input = getUserinput
            openai.api_key = self.OPENAI_API_KEY
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[{"role": "user", "content": input}]
            )
            answer = completion["choices"][0]["message"]["content"]
            answer = "heelo boss"
            r = messenger.reply_to_message(
                message_id=message_id, message=answer, recipient_id=user_number
            )

            return Response(r)
        return Response("Bad Request", status=400)
