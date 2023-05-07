from gi.repository import Gtk, Adw

from .provider import PROVIDERS

@Gtk.Template(resource_path="/io/github/Bavarder/Bavarder/ui/preferences.ui")
class Preferences(Adw.PreferencesWindow):
    __gtype_name__ = "Preferences"

    clear_after_send_switch = Gtk.Template.Child()
    provider_group = Gtk.Template.Child()

    def __init__(self, application, **kwargs):
        super().__init__(**kwargs)

        self.app = application
        self.settings = application.settings

        self.clear_after_send_switch.set_active(self.app.clear_after_send)
        self.clear_after_send_switch.connect(
            "notify::active", self.on_clear_after_send_switch_toggled
        )

        self.setup_providers()

    def on_clear_after_send_switch_toggled(self, widget, *args):
        """Callback for the clear_after_send_switch toggled event."""
        if widget.get_active():
            self.settings.set_boolean("clear-after-send", True)
            self.app.clear_after_send = True
        else:
            self.settings.set_boolean("clear-after-send", False)
            self.app.clear_after_send = False

    def setup_providers(self):
        # for provider in self.app.providers.values():
        #     try:
        #         self.provider_group.add(provider.preferences(self))
        #     except TypeError:  # no prefs
        #         pass
        # else:
        #     row = Adw.ActionRow()
        #     row.props.title = "No providers available"
        #     self.provider_group.add(row)
        for provider in PROVIDERS.values():
            try:
                self.provider_group.add(provider(self.app.win, self.app).preferences(self))
            except TypeError:
                pass
        