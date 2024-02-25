from .basehfimage import BaseHFImageProvider

class StableDiffusionProvider(BaseHFImageProvider):
    name = "Stable Diffusion"
    provider = "stabilityai/stable-diffusion-2-1"