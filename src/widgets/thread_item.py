from gi.repository import Gtk, Adw, Gio, GLib

from bavarder.constants import app_id, rootdir

@Gtk.Template(resource_path=f"{rootdir}/ui/thread_item.ui")
class ThreadItem(Gtk.Box):
    __gtype_name__ = "ThreadItem"

    label = Gtk.Template.Child()
    text_value = Gtk.Template.Child("text-value")
    value_stack = Gtk.Template.Child("value-stack")
    text_value_toggle = Gtk.Template.Child("text-value-toggle")
    popover = Gtk.Template.Child()

    def __init__(self, parent, chat, **kwargs):
        super().__init__(**kwargs)

        self.chat = chat
        self.id = chat["id"]
        self.label_text = chat["title"]
        self.is_starred = chat.get("starred", False)

        self.label.set_text(self.label_text)

        self.parent = parent
        self.settings = parent.settings

        self.app = self.parent.get_application()
        self.win = self.app.get_active_window()

        self.setup()

    def setup(self):
        self.setup_signals()

        evk = Gtk.GestureClick.new()
        evk.connect("pressed", self.show_menu)
        evk.set_button(3)
        self.add_controller(evk)

        #self.update_star()

    def show_menu(self, gesture, data, x, y):
        self.popover.set_parent(self)
        self.popover.popup()

    def setup_signals(self):
        self.action_group = Gio.SimpleActionGroup()
        self.create_action("delete", self.on_delete)
        self.create_action("star", self.on_star)
        self.insert_action_group("event", self.action_group);

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.action_group.add_action(action)

        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    @Gtk.Template.Callback()
    def on_text_value_toggled(self, *args):
        if self.text_value_toggle.get_active():
            self.text_value_toggle.set_icon_name("check-round-outline-symbolic")
            self.text_value.set_text(self.label_text)
            widget = self.text_value
            tooltip = _("Set Title")
        else:
            self.text_value_toggle.set_icon_name("document-edit-symbolic")
            self.label_text = self.text_value.get_text()
            self.chat["title"] = self.label_text
            self.text_value.set_text(self.label_text)
            self.win.title.set_title(self.label_text)

            tooltip = _("Edit Title")
            widget = self.label

        self.value_stack.set_visible_child(widget)
        self.text_value_toggle.set_tooltip_text(tooltip)
        self.label.set_text(self.label_text)

    def on_star(self, *args):
        self.is_starred =  not self.is_starred
        self.update_star()

    def update_star(self):
        self.chat["starred"] = self.is_starred
        if self.is_starred:
            #self.star_button.set_icon_name("starred-symbolic")
            self.label.set_css_classes(["accent"])
        else:
            #self.star_button.set_icon_name("non-starred-symbolic")
            self.label.set_css_classes([])

    def on_delete(self, *args):

        dialog = Adw.MessageDialog(
            title=_("Delete Thread"),
            body=_("Are you sure you want to delete this thread?"),
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
            self.app.data["chats"].remove(self.chat)
            self.win.load_threads()

            toast = Adw.Toast()
            toast.set_title(_("Thread Deleted"))
            self.win.toast_overlay.add_toast(toast)
    


