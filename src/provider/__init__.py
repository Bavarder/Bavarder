from .huggingchat import HuggingChatProvider
from .baichat import BAIChatProvider
from .openaigpt35turbo import OpenAIGPT35TurboProvider
from .openaigpt4 import OpenAIGPT4Provider
from .catgpt import CatGPTProvider
from .openaitextdavinci003 import OpenAITextDavinci003
from .alpacalora import AlpacaLoRAProvider
from .hfgoogleflant5xxl import HuggingFaceGoogleFlanT5XXLProvider
from .hfgoogleflanu12 import HuggingFaceGoogleFlanU12Provider
from .hfopenassistantsft1pythia12b import HuggingFaceOpenAssistantSFT1PythiaProvider
from .hfgpt2 import HuggingFaceGPT2Provider
from .hfdialogpt import HuggingFaceDialoGPTLargeProvider
from .bard import BardProvider

PROVIDERS = {
    "alpacalora": AlpacaLoRAProvider,
    "baichat": BAIChatProvider,
    #"bard": BardProvider, # Disabled because we need more documentation on how to use it
    "catgpt": CatGPTProvider,
    "hfdialogpt": HuggingFaceDialoGPTLargeProvider,
    "hfgoogleflant5xxl": HuggingFaceGoogleFlanT5XXLProvider,
    "hfgoogleflanu12": HuggingFaceGoogleFlanU12Provider,
    "hfgpt2": HuggingFaceGPT2Provider,
    "hfopenassistantsft1pythia12b": HuggingFaceOpenAssistantSFT1PythiaProvider,
    "huggingchat": HuggingChatProvider,
    "openaigpt35turbo": OpenAIGPT35TurboProvider,
    "openaigpt4": OpenAIGPT4Provider,
    "openaitextdavinci003": OpenAITextDavinci003,
}
