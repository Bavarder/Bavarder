from .hfbasechat import BaseHFChatProvider

class GPT2Provider(BaseHFChatProvider):
    name = "GPT 2"
    description = "GPT-2 is a transformers model pretrained on a very large corpus of English data in a self-supervised fashion"
    provider = "gpt2"
    chat_mode = False
