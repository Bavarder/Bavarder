from gi.repository import Gtk, Adw, GLib

from bavarder.constants import app_id, rootdir
from bavarder.threading import KillableThread


@Gtk.Template(resource_path=f"{rootdir}/ui/marketplace_item.ui")
class MarketplaceItem(Adw.ActionRow):
    __gtype_name__ = "MarketplaceItem"

    def __init__(self, app, window, model_info, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.window = window
        self.model_info = model_info

        self.setup()

    def setup(self):
        self.set_title(self.model_info.get("name", ""))
        self.set_subtitle(self.model_info.get("id", ""))

    @Gtk.Template.Callback()
    def on_download_button_clicked(self, widget, *args):
        self.download_cancelled = False

        def thread_run():
            self.app.action_running_in_background = True

            toast = Adw.Toast()
            toast.set_timeout(0)
            toast.set_title(_("Downloading model %s" % self.model_info.get("name")))
            self.window.toast_overlay.add_toast(toast)

            model_id = self.model_info.get("id")
            from huggingface_hub import hf_hub_download, list_repo_files
            
            files = list_repo_files(model_id, repo_type="model")
            litertlm_files = [f for f in files if f.endswith('.litertlm')]
            
            if not litertlm_files:
                GLib.idle_add(show_error, _("No .litertlm file found in this model"))
                return
            
            try:
                model_file = hf_hub_download(
                    repo_id=model_id,
                    filename=litertlm_files[0],
                    cache_dir=self.app.user_cache_dir,
                )
            except Exception as e:
                GLib.idle_add(show_error, str(e))
                return

            if "models" not in self.app.data:
                self.app.data["models"] = {}
            self.app.data["models"]["model_path"] = model_file
            self.app.data["models"]["hf_model"] = model_id
            GLib.idle_add(cleanup, toast, model_file)

        def cleanup(toast, model_file):
            t.join()

            toast.dismiss()

            self.app.action_running_in_background = False

            toast = Adw.Toast()
            toast.set_title(_("Model %s downloaded!" % self.model_info.get("name")))
            self.window.toast_overlay.add_toast(toast)
            
            self.set_subtitle(self.model_info.get("id"))

        def show_error(message):
            try:
                t.join()
            except Exception:
                pass
            self.app.action_running_in_background = False
            toast = Adw.Toast()
            toast.set_title(message)
            self.window.toast_overlay.add_toast(toast)

        t = KillableThread(target=thread_run)
        t.start()
