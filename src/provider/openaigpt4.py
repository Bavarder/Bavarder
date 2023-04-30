from .openai import BaseOpenAIProvider

class OpenAIGPT4Provider(BaseOpenAIProvider):
    name = "OpenAI GPT 4"
    slug = "openaigpt4"
    model = "gpt-4"