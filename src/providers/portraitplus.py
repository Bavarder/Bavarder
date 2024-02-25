from .basehfimage import BaseHFImageProvider

class PortraitPlusProvider(BaseHFImageProvider):
    name = "Portrait Plus"
    model = "wavymulder/portraitplus"
    description = "Portrait Plus is a model that can generate images from a prompt."