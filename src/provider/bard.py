from .base import BavarderProvider

import socket
import requests
import re
import random
import json
import string

from gi.repository import Gtk, Adw

class BardChat:
    def __init__(self, session_id):
        headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
        self._reqid = int("".join(random.choices(string.digits, k=4)))
        self.conversation_id = ""
        self.response_id = ""
        self.choice_id = ""
        self.session = requests.Session()
        self.session.headers = headers
        self.session.cookies.set("__Secure-1PSID", session_id)
        self.SNlM0e = self.__get_snlm0e()

    def __get_snlm0e(self):
        resp = self.session.get(url="https://bard.google.com/", timeout=10)
        # Find "SNlM0e":"<ID>"
        if resp.status_code != 200:
            raise Exception("Could not get Google Bard")
        SNlM0e = re.search(r"SNlM0e\":\"(.*?)\"", resp.text).group(1)
        return SNlM0e

    def ask(self, prompt: str) -> dict:
        # url params
        params = {
            "bl": "boq_assistant-bard-web-server_20230419.00_p1",
            "_reqid": str(self._reqid),
            "rt": "c",
        }

        # prompt arr -> data["f.req"]. Message is double json stringified
        message_struct = [
            [prompt],
            None,
            [self.conversation_id, self.response_id, self.choice_id],
        ]
        data = {
            "f.req": json.dumps([None, json.dumps(message_struct)]),
            "at": self.SNlM0e,
        }

        # do the request!
        resp = self.session.post(
            "https://bard.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate",
            params=params,
            data=data,
            timeout=120,
        )

        chat_data = json.loads(resp.content.splitlines()[3])[0][2]
        if not chat_data:
            return {"content": f"Google Bard encountered an error: {resp.content}."}
        json_chat_data = json.loads(chat_data)
        results = {
            "content": json_chat_data[0][0],
            "conversation_id": json_chat_data[1][0],
            "response_id": json_chat_data[1][1],
            "factualityQueries": json_chat_data[3],
            "textQuery": json_chat_data[2][0] if json_chat_data[2] is not None else "",
            "choices": [{"id": i[0], "content": i[1]} for i in json_chat_data[4]],
        }
        self.conversation_id = results["conversation_id"]
        self.response_id = results["response_id"]
        self.choice_id = results["choices"][0]["id"]
        self._reqid += 100000
        return results
    


class BardProvider(BavarderProvider):
    name = "Bard"
    slug = "bard"
    version = "0.1.0"

    def __init__(self, win, app, *args, **kwargs):
        super().__init__(win, app, *args, **kwargs)
        self.pref_win = None

    def ask(self, prompt):
        try:
            response = self.chat.ask(prompt)
            response = response["content"]
        except AttributeError:
            self.no_api_key()
            return ""
        except socket.gaierror:
            self.no_connection()
            return ""
        else:
            self.hide_banner()
            self.update_response(response)
            return response

    @property
    def require_api_key(self):
        return True

    def preferences(self, win):
        self.pref_win = win

        self.expander = Adw.ExpanderRow()
        self.expander.props.title = self.name

        about_button = Gtk.Button()
        about_button.set_label("About")
        about_button.connect("clicked", self.about)
        about_button.set_valign(Gtk.Align.CENTER)
        self.expander.add_action(about_button) # TODO: in Adw 1.4, use add_suffix


        self.api_row = Adw.PasswordEntryRow()
        self.api_row.connect("apply", self.on_apply)
        self.api_row.props.title = "__Secure-1PSID cookie"
        self.api_row.set_show_apply_button(True)
        self.expander.add_row(self.api_row)

        return self.expander

    def on_apply(self, widget):
        self.hide_banner()
        api_key = self.api_row.get_text()
        print(api_key)
        self.api_key = api_key
        self.chat = BardChat(api_key)

    def about(self, *args):
        about = Adw.AboutWindow(
            transient_for=self.pref_win,
            application_name="Bard",
            developer_name="Google",
            developers=["0xMRTT https://github.com/0xMRTT"],
            license_type=Gtk.License.GPL_3_0,
            version=self.version,
            copyright="© 2023 0xMRTT",
        )
        about.present()

    def save(self):
        return {"api_key": self.api_key}

    def load(self, data):
        self.chat = BardChat(api_key)
        self.api_key = api_key
