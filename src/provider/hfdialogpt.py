from .huggingface import BaseHFProvider
import json
import socket
import requests


class HuggingFaceDialoGPTLargeProvider(BaseHFProvider):
    name = "DialoGPT"
    slug = "dialogpt"
    model = "microsoft/DialoGPT-large"
    authorization = False

    def ask(self, prompt):
        try:
            payload = json.dumps(
                {
                    "inputs": {
                        # "past_user_inputs": ["Which movie is the best ?"],
                        # "generated_responses": ["It's Die Hard for sure."],
                        "text": prompt
                    },
                }
            )
            headers = {"Content-Type": "application/json"}
            if self.authorization:
                headers["Authorization"] = f"Bearer {self.api_key}"
            url = f"https://api-inference.huggingface.co/models/{self.model}"
            print(url)
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.json())
            response = response.json()["generated_text"]

        # except NoApikey:
        #     self.no_api_key()
        #     return ""
        except KeyError:
            pass
        except socket.gaierror:
            self.no_connection()
            return ""
        else:
            self.hide_banner()
            print(response)
            self.update_response(response)
            return response
