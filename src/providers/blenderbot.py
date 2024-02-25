from .hfbasechat import BaseHFChatProvider, ProviderType

class BlenderBotProvider(BaseHFChatProvider):
    name = "BlenderBot"
    description = "An open domain chatbot"
    provider = "facebook/blenderbot-400M-distill"
    provider_type = ProviderType.TEXT