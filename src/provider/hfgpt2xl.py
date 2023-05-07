from .huggingface import BaseHFProvider


class HuggingFaceGPT2XLProvider(BaseHFProvider):
    name = "GPT 2 XL"
    slug = "hfgpt2"
    model = "gpt2-xl"

    @property
    def require_api_key(self):
        return False
