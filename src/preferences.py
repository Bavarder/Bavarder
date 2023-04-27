from gi.repository import Gtk, Adw


@Gtk.Template(resource_path="/com/github/Bavarder/Bavarder/ui/preferences.ui")
class Preferences(Adw.PreferencesWindow):
    __gtype_name__ = "GradiencePreferencesWindow"

    clear_after_send_switch = Gtk.Template.Child()

    def __init__(self, application, **kwargs):
        super().__init__(**kwargs)

        self.app = application
        self.settings = application.settings

        self.win = self.app.get_active_window()

        self.setup()

    def setup(self):
        clear_after_send = self.settings.get_boolean("clear-after-send")
        self.clear_after_send_switch.connect(
            "state-set", self.on_clear_after_send_switch_toggled
        )

    def on_clear_after_send_switch_toggled(self, *args):
        state = self.clear_after_send_switch.props.state

        if state:
            self.settings.set_boolean("clear-after-send", True)
        else:
            self.settings.set_boolean("clear-after-send", False)
