from .base import BavarderProvider

from hgchat import HGChat
import socket


from gi.repository import Gtk, Adw, GLib


class HuggingChatProvider(BavarderProvider):
    name = "Hugging Chat"
    slug = "huggingchat"

    def __init__(self, win, app, *args, **kwargs):
        super().__init__(win, app, *args, **kwargs)
        self.chat = HGChat()

    def ask(self, prompt):
        try:
            response = self.chat.ask(prompt)
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
        return False

    def preferences(self):
        self.no_preferences()

    def about(self):
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="Hugging Chat",
            developer_name="Hugging Face",
            developers=["0xMRTT https://github.com/0xMRTT"],
            license_type=Gtk.License.GPL_3_0,
            version=version,
            copyright="© 2023 0xMRTT",
        )

    def save(self):
        return {}

    def load(self, data):
        pass
