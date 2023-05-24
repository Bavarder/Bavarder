import requests
import json
from .base import BavarderProvider

import socket

from gi.repository import Gtk, Adw, GLib

from transformers import AutoModelForCausalLM, AutoTokenizer

class BaseTransformerProvider(BavarderProvider):
    name = None
    slug = None
    checkpoint = None
    device = "cpu"
    is_setup = False
    api_key = None

    def __init__(self, win, app, *args, **kwargs):
        super().__init__(win, app, *args, **kwargs)

    def setup(self):
        try:
            if self.require_api_key:
                self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint, use_auth_token=self.api_key)
            else:
                self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)
            self.model = AutoModelForCausalLM.from_pretrained(self.checkpoint).to(self.device)
        except Exception as e:
            print(e)
            self.win.banner.props.title = str(e)
            self.win.banner.props.button_label = ""
            self.win.banner.set_revealed(True)
        else:
            self.is_setup = True

    def ask(self, prompt):
        self.setup()
        if self.is_setup:
            try:
                inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
                outputs = self.model.generate(inputs)
                response = self.tokenizer.decode(outputs[0])
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
        return True

    def preferences(self, win):
        if self.require_api_key:
            self.expander = Adw.ExpanderRow()
            self.expander.props.title = self.name

            self.expander.add_action(self.about())
            self.expander.add_action(self.enable_switch())

            self.api_row = Adw.PasswordEntryRow()
            self.api_row.connect("apply", self.on_apply)
            self.api_row.props.title = _("API Key")
            self.api_row.props.text = self.api_key or ""
            self.api_row.add_suffix(self.how_to_get_a_token())
            self.api_row.set_show_apply_button(True)
            self.expander.add_row(self.api_row)

            return self.expander
        else:
            return self.no_preferences(win)

    def on_apply(self, widget):
        self.hide_banner()
        self.api_key = self.api_row.get_text()

    def save(self):
        if self.require_api_key:
            return {"api_key": self.api_key}
        return {}

    def load(self, data):
        if self.require_api_key:
            self.api_key = data["api_key"]