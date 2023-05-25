
from gi.repository import Gtk, Adw

from bavarder import constants

import os
import platform

# TRANSLATORS: This is a place to put your credits (formats:
# "Name https://example.com" or "Name <email@example.com>",
# no quotes) and is not meant to be translated literally.
translator_credits = _("translator-credits")

class BavarderAboutWindow:
    def __init__(self, parent):
        self.parent = parent
        self.app = self.parent.get_application()

        self.setup()

    def setup(self):
        self.about_window = Adw.AboutWindow(
            application_name="Bavarder",
            transient_for=self.app.get_active_window(),
            application_icon=constants.app_id,
            developer_name=_("0xMRTT"),
            website=constants.project_url,
            support_url=constants.help_url,
            issue_url=constants.bugtracker_url,
            developers=[
                "0xMRTT https://github.com/0xMRTT",
            ],
            documenters=[
                "0xMRTT https://github.com/0xMRTT",
            ],
            designers=[
                "David Lapshin https://github.com/daudix-UFO"
            ],
            artists=[
                "David Lapshin https://github.com/daudix-UFO"
            ],

            translator_credits=_(translator_credits),
            copyright=_("Copyright © 2023 0xMRTT"),
            license_type=Gtk.License.GPL_3_0,
            version=constants.version,
            release_notes_version=constants.rel_ver,
        )

        self.about_window.add_acknowledgement_section(
            "Special thanks to",
            [
                "Telegraph https://apps.gnome.org/app/io.github.fkinoshita.Telegraph",
                "Apostrophe https://apps.gnome.org/app/org.gnome.gitlab.somas.Apostrophe",
            ],
        )
        self.about_window.set_debug_info(
            f"""{constants.app_id} {constants.version}
Environment: {os.environ.get("XDG_CURRENT_DESKTOP", "Unknown")}
Gtk: {Gtk.MAJOR_VERSION}.{Gtk.MINOR_VERSION}.{Gtk.MICRO_VERSION}
Python: {platform.python_version()}
OS: {platform.system()} {platform.release()} {platform.version()}
Providers: {self.app.enabled_providers}
Use Theme: {self.app.use_theme}
Use Text View: {self.app.use_text_view}
Clear After Send: {self.app.clear_after_send}
Close All Without Dialog: {self.app.close_all_without_dialog}
Current Provider: {self.app.provider}
"""
        )
        self.about_window.present()

        

    def show_about(self):
        self.about_window.present()
