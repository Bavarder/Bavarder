from .openai import BaseOpenAIProvider

from gi.repository import Gtk, Adw

class LocalProvider(BaseOpenAIProvider):
    name = "Local"
    description = "Choose any model you want!"

    def get_settings_rows(self):
        rows = super().get_settings_rows()

        self.model_row = Adw.EntryRow()
        self.model_row.connect("apply", self.on_apply)
        self.model_row.props.title = _("Model")
        if 'model' in self.data:
            self.model_row.props.text = str(self.data["model"])
        else:
            self.model_row.props.text = ""
        self.model_row.add_suffix(self.how_to_choose_model())
        self.model_row.set_show_apply_button(True)

        rows.append(self.model_row)

        return rows

    def how_to_choose_model(self):
        about_button = Gtk.Button()
        about_button.set_icon_name("dialog-information-symbolic")
        about_button.set_tooltip_text(_("How to choose a model"))
        about_button.add_css_class("flat")
        about_button.set_valign(Gtk.Align.CENTER)
        about_button.connect("clicked", self.open_documentation)
        return about_button

    def on_apply(self, widget):
        api_key = self.api_row.get_text()
        openai.api_key = api_key
        openai.api_base = self.api_url_row.get_text()

        self.model = str(self.model_row.get_text())

        self.data["model"] = self.model
        self.data["api_key"] = openai.api_key
        self.data["api_base"] = openai.api_base
