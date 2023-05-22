from gettext import gettext as _

from gi.repository import Gtk, Adw, GLib

import json


class BavarderProvider:
    name = None
    slug = None
    description = ""
    languages = ""
    version = "0.1.7"
    developer_name = "0xMRTT"
    developers = ["0xMRTT https://github.com/0xMRTT"]
    license_type = Gtk.License.GPL_3_0
    copyright = "© 2023 0xMRTT"
    url = "https://bavarder.codeberg.page/help/bard"


    def __init__(self, win, app, *args, **kwargs):
        self.win = win
        self.banner = win.banner
        self.app = app
        self.chat = None
        self.update_response = app.update_response

    def ask(self, prompt):
        raise NotImplementedError()

    @property
    def require_api_key(self):
        raise NotImplementedError()

    def preferences(self, win):
        return self.no_preferences(win)

    def no_api_key(self, title=None):
        if title:
            self.win.banner.props.title = title
        else:
            self.win.banner.props.title = _(
                "No API key provided, you can provide one in settings"
            )
        self.win.banner.props.button_label = _("Open settings")
        self.win.banner.connect("button-clicked", self.app.on_preferences_action)
        self.win.banner.set_revealed(True)

    def no_connection(self):
        self.win.banner.props.title = _("No network connection")
        self.win.banner.props.button_label = ""
        self.win.banner.set_revealed(True)

    def hide_banner(self):
        self.win.banner.set_revealed(False)

    def about(self, *args, **kwargs):
        popover = Gtk.Popover()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        title = Gtk.Label()
        title.set_markup(f"<b>{self.name}</b>\n<small>Version {self.version}</small>")
        title.set_halign(Gtk.Align.CENTER)
        title.set_valign(Gtk.Align.CENTER)
        vbox.append(title)

        if self.description:
            description = Gtk.Label()
            if self.languages:
                description.set_markup(
                    f"<small>{self.description}</small>\n<small>Languages: {self.languages}</small>"
                )
            else:
                description.set_markup(f"<small>{self.description}</small>")
            description.set_halign(Gtk.Align.CENTER)
            description.set_valign(Gtk.Align.CENTER)
            vbox.append(description)
        popover.set_child(vbox)

        about_button = Gtk.MenuButton()
        about_button.set_icon_name("help-about-symbolic")
        about_button.set_tooltip_text(_("About provider"))
        about_button.add_css_class("flat")
        about_button.set_valign(Gtk.Align.CENTER)
        about_button.set_popover(popover)
        return about_button

    def open_documentation(self, *args, **kwargs):
        GLib.spawn_command_line_async(
            f"xdg-open {self.url}"
        )
    
    def how_to_get_a_token(self):
        about_button = Gtk.Button()
        about_button.set_icon_name("dialog-information-symbolic")
        about_button.set_tooltip_text(_("How to get a token"))
        about_button.add_css_class("flat")
        about_button.set_valign(Gtk.Align.CENTER)
        about_button.connect("clicked", self.open_documentation)
        return about_button

    def enable_switch(self):
        enabled = Gtk.Switch()
        enabled.set_active(self.slug in self.app.enabled_providers)
        enabled.connect("notify::active", self.on_enabled)
        enabled.set_valign(Gtk.Align.CENTER)
        return enabled

    def no_preferences(self, win):
        self.pref_win = win

        self.expander = Adw.ExpanderRow()
        self.expander.props.title = self.name

        self.expander.add_action(self.about())  # TODO: in Adw 1.4, use add_suffix
        self.expander.add_action(self.enable_switch())

        self.no_pref_row = Adw.ActionRow()
        self.no_pref_row.props.title = _("No preferences available")
        self.expander.add_row(self.no_pref_row)

        return self.expander

    def save(self):
        return {}

    def load(self, data):
        raise NotImplementedError()

    def chunk(self, prompt, n=4000):
        if len(prompt) > n:
            print("Chuncking prompt")
            prompt = [(prompt[i : i + n]) for i in range(0, len(prompt), n)]
        return prompt

    def on_enabled(self, widget, *args):
        if widget.get_active():
            self.app.enabled_providers.append(self.slug)
        else:
            self.app.enabled_providers.remove(self.slug)
        self.app.load_dropdown()
