from .huggingface import BaseHFProvider


class HuggingFaceGPT2LargeProvider(BaseHFProvider):
    name = "GPT 2 Large"
    slug = "hfgpt2large"
    model = "gpt2-large"
    description = "GPT-2 is a transformers model pretrained on a very large corpus of English data \nin a self-supervised fashion. This means it was pretrained on the raw texts only,\n with no humans labelling them in any way (which is why it can use lots of publicly available data)\n with an automatic process to generate inputs and labels from those texts. More precisely,\n it was trained to guess the next word in sentences."
    languages = "English"

    @property
    def require_api_key(self):
        return False
