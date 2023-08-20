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
    repetition_penalty = Gtk.Template.Child("repetition-penalty")
    repetition_penalty_adjustment = Gtk.Template.Child("repetition-penalty-adjustment")
    n_batch = Gtk.Template.Child("n-batch")
    n_batch_adjustment = Gtk.Template.Child("n-batch-adjustment")
    repeat_last_n = Gtk.Template.Child("repeat-last-n")
    repeat_last_n_adjustment = Gtk.Template.Child("repeat-last-n-adjustment")
    system_prompt = Gtk.Template.Child("system-prompt")

    def __init__(self, app, window, model, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.window = window
        self.model = model
        self.max_tokens_adjustment.set_value(self.app.model_settings.get("max_tokens", 200))
        self.temperature_adjustment.set_value(self.app.model_settings.get("temperature", 0.7))
        self.top_p_adjustment.set_value(self.app.model_settings.get("top_p", 0.4))
        self.top_k_adjustment.set_value(self.app.model_settings.get("top_k", 40))
        self.repetition_penalty_adjustment.set_value(self.app.model_settings.get("repetition_penalty", 1.18))
        self.n_batch_adjustment.set_value(self.app.model_settings.get("n_batch", 8))
        self.repeat_last_n_adjustment.set_value(self.app.model_settings.get("repeat_last_n", 64))
        self.system_prompt.set_text(self.app.model_settings.get("system_template", "A chat between a curious user and an artificial intelligence assistant."))
        
        self.add_row(self.max_tokens)
        self.add_row(self.temperature)
        self.add_row(self.top_p)
        self.add_row(self.top_k)
        self.add_row(self.repetition_penalty)
        self.add_row(self.n_batch)
        self.add_row(self.repeat_last_n)
        self.add_row(self.system_prompt)

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

    @Gtk.Template.Callback()
    def on_repetition_penalty_changed(self, widget, *args):
        self.app.model_settings["repetition_penalty"] = widget.get_value()

    @Gtk.Template.Callback()
    def on_n_batch_changed(self, widget, *args):
        self.app.model_settings["n_batch"] = widget.get_value()

    @Gtk.Template.Callback()
    def on_repeat_last_n_changed(self, widget, *args):
        self.app.model_settings["repeat_last_n"] = widget.get_value()

    @Gtk.Template.Callback()
    def on_system_prompt_changed(self, widget, *args):
        self.app.model_settings["system_template"] = widget.get_text()