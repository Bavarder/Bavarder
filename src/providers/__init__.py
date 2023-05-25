# from .huggingchat import HuggingChatProvider
from .baichat import BAIChatProvider
from .openaigpt35turbo import OpenAIGPT35TurboProvider
from .openaigpt4 import OpenAIGPT4Provider
from .openaicustom import OpenAICustomProvider, LocalModel
from .catgpt import CatGPTProvider
from .openaitextdavinci003 import OpenAITextDavinci003
from .alpacalora import AlpacaLoRAProvider
from .hfgoogleflant5xxl import HuggingFaceGoogleFlanT5XXLProvider
from .hfgoogleflanu12 import HuggingFaceGoogleFlanU12Provider
from .hfopenassistantsft1pythia12b import HuggingFaceOpenAssistantSFT1PythiaProvider, HuggingChatMask
from .hfgpt2 import HuggingFaceGPT2Provider
from .hfdialogpt import HuggingFaceDialoGPTLargeProvider
# from .bard import BardProvider
from .hfgpt2large import HuggingFaceGPT2LargeProvider
from .hfgpt2xl import HuggingFaceGPT2XLProvider
from .stablelm import StableLMProvider
from .starcoder import StarCoderProvider

PROVIDERS = {
    "alpacalora": AlpacaLoRAProvider,
    "baichat": BAIChatProvider,
    # "bard": BardProvider, # Disabled because we need more documentation on how to use it
    "catgpt": CatGPTProvider,
    "hfdialogpt": HuggingFaceDialoGPTLargeProvider,
    "hfgoogleflant5xxl": HuggingFaceGoogleFlanT5XXLProvider,
    "hfgoogleflanu12": HuggingFaceGoogleFlanU12Provider,
    "hfgpt2": HuggingFaceGPT2Provider,
    "hfgpt2large": HuggingFaceGPT2LargeProvider,
    "hfgpt2xl": HuggingFaceGPT2XLProvider,
    "hfopenassistantsft1pythia12b": HuggingFaceOpenAssistantSFT1PythiaProvider,
    "huggingchat": HuggingChatMask, # hugging chat is replaced by open assistant
    "local": LocalModel,
    "openaicustom": OpenAICustomProvider,
    "openaigpt35turbo": OpenAIGPT35TurboProvider,
    "openaigpt4": OpenAIGPT4Provider,
    "openaitextdavinci003": OpenAITextDavinci003,
    "stablelm": StableLMProvider,
    "starcoder": StarCoderProvider,
}
