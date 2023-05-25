from .huggingchatbase import BaseHuggingChatProvider


class HuggingChatProvider(BaseHuggingChatProvider):
    name = "Hugging Chat"
    slug = "huggingchat"
    model = "OpenAssistant/oasst-sft-6-llama-30b-xor"
