import unicodedata
import re
from typing import List, Dict
from gi.repository import Gtk, Adw, GLib

from bavarder.constants import app_id, rootdir
from .base import  ProviderType
    
@Gtk.Template(resource_path=f"{rootdir}/ui/provider_item.ui")
class Provider(Adw.ExpanderRow):
    __gtype_name__ = "Provider"

    enable_switch = Gtk.Template.Child()
    no_preferences_available = Gtk.Template.Child()
    provider_type = Gtk.Template.Child()

    def __init__(self, app, window, provider, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.window = window
        self.provider = provider

        self.setup()

    def setup(self):
        self.set_title(self.provider.name)
        self.set_subtitle(self.provider.description)
        self.provider_type.set_label(self.provider.provider_type.value)
        match self.provider.provider_type:
            case ProviderType.IMAGE:
                self.provider_type.add_css_class("badge-silver")
            case ProviderType.CHAT:
                self.provider_type.add_css_class("badge-gold")
            case ProviderType.VOICE:
                self.provider_type.add_css_class("badge-iron")
            case ProviderType.TEXT:
                self.provider_type.add_css_class("badge-tin")
            case ProviderType.MOVIE:
                self.provider_type.add_css_class("badge-titanium")

        self.enable_switch.set_active( self.app.data["providers"][self.provider.slug]["enabled"])

        if self.provider.get_settings_rows():
            self.no_preferences_available.set_visible(False)
            
            for row in self.provider.get_settings_rows():
                self.add_row(row)

    # CALLBACKS
    @Gtk.Template.Callback()
    def on_switch_state_changed(self, widget, _):
        self.provider.set_enabled(widget.get_active())
        self.app.win.load_provider_selector()

    # TOOLS
    def slugify(self, value):
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub('[^\w\s-]', '', value).strip().lower()
        return re.sub('[-\s]+', '-', value)

    def chunk(self, prompt, n=4000):
        if len(prompt) > n:
            prompt = [(prompt[i : i + n]) for i in range(0, len(prompt), n)]
        return prompt

