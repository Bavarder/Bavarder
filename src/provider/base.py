from gettext import gettext as _

class BavarderProvider:
    name = None
    slug = None

    def __init__(self, win, app, data, *args, **kwargs):
        self.win = win
        self.banner = win.banner
        self.bot_text_view = win.bot_text_view
        self.app = app
        self.chat = None
        self.data = data
        self.update_response = app.update_response
        if data:
            self.load(data)
            self.no_data = False
        else:
            self.no_data = True

    def ask(self, prompt):
        raise NotImplementedError()

    @property
    def require_api_key(self):
        raise NotImplementedError()

    def preferences(self):
        raise NotImplementedError()

    def no_api_key(self, title=None):
        if title:
            self.win.banner.props.title = title
        else:
            self.win.banner.props.title = (
                _("No API key provided, you can provide one in settings")
            )
        self.win.banner.props.button_label = _("Open settings")
        self.win.banner.connect("button-clicked", self.app.on_preferences_action)
        self.win.banner.set_revealed(True)

    def no_connection(self):
        self.win.banner.props.title = _("No network connection")
        self.win.banner.props.button_label = ""
        self.win.banner.set_revealed(True)

    def hide_banner(self):
        self.win.banner.set_revealed(False)

    def about(self):
        raise NotImplementedError()

    def no_preferences(self):
        pass

    def save(self):
        raise NotImplementedError()

    def load(self, data):
        raise NotImplementedError()
