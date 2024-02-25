from .basehfimage import BaseHFImageProvider

class NitroDiffusionProvider(BaseHFImageProvider):
    name = "Nitro Diffusion"
    provider = "nitrosocke/Nitro-Diffusion"
    description = "Nitro Diffusion is a model that can generate images from a prompt."