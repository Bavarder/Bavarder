from .basehfimage import BaseHFImageProvider

class StableDiffusionProvider(BaseHFImageProvider):
    name = "Stable Diffusion"
    provider = "stabilityai/stable-diffusion-2-1"
    description = "Stable Diffusion is a model that can generate images from a prompt."