from .blenderbot import BlenderBotProvider
from .catgpt import CatGPTProvider
from .dialogpt import DialoGPTProvider

PROVIDERS = {
    BlenderBotProvider,
    CatGPTProvider,
    DialoGPTProvider
}