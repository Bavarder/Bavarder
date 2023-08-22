from .blenderbot import BlenderBotProvider
from .catgpt import CatGPTProvider
from .dialogpt import DialoGPTProvider
from .stablebeluga2 import StableBeluga2Provider
from .openaigpt35turbo import OpenAIGPT35TurboProvider
from .googleflant5xxl import GoogleFlant5XXLProvider
from .openaigpt4 import OpenAIGPT4Provider
from .gpt2 import GPT2Provider
from .openassistantsft1pythia12b import HuggingFaceOpenAssistantSFT1PythiaProvider
from .robertasquad2 import RobertaSquad2Provider
from .local import LocalProvider
from .aihorde import AIHordeProvider

PROVIDERS = {
    AIHordeProvider,
    BlenderBotProvider,
    CatGPTProvider,
    DialoGPTProvider,
    OpenAIGPT35TurboProvider,
    OpenAIGPT4Provider,
    GoogleFlant5XXLProvider,
    GPT2Provider,
    LocalProvider
    # StableBeluga2Provider,
    # HuggingFaceOpenAssistantSFT1PythiaProvider,
    # RobertaSquad2Provider
}