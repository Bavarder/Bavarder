from .huggingface import BaseHFProvider


class HuggingFaceGPT2LargeProvider(BaseHFProvider):
    name = "GPT 2 Large"
    slug = "hfgpt2large"
    model = "gpt2-large"

    @property
    def require_api_key(self):
        return False
