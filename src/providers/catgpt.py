from random import choice, randint

from .base import BaseProvider

class CatGPTProvider(BaseProvider):
    name = "Cat GPT"
    description = _("Chit-Chat with a Cat")

    def ask(self, prompt, _):
        return " ".join([self.pick_generator()() for i in range(randint(1, 12))])

    def pick_generator(self):
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
