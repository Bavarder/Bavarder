import requests
import json
from .base import BavarderProvider

import socket

from gi.repository import Gtk, Adw, GLib


class BaseHFProvider(BavarderProvider):
    name = None
    slug = None
    model = None
    authorization = True

    def __init__(self, win, app, *args, **kwargs):
        super().__init__(win, app, *args, **kwargs)
        self.api_key = None

    def ask(self, prompt):
        try:
            payload = json.dumps({"inputs": prompt})
            headers = {"Content-Type": "application/json"}
            if self.authorization:
                headers["Authorization"] = f"Bearer {self.api_key}"
            url = f"https://api-inference.huggingface.co/models/{self.model}"
            print(url)
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 403:
                self.no_api_key()
                return ""
            elif response.status_code != 200:
                self.win.banner.props.title = response.json()["error"]
                self.win.banner.props.button_label = ""
                self.win.banner.set_revealed(True)
                return ""
            print(response)
            response = response.json()[0]["generated_text"]

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

    @property
    def require_api_key(self):
        return False

    def preferences(self):
        if self.require_api_key:
            self.expander = Adw.ExpanderRow()
            self.expander.props.title = self.name

            self.api_row = Adw.PasswordEntryRow()
            self.api_row.connect("apply", self.on_apply)
            self.api_row.props.title = "API Key"
            self.api_row.props.text = self.api_key or ""
            self.api_row.set_show_apply_button(True)
            self.expander.add_row(self.api_row)

            return self.expander
        pass

    def on_apply(self, widget):
        self.hide_banner()
        self.api_key = self.api_row.get_text()
        print(self.api_key)

    def about(self):
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name=self.name,
            developer_name="HuggingFace",
            developers=["0xMRTT https://github.com/0xMRTT"],
            license_type=Gtk.License.GPL_3_0,
            version=version,
            copyright="© 2023 0xMRTT",
        )

    def save(self):
        if self.require_api_key:
            return {"api_key": self.api_key}
        return {}

    def load(self, data):
        if self.require_api_key:
            self.api_key = data["api_key"]
