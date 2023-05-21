from .base import BavarderProvider

import openai
import socket

from gi.repository import Gtk, Adw, GLib


class BaseOpenAIProvider(BavarderProvider):
    name = None
    slug = None
    model = None
    version = "0.1.0"
    api_key_title = "API Key"
    url = "https://bavarder.codeberg.page/help/openai"

    def __init__(self, win, app, *args, **kwargs):
        super().__init__(win, app, *args, **kwargs)
        self.chat = openai.ChatCompletion
        self.pref_win = None

    def ask(self, prompt):
        if self.model:
            prompt = self.chunk(prompt)
            try:
                if isinstance(prompt, list):
                    self.win.banner.props.title = "Prompt too long, splitting into chunks."
                    self.win.banner.props.button_label = ""
                    self.win.banner.set_revealed(True)
                    response = ""
                    for chunk in prompt:
                        response += (
                            self.chat.create(
                                model=self.model,
                                messages=[{"role": "user", "content": chunk}],
                            )
                            .choices[0]
                            .message.content
                        )
                else:
                    response = self.chat.create(
                        model=self.model, messages=[{"role": "user", "content": prompt}]
                    )
                    response = response.choices[0].message.content
            except openai.error.AuthenticationError:
                self.no_api_key()
                return ""
            except openai.error.InvalidRequestError:
                self.win.banner.props.title = "You don't have access to this model"
                self.win.banner.props.button_label = ""
                self.win.banner.set_revealed(True)
                return ""
            except openai.error.RateLimitError:
                self.win.banner.props.title = "You exceeded your current quota, please check your plan and billing details."
                self.win.banner.props.button_label = ""
                self.win.banner.set_revealed(True)
                return ""
            except socket.gaierror:
                self.no_connection()
                return ""
            else:
                self.hide_banner()
                GLib.idle_add(self.update_response, response)
                return response
        else:
            self.no_api_key(title="No model selected, you can choose one in preferences")
            return ""


    @property
    def require_api_key(self):
        return True

    def preferences(self, win):
        self.pref_win = win

        self.expander = Adw.ExpanderRow()
        self.expander.props.title = self.name

        self.expander.add_action(self.about())  # TODO: in Adw 1.4, use add_suffix
        self.expander.add_action(self.enable_switch())

        self.api_row = Adw.PasswordEntryRow()
        self.api_row.connect("apply", self.on_apply)
        self.api_row.props.text = openai.api_key or ""
        self.api_row.props.title = self.api_key_title
        self.api_row.set_show_apply_button(True)
        self.api_row.add_suffix(self.how_to_get_a_token())
        self.expander.add_row(self.api_row)

        self.api_url_row = Adw.EntryRow()
        self.api_url_row.connect("apply", self.on_apply)
        self.api_url_row.props.text = openai.api_key or ""
        self.api_url_row.props.title = "API Url"
        self.api_url_row.set_show_apply_button(True)
        self.api_url_row.add_suffix(self.how_to_get_base_url())
        self.expander.add_row(self.api_url_row)

        return self.expander

    def on_apply(self, widget):
        self.hide_banner()
        api_key = self.api_row.get_text()
        openai.api_key = api_key
        openai.api_base = self.api_url_row.get_text()

    def save(self):
        return {
            "api_key": openai.api_key,
            "api_base": openai.api_base,
        }

    def load(self, data):
        if data["api_key"]:
            openai.api_key = data["api_key"]
        if data["api_base"]:
            openai.api_base = data["api_base"]

    def how_to_get_base_url(self):
        about_button = Gtk.Button()
        about_button.set_icon_name("dialog-information-symbolic")
        about_button.set_tooltip_text("How to choose base url")
        about_button.add_css_class("flat")
        about_button.set_valign(Gtk.Align.CENTER)
        about_button.connect("clicked", self.open_documentation)
        return about_button