from .basehfimage import BaseHFImageProvider

class AnalogDiffusionProvider(BaseHFImageProvider):
    name = "Analog Diffusion"
    provider = "wavymulder/Analog-Diffusion"
    description = "Analog Diffusion is a model that can generate images from a prompt."