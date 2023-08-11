from .openai import BaseOpenAIProvider


class OpenAIGPT4Provider(BaseOpenAIProvider):
    name = "OpenAI GPT 4"
    model = "gpt-4"
    description = "More capable than any GPT-3.5 model, able to do more complex tasks, and optimized for chat."
    api_key_title = "API Key (Require a plan with access to the GPT-4 model)"
