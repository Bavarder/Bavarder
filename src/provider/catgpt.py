from .base import BavarderProvider

from random import choice, randint

from gi.repository import Gtk, Adw, GLib


class CatGPTProvider(BavarderProvider):
    name = _("Cat GPT")
    slug = "catgpt"
    description = "🐱️"
    version = "0.1.0"

    def __init__(self, win, app, *args, **kwargs):
        super().__init__(win, app, *args, **kwargs)
        self.chat = None

    def ask(self, prompt):
        return " ".join([self.pick_generator()() for i in range(randint(1, 12))])

    def pick_generator(self):
        if randint(1, 15) == 1:
            return choice(
                [
                    lambda: "ня" * randint(1, 4),
                    lambda: "ニャン" * randint(1, 4),
                    lambda: "喵" * randint(1, 4),
                    lambda: "ña" * randint(1, 4),
                    lambda: "ڽا" * randint(1, 4),
                    lambda: "ম্যাও" * randint(1, 4),
                ]
            )

        return choice(
            [
                lambda: "meow" * randint(1, 3),
                lambda: "mew" * randint(1, 3),
                lambda: "miau" * randint(1, 3),
                lambda: "miaou" * randint(1, 3),
                lambda: "miao" * randint(1, 3),
                lambda: "nya" * randint(1, 3),
                lambda: "m" + "r" * randint(1, 6) + "p",
                lambda: "pur" + "r" * randint(1, 6),
                lambda: "nya" * randint(1, 3) + "ny" + "a" * randint(1, 10),
            ]
        )

    @property
    def require_api_key(self):
        return False

    def save(self):
        return {}

    def load(self, data):
        pass
