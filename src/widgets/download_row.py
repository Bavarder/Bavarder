from gi.repository import Gtk, Adw, GLib

from bavarder.constants import app_id, rootdir
from bavarder.threading import KillableThread

@Gtk.Template(resource_path=f"{rootdir}/ui/download_row.ui")
class DownloadRow(Adw.ActionRow):
    __gtype_name__ = "DownloadRow"

    def __init__(self, app, window, model, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.window = window
        self.model = model

        self.setup()

    def setup(self):
        self.set_title(self.model["name"])
        self.set_subtitle(self.model["filename"])

    @Gtk.Template.Callback()
    def on_download_button_clicked(self, widget, *args):
        def thread_run():
            self.app.action_running_in_background = True

            toast = Adw.Toast()
            toast.set_timeout(0)
            toast.set_title(_("Downloading model %s" % self.model["name"]) )
            self.window.add_toast(toast)

            self.app.download_model(self.model["filename"])
            GLib.idle_add(cleanup, toast)

        def cleanup(toast):
            t.join()

            toast.dismiss()
            
            self.app.action_running_in_background = False
            self.app.list_models()
            self.window.load_models()

            toast = Adw.Toast()
            toast.set_title(_("Model %s downloaded!" % self.model["name"]) )
            self.window.add_toast(toast)

        t = KillableThread(target=thread_run)
        t.start()