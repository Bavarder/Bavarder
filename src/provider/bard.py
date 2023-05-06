from .base import BavarderProvider

import socket

from googlebardpy import BardChat

from gi.repository import Gtk, Adw, GLib

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
            GLib.idle_add(self.update_response, response)
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
        self.api_key = api_key
        try:
            self.chat = BardChat(api_key)
        except AttributeError:
            self.banner.props.title = "Invalid API key"
            self.banner.props.button_label = ""
            self.banner.set_revealed(True)

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
        try:
            return {"api_key": self.api_key}
        except AttributeError: # no api key
            return {}

    def load(self, data):
        try:
            self.chat = BardChat(data['api_key'])
            self.api_key = data['api_key']
        except AttributeError:
            self.chat = None
            self.api_key = None
