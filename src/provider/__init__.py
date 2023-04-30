from .huggingchat import HuggingChatProvider
from .baichat import BAIChatProvider
from .openaigpt35turbo import OpenAIGPT35TurboProvider
from .openaigpt4 import OpenAIGPT4Provider
from .catgpt import CatGPTProvider
from .openaitextdavinci003 import OpenAITextDavinci003
from .alpacalora import AlpacaLoRAProvider
from .hfgoogleflant5xxl import HuggingFaceGoogleFlanT5XXLProvider

PROVIDERS = {
    'alpacalora': AlpacaLoRAProvider,
    'baichat': BAIChatProvider,
    'catgpt': CatGPTProvider,
    'hfgoogleflant5xxl': HuggingFaceGoogleFlanT5XXLProvider,
    'huggingchat': HuggingChatProvider,
    'openaigpt35turbo': OpenAIGPT35TurboProvider,
    'openaigpt4': OpenAIGPT4Provider,
    'openaitextdavinci003': OpenAITextDavinci003,
}