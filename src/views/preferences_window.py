from gi.repository import Gtk, Adw, Gio

from bavarder.constants import app_id, rootdir
from bavarder.providers.provider_item import Provider
from bavarder.widgets.model_item import Model
from bavarder.widgets.download_row import DownloadRow

from gpt4all import GPT4All

@Gtk.Template(resource_path=f"{rootdir}/ui/preferences_window.ui")
class PreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = "Preferences"

    provider_group = Gtk.Template.Child()
    general_page = Gtk.Template.Child()
    model_group = Gtk.Template.Child()
    miscellaneous_group = Gtk.Template.Child()
    user_name = Gtk.Template.Child()
    bot_name = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.settings = parent.settings

        self.app = self.parent.get_application()
        self.win = self.app.get_active_window()

        self.set_transient_for(self.win)

        self.setup()

    def setup(self):
        self.setup_signals()
        self.load_providers()
        self.load_models()

        self.bot_name.set_text(self.app.bot_name)
        self.user_name.set_text(self.app.user_name)

    def setup_signals(self):
        pass

    def load_providers(self):
        for provider in self.app.providers.values():
            p = Provider(self.app, self, provider)
            self.provider_group.add(p)

    def load_models(self):
        self.general_page.remove(self.model_group)
        self.model_group = Adw.PreferencesGroup()
        self.model_group.set_title(_("Models"))
        
        for model in self.app.models:
            p = Model(self.app, self, model)
            self.model_group.add(p)
        else:
            self.no_models_available = Adw.ExpanderRow()
            self.no_models_available.set_title(_("List of available models"))

            for model in GPT4All.list_models():
                self.no_models_available.add_row(DownloadRow(self.app, self, model))

            self.model_group.add(self.no_models_available)

        self.general_page.add(self.model_group)

    @Gtk.Template.Callback()
    def clear_all_chats_clicked(self, widget, *args):
        dialog = Adw.MessageDialog(
            heading=_("Delete All Threads"),
            body=_("Are you sure you want to delete all threads? This can't be undone!"),
            body_use_markup=True
        )

        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("delete", _("Delete"))
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")

        dialog.connect("response", self.on_delete_response)

        dialog.set_transient_for(self.win)
        dialog.present()

    def on_delete_response(self, _widget, response):
        if response == "delete":
            self.app.clear_all_chats()

            toast = Adw.Toast()
            toast.set_title(_("All chats cleared!"))
            self.add_toast(toast)

    @Gtk.Template.Callback()
    def on_bot_entry_apply(self, user_data, *args):
        self.app.bot_name = user_data.get_text()

        self.app.load_bot_and_user_name()

    @Gtk.Template.Callback()
    def on_user_entry_apply(self, user_data, *args):
        self.app.user_name = user_data.get_text()

        self.app.load_bot_and_user_name()
    