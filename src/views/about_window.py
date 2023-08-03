
from gi.repository import Gtk, Adw

from bavarder import constants

import os
import platform

# TRANSLATORS: This is a place to put your credits (formats:
# "Name https://example.com" or "Name <email@example.com>",
# no quotes) and is not meant to be translated literally.
translator_credits = _("translator-credits")

class AboutWindow:
    def __init__(self, parent):
        self.parent = parent
        self.app = self.parent.get_application()

        self.setup()

    def setup(self):
        self.about_window = Adw.AboutWindow(
            application_name="Bavarder",
            transient_for=self.app.get_active_window(),
            application_icon=constants.app_id,
            developer_name="0xMRTT",
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
                "David Lapshin https://github.com/daudix-UFO",
            ],
            artists=[
                "David Lapshin https://github.com/daudix-UFO",
            ],
            comments=_("Chit-Chat with AI"),
            translator_credits=translator_credits,
            copyright=_("Copyright © 2023 0xMRTT"),
            license_type=Gtk.License.GPL_3_0,
            version=constants.version,
            release_notes_version=constants.rel_ver,
        )

        self.about_window.add_credit_section(
            _("Packaging"),
            [
                "Soumyadeep Ghosh https://codeberg.org/soumyadghosh"
            ]
        )
        self.about_window.add_link(
            _("Translate"),
            constants.translate_url
        )

        self.about_window.set_debug_info(
            f"""{constants.app_id} {constants.version}
Environment: {os.environ.get("XDG_CURRENT_DESKTOP", "Unknown")}
Gtk: {Gtk.MAJOR_VERSION}.{Gtk.MINOR_VERSION}.{Gtk.MICRO_VERSION}
Python: {platform.python_version()}
OS: {platform.system()} {platform.release()} {platform.version()}
"""
        )
        self.about_window.present()



    def present(self):
        self.about_window.present()

