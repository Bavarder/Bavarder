from gi.repository import Gtk, Adw, Gio, GLib

from bavarder.constants import app_id, rootdir

@Gtk.Template(resource_path=f"{rootdir}/ui/thread_item.ui")
class ThreadItem(Gtk.Box):
    __gtype_name__ = "ThreadItem"

    label = Gtk.Template.Child()
    popover = Gtk.Template.Child()

    edit_mode = False

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
        self.create_action("edit", self.on_edit_button_clicked)
        self.insert_action_group("event", self.action_group)

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.action_group.add_action(action)

        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def on_edit_button_clicked(self, *args):
        box = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,
                margin_top=12,
                spacing=24,
            )
        listbox = Gtk.ListBox(
            selection_mode=Gtk.SelectionMode.NONE,
            hexpand=True,
            vexpand=True,
        )
        listbox.add_css_class("boxed-list")
        self.row = Adw.EntryRow()
        self.row.set_text(self.chat["title"])
        self.row.set_title(_("Edit Title"))
        listbox.append(self.row)
        box.append(listbox)

        dialog = Adw.MessageDialog(
            heading=_("Edit Title"),
            transient_for=self.win,
            modal=True,
            extra_child=box
        )

        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("edit", _("Edit"))
        dialog.set_response_appearance("edit", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")

        dialog.connect("response", self.on_edit_response)
        dialog.present()
        
    def on_edit_response(self, _widget, response):
        if response == "edit":
            self.label_text = self.row.get_text()
            self.chat["title"] = self.label_text
            self.win.title.set_title(self.label_text)
            self.label.set_text(self.label_text)

            toast = Adw.Toast()
            toast.set_title(_("Title Edited"))
            self.win.toast_overlay.add_toast(toast)
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
            heading=_("Delete Thread"),
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
    


