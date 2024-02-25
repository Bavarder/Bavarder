from .hfbasechat import BaseHFChatProvider

class HuggingFaceOpenAssistantSFT1PythiaProvider(BaseHFChatProvider):
    name = "Open-Assistant SFT-1 12B"
    provider = "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
    description = "OpenAssistant's SFT-1 Pythia 12B model"

    def make_prompt(self, prompt, chat):
        p = ""
        for i in range(0, len(chat)):
            if chat[i]['role'] == self.app.bot_name:
                p += f"<|assistant|>{chat[i]['content']}<|endoftext|>"
            else:
                p += f"<|prompter|>{chat[i]['content']}<|endoftext|>"
        p += f"<|prompter|> {prompt}<|endoftext|>"
        return p