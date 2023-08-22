from .base import BaseProvider

import json
import requests
import time

from gi.repository import Adw, Gtk

class AIHordeProvider(BaseProvider):
    name = "AI Horde"
    
    ASYNC_URL = "https://stablehorde.net/api/v2/generate/text/async"
    STATUS_URL = "https://stablehorde.net/api/v2/generate/text/status/"
    API_KEY = "0000000000"
    model = "PygmalionAI/pygmalion-7b"
    

    def ask(self, prompt, chat, **kwargs):
        self.API_KEY = self.data.get("api_key", "0000000000")
       
        chat = chat["content"]

        self.headers = {
            "Client-Agent": "bavarder:1:linux",
            "apikey": self.API_KEY,
        }

        data = {
            "prompt": prompt,
            "models": [
                self.model
            ]
        }

        r = requests.post(self.ASYNC_URL, json=data, headers=self.headers)

        if r.status_code == 202:
            rid =  r.json()["id"]
        else:
            print(r.json())
            print(r.status_code)
            return _("I'm sorry, I don't know what to say!")


        # do the request every seconds and check if it's finished
        while True:
            r = self.check_status(rid)
            if r:
                return r
            else:
                time.sleep(1)
        return _("I'm sorry, I don't know what to say!")

    def check_status(self, rid):
        r = requests.get(self.STATUS_URL + rid)
        rj = r.json()

        if r.status_code == 200:
            print(rj)
            if rj["done"]:
                return r.json()["generations"][0]["text"]
        return None

    def get_settings_rows(self):
        self.rows = []

        self.api_row = Adw.PasswordEntryRow()
        self.api_row.connect("apply", self.on_apply)
        self.api_row.props.text = self.data.get('api_key') or self.API_KEY
        self.api_row.props.title = _("API Key")
        self.api_row.set_show_apply_button(True)
        self.api_row.add_suffix(self.how_to_get_a_token())
        self.rows.append(self.api_row)

        r = requests.get("https://stablehorde.net/api/v2/status/models?type=text")

        if r.status_code != 200:
            print(r.json())
            return self.rows
        else:
            rj = r.json()

            models_row = Adw.ActionRow()
            models_row.set_title(_("Models"))
            models_row.set_subtitle(_("Select a model to use"))

            go_to_sub_button = Gtk.Button.new_from_icon_name("go-next-symbolic")
            go_to_sub_button.set_valign(Gtk.Align.CENTER)
            go_to_sub_button.set_tooltip_text(_("Go to the models page"))
            go_to_sub_button.add_css_class("flat")
            go_to_sub_button.connect("clicked", self.open_subpage)

            models_row.add_suffix(go_to_sub_button)

            self.page = Adw.NavigationPage()

            prefpage = Adw.PreferencesPage()

            group = Adw.PreferencesGroup()

            self.selected_row = Adw.ActionRow()
            self.selected_row.set_title(_("Selected model"))
            if self.model:
                self.selected_row.set_subtitle(self.model)
            else:
                self.selected_row.set_subtitle(_("No model selected"))

            group.add(self.selected_row)

            for model in rj:
                mr = Adw.ActionRow()
                mr.props.title = model["name"]
                mr.props.subtitle = f"Performance {model['performance']} - Jobs {model['jobs']} - Queued {model['queued']}"

                apply_button = Gtk.Button.new_from_icon_name("object-select-symbolic")
                apply_button.connect("clicked", self.on_apply_model, model["name"])
                apply_button.set_valign(Gtk.Align.CENTER)
                apply_button.set_tooltip_text(_("Select this model"))
                apply_button.add_css_class("flat")

                mr.add_suffix(apply_button)

                group.add(mr)


            toolbar = Adw.ToolbarView()
            header = Adw.HeaderBar()
            label = Gtk.Label()
            label.set_label(_("Models"))
            header.set_title_widget(label)
            toolbar.add_top_bar(header)
            prefpage.add(group)
            toolbar.set_content(prefpage)
            self.page.set_child(toolbar)



            self.rows.append(models_row)

        return self.rows

    def open_subpage(self, widget):
        self.app.preferences_window.push_subpage(self.page)

    def on_apply(self, widget):
        self.API_KEY = self.api_row.get_text()
        self.data["api_key"] = self.API_KEY

    def on_apply_model(self, widget, name):
        self.model = name
        if self.model:
            self.selected_row.set_subtitle(self.model)
        else:
            self.selected_row.set_subtitle(_("No model selected"))
