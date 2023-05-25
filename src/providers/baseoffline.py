from .base import BavarderProvider

import requests
import shutil

class BaseOfflineProvider(BavarderProvider):
    data = {
        "setup": False,
        "weight_path": "",
    }
    download_url = ""

    def save(self):
        return data

    def load(self, data):
        self.data = data

    def download_file(self, url, filename=None):
        if not filename:
            filename = url.split('/')[-1]

        with requests.get(url, stream=True) as r:
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        return filename


    def setup(self):
        if self.data["setup"]:
            return
        else:
            self.data["setup"] = True
            self.data["weight_path"] = self.download_file(self.download_url)

    def ask(self, prompt):
        self.setup()
        return self._ask(prompt)

    def _ask(self, prompt):
        raise NotImplementedError()