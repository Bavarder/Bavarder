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
from .stablediffusion import StableDiffusionProvider 
from .analogdiffusion import AnalogDiffusionProvider
from .nitrodiffusion import NitroDiffusionProvider
from .openjourney import OpenJourneyProvider
from .openaiimage import DallE2, DallE3
from .portraitplus import PortraitPlusProvider

PROVIDERS = {
    AIHordeProvider,
    BlenderBotProvider,
    CatGPTProvider,
    DialoGPTProvider,
    OpenAIGPT35TurboProvider,
    OpenAIGPT4Provider,
    GoogleFlant5XXLProvider,
    GPT2Provider,
    LocalProvider,
    StableDiffusionProvider,
    AnalogDiffusionProvider,
    NitroDiffusionProvider,
    OpenJourneyProvider,
    DallE2,
    DallE3,
    PortraitPlusProvider,
    # StableBeluga2Provider,
    # HuggingFaceOpenAssistantSFT1PythiaProvider,
    # RobertaSquad2Provider
}