from gi.repository import Gtk, Adw

from .provider import PROVIDERS


@Gtk.Template(resource_path="/io/github/Bavarder/Bavarder/ui/preferences.ui")
class Preferences(Adw.PreferencesWindow):
    __gtype_name__ = "Preferences"

    clear_after_send_switch = Gtk.Template.Child()
    provider_group = Gtk.Template.Child()
    use_text_view_switch = Gtk.Template.Child()
    close_all_without_dialog_switch = Gtk.Template.Child()
    allow_remote_fetching_switch = Gtk.Template.Child()

    def __init__(self, application, **kwargs):
        super().__init__(**kwargs)

        self.app = application
        self.settings = application.settings

        self.clear_after_send_switch.set_active(self.app.clear_after_send)
        self.clear_after_send_switch.connect(
            "notify::active", self.on_clear_after_send_switch_toggled
        )

        self.use_text_view_switch.set_active(self.app.use_text_view)
        self.use_text_view_switch.connect(
            "notify::active", self.on_use_text_view_switch_toggled
        )

        self.close_all_without_dialog_switch.set_active(self.app.close_all_without_dialog)
        self.close_all_without_dialog_switch.connect(
            "notify::active", self.on_close_all_without_dialog_switch_toggled
        )

        self.allow_remote_fetching_switch.set_active(self.app.allow_remote_fetching)
        self.allow_remote_fetching_switch.connect(
            "notify::active", self.on_allow_remote_fetching_switch_toggled
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

    def on_use_text_view_switch_toggled(self, widget, *args):
        """Callback for the use_text_view_switch toggled event."""
        if widget.get_active():
            self.settings.set_boolean("use-text-view", True)
            self.app.use_text_view = True
        else:
            self.settings.set_boolean("use-text-view", False)
            self.app.use_text_view = False

    def on_close_all_without_dialog_switch_toggled(self, widget, *args):
        """Callback for the close_all_without_dialog_switch toggled event."""
        if widget.get_active():
            self.settings.set_boolean("close-all-without-dialog", True)
            self.app.close_all_without_dialog = True
        else:
            self.settings.set_boolean("close-all-without-dialog", False)
            self.app.close_all_without_dialog = False

    def on_allow_remote_fetching_switch_toggled(self, widget, *args):
        """Callback for the allow_remote_fetching_switch toggled event."""
        if widget.get_active():
            self.settings.set_boolean("allow-remote-fetching", True)
            self.app.load_annoucements()
            self.app.allow_remote_fetching = True
        else:
            self.settings.set_boolean("allow-remote-fetching", False)
            self.app.allow_remote_fetching = False

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
                self.provider_group.add(
                    provider(self.app.win, self.app).preferences(self)
                )
            except TypeError:
                pass
