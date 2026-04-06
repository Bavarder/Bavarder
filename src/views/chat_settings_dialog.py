from gi.repository import Gtk, Adw, GLib, Gio

from bavarder.constants import app_id, rootdir


@Gtk.Template(resource_path=f"{rootdir}/ui/chat_settings_dialog.ui")
class ChatSettingsDialog(Adw.PreferencesDialog):
    __gtype_name__ = "ChatSettingsDialog"

    title_entry = Gtk.Template.Child()
    system_prompt_entry = Gtk.Template.Child()

    def __init__(self, parent, chat, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.chat = chat
        self.app = parent.app

        self.connect("closed", self.on_closed)
        self.setup()

    def setup(self):
        self.title_entry.set_text(self.chat.get("title", ""))
        
        system_prompt = self.chat.get("system_prompt", "")
        self.system_prompt_entry.set_text(system_prompt)

    def on_closed(self, *args):
        new_title = self.title_entry.get_text().strip()
        if new_title:
            self.chat["title"] = new_title
            self.parent.title.set_title(new_title)

        system_prompt = self.system_prompt_entry.get_text()
        self.chat["system_prompt"] = system_prompt
        
        self.app.save()
        
        for row in self.parent.threads_list:
            if row.get_child().chat.get("id") == self.chat.get("id"):
                self.parent.threads_list.select_row(row)
                self.parent.threads_row_activated_cb()
                break
        else:
            self.parent.load_threads()
