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
import socket

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gdk", "4.0")
gi.require_version('Gst', '1.0')

from gi.repository import Gtk, Gio, Adw, Gdk, GLib, Gst
from .window import BavarderWindow
from .preferences import Preferences

from .constants import app_id, version

from hgchat import HGChat
from gtts import gTTS
from tempfile import NamedTemporaryFile

from baichat_py import BAIChat

BACKEND = "hgchat" # "hgchat" or "bai"

class BavarderApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(
            application_id="io.github.Bavarder.Bavarder",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self.create_action("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_action("about", self.on_about_action)
        self.create_action("preferences", self.on_preferences_action)
        self.create_action("copy_prompt", self.on_copy_prompt_action)
        self.create_action("copy_bot", self.on_copy_bot_action)
        self.create_action("ask", self.on_ask_action, ["<primary>Return"])
        self.create_action("speak", self.on_speak_action, ["<primary>S"])
        self.create_action("listen", self.on_listen_action, ["<primary>L"])

        self.settings = Gio.Settings(schema_id="io.github.Bavarder.Bavarder")

        self.clear_after_send = self.settings.get_boolean("clear-after-send")

        if BACKEND == "hgchat":
            self.chat = HGChat()
        elif BACKEND == "bai":
            self.chat = BAIChat()
        else:
            raise ValueError("Invalid backend")

        # GStreamer playbin object and related setup
        Gst.init(None)
        self.player = Gst.ElementFactory.make('playbin', 'player')
        self.pipeline = Gst.Pipeline()
        # bus = self.player.get_bus()
        # bus.add_signal_watch()
        # bus.connect('message', self.on_gst_message)
        self.player_event = threading.Event()  # An event for letting us know when Gst is done playing


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

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="Bavarder",
            application_icon=app_id,
            developer_name="0xMRTT",
            developers=["0xMRTT https://github.com/0xMRTT"],
            designers=["David Lapshin https://github.com/daudix-UFO"],
            documenters=[],
            license_type=Gtk.License.GPL_3_0,
            version=version,
            copyright="© 2023 0xMRTT",
        )

        about.add_acknowledgement_section(
            "Special thanks to",
            [
                "Telegraph https://apps.gnome.org/app/io.github.fkinoshita.Telegraph",
                "BAIChat https://chatbot.theb.ai/",
            ],
        )
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print("app.preferences action activated")

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
        try:
            if BACKEND == "hgchat":
                response = self.chat.ask(self.prompt)
            elif BACKEND == "bai":
                response = self.chat.sync_ask(self.prompt)
        except KeyError:
            self.win.banner.set_revealed(False)
            return ""
        except socket.gaierror:
            #self.win.response_stack.set_visible_child_name("page_offline")
            self.win.banner.set_revealed(True)
            return ""
        else:
            self.win.banner.set_revealed(False)
            r = ""
            for i in response:
                char = i["token"]["text"]
                if char == "</s>":
                    r += "\n"
                else:
                    r += char
                GLib.idle_add(self.update_response, r)
            return r

    def update_response(self, response):
        self.win.bot_text_view.get_buffer().set_text(response)

    def on_ask_action(self, widget, _):
        """Callback for the app.ask action."""

        self.win.spinner.start()
        self.win.ask_button.set_visible(False)
        self.win.wait_button.set_visible(True)
        self.prompt = self.win.prompt_text_view.get_buffer().props.text

        def thread_run():
            response = self.ask(self.prompt)
            GLib.idle_add(cleanup, response)

        def cleanup(response):
            self.win.spinner.stop()
            self.win.ask_button.set_visible(True)
            self.win.wait_button.set_visible(False)
            t.join()
            self.win.bot_text_view.get_buffer().set_text(response)
            if self.clear_after_send:
                self.win.prompt_text_view.get_buffer().set_text("")

        t = threading.Thread(target=thread_run)
        t.start()

    def on_speak_action(self, widget, _):
        """Callback for the app.speak action."""
        print("app.speak action activated")

        try:

            with NamedTemporaryFile() as file_to_play:

                tts = gTTS(self.win.bot_text_view.get_buffer().props.text)
                tts.write_to_fp(file_to_play)
                file_to_play.seek(0)
                self._play_audio(file_to_play.name)
        except Exception as exc:
            print(exc)

    def _play_audio(self, path):
        uri = 'file://' + path
        self.player.set_property('uri', uri)
        self.pipeline.add(self.player)
        self.pipeline.set_state(Gst.State.PLAYING)
        self.player.set_state(Gst.State.PLAYING)
        
            

    def on_listen_action(self, widget, _):
        """Callback for the app.listen action."""
        print("app.listen action activated")

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
