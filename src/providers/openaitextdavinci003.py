from .openai import BaseOpenAIProvider


class OpenAITextDavinci003(BaseOpenAIProvider):
    name = "OpenAI Text Davinci 003"
    slug = "openaitextdavinci003"
    model = "text-davinci-003"
