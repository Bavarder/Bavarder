# main.py
#
# Copyright 2023
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
import time

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Xdp', '1.0')
gi.require_version('XdpGtk4', '1.0')
gi.require_version('GtkSource', '5')

from gi.repository import Gtk, Gio, Adw, Xdp, XdpGtk4, GLib
from .views.window import BavarderWindow
from .views.about_window import AboutWindow
from .views.preferences_window import PreferencesWindow
from .constants import app_id
from .providers import PROVIDERS

import json
from gpt4all import GPT4All
import os

user_config_dir = os.environ.get(
    "XDG_CONFIG_HOME", os.environ["HOME"] + "/.config"
)

user_data_dir = os.environ.get(
    "XDG_DATA_HOME", os.environ["HOME"] + "/.local/share"
)

user_cache_dir = os.environ.get(
    "XDG_CACHE_HOME", os.environ["HOME"] + "/.cache"
)

model_path = os.path.join(user_cache_dir, "bavarder", "models")

class BavarderApplication(Adw.Application):
    """The main application singleton class."""

    model_name = "ggml-model-gpt4all-falcon-q4_0.bin"
    models = set()
    model = None
    action_running_in_background = False
    number_of_win = 0

    def __init__(self):
        super().__init__(application_id='io.github.Bavarder.Bavarder',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action("quit", self.on_quit, ["<primary>q"])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action, ['<primary>comma'])
        self.create_action('new_chat', self.on_new_chat_action, ["<primary>n"])
        self.create_action('ask', self.on_ask, ["Return"])
        self.create_action('new_window', self.on_new_window, ["<primary>w"])

        self.data_path = os.path.join(user_data_dir, "bavarder")

        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        if not os.path.exists(model_path):
            os.makedirs(model_path)

        self.data_path = os.path.join(self.data_path, "data.json")

        self.data = {
            "chats": [],
            "providers": {},
            "models": {}
        }

        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception: # if there is an error, we use a plain config
                pass

        self.settings = Gio.Settings(schema_id=app_id)

        self.local_mode = self.settings.get_boolean("local-mode")
        self.current_provider = self.settings.get_string("current-provider")
        self.model_name = self.settings.get_string("model")

        self.create_stateful_action(
            "set_provider",
            GLib.VariantType.new("s"),
            GLib.Variant("s", self.current_provider),
            self.on_set_provider_action
        )

        self.create_stateful_action(
            "set_model",
            GLib.VariantType.new("s"),
            GLib.Variant("s", self.model_name),
            self.on_set_model_action
        )

        self.bot_name = self.settings.get_string("bot-name")
        self.user_name = self.settings.get_string("user-name")


    def on_set_provider_action(self, action, *args):
        self.current_provider = args[0].get_string()
        Gio.SimpleAction.set_state(self.lookup_action("set_provider"), args[0])

    def on_set_model_action(self, action, *args):
        previous = self.model_name
        self.model_name = args[0].get_string()
        if previous != self.model_name:
            # reset model for loading the new one
            self.model = None
        Gio.SimpleAction.set_state(self.lookup_action("set_model"), args[0])

    def save(self):
        with open(self.data_path, "w", encoding="utf-8") as f:
            for name, d in self.data["providers"].items():
                print(d)
            self.data = json.dump(self.data, f)
            self.settings.set_boolean("local-mode", self.local_mode)
            self.settings.set_string("current-provider", self.current_provider)
            self.settings.set_string("model", self.model_name)
            self.settings.set_string("bot-name", self.bot_name)
            self.settings.set_string("user-name", self.user_name)

    def on_quit(self, action, *args, **kwargs):
        """Called when the user activates the Quit action."""
        if self.number_of_win == 1:
            self.save()
            self.quit()
        else:
            self.win.destroy()
            self.number_of_win -= 1

    def on_new_chat_action(self, widget, _):
        chat_id = 0
        for chat in self.data["chats"]:
            if chat["id"] > chat_id:
                chat_id = chat["id"]
        chat_id += 1
        chat = {
            "id": chat_id,
            "title": "New Chat " + str(chat_id),
            "starred": False,
            "content": [],
        }

        self.data["chats"].append(chat)
        self.win.load_threads()

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.new_window()

    @property
    def win(self):
        """The application's main window."""
        return self.props.active_window
        
    def new_window(self, window=None):
        if window:
            win = self.props.active_window
        else:
            win = BavarderWindow(application=self)
            self.number_of_win += 1

        
        win.connect("close-request", self.on_quit)

        self.providers = {}

        for provider in PROVIDERS:
            p = provider(self, win)

            self.providers[p.slug] = p

        win.load_model_selector()
        win.load_provider_selector()
        win.present()


    def on_new_window(self, widget, _):
        self.new_window()


    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = AboutWindow(self.win)
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        preferences = PreferencesWindow(self.win)
        preferences.present()


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

    def create_stateful_action(self, name, parameter_type, initial_state, callback, shortcuts=None):
        """Add a stateful application action."""

        action = Gio.SimpleAction.new_stateful(
            name, parameter_type, initial_state)
        action.connect("activate", callback)

        self.add_action(action)

        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def on_ask(self, widget, _):
        try:
            print("ASK-APP")
            self.win.on_ask()
        except AttributeError:
            pass

    def ask(self, prompt, chat):
        if self.local_mode:
            if not self.setup_chat(): # NO MODELS:
                return _("Please download a model from Preferences by clicking on the Dot Menu at the top!")
            else:
                for p in ["Hi", "Hello"]:
                    if p.lower() in prompt.lower():
                        return _("Hello, I am Bavarder, a Chit-Chat AI")
                system_template = """A chat between a curious user and an artificial intelligence assistant."""
                with self.model.chat_session(self.model_settings.get("system_template", system_template)):
                    self.model.current_chat_session = chat["content"].copy()
                response = self.model.generate(
                    prompt=prompt, 
                    top_k=int(self.model_settings.get("top_k", 40)),
                    top_p=float(self.model_settings.get("top_p", 0.5)),
                    temp=float(self.model_settings.get("temperature", 0.9)),
                    max_tokens=int(self.model_settings.get("max_tokens", 500)),
                    repeat_penalty=float(self.model_settings.get("repetition_penalty", 1.20)),
                    repeat_last_n=int(self.model_settings.get("repeat_last_n", 64)),
                    n_batch=int(self.model_settings.get("n_batch", 10)),
                )

        else:
            l = list(self.providers.values())

            for p in l:
                if p.enabled and p.slug == self.current_provider:
                    response = self.providers[self.current_provider].ask(prompt, chat)
                    break
                else:
                    response = _("Please enable a provider from the Dot Menu")
                
        return response

    @property
    def model_settings(self):
        try:
            return self.data["models"][self.model_name]
        except KeyError:
            try:
                self.data["models"][self.model_name] = {}
            except KeyError:
                self.data["models"] = {}
                self.data["models"][self.model_name] = {}

        return self.data["models"][self.model_name]

    def setup_chat(self):
        if not self.models:
            self.list_models()

        if not self.models:
            return False
        else:
            if self.model is None:
                if self.model_name not in self.models:
                    self.download_model(self.model_name)
                self.model = GPT4All(self.model_name, model_path=model_path)
            return True

    def download_model(self, model=None):
        if model:
            self.model_name = model
        GPT4All.retrieve_model(self.model_name, model_path=model_path,  verbose=True)
        self.models.add(self.model_name)

    def list_models(self):
        self.models = set()
        for root, dirs, files in os.walk(model_path):
            for model in files:
                self.models.add(model)
    
    def delete_model(self, model):
        os.remove(os.path.join(model_path, model))
        self.list_models()

    def check_network(self):
        return False

    def clear_all_chats(self):
        self.data["chats"] = []
        self.win.load_threads()

    def load_bot_and_user_name(self):
        print(self.bot_name)
        print(self.user_name)

def main(version):
    """The application's entry point."""
    app = BavarderApplication()
    return app.run(sys.argv)



