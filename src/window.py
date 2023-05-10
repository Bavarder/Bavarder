# window.py
#
# Copyright 2023 Me
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk, Gio


@Gtk.Template(resource_path="/io/github/Bavarder/Bavarder/ui/window.ui")
class BavarderWindow(Adw.ApplicationWindow):
    __gtype_name__ = "BavarderWindow"

    toast_overlay = Gtk.Template.Child()
    prompt_text_view = Gtk.Template.Child()
    spinner = Gtk.Template.Child()
    ask_button = Gtk.Template.Child()
    wait_button = Gtk.Template.Child()
    scrolled_response_window = Gtk.Template.Child()
    bot_text_view = Gtk.Template.Child()
    response_stack = Gtk.Template.Child()
    banner = Gtk.Template.Child()
    # listen = Gtk.Template.Child()
    # listen_wait = Gtk.Template.Child()
    # listen_spinner = Gtk.Template.Child()
    # speak = Gtk.Template.Child()
    # speak_wait = Gtk.Template.Child()
    # speak_spinner = Gtk.Template.Child()
    provider_selector = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings(schema_id="io.github.Bavarder.Bavarder")

        self.settings.bind(
            "width", self, "default-width", Gio.SettingsBindFlags.DEFAULT
        )
        self.settings.bind(
            "height", self, "default-height", Gio.SettingsBindFlags.DEFAULT
        )
        self.settings.bind(
            "is-maximized", self, "maximized", Gio.SettingsBindFlags.DEFAULT
        )
        self.settings.bind(
            "is-fullscreen", self, "fullscreened", Gio.SettingsBindFlags.DEFAULT
        )
