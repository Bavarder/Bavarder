from .basehfimage import BaseHFImageProvider

class OpenJourneyProvider(BaseHFImageProvider):
    name = "Open Journey"
    provider = "prompthero/openjourney-v4"
    description = "Open Journey is a model that can generate images from a prompt."