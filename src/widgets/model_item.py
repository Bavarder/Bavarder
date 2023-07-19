import unicodedata
import re
from typing import List, Dict
from gi.repository import Gtk, Adw, GLib

from bavarder.constants import app_id, rootdir

    
@Gtk.Template(resource_path=f"{rootdir}/ui/model_item.ui")
class Model(Adw.ActionRow):
    __gtype_name__ = "Model"

    def __init__(self, app, window, model, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.window = window
        self.model = model

        self.setup()

    def setup(self):
        self.set_title(self.model)
        self.app.win.load_model_selector()

    @Gtk.Template.Callback()
    def on_delete_button_clicked(self, widget, *args):
        self.app.delete_model(self.model)
        self.window.load_models()
        
        toast = Adw.Toast()
        toast.set_title(_("Model %s deleted!" % self.model) )
        self.window.add_toast(toast)