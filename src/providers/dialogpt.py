from .hfbasechat import BaseHFChatProvider

class DialoGPTProvider(BaseHFChatProvider):
    name = "DialoGPT"
    description = "A State-of-the-Art Large-scale Pretrained Response generation model"
    provider = "microsoft/DialoGPT-large"
