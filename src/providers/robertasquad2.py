from .hfbasechat import BaseHFChatProvider

class RobertaSquad2Provider(BaseHFChatProvider):
    name = "Roberta Squad2"
    provider = "deepset/roberta-base-squad2"
    description = "A model for Question Answering on SQuAD2"

    def make_prompt(self, prompt, chat):
        context = ""
        for message in chat:
            if chat['role'] == self.app.user_name:
                context += f" {message['content']}"
        return {
            "question": prompt,
            "context": context
        }