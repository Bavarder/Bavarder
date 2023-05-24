from .transformer import BaseTransformerProvider


class StarCoderProvider(BaseTransformerProvider):
    name = "Star Coder"
    slug = "starcoder"
    checkpoint = "bigcode/starcoder"
