import unicodedata
import re
from typing import List, Dict
from gi.repository import Gtk, Adw, GLib

from bavarder.constants import app_id, rootdir

    
@Gtk.Template(resource_path=f"{rootdir}/ui/model_item.ui")
class Model(Adw.ExpanderRow):
    __gtype_name__ = "Model"

    max_tokens = Gtk.Template.Child("max-tokens")
    max_tokens_adjustment = Gtk.Template.Child("max-tokens-adjustment")
    temperature = Gtk.Template.Child("temperature")
    temperature_adjustment = Gtk.Template.Child("temperature-adjustment")
    top_p = Gtk.Template.Child("top-p")
    top_p_adjustment = Gtk.Template.Child("top-p-adjustment")
    top_k = Gtk.Template.Child("top-k")
    top_k_adjustment = Gtk.Template.Child("top-k-adjustment")

    def __init__(self, app, window, model, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.window = window
        self.model = model
        self.max_tokens_adjustment.set_value(self.app.model_settings.get("max_tokens", 200))
        self.temperature_adjustment.set_value(self.app.model_settings.get("temperature", 0.7))
        self.top_p_adjustment.set_value(self.app.model_settings.get("top_p", 0.9))
        self.top_k_adjustment.set_value(self.app.model_settings.get("top_k", 40))
        
        self.add_row(self.max_tokens)
        self.add_row(self.temperature)
        self.add_row(self.top_p)
        self.add_row(self.top_k)

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

    @Gtk.Template.Callback()
    def on_max_tokens_changed(self, widget, *args):
        self.app.model_settings["max_tokens"] = widget.get_value()

    @Gtk.Template.Callback()
    def on_temperature_changed(self, widget, *args):
        self.app.model_settings["temperature"] = widget.get_value()

    @Gtk.Template.Callback()
    def on_top_p_changed(self, widget, *args):
        self.app.model_settings["top_p"] = widget.get_value()

    @Gtk.Template.Callback()
    def on_top_k_changed(self, widget, *args):
        self.app.model_settings["top_k"] = widget.get_value()