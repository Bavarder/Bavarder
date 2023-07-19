import unicodedata
import re
from typing import List, Dict
from gi.repository import Gtk, Adw, GLib

    
class BaseProvider:
    name: str
    description: str = ""
    languages: List[str] = []
    developer_name: str = "0xMRTT"
    developers = ["0xMRTT https://github.com/0xMRTT"]
    license_type = Gtk.License.GPL_3_0
    data: Dict[str, str] = {}
    has_auth: bool = False
    require_authentification: bool = False
    
    def __init__(self, app, window, providers):
        self.slug = self.slugify(self.name)
        self.copyright = f"© 2023 {self.developer_name}"
        self.url = f"https://bavarder.codeberg.page/providers/{self.slug}"

        self.app = app
        self.window = window

        self.providers = providers
        try:
            self.providers[self.slug]
        except KeyError:
            self.providers[self.slug] = {
                "enabled": False,
                "data": {

                }
            }
        finally:
            self.data = self.providers[self.slug]["data"]

    @property
    def enabled(self):
        return self.providers[self.slug]["enabled"]

    def set_enabled(self, status):
        self.providers[self.slug]["enabled"] = status

    def ask(self, prompt, chat):
        raise NotImplementedError()

    def load_authentification(self):
        """Must set self.has_auth to True when auth is done"""
        raise NotImplementedError()

    def get_settings_rows(self) -> list:
        return []

    # TOOLS
    def slugify(self, value):
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub('[^\w\s-]', '', value).strip().lower()
        return re.sub('[-\s]+', '-', value)

    def chunk(self, prompt, n=4000):
        if len(prompt) > n:
            prompt = [(prompt[i : i + n]) for i in range(0, len(prompt), n)]
        return prompt

