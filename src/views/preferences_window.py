from gi.repository import Gtk, Adw, Gio, GLib

from bavarder.constants import app_id, rootdir
from bavarder.widgets.marketplace_item import MarketplaceItem
from bavarder.widgets.model_item import Model


@Gtk.Template(resource_path=f"{rootdir}/ui/preferences_window.ui")
class PreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = "Preferences"

    provider_group = Gtk.Template.Child()
    general_page = Gtk.Template.Child()
    model_group = Gtk.Template.Child()
    marketplace_group = Gtk.Template.Child()
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
        self.load_models()
        self.load_marketplace()

        self.bot_name.set_text(self.app.bot_name)
        self.user_name.set_text(self.app.user_name)

    def setup_signals(self):
        pass

    def load_models(self):
        self.general_page.remove(self.model_group)
        self.model_group = Adw.PreferencesGroup()
        self.model_group.set_title(_("Models"))

        if self.app.models:
            for model in self.app.models:
                from bavarder.widgets.model_item import Model
                p = Model(self.app, self, model)
                self.model_group.add(p)
        else:
            no_models = Adw.ActionRow()
            no_models.set_title(_("No local models available"))
            self.model_group.add(no_models)

        self.general_page.add(self.model_group)

    def load_marketplace(self):
        def fetch_models():
            try:
                from huggingface_hub import list_models
                models = list(list_models(
                    filter={"library_name": "litert-lm"},
                    sort="downloads",
                    direction=-1,
                    limit=50
                ))
                model_list = []
                for m in models:
                    model_list.append({
                        "id": m.id,
                        "name": m.model_id if hasattr(m, 'model_id') else m.id,
                        "downloads": getattr(m, 'downloads', 0)
                    })
                GLib.idle_add(update_ui, model_list)
            except Exception as e:
                GLib.idle_add(show_error, str(e))

        def update_ui(model_list):
            self.marketplace_group.remove_all()
            for m in model_list:
                item = MarketplaceItem(self.app, self.win, m)
                self.marketplace_group.add(item)

        def show_error(message):
            toast = Adw.Toast()
            toast.set_title(_("Error loading marketplace: %s" % message))
            self.add_toast(toast)

        import threading
        t = threading.Thread(target=fetch_models)
        t.start()

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

        dialog.set_transient_for(self)
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
