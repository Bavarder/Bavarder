from gi.repository import Gtk, Adw


@Gtk.Template(resource_path="/io/github/Bavarder/Bavarder/ui/preferences.ui")
class Preferences(Adw.PreferencesWindow):
    __gtype_name__ = "Preferences"

    clear_after_send_switch = Gtk.Template.Child()
    provider_group = Gtk.Template.Child()

    def __init__(self, application, **kwargs):
        super().__init__(**kwargs)

        self.app = application
        self.settings = application.settings

        clear_after_send = self.settings.get_boolean("clear-after-send")
        self.clear_after_send_switch.props.state = clear_after_send
        self.clear_after_send_switch.connect(
            "state-set", self.on_clear_after_send_switch_toggled
        )

        self.setup_providers()

    def on_clear_after_send_switch_toggled(self, *args):
        """Callback for the clear_after_send_switch toggled event."""
        state = self.clear_after_send_switch.props.state

        if state:
            self.settings.set_boolean("clear-after-send", True)
        else:
            self.settings.set_boolean("clear-after-send", False)

    def setup_providers(self):
        for provider in self.app.providers.values():
            try:
                self.provider_group.add(provider.preferences())
            except TypeError:  # no prefs
                pass
