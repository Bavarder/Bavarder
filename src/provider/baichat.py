from .base import BavarderProvider

from baichat_py import BAIChat
import socket

from gi.repository import Gtk, Adw, GLib


class BAIChatProvider(BavarderProvider):
    name = "BAI Chat"
    slug = "baichat"

    def __init__(self, win, app, *args, **kwargs):
        super().__init__(win, app, *args, **kwargs)
        self.chat = BAIChat(sync=True)

    def ask(self, prompt):
        try:
            response = self.chat.sync_ask(prompt)
        except KeyError:
            self.win.banner.set_revealed(False)
            return ""
        except socket.gaierror:
            self.no_connection()
            return ""
        else:
            self.win.banner.set_revealed(False)
            GLib.idle_add(self.update_response, response.text)
            return response.text

    @property
    def require_api_key(self):
        return False

    def save(self):
        return {}

    def load(self, data):
        pass
