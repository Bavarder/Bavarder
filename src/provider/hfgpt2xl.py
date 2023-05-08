from .huggingface import BaseHFProvider


class HuggingFaceGPT2XLProvider(BaseHFProvider):
    name = "GPT 2 XL"
    slug = "hfgpt2"
    model = "gpt2-xl"
    description = "GPT-2 is a transformers model pretrained on a very large corpus of English data in a self-supervised fashion. This means it was pretrained on the raw texts only, with no humans labelling them in any way (which is why it can use lots of publicly available data) with an automatic process to generate inputs and labels from those texts. More precisely, it was trained to guess the next word in sentences."
    languages = "English"

    @property
    def require_api_key(self):
        return False
