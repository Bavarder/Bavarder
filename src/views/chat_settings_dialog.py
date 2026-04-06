from gi.repository import Gtk, Adw, GLib

from bavarder.constants import app_id, rootdir


@Gtk.Template(resource_path=f"{rootdir}/ui/chat_settings_dialog.ui")
class ChatSettingsDialog(Adw.MessageDialog):
    __gtype_name__ = "ChatSettingsDialog"

    title_entry = Gtk.Template.Child()
    system_prompt_view = Gtk.Template.Child()

    def __init__(self, parent, chat, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.chat = chat
        self.app = parent.app

        self.setup()

    def setup(self):
        self.title_entry.set_text(self.chat.get("title", ""))
        
        system_prompt = self.chat.get("system_prompt", "")
        buffer = self.system_prompt_view.get_buffer()
        buffer.set_text(system_prompt, -1)

    @Gtk.Template.Callback()
    def on_save_clicked(self, widget, *args):
        new_title = self.title_entry.get_text().strip()
        if new_title:
            self.chat["title"] = new_title
            self.parent.title.set_title(new_title)

        buffer = self.system_prompt_view.get_buffer()
        system_prompt = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        self.chat["system_prompt"] = system_prompt

        self.parent.threads_row_activated_cb()
        self.close()

    @Gtk.Template.Callback()
    def on_cancel_clicked(self, widget, *args):
        self.close()
