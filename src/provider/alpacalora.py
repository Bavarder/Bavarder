from .base import BavarderProvider

import socket
import requests

from gi.repository import Gtk, Adw, GLib


class AlpacaLoRAProvider(BavarderProvider):
    name = "Alpaca-LoRA"
    slug = "alpacalora"

    def __init__(self, win, app, *args, **kwargs):
        super().__init__(win, app, *args, **kwargs)

    def ask(self, prompt):
        try:
            response = requests.post(
                "https://tloen-alpaca-lora.hf.space/run/predict",
                json={
                    "data": [
                        prompt,
                        prompt,
                        0.1,
                        0.75,
                        40,
                        4,
                        128,
                    ]
                },
            ).json()
        except socket.gaierror:
            self.no_connection()
            return ""
        else:
            self.win.banner.set_revealed(False)
            r = response["data"][0]
            GLib.idle_add(self.update_response, r)
            return r

    @property
    def require_api_key(self):
        return False
        
    def save(self):
        return {}

    def load(self, data):
        pass
