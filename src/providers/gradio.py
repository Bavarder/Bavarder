import requests
import json
from .base import BavarderProvider

import socket

from gi.repository import Gtk, Adw, GLib

from gradio_client import Client

class BaseGradioProvider(BavarderProvider):
    name = None
    slug = None
    url = None

    def __init__(self, win, app, *args, **kwargs):
        super().__init__(win, app, *args, **kwargs)

        self.client = Client(self.url)

    def ask(self, prompt):
        print("ASKING " + "="*100)
        try:
            response = self.client.predict(
				prompt,	# str representing string value in 'Chat Message Box' Textbox component
				fn_index=0
            )
            print(response)
        except Exception as e:
            print(e)
            self.win.banner.props.title = str(e)
            self.win.banner.props.button_label = ""
            self.win.banner.set_revealed(True)
        else:
            self.hide_banner()
            GLib.idle_add(self.update_response, response)
            return response

    @property
    def require_api_key(self):
        return False

    def preferences(self, win):
        if self.require_api_key:
            self.expander = Adw.ExpanderRow()
            self.expander.props.title = self.name

            self.expander.add_action(self.about())
            self.expander.add_action(self.enable_switch())

            # TODO: ADD DEVICE

            return self.expander
        else:
            return self.no_preferences(win)

    def on_apply(self, widget):
        self.hide_banner()

    def save(self):
        return {}

    def load(self, data):
        pass
