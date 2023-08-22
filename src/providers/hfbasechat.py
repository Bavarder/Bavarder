from .base import BaseProvider

import requests

from gi.repository import Gtk, Adw, GLib


class BaseHFChatProvider(BaseProvider):
    provider = None
    chat_mode = True

    def ask(self, prompt, chat, **kwargs):
        chat = chat["content"]

        API_URL = f"https://api-inference.huggingface.co/models/{self.provider}"

        def query(payload):
            if self.data.get('api_key'):
                headers = {"Authorization": f"Bearer {self.data['api_key']}"}
                response = requests.post(API_URL, json=payload, headers=headers)
            else:
                response = requests.post(API_URL, json=payload)

            return response.json()
            
        if self.chat_mode:
            output = query({
                "inputs": {
                    "past_user_inputs": [i['content'] for i in chat if i['role'] == self.app.user_name],
                    "generated_responses": [i['content'] for i in chat if i['role'] == self.app.bot_name],
                    "text": prompt
                },
            })
        else:
            output = query({
                "inputs": self.make_prompt(prompt, chat),
            })

        if 'generated_text' in output:
            return output['generated_text']
        elif 'error' in output:
            match output['error']:
                case "Rate limit reached. Please log in or use your apiToken":
                    return _("You've reached the rate limit! Please add a token to the preferences. You can get the token by following this [guide](https://bavarder.codeberg.page/help/huggingface/)")
        elif isinstance(output, list):
            if 'generated_text' in output[0]:
                return output[0]['generated_text']
        else:
            print(output)
            return _("Sorry, I don't know what to say!")

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