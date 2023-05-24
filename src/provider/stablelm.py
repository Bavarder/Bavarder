from .gradio import BaseGradioProvider

class StableLMProvider(BaseGradioProvider):
    name = "StableLM"
    slug = "stablelm"
    url = "https://stabilityai-stablelm-tuned-alpha-chat.hf.space/"