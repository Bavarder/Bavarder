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
gi.require_version('WebKit', '6.0')

from gi.repository import Gtk, Gio, Adw, Gdk, GLib, Gst, WebKit
from .views.main_window import BavarderWindow
from .views.preferences_window import Preferences
from .views.about_window import BavarderAboutWindow
from enum import auto, IntEnum

from .constants import app_id, version, build_type

from tempfile import NamedTemporaryFile

from .providers import PROVIDERS
import platform
import os
import markdown
import tempfile
import re
import requests

from .threading import KillableThread

from enum import auto, IntEnum

class Step(IntEnum):
    CONVERT_HTML = auto()
    LOAD_WEBVIEW = auto()
    RENDER = auto()

ANNOUCEMENT_URL = "https://bavarder.codeberg.page/annoucements.json"


class BavarderApplication(Adw.Application):
    """The main application singleton class."""

    annoucements = {}

    def __init__(self):
        super().__init__(
            application_id=app_id,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self.create_action("quit_all", self.on_close_all, ["<primary>q"])
        self.create_action("quit", self.on_quit, ["<primary>w"])
        self.create_action("about", self.on_about_action)
        self.create_action(
            "preferences", self.on_preferences_action, ["<primary>comma"]
        )
        self.create_action("copy_prompt", self.on_copy_prompt_action)
        self.create_action("copy_bot", self.on_copy_bot_action, ["<primary><shift>c"])
        self.create_action("ask", self.on_ask_action, ["<primary>Return"])
        self.create_action("clear", self.on_clear_action, ["<primary><shift>BackSpace"])
        self.create_action("stop", self.on_stop_action, ["<primary>Escape"])
        self.create_action("new", self.on_new_window, ["<primary>n"])
        self.create_action("open_help", self.on_open_help, ["F1"])
        # self.create_action("speak", self.on_speak_action, ["<primary>S"])
        # self.create_action("listen", self.on_listen_action, ["<primary>L"])

        self.settings = Gio.Settings(schema_id=app_id)

        self.clear_after_send = self.settings.get_boolean("clear-after-send")
        self.use_text_view = self.settings.get_boolean("use-text-view")

        self.enabled_providers = sorted(
            set(self.settings.get_strv("enabled-providers"))
        )
        self.latest_provider = self.settings.get_string("latest-provider")
        self.provider = self.latest_provider
        self.close_all_without_dialog = self.settings.get_boolean(
            "close-all-without-dialog"
        )
        self.create_stateful_action(
            "set_provider",
            GLib.VariantType.new("s"),
            GLib.Variant("s", self.latest_provider),
            self.on_set_provider_action
        )
        self.allow_remote_fetching = self.settings.get_boolean("allow-remote-fetching")
        self.use_theme = False
        self.providers = {}

    def load_annoucements(self):
        try:
            self.annoucements = requests.get(ANNOUCEMENT_URL).json()
        except:
            pass
        else:
            try:
                self.latest = self.annoucements["latest"]
                del self.annoucements["latest"]
            except:
                pass
            else:
                if not self.latest in version:
                    self.win.banner.set_title(_("New version available!"))
                    self.win.banner.set_revealed(True)



    def on_open_help(self, action, *args):
        GLib.spawn_command_line_async(
            f"xdg-open https://bavarder.codeberg.page"
        )

    def on_set_provider_action(self, action, *args):
        self.provider = args[0].get_string()
        Gio.SimpleAction.set_state(self.lookup_action("set_provider"), args[0])


    def quitting(self, *args, **kwargs):
        """Called before closing main window."""
        self.settings.set_strv("enabled-providers", list(self.enabled_providers))
        self.settings.set_string("latest-provider", self.provider)


        print("Saving providers data...")

        self.save_providers()

    @property
    def win(self):
        return self.props.active_window

    def on_new_window(self, action, *args):
        self.new_window()

    def new_window(self, window=None):
        if window:
            win = self.props.active_window
        else:
            win = BavarderWindow(application=self)
        win.connect("close-request", self.quitting)
        self.load_dropdown(win)
        self.load()
        win.web_view = None
        win.web_view_pending_html = None
        win.loading = False
        win.shown = False
        win.preview_visible = False

        win.present()

    def close_all(self):
        self.quitting()
        for w in self.get_windows():
            w.close()


    def on_close_all(self, action, param):
        print("Closing all windows...")

        
        if len(self.get_windows()) == 1:
            self.on_quit(action, param)
        elif self.close_all_without_dialog:
            self.close_all()
        else:
            dialog = Adw.MessageDialog(
                heading="Close all windows?",
                body="Closing all windows will lead to chat data loss",
                transient_for=self.props.active_window,
            )
            dialog.add_response("cancel", "Cancel")
            dialog.add_response("close", "Close")
            dialog.set_response_appearance("close", Adw.ResponseAppearance.DESTRUCTIVE)
            dialog.set_default_response("cancel")
            dialog.set_close_response("cancel")
            dialog.connect("response", self.on_close_all_response)
            dialog.present()

    def on_close_all_response(self, dialog, response):
        if response == "close":
            self.close_all()
        dialog.close()
        

    def on_quit(self, action, param):
        """Called when the user activates the Quit action."""
        print("Closing active window...")
        self.quitting()
        self.win.close()

    def save_providers(self):
        r = {}
        for k, p in self.providers.items():
            r[p.slug] = json.dumps(p.save())
        data = GLib.Variant("a{ss}", r)
        self.settings.set_value("providers-data", data)

    def on_clear_action(self, action, param):
        self.win.bot_text_view.get_buffer().set_text("")
        self.win.prompt_text_view.get_buffer().set_text("")
        self.win.prompt_text_view.grab_focus()

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.new_window()
        if self.allow_remote_fetching:
            self.load_annoucements()
        self.win.prompt_text_view.grab_focus()

    def load_dropdown(self, window=None):
        if window is None:
            window = self.props.active_window

        self.menu_model = Gio.Menu()
        self.menu_model.append_item(Gio.MenuItem.new(label=_("New Window"), detailed_action="app.new"))

        section_menu = Gio.Menu()

        provider_menu = Gio.Menu()


        self.providers = {}
        self.providers_data = self.settings.get_value("providers-data")

        for provider in self.enabled_providers:
            if provider in self.providers:
                p = self.providers[provider]
                name = p.name
                slug = p.slug
            else:
                try:
                    p = PROVIDERS[provider]
                    name = p.name
                    slug = p.slug
                except KeyError:
                    continue
                else:
                    self.providers[slug] = PROVIDERS[provider](window, self)

            item_model = Gio.MenuItem()
            item_model.set_label(name)
            item_model.set_action_and_target_value(
                "app.set_provider",
                GLib.Variant("s", slug))
            provider_menu.append_item(item_model)
        section_menu.append_submenu(_("Providers"), provider_menu)

        section_menu.append_item(Gio.MenuItem.new(label=_("Preferences"), detailed_action="app.preferences"))
        section_menu.append_item(Gio.MenuItem.new(label=_("Keyboard Shortcuts"), detailed_action="win.show-help-overlay"))
        section_menu.append_item(Gio.MenuItem.new(label=_("About Bavarder"), detailed_action="app.about"))

        self.menu_model.append_section(None, section_menu)

        window.menu.set_menu_model(self.menu_model)

    def load(self):
        for p in self.providers.values():
            try:
                p.load(data=json.loads(self.providers_data[p.slug]))
            except KeyError:  # provider not in data
                pass

    def on_provider_selector_notify(self, _unused, pspec):
        try:
            self.win.banner.set_revealed(False)
        except AttributeError:
            pass

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = BavarderAboutWindow(self.win)
        about.show_about()

    def on_preferences_action(self, widget, *args, **kwargs):
        """Callback for the app.preferences action."""
        preferences = Preferences(
            parent=self.win
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
        toast.set_title("Text copied")
        
        try: 
            text = self.response 
        except AttributeError:
            return
        else:
            if len(text) == 0:
                return
            else:
                Gdk.Display.get_default().get_clipboard().set(text)

                self.win.toast_overlay.add_toast(toast)

    @staticmethod
    def on_click_link(web_view, decision, _decision_type):
        if web_view.get_uri().startswith(("http://", "https://", "www.")):
            Glib.spawn_command_line_async(f"xdg-open {web_view.get_uri()}")
            decision.ignore()
            return True

    @staticmethod
    def on_right_click(web_view, context_menu, _event, _hit_test):
        # disable some context menu option
        for item in context_menu.get_items():
            if item.get_stock_action() in [WebKit.ContextMenuAction.RELOAD,
                                           WebKit.ContextMenuAction.GO_BACK,
                                           WebKit.ContextMenuAction.GO_FORWARD,
                                           WebKit.ContextMenuAction.STOP]:
                context_menu.remove(item)


    def show(self, html=None, step=Step.LOAD_WEBVIEW):
        if step == Step.LOAD_WEBVIEW:
            self.win.loading = True
            if not self.win.web_view:
                self.win.web_view = WebKit.WebView()
                self.win.web_view.get_settings().set_allow_universal_access_from_file_urls(True)

                self.win.web_view.get_settings().set_enable_developer_extras(True)

                # Show preview once the load is finished
                self.win.web_view.connect("load-changed", self.on_load_changed)

                # All links will be opened in default browser, but local files are opened in apps.
                self.win.web_view.connect("decide-policy", self.on_click_link)

                self.win.web_view.connect("context-menu", self.on_right_click)

                self.win.web_view.set_hexpand(True)
                self.win.web_view.set_vexpand(True)

                self.win.response_stack.add_child(self.win.web_view)
                self.win.response_stack.set_visible_child(self.win.web_view)
            
            if self.win.web_view.is_loading():
                self.win.web_view_pending_html = html
            else:
                try:
                    self.win.web_view.load_html(html, "file://localhost/")
                except TypeError: # Argument 1 does not allow None as a value
                    pass


        elif step == Step.RENDER:
            if not self.win.preview_visible:
                self.win.preview_visible = True
                self.show()

    def reload(self, *_widget, reshow=False):
        if self.win.preview_visible:
            if reshow:
                self.hide()
            self.show()

    def on_load_changed(self, _web_view, event):
        if event == WebKit.LoadEvent.FINISHED:
            self.win.loading = False
            if self.win.web_view_pending_html:
                self.show(html=self.win.web_view_pending_html, step=Step.LOAD_WEBVIEW)
                self.win.web_view_pending_html = None
            else:
                # we only lazyload the webview once
                self.show(step=Step.RENDER)

    def parse_css(self, path):

        adw_palette_prefixes = [
            "blue_",
            "green_",
            "yellow_",
            "orange_",
            "red_",
            "purple_",
            "brown_",
            "light_",
            "dark_"
        ]

        # Regular expressions
        not_define_color = re.compile(r"(^(?:(?!@define-color).)*$)")
        define_color = re.compile(r"(@define-color .*[^\s])")
        css = ""
        variables = {}
        palette = {}

        for color in adw_palette_prefixes:
            palette[color] = {}

        with open(path, "r", encoding="utf-8") as sheet:
            for line in sheet:
                cdefine_match = re.search(define_color, line)
                not_cdefine_match = re.search(not_define_color, line)
                if cdefine_match != None: # If @define-color variable declarations were found
                    palette_part = cdefine_match.__getitem__(1) # Get the second item of the re.Match object
                    name, color = palette_part.split(" ", 1)[1].split(" ", 1)
                    if name.startswith(tuple(adw_palette_prefixes)): # Palette colors
                        palette[name[:-1]][name[-1:]] = color[:-1]
                    else: # Other color variables
                        variables[name] = color[:-1]
                elif not_cdefine_match != None: # If CSS rules were found
                    css_part = not_cdefine_match.__getitem__(1)
                    css += f"{css_part}\n"

            sheet.close()
            return variables, palette, css
            
    def update_response(self, response):
        """Update the response text view with the response."""
        self.response = response

        if not self.use_text_view:
            response = markdown.markdown(response, extensions=["markdown.extensions.extra", 'pymdownx.arithmatex', 'pymdownx.highlight'])

            TEMPLATE = """
            <html>
                <head>
                    <style>
                        @font-face {
                        font-family: 'Cantarell';
                        src: local("Cantarell")
                        }

                        @font-face {
                        font-family: 'Monospace';
                        src: local("Monospace")
                        }

                        @font-face {
                        font-family: color-emoji;
                        src: local("Noto Color Emoji"), local("Apple Color Emoji"), local("Segoe UI Emoji"), local("Segoe UI Symbol");
                        }

                        {theme_css}

                        * {
                        box-sizing: border-box;
                        }

                        html {
                        font-size: 11pt;
                        }

                        body {
                        color: var(--text-color);
                        background-color: var(--background-color);
                        font-family: "Cantarell", "Monospace", sans-serif, color-emoji;
                        line-height: 1.5;
                        word-wrap: break-word;
                        max-width: 980px;
                        margin: 0;
                        //padding: 4em;
                        }

                        a {
                        background-color: transparent;
                        color: var(--link-color);
                        text-decoration: none;
                        }

                        a:active,
                        a:hover {
                        outline-width: 0;
                        }

                        a:hover {
                        text-decoration: underline;
                        }

                        strong {
                        font-weight: bold;
                        }

                        img {
                        border-style: none;
                        }

                        hr {
                        box-sizing: content-box;
                        height: 0.25em;
                        padding: 0;
                        margin: 1.5em 0;
                        overflow: hidden;
                        background-color: var(--hr-background-color);
                        border: 0;
                        }

                        hr::before {
                        display: table;
                        content: "";
                        }

                        hr::after {
                        display: table;
                        clear: both;
                        content: "";
                        }

                        input {
                        font-family: inherit;
                        font-size: inherit;
                        line-height: inherit;
                        margin: 0;
                        overflow: visible;
                        }

                        [type="checkbox"] {
                        box-sizing: border-box;
                        padding: 0;
                        }

                        table {
                        border-spacing: 0;
                        border-collapse: collapse;
                        }

                        td,
                        th {
                        padding: 0;
                        }

                        h1,
                        h2,
                        h3,
                        h4,
                        h5,
                        h6 {
                        font-weight: bold;
                        margin: 0;
                        }

                        h1 {
                        font-size: 24pt;
                        }

                        h2 {
                        font-size: 18pt;
                        }

                        h3 {
                        font-size: 14pt;
                        }

                        h4 {
                        font-size: 12pt;
                        }

                        h5 {
                        font-size: 10pt;
                        }

                        h6 {
                        font-size: 8pt;
                        }

                        p {
                        margin-top: 0;
                        margin-bottom: 0.625em;
                        }

                        blockquote {
                        margin: 0;
                        }

                        ul,
                        ol {
                        padding-left: 0;
                        margin-top: 0;
                        margin-bottom: 0;
                        }

                        ol ol,
                        ul ol {
                        list-style-type: lower-roman;
                        }

                        ul ul ol,
                        ul ol ol,
                        ol ul ol,
                        ol ol ol {
                        list-style-type: lower-alpha;
                        }

                        dd {
                        margin-left: 0;
                        }

                        code,
                        kbd,
                        pre {
                        font-family: "Monospace", monospace, color-emoji;
                        font-size: 12pt;
                        word-wrap: normal;
                        }

                        code {
                        border-radius: 0.1875em;
                        font-size: 10pt;
                        padding: 0.2em 0.4em;
                        margin: 0;
                        }

                        pre {
                        margin-top: 0;
                        margin-bottom: 0;
                        font-size: 8pt;
                        }

                        pre>code {
                        padding: 0;
                        margin: 0;
                        font-size: 12pt;
                        word-break: normal;
                        white-space: pre;
                        background: transparent;
                        border: 0;
                        }

                        .highlight {
                        margin-bottom: 1em;
                        }

                        .highlight pre {
                        margin-bottom: 0;
                        word-break: normal;
                        }

                        .highlight pre,
                        pre {
                        padding: 1em;
                        overflow: auto;
                        font-size: 10pt;
                        line-height: 1.5;
                        background-color: var(--alt-background-color);
                        border-radius: 0.1875em;
                        }

                        pre code {
                        background-color: transparent;
                        border: 0;
                        display: inline;
                        padding: 0;
                        margin: 0;
                        overflow: visible;
                        line-height: inherit;
                        word-wrap: normal;
                        }

                        .pl-0 {
                        padding-left: 0 !important;
                        }

                        .pl-1 {
                        padding-left: 0.25em !important;
                        }

                        .pl-2 {
                        padding-left: 0.5em !important;
                        }

                        .pl-3 {
                        padding-left: 1em !important;
                        }

                        .pl-4 {
                        padding-left: 1.5em !important;
                        }

                        .pl-5 {
                        padding-left: 2em !important;
                        }

                        .pl-6 {
                        padding-left: 2.5em !important;
                        }

                        .markdown-body::before {
                        display: table;
                        content: "";
                        }

                        .markdown-body::after {
                        display: table;
                        clear: both;
                        content: "";
                        }

                        .markdown-body>*:first-child {
                        margin-top: 0 !important;
                        }

                        .markdown-body>*:last-child {
                        margin-bottom: 0 !important;
                        }

                        a:not([href]) {
                        color: inherit;
                        text-decoration: none;
                        }

                        .anchor {
                        float: left;
                        padding-right: 0.25em;
                        margin-left: -1.25em;
                        line-height: 1;
                        }

                        .anchor:focus {
                        outline: none;
                        }

                        p,
                        blockquote,
                        ul,
                        ol,
                        dl,
                        table,
                        pre {
                        margin-top: 0;
                        margin-bottom: 1em;
                        }

                        blockquote {
                        padding: 0 1em;
                        color: var(--blockquote-text-color);
                        border-left: 0.25em solid var(--blockquote-border-color);
                        }

                        blockquote>:first-child {
                        margin-top: 0;
                        }

                        blockquote>:last-child {
                        margin-bottom: 0;
                        }

                        kbd {
                        display: inline-block;
                        padding: 0.1875em 0.3125em;
                        font-size: 8pt;
                        line-height: 1;
                        color: var(--kbd-text-color);
                        vertical-align: middle;
                        background-color: var(--kbd-background-color);
                        border: solid 1px var(--kbd-border-color);
                        border-bottom-color: var(--kbd-shadow-color);
                        border-radius: 3px;
                        box-shadow: inset 0 -1px 0 var(--kbd-shadow-color);;
                        }

                        h1,
                        h2,
                        h3,
                        h4,
                        h5,
                        h6 {
                        margin-top: 1.5em;
                        margin-bottom: 1em;
                        font-weight: 600;
                        line-height: 1.25;
                        }

                        h1:hover .anchor,
                        h2:hover .anchor,
                        h3:hover .anchor,
                        h4:hover .anchor,
                        h5:hover .anchor,
                        h6:hover .anchor {
                        text-decoration: none;
                        }

                        h1 {
                        padding-bottom: 0.3em;
                        font-size: 24pt;
                        border-bottom: 1px solid var(--header-border-color);
                        }

                        h2 {
                        padding-bottom: 0.3em;
                        font-size: 18pt;
                        border-bottom: 1px solid var(--header-border-color);
                        }

                        h3 {
                        font-size: 14pt;
                        }

                        h4 {
                        font-size: 12pt;
                        }

                        h5 {
                        font-size: 10pt;
                        }

                        h6 {
                        font-size: 8pt;
                        opacity: 0.67;
                        }

                        ul,
                        ol {
                        padding-left: 2em;
                        }

                        ul ul,
                        ul ol,
                        ol ol,
                        ol ul {
                        margin-top: 0;
                        margin-bottom: 0;
                        }

                        li {
                        overflow-wrap: break-word;
                        }

                        li>p {
                        margin-top: 1em;
                        }

                        li+li {
                        margin-top: 0.25em;
                        }

                        dl {
                        padding: 0;
                        }

                        dl dt {
                        padding: 0;
                        margin-top: 1em;
                        font-size: 12pt;
                        font-style: italic;
                        font-weight: 600;
                        }

                        dl dd {
                        padding: 0 1em;
                        margin-bottom: 1em;
                        }

                        table {
                        display: block;
                        width: 100%;
                        overflow: auto;
                        }

                        table th {
                        font-weight: 600;
                        }

                        table th,
                        table td {
                        padding: 0.375em 0.8125em;
                        border: 1px solid var(--table-td-border-color);
                        }

                        table tr {
                        background-color: var(--background-color);
                        border-top: 1px solid var(--table-tr-border-color);
                        }

                        table tr:nth-child(2n) {
                        background-color: var(--alt-background-color);
                        }

                        img {
                        max-width: 100%;
                        box-sizing: content-box;
                        }

                        img[align=right] {
                        padding-left: 1.25em;
                        }

                        img[align=left] {
                        padding-right: 1.25em;
                        }

                        .task-list-item {
                        list-style-type: none;
                        }

                        .task-list-item+.task-list-item {
                        margin-top: 0.1875em;
                        }

                        .task-list-item input {
                        margin: 0 0.2em 0.25em -1.6em;
                        vertical-align: middle;
                        }
                    </style>

                    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
                    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>

                    <script>
                    window.MathJax = {
                        tex: {
                            inlineMath: [ ["\\(","\\)"] ],
                            displayMath: [ ["\\[","\\]"] ],
                            processEscapes: true,
                            processEnvironments: true
                        },
                        options: {
                            ignoreHtmlClass: ".*",
                            processHtmlClass: "arithmatex"
                        }
                        };
                    </script>

                </head>
                <body>
                    {response}
                </body>
            </html>
            """

            ADWAITA_STYLE = """:root {
                            --text-color: rgba(0, 0, 0, 0.8);
                            --background-color: #ffffff;
                            --alt-background-color: #ebebeb;
                            --link-color: #1c71d8;
                            --blockquote-text-color: rgba(0, 0, 0, 0.8);
                            --blockquote-border-color: #dbdbdb;
                            --header-border-color: #dbdbdb;
                            --hr-background-color: #dbdbdb;
                            --table-tr-border-color: #dcdcdc;
                            --table-td-border-color: #dcdcdc;
                            --kbd-text-color: rgba(0, 0, 0, 0.8);
                            --kbd-background-color: #ffffff;
                            --kbd-border-color: #dcdcdc;
                            --kbd-shadow-color: #dddddd;
                        }

                        @media (prefers-color-scheme: dark) {
                            :root {
                                --text-color: #ffffff;
                                --background-color: #363636;
                                --alt-background-color: #4a4a4a;
                                --link-color: #78aeed;
                                --blockquote-text-color: #ffffff;
                                --blockquote-border-color: #454545;
                                --header-border-color: #454545;
                                --hr-background-color: #505050;
                                --table-tr-border-color: #6e6e6e;
                                --table-td-border-color: #6e6e6e;
                                --kbd-text-color: #ffffff;
                                --kbd-background-color: #4a4a4a;
                                --kbd-border-color: #6e6e6e;
                                --kbd-shadow-color: #575757;
                            }
                        }"""
            CUSTOM_STYLE = """
                --text-color: {card_fg_color};
                --background-color: {card_bg_color};
                --alt-background-color: {view_bg_color};
                --link-color: {accent_fg_color};
                --blockquote-text-color: {card_fg_color};
                --blockquote-border-color: {card_bg_color};
                --header-border-color: {headerbar_border_color};
                --hr-background-color: {headerbar_bg_color};
                --table-tr-border-color: {headerbar_border_color};
                --table-td-border-color: {headerbar_border_color};
                --kbd-text-color: #4e585e;
                --kbd-background-color: #f1f1f1;
                --kbd-border-color: #bdc1c6;
                --kbd-shadow-color: #8c939a;
            """
            DARK_CUSTOM_STYLE = """
                --text-color: {card_fg_color};
                --background-color: {card_bg_color};
                --alt-background-color: {view_bg_color};
                --link-color: {accent_fg_color};
                --blockquote-text-color: {card_fg_color};
                --blockquote-border-color: {card_bg_color};
                --header-border-color: {headerbar_border_color};
                --hr-background-color: {headerbar_bg_color};
                --table-tr-border-color: {headerbar_border_color};
                --table-td-border-color: {headerbar_border_color};
                --kbd-text-color: #ffffff;
                --kbd-background-color: #4a4a4a;
                --kbd-border-color: #1f1f1f;
                --kbd-shadow-color: #1e1e1e;
            """

            if os.path.exists(os.path.expanduser("~/.config/gtk-4.0/gtk.css")):
                self.use_theme = True
                variables, palette, css = self.parse_css(os.path.expanduser("~/.config/gtk-4.0/gtk.css"))
                variables["card_fg_color"] = variables.get("card_fg_color", "#2e3436")
                variables["card_bg_color"] = variables.get("card_bg_color", "#f6f5f4")
                variables["view_bg_color"] = variables.get("view_bg_color", "#edeeef")
                variables["accent_fg_color"] = variables.get("accent_fg_color", "#0d71de")
                variables["headerbar_border_color"] = variables.get("headerbar_border_color", "#e1e2e4")
                variables["headerbar_bg_color"] = variables.get("headerbar_bg_color", "#d8dadd")
                theme_css = ":root {\n" + CUSTOM_STYLE.format(**variables) + " \n}\n" + "@media (prefers-color-scheme: dark) {\n:root {\n" + \
                     DARK_CUSTOM_STYLE.format(**variables) + "\n}\n}\n" + css
            else:
                self.use_theme = False
                theme_css = ADWAITA_STYLE
            self.show(TEMPLATE.replace("{response}", response).replace("{theme_css}", theme_css), Step.LOAD_WEBVIEW)
        else:
            self.win.bot_text_view.get_buffer().props.text = response
            self.win.response_stack.set_visible_child_name("page_response")

    def on_ask_action(self, widget, _):
        """Callback for the app.ask action."""

        self.win.banner.set_revealed(False)

        for key, an in self.annoucements.items():
            if an["provider"] == self.provider:
                if an["status"] == "open":
                    match an["action"]:
                        case "error": # show an error banner with a button to open settings
                            self.win.banner.set_title(an["message"])
                            self.win.banner.props.button_label = "Open settings"
                            self.win.banner.connect("button-clicked", self.on_preferences_action)
                            self.win.banner.set_revealed(True)
                        case _:
                            self.win.banner.set_title(an["message"])
                            self.win.banner.set_revealed(True)
                del self.annoucements[key]
                break

        self.prompt = self.win.prompt_text_view.get_buffer().props.text.strip()

        if self.prompt == "" or self.prompt is None:  # empty prompt
            return
        else:
            self.win.spinner.start()
            self.win.ask_button.set_visible(False)
            self.win.wait_button.set_visible(True)
            self.win.stop_button.set_visible(True)

            def thread_run():
                try:
                    response = self.providers[self.provider].ask(self.prompt)
                except GLib.Error as e:
                    response = e.message
                except KeyError:
                    del self.providers[self.provider]
                GLib.idle_add(cleanup, response)

            def cleanup(response):
                self.win.spinner.stop()
                self.win.ask_button.set_visible(True)
                self.win.wait_button.set_visible(False)
                self.win.stop_button.set_visible(False)
                GLib.idle_add(self.update_response, response)
                self.t.join()
                if self.clear_after_send:
                    self.win.prompt_text_view.get_buffer().set_text("")

            self.t = KillableThread(target=thread_run)
            self.t.start()

    def on_stop_action(self, widget, _):
        """Callback for the app.stop action."""
        self.win.spinner.stop()
        self.win.ask_button.set_visible(True)
        self.win.wait_button.set_visible(False)
        self.win.stop_button.set_visible(False)
        self.t.kill()
        self.t.join()

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

    def create_stateful_action(self, name, parameter_type, initial_state, callback, shortcuts=None):
        """Add a stateful application action."""

        action = Gio.SimpleAction.new_stateful(
            name, parameter_type, initial_state)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.parent.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = BavarderApplication()
    return app.run(sys.argv)
