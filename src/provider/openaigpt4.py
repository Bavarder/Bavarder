from .openai import BaseOpenAIProvider


class OpenAIGPT4Provider(BaseOpenAIProvider):
    name = "OpenAI GPT 4"
    slug = "openaigpt4"
    model = "gpt-4"
    api_key_title = "API Key (Require a plan with access to the GPT-4 model)"