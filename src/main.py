# main.py
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

import sys
import gi
import sys
import threading
import json

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gdk", "4.0")
gi.require_version("Gst", "1.0")

from gi.repository import Gtk, Gio, Adw, Gdk, GLib, Gst
from .window import BavarderWindow
from .preferences import Preferences

from .constants import app_id, version

from gtts import gTTS
from tempfile import NamedTemporaryFile

from .provider import PROVIDERS
import platform
import os


class BavarderApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(
            application_id="io.github.Bavarder.Bavarder",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self.create_action("quit", self.on_quit, ["<primary>q"])
        self.create_action("about", self.on_about_action, ["<primary>a"])
        self.create_action("preferences", self.on_preferences_action, ["<primary>comma"])
        self.create_action("copy_prompt", self.on_copy_prompt_action)
        self.create_action("copy_bot", self.on_copy_bot_action, ["<primary>c"])
        self.create_action("ask", self.on_ask_action, ["<primary>Return"])
        self.create_action("clear", self.on_clear_action, ["<primary>BackSpace"])
        # self.create_action("speak", self.on_speak_action, ["<primary>S"])
        # self.create_action("listen", self.on_listen_action, ["<primary>L"])

        self.settings = Gio.Settings(schema_id="io.github.Bavarder.Bavarder")

        self.clear_after_send = self.settings.get_boolean("clear-after-send")

        self.enabled_providers = sorted(
            set(self.settings.get_strv("enabled-providers"))
        )
        self.latest_provider = self.settings.get_string("latest-provider")

    def quitting(self, *args, **kwargs):
        """Called before closing main window."""
        self.settings.set_strv("enabled-providers", list(self.enabled_providers))
        self.settings.set_string("latest-provider", self.get_provider().slug)

        print("Saving providers data...")

        self.save_providers()
        self.quit()

    def on_quit(self, action, param):
        """Called when the user activates the Quit action."""
        self.quitting()

    def save_providers(self):
        r = {}
        for k, p in self.providers.items():
            r[p.slug] = json.dumps(p.save())
        print(r)
        data = GLib.Variant("a{ss}", r)
        self.settings.set_value("providers-data", data)

    def on_clear_action(self, action, param):
        self.win.bot_text_view.get_buffer().set_text("")
        self.win.prompt_text_view.get_buffer().set_text("")
        self.win.prompt_text_view.grab_focus()

    def get_provider(self):
        print(self.providers)
        return self.providers[self.win.provider_selector.props.selected]

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.win = self.props.active_window
        if not self.win:
            self.win = BavarderWindow(application=self)
        self.win.present()

        self.win.response_stack.set_visible_child_name("page_response")

        self.win.connect("close-request", self.quitting)

        self.load_dropdown()

        self.load()


        print(self.latest_provider)
        for k, p in self.providers.items():
            if p.slug == self.latest_provider:
                print("Setting selected provider to", k)
                self.win.provider_selector.set_selected(k)
                break

        self.win.prompt_text_view.grab_focus()

    def load_dropdown(self):

        self.provider_selector_model = Gtk.StringList()
        self.providers = {}

        self.providers_data = self.settings.get_value("providers-data")
        print(self.providers_data)
        print(self.enabled_providers)

        for provider, i in zip(
            self.enabled_providers, range(len(self.enabled_providers))
        ):
            print("Loading provider", provider)
            try:
                self.provider_selector_model.append(PROVIDERS[provider].name)
            except KeyError:
                print("Provider", provider, "not found")
                self.enabled_providers.remove(provider)
                continue
            else:
                try:
                    _ = self.providers[i] # doesn't re load if already loaded
                except KeyError:
                    self.providers[i] = PROVIDERS[provider](self.win, self)

        self.win.provider_selector.set_model(self.provider_selector_model)
        self.win.provider_selector.connect("notify", self.on_provider_selector_notify)
        

    def load(self):
        for p in self.providers.values():
            print(self.providers_data)
            try:
                p.load(data=json.loads(self.providers_data[p.slug]))
            except KeyError:  # provider not in data
                pass

    def on_provider_selector_notify(self, _unused, pspec):
        self.win.banner.set_revealed(False)

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="Bavarder",
            application_icon=app_id,
            developer_name="0xMRTT",
            developers=["0xMRTT https://github.com/0xMRTT"],
            designers=["David Lapshin https://github.com/daudix-UFO"],
            artists=["David Lapshin https://github.com/daudix-UFO"],
            documenters=[],
            translator_credits="""0xMRTT <0xmrtt@proton.me>
                David Lapshin <ddaudix@gmail.com>
                Morgan Antonsson <morgan.antonsson@gmail.com>
                thepoladov13 <thepoladov@protonmail.com>
                Muznyo <codeberg.vqtek@simplelogin.com>
                Deimidis <gmovia@pm.me>
                sjdonado <jsrd98@gmail.com>
                artnay <jiri.gronroos@iki.fi>
                Rene Coty <irenee.thirion@e.email>
                galegovski <galegovski@outlook.com>""",
            license_type=Gtk.License.GPL_3_0,
            version=version,
            website="https://bavarder.codeberg.page",
            issue_url="https://github.com/Bavarder/Bavarder/issues",
            support_url="https://codeberg.org/Bavarder/Bavarder/issues",
            copyright="© 2023 0xMRTT",
        )

        about.add_acknowledgement_section(
            "Special thanks to",
            [
                "Telegraph https://apps.gnome.org/app/io.github.fkinoshita.Telegraph",
            ],
        )
        about.set_debug_info(
            f"""{app_id} {version}
Environment: {os.environ.get("XDG_CURRENT_DESKTOP", "Unknown")}
Gtk: {Gtk.MAJOR_VERSION}.{Gtk.MINOR_VERSION}.{Gtk.MICRO_VERSION}
Python: {platform.python_version()}
OS: {platform.system()} {platform.release()} {platform.version()}
Providers: {self.enabled_providers}
"""
        )
        about.present()

    def on_preferences_action(self, widget, *args, **kwargs):
        """Callback for the app.preferences action."""
        preferences = Preferences(
            application=self, transient_for=self.props.active_window
        )
        preferences.present()

    def on_copy_prompt_action(self, widget, _):
        """Callback for the app.copy_prompt action."""

        toast = Adw.Toast()

        text = self.win.prompt_text_view.get_buffer()
        toast.set_title("Text copied")

        (start, end) = text.get_bounds()
        text = text.get_text(start, end, False)

        if len(text) == 0:
            return

        Gdk.Display.get_default().get_clipboard().set(text)

        self.win.toast_overlay.add_toast(toast)

    def on_copy_bot_action(self, widget, _):
        """Callback for the app.copy_bot action."""

        toast = Adw.Toast()

        text = self.win.bot_text_view.get_buffer()
        toast.set_title("Text copied")

        (start, end) = text.get_bounds()
        text = text.get_text(start, end, False)

        if len(text) == 0:
            return

        Gdk.Display.get_default().get_clipboard().set(text)

        self.win.toast_overlay.add_toast(toast)

    def ask(self, prompt):
        return self.providers[self.provider].ask(prompt)

    def update_response(self, response):
        self.win.bot_text_view.get_buffer().set_text(response)

    def on_ask_action(self, widget, _):
        """Callback for the app.ask action."""

        self.win.spinner.start()
        self.win.ask_button.set_visible(False)
        self.win.wait_button.set_visible(True)
        self.prompt = self.win.prompt_text_view.get_buffer().props.text

        if self.prompt == "":
            return

        self.provider = self.win.provider_selector.props.selected

        def thread_run():
            try:
                response = self.ask(self.prompt)
            except GLib.Error as e:
                response = e.message
            GLib.idle_add(cleanup, response)

        def cleanup(response):
            self.win.spinner.stop()
            self.win.ask_button.set_visible(True)
            self.win.wait_button.set_visible(False)
            GLib.idle_add(self.update_response, response)
            if self.clear_after_send:
                GLib.idle_add(self.update_response, "")
            self.t.join()

        self.t = threading.Thread(target=thread_run)
        self.t.start()

    # def on_speak_action(self, widget, _):
    #     """Callback for the app.speak action."""
    #     print("app.speak action activated")
    #
    #     try:
    #
    #         with NamedTemporaryFile() as file_to_play:
    #
    #             tts = gTTS(self.win.bot_text_view.get_buffer().props.text)
    #             tts.write_to_fp(file_to_play)
    #             file_to_play.seek(0)
    #             self._play_audio(file_to_play.name)
    #     except Exception as exc:
    #         print(exc)
    #
    # def _play_audio(self, path):
    #     uri = "file://" + path
    #     self.player.set_property("uri", uri)
    #     self.pipeline.add(self.player)
    #     self.pipeline.set_state(Gst.State.PLAYING)
    #     self.player.set_state(Gst.State.PLAYING)
    #
    # def on_listen_action(self, widget, _):
    #     """Callback for the app.listen action."""
    #     print("app.listen action activated")

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = BavarderApplication()
    return app.run(sys.argv)
