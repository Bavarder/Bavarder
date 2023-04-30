from .huggingface import BaseHFProvider

class HuggingFaceOpenAssistantSFT1PythiaProvider(BaseHFProvider):
    name = "Open-Assistant SFT-1 12B Model "
    slug = "hfopenassistantsft1pythia12b"
    model = "OpenAssistant/oasst-sft-1-pythia-12b"
    authorization = False