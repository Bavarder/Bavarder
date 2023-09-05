from .base import BaseProvider

import openai
import socket
from litellm import completion

from gi.repository import Gtk, Adw, GLib


class BaseOpenAIProvider(BaseProvider):
    model = None
    api_key_title = "API Key"
    chat = openai.ChatCompletion

    def __init__(self, app, window):
        super().__init__(app, window)

        if self.data.get("api_key"):
            openai.api_key = self.data["api_key"]
        if self.data.get("api_base"):
            openai.api_base = self.data["api_base"]

    def ask(self, prompt, chat):
        chat = chat["content"]

        if self.data.get("api_key"):
            api_key = self.data["api_key"]
        if self.data.get("api_base"):
            api_base = self.data["api_base"]

        if self.model:
            prompt = self.chunk(prompt)
            try:
                response = completion(
                            model=self.model,
                            messages=chat,
                            api_key=api_key,
                            api_base=api_base,
                        ).choices[0].message.content
            except openai.error.AuthenticationError:
                return _("Your API key is invalid, please check your preferences.")
            except openai.error.InvalidRequestError:
                return _("You don't have access to this model, please check your plan and billing details.")
            except openai.error.RateLimitError:
                return _("You exceeded your current quota, please check your plan and billing details.")
            except openai.error.APIError:
                return _("I'm having trouble connecting to the API, please check your internet connection.")
            except socket.gaierror:
                return _("I'm having trouble connecting to the API, please check your internet connection.")
            else:
                return response
        else:
            return _("No model selected, you can choose one in preferences")


    def get_settings_rows(self):
        self.rows = []


        self.api_row = Adw.PasswordEntryRow()
        self.api_row.connect("apply", self.on_apply)
        self.api_row.props.text = openai.api_key or ""
        self.api_row.props.title = self.api_key_title
        self.api_row.set_show_apply_button(True)
        self.api_row.add_suffix(self.how_to_get_a_token())
        self.rows.append(self.api_row)

        self.api_url_row = Adw.EntryRow()
        self.api_url_row.connect("apply", self.on_apply)
        self.api_url_row.props.text = openai.api_base or ""
        self.api_url_row.props.title = "API Url"
        self.api_url_row.set_show_apply_button(True)
        self.api_url_row.add_suffix(self.how_to_get_base_url())
        self.rows.append(self.api_url_row)

        return self.rows

    def on_apply(self, widget):
        api_key = self.api_row.get_text()
        openai.api_key = api_key
        openai.api_base = self.api_url_row.get_text()

        self.data["api_key"] = openai.api_key
        self.data["api_base"] = openai.api_base


    def how_to_get_base_url(self):
        about_button = Gtk.Button()
        about_button.set_icon_name("dialog-information-symbolic")
        about_button.set_tooltip_text("How to choose base url")
        about_button.add_css_class("flat")
        about_button.set_valign(Gtk.Align.CENTER)
        about_button.connect("clicked", self.open_documentation)
        return about_button