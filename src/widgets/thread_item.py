from gi.repository import Gtk, Adw, Gio, GLib

from bavarder.constants import app_id, rootdir

@Gtk.Template(resource_path=f"{rootdir}/ui/thread_item.ui")
class ThreadItem(Gtk.Box):
    __gtype_name__ = "ThreadItem"

    label = Gtk.Template.Child()
    text_value = Gtk.Template.Child("text-value")
    value_stack = Gtk.Template.Child("value-stack")
    text_value_toggle = Gtk.Template.Child("text-value-toggle")
    star_button = Gtk.Template.Child()

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
        self.update_star()

    def setup_signals(self):
        pass

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

    @Gtk.Template.Callback()
    def on_star_button_clicked(self, *args):
        self.is_starred =  not self.is_starred
        self.update_star()

    def update_star(self):
        self.chat["starred"] = self.is_starred
        if self.is_starred:
            self.star_button.set_icon_name("starred-symbolic")
            self.label.set_css_classes(["accent"])
        else:
            self.star_button.set_icon_name("non-starred-symbolic")
            self.label.set_css_classes([])

    @Gtk.Template.Callback()
    def on_delete_button_clicked(self, *args):
        self.app.data["chats"].remove(self.chat)
        self.win.load_threads()
    


