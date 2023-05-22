from .openai import BaseOpenAIProvider

from gi.repository import Gtk, Adw, GLib

import openai

class OpenAICustomProvider(BaseOpenAIProvider):
    name = "OpenAI Custom Model"
    slug = "openaicustom"

    api_base = ""

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
        self.api_url_row.props.text = self.api_base or ""
        self.api_url_row.props.title = _("API Url")
        self.api_url_row.set_show_apply_button(True)
        self.api_url_row.add_suffix(self.how_to_get_a_token())
        self.expander.add_row(self.api_url_row)

        self.model_row = Adw.EntryRow()
        self.model_row.connect("apply", self.on_apply)
        self.model_row.props.title = _("Model")
        if self.model:
            self.model_row.props.text = str(self.model)
        else:
            print("No model")
            self.model_row.props.text = ""
        self.model_row.add_suffix(self.how_to_choose_model())
        self.model_row.set_show_apply_button(True)
        self.expander.add_row(self.model_row)
        return self.expander
    
    def on_apply(self, widget):
        self.hide_banner()
        api_key = self.api_row.get_text()
        openai.api_key = api_key
        self.api_base = self.api_url_row.get_text()
        openai.api_base = self.api_base
        self.model = str(self.model_row.get_text())

    def save(self):
        return {
            "api_key": openai.api_key,
            "api_base": self.api_base,
            "model": self.model,
        }

    def load(self, data):
        if data["api_key"]:
            openai.api_key = data["api_key"]
        else:
            openai.api_key = ""
        if data["api_base"]:
            self.api_base = data["api_base"]
            openai.api_base = self.api_base
        if data["model"]:
            self.model = data["model"]

    def how_to_choose_model(self):
        about_button = Gtk.Button()
        about_button.set_icon_name("dialog-information-symbolic")
        about_button.set_tooltip_text(_("How to choose a model"))
        about_button.add_css_class("flat")
        about_button.set_valign(Gtk.Align.CENTER)
        about_button.connect("clicked", self.open_documentation)
        return about_button

class LocalModel(OpenAICustomProvider):
    name = "Local Model"
    slug = "local"
    url = "https://bavarder.codeberg.page/help/local" # just for the url :)
