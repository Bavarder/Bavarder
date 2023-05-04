from gettext import gettext as _

from gi.repository import Gtk, Adw

import json 
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
        if self.data:
            self.load(json.loads(self.data))
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

    def about(self, *args):
        raise NotImplementedError()

    def no_preferences(self, win):
        self.pref_win = win

        self.expander = Adw.ExpanderRow()
        self.expander.props.title = self.name

        about_button = Gtk.Button()
        about_button.set_label("About")
        about_button.connect("clicked", self.about)
        about_button.set_valign(Gtk.Align.CENTER)
        self.expander.add_action(about_button) # TODO: in Adw 1.4, use add_suffix


        self.no_pref_row = Adw.ActionRow()
        self.no_pref_row.props.title = "No preferences available"
        self.expander.add_row(self.no_pref_row)

        return self.expander

    def save(self):
        raise NotImplementedError()

    def load(self, data):
        raise NotImplementedError()
