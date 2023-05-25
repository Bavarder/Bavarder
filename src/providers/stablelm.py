from .huggingface import BaseHFProvider

class StableLMProvider(BaseHFProvider):
    name = "StableLM"
    slug = "stablelm"
    model = "stabilityai/stablelm-tuned-alpha-3b"