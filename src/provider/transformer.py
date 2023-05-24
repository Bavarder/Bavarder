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

    def __init__(self, win, app, *args, **kwargs):
        super().__init__(win, app, *args, **kwargs)

    def setup(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)
        self.model = AutoModelForCausalLM.from_pretrained(self.checkpoint).to(self.device)

    def ask(self, prompt):
        if not self.is_setup:
            self.setup()
        try:
            inputs = tokenizer.encode(prompt, return_tensors="pt").to(self.device)
            outputs = model.generate(inputs)
            response = tokenizer.decode(outputs[0])
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
