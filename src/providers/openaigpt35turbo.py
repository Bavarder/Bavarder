from .openai import BaseOpenAIProvider


class OpenAIGPT35TurboProvider(BaseOpenAIProvider):
    name = "OpenAI GPT 3.5 Turbo"
    description = "Most capable GPT-3.5 model and optimized for chat."
    model = "gpt-3.5-turbo"
