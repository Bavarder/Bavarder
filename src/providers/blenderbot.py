from .hfbasechat import BaseHFChatProvider

class BlenderBotProvider(BaseHFChatProvider):
    name = "BlenderBot"
    description = "An open domain chatbot"
    provider = "facebook/blenderbot-400M-distill"

