from .huggingchat import HuggingChatProvider
from .baichat import BAIChatProvider

PROVIDERS = {
    'huggingchat': HuggingChatProvider,
    'baichat': BAIChatProvider,
}