import litert_lm
from .base import BaseProvider, ProviderType
from gi.repository import Gtk, Adw
import os


class LiteRTLMProvider(BaseProvider):
    name = "LiteRT-LM"
    description = _("Run local LLMs using LiteRT-LM")
    provider_type = ProviderType.CHAT

    def __init__(self, app, window):
        super().__init__(app, window)
        self.model = None
        self.conversation = None
        self.url = "https://ai.google.dev/edge/litert-lm"

    def get_settings_rows(self):
        rows = []

        self.model_path_row = Adw.EntryRow()
        self.model_path_row.connect("apply", self.on_apply)
        self.model_path_row.props.title = _("Model Path")
        self.model_path_row.props.subtitle = _(
            "Path to .litertlm model file"
        )
        if "model_path" in self.data:
            self.model_path_row.props.text = str(self.data["model_path"])
        else:
            self.model_path_row.props.text = ""
        self.model_path_row.set_show_apply_button(True)

        rows.append(self.model_path_row)

        return rows

    def on_apply(self, widget):
        model_path = self.model_path_row.get_text()
        self.data["model_path"] = model_path
        self.model = None

    def load_model(self):
        if self.model is not None:
            return

        model_path = self.data.get("model_path", "")
        if not model_path or not os.path.exists(model_path):
            raise ValueError("Model path not set or file does not exist")

        self.model = litert_lm.Engine(model_path, backend=litert_lm.Backend.CPU)

    def ask(self, prompt, chat):
        self.load_model()

        messages = []
        for msg in chat["content"]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            messages.append({
                "role": role,
                "content": [{"type": "text", "text": content}]
            })

        messages.append({
            "role": "user",
            "content": [{"type": "text", "text": prompt}]
        })

        with self.model.create_conversation(messages=messages) as conv:
            response = conv.send_message(prompt)
            return response["content"][0]["text"]
