from .hfbasechat import BaseHFChatProvider, ProviderType

class GoogleFlant5XXLProvider(BaseHFChatProvider):
    name = "Google Flan T5 XXL"
    description = "A better Text-To-Text Transfer Transformer (T5) model"
    provider = "google/flan-t5-xxl"
    provider_type = ProviderType.TEXT
