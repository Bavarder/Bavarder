from .huggingface import BaseHFProvider

class HuggingFaceGoogleFlanT5XXLProvider(BaseHFProvider):
    name = "Google Flan T5 XXL"
    slug = "hfgoogleflant5xxl"
    model = "google/flan-t5-xxl"
    authorization = False