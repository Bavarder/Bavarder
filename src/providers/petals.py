from .base import BaseProvider

import json
import requests

class BasePetalsProvider(BaseProvider):
    provider = None

    API_URL = "https://chat.petals.dev/"
    ENDPOINT = "/api/v1/generate"

    model = None

    def ask(self, prompt, chat, **kwargs):
        try:
            API_URL = self.data["api_url"]
        except KeyError:
            API_URL = self.API_URL

        API_URL += self.ENDPOINT

        chat = chat["content"]

            
        r = f"{API_URL}?model={self.model}&do_sample=1&temperature=0.75&top_p=0.9&max_length=1000&inputs={prompt}"
        
        output = requests.post(r).json()

        if output["ok"]:
            return output["outputs"]
        else:
            return _("I'm sorry, I don't know what to say!")