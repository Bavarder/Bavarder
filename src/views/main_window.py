
from gi.repository import Adw, Gtk, Gio

from bavarder.constants import app_id, build_type

@Gtk.Template(resource_path="/io/github/Bavarder/Bavarder/ui/window.ui")
class BavarderWindow(Adw.ApplicationWindow):
    __gtype_name__ = "BavarderWindow"

    toast_overlay = Gtk.Template.Child()
    prompt_text_view = Gtk.Template.Child()
    ask_button = Gtk.Template.Child()
    scrolled_response_window = Gtk.Template.Child()
    bot_text_view = Gtk.Template.Child()
    banner = Gtk.Template.Child()
    stop_button = Gtk.Template.Child()
    # listen = Gtk.Template.Child()
    # listen_wait = Gtk.Template.Child()
    # listen_spinner = Gtk.Template.Child()
    # speak = Gtk.Template.Child()
    # speak_wait = Gtk.Template.Child()
    # speak_spinner = Gtk.Template.Child()
    menu = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = Gtk.Application.get_default()
        self.settings = Gio.Settings(schema_id=app_id)

        self.setup_signals()
        self.setup_window_props()

        self.setup()


    def setup_window_props(self):
        self.settings.bind(
            "width", self, "default-width", Gio.SettingsBindFlags.DEFAULT
        )
        self.settings.bind(
            "height", self, "default-height", Gio.SettingsBindFlags.DEFAULT
        )
        self.settings.bind(
            "is-maximized", self, "maximized", Gio.SettingsBindFlags.DEFAULT
        )
        self.settings.bind(
            "is-fullscreen", self, "fullscreened", Gio.SettingsBindFlags.DEFAULT
        )


    def setup_signals(self):
        self.connect("close-request",
            self.on_close_request)

        

    def setup(self):
        # Set devel style
        if build_type == "debug":
            self.get_style_context().add_class("devel")

    def on_close_request(self, *args):
        self.settings.set_strv("enabled-providers", list(self.app.enabled_providers))
        self.settings.set_string("latest-provider", self.app.provider)
        self.app.save_providers()
        self.close()
