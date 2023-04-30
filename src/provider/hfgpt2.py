from .huggingface import BaseHFProvider

class HuggingFaceGPT2Provider(BaseHFProvider):
    name = "GPT 2"
    slug = "gpt2"
    model = "gpt2"
    authorization = False