from .base import BavarderProvider

from hugchat import hugchat
import socket
import requests
import json

from gi.repository import Gtk, Adw, GLib


class BaseHuggingChatProvider(BavarderProvider):
    name = "Hugging Chat"
    slug = "huggingchat"
    model = None
    url = "https://bavarder.codeberg.page/help/huggingchat"
    cookies = {}

    def __init__(self, win, app, *args, **kwargs):
        super().__init__(win, app, *args, **kwargs)
        
    def ask(self, prompt):
        print(self.cookies)
        try:
            self.chat = hugchat.ChatBot(cookies=self.cookies)  # or cookies=[...]
            print(self.chat)
            print(self.cookies)
        except Exception as e:
            print(e)
            self.win.banner.props.title = str(e)
            self.win.banner.props.button_label = ""
            self.win.banner.set_revealed(True)
            return ""
        else:
            try:
                response = self.chat.chat(prompt)
            except socket.gaierror:
                self.no_connection()
                return ""
            except Exception as e:
                self.win.banner.props.title = str(e)
                self.win.banner.props.button_label = ""
                self.win.banner.set_revealed(True)
                return ""
            else:
                self.win.banner.set_revealed(False)
                r = ""
                for i in response:
                    char = i["token"]["text"]
                    if char == "</s>":
                        r += "\n"
                    else:
                        r += char
                    GLib.idle_add(self.update_response, r)
                return r

    @property
    def require_api_key(self):
        return True

    def preferences(self, win):
        self.pref_win = win

        self.expander = Adw.ExpanderRow()
        self.expander.props.title = self.name

        self.expander.add_action(self.about())  # TODO: in Adw 1.4, use add_suffix
        self.expander.add_action(self.enable_switch())

        self.api_row = Adw.EntryRow()
        self.api_row.connect("apply", self.on_apply)
        self.api_row.props.text = str(self.cookies) or ""
        self.api_row.props.title = "Cookies"
        self.api_row.set_show_apply_button(True)
        self.api_row.add_suffix(self.how_to_get_a_token())
        self.expander.add_row(self.api_row)

        return self.expander

    def on_apply(self, widget):
        self.hide_banner()
        cookies = self.api_row.get_text()
        print("cookies", cookies)
        self.cookies = json.loads(cookies)
        print("Applied cookies", self.cookies)

    def save(self):
        print(self.cookies)
        print("Saved cookies", self.cookies)
        return self.cookies

    def load(self, data):
        self.cookies = data
