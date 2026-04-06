# window.py
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

from datetime import datetime
import locale
import io
import base64
import os

from gi.repository import Gtk, Gio, Adw, GLib
from babel.dates import format_date, format_datetime, format_time

from bavarder.constants import app_id, build_type, rootdir
from bavarder.widgets.thread_item import ThreadItem
from bavarder.widgets.item import Item
from bavarder.threading import KillableThread
from bavarder.views.export_dialog import ExportDialog
from bavarder.views.chat_settings_dialog import ChatSettingsDialog

class CustomEntry(Gtk.TextView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().set_css_name("entry")

@Gtk.Template(resource_path=f'{rootdir}/ui/window.ui')
class BavarderWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'BavarderWindow'

    split_view = Gtk.Template.Child()
    threads_list = Gtk.Template.Child()
    title = Gtk.Template.Child()
    main_list = Gtk.Template.Child()
    status_no_chat = Gtk.Template.Child()
    status_no_chat_thread = Gtk.Template.Child()
    status_no_thread = Gtk.Template.Child()
    status_no_thread_main = Gtk.Template.Child()
    status_no_internet = Gtk.Template.Child()
    scrolled_window = Gtk.Template.Child()
    model_selector_button = Gtk.Template.Child()
    banner = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    thread_stack = Gtk.Template.Child()
    main = Gtk.Template.Child()
    scroll_down_button = Gtk.Template.Child()

    threads = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = Gtk.Application.get_default()
        self.settings = Gio.Settings(schema_id=app_id)

        CustomEntry.set_css_name("entry")
        self.message_entry = CustomEntry()
        self.message_entry.set_hexpand(True)
        self.message_entry.set_accepts_tab(False)
        self.message_entry.set_top_margin(7)
        self.message_entry.set_bottom_margin(7)
        self.message_entry.set_margin_start(5)
        self.message_entry.set_margin_end(5)
        self.message_entry.set_wrap_mode(Gtk.WrapMode.WORD)
        self.message_entry.add_css_class("chat-entry")

        self.scrolled_window.set_child(self.message_entry)
        self.load_threads()

        self.create_action("cancel", self.cancel, ["<primary>Escape"])
        self.create_action("clear_all", self.on_clear_all)
        self.create_action("export", self.on_export, ["<primary>e"])
        self.create_action("chat_settings", self.on_chat_settings, ["<primary>comma"])

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

        self.message_entry.grab_focus()

        self.main.connect("edge-reached", self.on_edge_reached)
        self.main.connect("edge-overshot", self.on_edge_reached)

    @property
    def chat(self):
        try:
            return self.threads_list.get_selected_row().get_child().chat
        except AttributeError: # create a new chat
            #self.on_new_chat_action()
            return {}


    @property
    def content(self):
        try:
            return self.chat["content"]
        except KeyError: # no content
            return []

    def load_threads(self):
        self.threads_list.remove_all()
        if self.app.data["chats"]:
            self.thread_stack.set_visible_child(self.threads_list)
            self.stack.set_visible_child(self.main)
            for chat in self.app.data["chats"]:
                thread = ThreadItem(self, chat)
                self.threads_list.append(thread)
                self.threads.append(thread)

                try:
                    if not chat["content"]:
                        self.stack.set_visible_child(self.status_no_chat)
                except KeyError:
                    self.stack.set_visible_child(self.status_no_chat)
            self.stack.set_visible_child(self.status_no_thread_main)
        else:
            if self.props.default_width < 500:
                self.thread_stack.set_visible_child(self.status_no_thread)
                self.stack.set_visible_child(self.status_no_chat)
            else:
                self.stack.set_visible_child(self.status_no_thread_main)
                self.thread_stack.set_visible_child(self.status_no_chat_thread)

    @Gtk.Template.Callback()
    def mobile_mode_apply(self, *args):
        if not self.app.data["chats"]:
            self.thread_stack.set_visible_child(self.status_no_thread)
            self.stack.set_visible_child(self.status_no_chat)

    @Gtk.Template.Callback()
    def mobile_mode_unapply(self, *args):
        if not self.app.data["chats"]:
            self.stack.set_visible_child(self.status_no_thread_main)
            self.thread_stack.set_visible_child(self.status_no_chat_thread)

    def do_size_allocate(self, width, height, baseline):
        try:
            self.has_been_allocated
        except Exception:
            self.has_been_allocated = True
            self.load_threads()

        Adw.ApplicationWindow.do_size_allocate(self, width, height, baseline)

    @Gtk.Template.Callback()
    def threads_row_activated_cb(self, *args):
        self.split_view.set_show_content(True)

        try:
            self.title.set_title(self.chat["title"])
        except KeyError:
            self.title.set_title(_("New chat"))

        if self.content:
            self.stack.set_visible_child(self.main)
            self.main_list.remove_all()
            i = 0
            for item in self.content:
                i += 1
                item = Item(self, self.chat, item)
                self.main_list.append(item)

            for i in range(i):
                row = self.main_list.get_row_at_index(i)
                row.set_selectable(False)
                row.set_activatable(False)
        else:
            self.stack.set_visible_child(self.status_no_chat)

    @Gtk.Template.Callback()
    def on_new_chat_action(self, *args):
        self.app.on_new_chat_action(_, _)

    @Gtk.Template.Callback()
    def scroll_down(self, *args):
        code = self.main.emit("scroll-child", Gtk.ScrollType.END, False)

    def on_edge_reached(self, widget, edge):
        if edge == Gtk.PositionType.BOTTOM:
            self.scroll_down_button.set_visible(False)
        else:
            self.scroll_down_button.set_visible(True)

    def on_clear_all(self, *args):
        if self.app.data["chats"]:
            dialog = Adw.MessageDialog(
                heading=_("Delete All Chats"),
                body=_("Are you sure you want to delete all chats in this thread? This can't be undone!"),
                body_use_markup=True
            )

            dialog.add_response("cancel", _("Cancel"))
            dialog.add_response("delete", _("Delete"))
            dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
            dialog.set_default_response("cancel")
            dialog.set_close_response("cancel")

            dialog.connect("response", self.on_clear_all_response)

            dialog.set_transient_for(self)
            dialog.present()
        else:
            toast = Adw.Toast()
            toast.set_title(_("Nothing to clear!"))
            self.toast_overlay.add_toast(toast)


    def on_clear_all_response(self, _widget, response):
        if response == "delete":
            toast = Adw.Toast()
            if self.app.data["chats"]:
                if self.content:
                    self.stack.set_visible_child(self.main)
                    self.main_list.remove_all()
                    del self.chat["content"]
                self.stack.set_visible_child(self.status_no_chat)

                toast.set_title(_("All chats cleared!"))
            else:
                toast.set_title(_("Nothing to clear!"))
            self.toast_overlay.add_toast(toast)

    def on_export(self, *args):
        if self.content:
            dialog = ExportDialog(self, self.chat["content"])
            dialog.set_transient_for(self)
            dialog.present()
        else:
            toast = Adw.Toast()
            toast.set_title(_("Nothing to export!"))
            self.toast_overlay.add_toast(toast)

    def on_chat_settings(self, *args):
        if self.chat:
            dialog = ChatSettingsDialog(self, self.chat)
            dialog.set_transient_for(self)
            dialog.present()

    # MODEL - OFFLINE
    def load_model_selector(self):
        provider_menu = Gio.Menu()

        section = Gio.Menu()

        models = set()

        model_path = self.app.data.get("models", {}).get("model_path", "")
        if model_path and os.path.exists(model_path):
            models.add(os.path.basename(model_path))

        models_dir = os.path.join(self.app.user_cache_dir, "bavarder", "models")
        if os.path.exists(models_dir):
            for f in os.listdir(models_dir):
                if f.endswith(".litertlm"):
                    models.add(f)

        if models:
            for model in models:
                item_provider = Gio.MenuItem()
                item_provider.set_label(model)
                item_provider.set_action_and_target_value(
                    "app.set_model",
                    GLib.Variant("s", model))
                section.append_item(item_provider)
            provider_menu.append_section(_("Models"), section)

        section = Gio.Menu()
        item_provider = Gio.MenuItem()
        item_provider.set_label(_("Preferences"))
        item_provider.set_action_and_target_value("app.preferences", None)
        section.append_item(item_provider)

        item_provider = Gio.MenuItem()
        item_provider.set_label(_("Clear all"))
        item_provider.set_action_and_target_value("win.clear_all", None)
        section.append_item(item_provider)

        item_provider = Gio.MenuItem()
        item_provider.set_label(_("Export"))
        item_provider.set_action_and_target_value("win.export", None)
        section.append_item(item_provider)

        provider_menu.append_section(None, section)

        self.model_selector_button.set_menu_model(provider_menu)

    def check_network(self):
        if self.app.check_network(): # Internet
            if not self.content:
                self.status_no_chat.set_visible(True)
                self.status_no_internet.set_visible(False)
            else:
                self.status_no_chat.set_visible(False)
                self.status_no_internet.set_visible(False)
        else:
            self.status_no_chat.set_visible(False)
            self.status_no_internet.set_visible(True)



    @Gtk.Template.Callback()
    def on_ask(self, *args):
        prompt = self.message_entry.get_buffer().props.text.strip()
        if prompt:
            self.message_entry.get_buffer().set_text("")

            if not self.chat:
                self.on_new_chat_action()

                # now get the latest row
                row = self.threads_list.get_row_at_index(len(self.app.data["chats"]) - 1)


                self.threads_list.select_row(row)
                self.threads_row_activated_cb()


            self.add_user_item(prompt)

            self.response_buffer = ""
            self.assistant_item_added = False

            def on_token(token):
                if token is None:
                    self.toast.dismiss()
                    if not self.response_buffer:
                        self.add_assistant_item(_("Sorry, I don't know what to say."))
                    else:
                        self.update_last_assistant_item(self.response_buffer.strip())
                    return
                
                self.response_buffer += token
                
                min_content = 5
                if len(self.response_buffer) >= min_content:
                    if not self.assistant_item_added:
                        self.add_assistant_item(self.response_buffer.strip())
                        self.assistant_item_added = True
                    else:
                        self.update_last_assistant_item(self.response_buffer.strip())
                    self.scroll_down()

            def on_error(error):
                self.toast.dismiss()
                self.add_assistant_item(_("Error: ") + error)

            self.toast = Adw.Toast()
            self.toast.set_title(_("Generating response"))
            self.toast.set_timeout(0)
            self.toast_overlay.add_toast(self.toast)

            self.app.ask(prompt, self.chat, on_token, on_error)

    # @Gtk.Template.Callback()
    # def on_emoji(self, *args):
    #     self.message_entry.do_insert_emoji(self.message_entry)

    def cancel(self, *args):
        try:
            self.t.kill()
            self.t.join()

            del self.t
            self.toast.dismiss()
        except AttributeError: # nothing to stop
            pass
        except Exception:
            self.t.join()
            del self.t
            self.toast.dismiss()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)

        if shortcuts:
            self.app.set_accels_for_action(f"win.{name}", shortcuts)

    def get_time(self):
        return format_time(datetime.now())


    def add_user_item(self, content):
        self.content.append(
            {
                "role": self.app.user_name,
                "content": content,
                "time": self.get_time(),
                "model": _("human"),
            }
        )

        self.threads_row_activated_cb()

        self.scroll_down()

    def get_model_name(self):
        model_path = self.app.data.get("models", {}).get("model_path", "")
        if model_path and os.path.exists(model_path):
            return os.path.basename(model_path)
        return "litert-lm"

    def add_assistant_item(self, content):
        model_name = self.get_model_name()
        c = {
            "role": self.app.bot_name,
            "content": content,
            "time": self.get_time(),
            "model": model_name,
        }

        self.content.append(c)

        self.threads_row_activated_cb()

        self.scroll_down()

    def update_last_assistant_item(self, content):
        if self.content:
            self.content[-1]["content"] = content
            self.threads_row_activated_cb()
            self.scroll_down()
