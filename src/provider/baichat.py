from .base import BaseProvider

from baichat_py import BaiChat

class BaiChatProvider:
    def __init__(self, win, app, *args, **kwargs):
        super().__init__(win, app, *args, **kwargs)
        self.chat = BaiChat(sync=True)

    def ask(self, prompt):
        try:
            response = self.chat.sync_ask(self.prompt)
        except KeyError:
            self.win.banner.set_revealed(False)
            return ""
        except socket.gaierror:
            self.win.banner.set_revealed(True)
            return ""
        else:
            self.win.banner.set_revealed(False)
            self.win.bot_text_view.get_buffer().set_text(response)
            return response

    @property
    def require_api_key(self):
        return False

    def preferences(self):
        self.no_preferences()
        
    def about(self):
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="Bai Chat",
            developer_name="Theb.ai",
            developers=["0xMRTT https://github.com/0xMRTT"],
            license_type=Gtk.License.GPL_3_0,
            version=version,
            copyright="© 2023 0xMRTT",
        )