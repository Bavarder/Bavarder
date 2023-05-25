from .huggingface import BaseHFProvider


class HuggingFaceGoogleFlanT5XXLProvider(BaseHFProvider):
    name = "Google Flan T5 XXL"
    slug = "hfgoogleflant5xxl"
    model = "google/flan-t5-xxl"

    @property
    def require_api_key(self):
        return False
