class BavarderProvider:
    def __init__(self, win, app, *args, **kwargs):
        self.win = win
        self.banner = win.banner
        self.bot_text_view = win.bot_text_view
        self.app = app
        self.chat = None

        super().__init__(*args, **kwargs)

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