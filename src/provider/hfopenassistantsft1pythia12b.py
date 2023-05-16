from .huggingface import BaseHFProvider

import requests
import json
import socket

from gi.repository import Gtk, Adw, GLib

class HuggingFaceOpenAssistantSFT1PythiaProvider(BaseHFProvider):
    name = "Open-Assistant SFT-1 12B Model"
    slug = "hfopenassistantsft1pythia12b"
    model = "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"

    @property
    def require_api_key(self):
        return False

    def ask(self, prompt):
        prompt = f"<|prompter|> {prompt}<|endoftext|><|assistant|>"
        try:
            payload = json.dumps({"inputs": prompt})
            headers = {"Content-Type": "application/json"}
            if self.require_api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            url = f"https://api-inference.huggingface.co/models/{self.model}"
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 403:
                self.no_api_key()
                return ""
            elif response.status_code != 200:
                self.win.banner.props.title = response.json()["error"]
                self.win.banner.props.button_label = ""
                self.win.banner.set_revealed(True)
                return ""
            response = response.json()[0]["generated_text"].split("<|assistant|>")[1].strip()

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
            GLib.idle_add(self.update_response, response)
            return response