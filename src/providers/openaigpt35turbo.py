from .openai import BaseOpenAIProvider


class OpenAIGPT35TurboProvider(BaseOpenAIProvider):
    name = "OpenAI GPT 3.5 Turbo"
    slug = "openaigpt35turbo"
    model = "gpt-3.5-turbo"
