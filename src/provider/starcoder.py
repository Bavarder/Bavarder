from .huggingchatbase import BaseHuggingChatProvider


class StarCoderProvider(BaseHuggingChatProvider):
    name = "Star Coder"
    slug = "starcoder"
    model = "bigcode/starcoder"
