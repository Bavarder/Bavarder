from .base import BavarderProvider

import openai
import socket

from gi.repository import Gtk, Adw

class BaseOpenAIProvider(BavarderProvider):
    name = None
    slug = None
    model = None

    def __init__(self, win, app, *args, **kwargs):
        super().__init__(win, app, *args, **kwargs)
        self.chat = openai.ChatCompletion

    def ask(self, prompt):
        try:
            response = self.chat.create(model=self.model, messages=[{"role": "user", "content": prompt}])
            response = response.choices[0].message.content
        except openai.error.AuthenticationError:
            self.no_api_key()
            return ""
        except openai.error.InvalidRequestError:
            self.win.banner.props.title = "You don't have access to this model"
            self.win.banner.props.button_label = ""
            self.win.banner.set_revealed(True)
            return ""
        except socket.gaierror:
            self.no_connection()
            return ""
        else:
            self.hide_banner()
            self.update_response(response)
            return response

    @property
    def require_api_key(self):
        return True

    def preferences(self):
        self.expander = Adw.ExpanderRow()
        self.expander.props.title = self.name

        self.api_row = Adw.PasswordEntryRow()
        self.api_row.connect("apply", self.on_apply)
        self.api_row.props.title = "API Key"
        self.api_row.set_show_apply_button(True)
        self.expander.add_row(self.api_row)

        return self.expander

    def on_apply(self, widget):
        self.hide_banner()
        api_key = self.api_row.get_text()
        print(api_key)
        openai.api_key = api_key

        
    def about(self):
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name=self.name,
            developer_name="OpenAI",
            developers=["0xMRTT https://github.com/0xMRTT"],
            license_type=Gtk.License.GPL_3_0,
            version=version,
            copyright="© 2023 0xMRTT",
        )
    
    def save(self):
        return {
            "api_key": openai.api_key
        }

    def load(self, data):
        openai.api_key = data["api_key"] 