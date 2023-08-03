from .base import BaseProvider

import json
import requests

class BaseHFChatProvider(BaseProvider):
    provider = None

    def ask(self, prompt, chat, **kwargs):
        chat = chat["content"]

        API_URL = f"https://api-inference.huggingface.co/models/{self.provider}"

        def query(payload):
            response = requests.post(API_URL, json=payload)
            return response.json()
            
        output = query({
            "inputs": {
                "past_user_inputs": [i['content'] for i in chat if i['role'] == self.app.user_name],
                "generated_responses": [i['content'] for i in chat if i['role'] == self.app.bot_name],
                "text": prompt
            },
        })

        print(output)

        if 'generated_text' in output:
            return output['generated_text']
        elif 'error' in output:
            match output['error']:
                case "Rate limit reached. Please log in or use your apiToken":
                    return _("You've reached the rate limit! Please add a token to the preferences. You can get the token by following this [guide](https://bavarder.codeberg.page/help/huggingface/)")
