from .baseimage import BaseImageProvider
import requests
import json
from gi.repository import Gtk, Adw, GLib
from PIL import Image, UnidentifiedImageError
import io


class BaseHFImageProvider(BaseImageProvider):
    provider = None

    def ask(self, prompt, chat, **kwargs):
        chat = chat["content"]

        API_URL = f"https://api-inference.huggingface.co/models/{self.provider}"

        def query(payload):
            if self.data.get('api_key'):
                headers = {"Authorization": f"Bearer {self.data['api_key']}"}
                response = requests.post(API_URL, json=payload, headers=headers)
            else:
                response = requests.post(API_URL, json=payload)

            if response.status_code == 403:
                return _("You've reached the rate limit! Please add a token to the preferences. You can get the token by following this [guide](https://bavarder.codeberg.page/help/huggingface/)")
            elif response.status_code != 200:
                return _("Sorry, I don't know what to say! (Error: {response.status_code})")

            return response.content
       
        prompt = self.make_prompt(prompt, chat)
        output = query({
            "inputs": prompt,
            "negative_prompts": "",
        })

        if output:
            print(output)
            try:
                print("IMAGE")
                return Image.open(io.BytesIO(output))
            except UnidentifiedImageError:
                print("FAILED IMAGE")
                return output

    def get_settings_rows(self):
        self.rows = []

        self.api_row = Adw.PasswordEntryRow()
        self.api_row.connect("apply", self.on_apply)
        self.api_row.props.text = self.data.get('api_key') or ""
        self.api_row.props.title = _("API Key")
        self.api_row.set_show_apply_button(True)
        self.api_row.add_suffix(self.how_to_get_a_token())
        self.rows.append(self.api_row)

        return self.rows

    def on_apply(self, widget):
        api_key = self.api_row.get_text()
        self.data["api_key"] = api_key

    def make_prompt(self, prompt, chat):
        return prompt   