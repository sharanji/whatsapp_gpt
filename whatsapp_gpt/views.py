from typing import Any
from rest_framework.response import Response
import openai
from rest_framework.views import APIView


class OpenAIGPTView(APIView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.OPENAI_API_KEY = "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"

    def get(self, request):
        input = request.GET.get("q")
        openai.api_key = self.OPENAI_API_KEY
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": input}]
        )
        answer = completion["choices"][0]["message"]["content"]
        return Response(answer)
