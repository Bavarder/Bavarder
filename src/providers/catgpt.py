from random import choice, randint

from .base import BaseProvider

class CatGPTProvider(BaseProvider):
    name = "Cat GPT"
    description = _("Chit-Chat with a Cat")

    def ask(self, prompt, _):
        return """
# H1
## H2
### H3

Alternatively, for H1 , an underline-ish style:

Alt-H1
======


1. First ordered list item
2. Another item

* Unordered list can use asterisks
- Or minuses
+ Or pluses

```
$ ls
```
        """
        #return " ".join([self.pick_generator()() for i in range(randint(1, 12))])

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
