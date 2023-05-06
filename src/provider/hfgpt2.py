from .huggingface import BaseHFProvider


class HuggingFaceGPT2Provider(BaseHFProvider):
    name = "GPT 2"
    slug = "gpt2"
    model = "gpt2"

    @property
    def require_api_key(self):
        return False