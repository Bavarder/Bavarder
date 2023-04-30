from .huggingface import BaseHFProvider

class HuggingFaceGoogleFlanU12Provider(BaseHFProvider):
    name = "Google Flan U12"
    slug = "hfgoogleflanu12"
    model = "google/flan-ul2"
    authorization = False