
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

    def about(self):
        raise NotImplementedError()

    def no_preferences(self):
        pass

    def save(self):
        raise NotImplementedError()

    def load(self, data):
        raise NotImplementedError()