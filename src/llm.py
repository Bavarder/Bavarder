import litert_lm
import os
import threading
from gi.repository import GLib

from bavarder.constants import app_id, rootdir


class LLM:
    def __init__(self, app):
        self.app = app
        self.model = None
        self.engine = None

    def get_data(self):
        return self.app.data.get("models", {})

    def get_model_path(self):
        model_name = self.app.model_name
        if model_name:
            model_file = os.path.join(self.app.user_cache_dir, "bavarder", "models", model_name)
            if os.path.exists(model_file):
                return model_file

        data = self.get_data()
        model_path = data.get("model_path", "")
        if model_path and os.path.exists(model_path):
            return model_path

        models_dir = os.path.join(self.app.user_cache_dir, "bavarder", "models")
        if os.path.exists(models_dir):
            for f in os.listdir(models_dir):
                if f.endswith(".litertlm"):
                    return os.path.join(models_dir, f)

    def load_model(self):
        model_path = self.get_model_path()
        if not model_path:
            raise ValueError(_("No model available. Please download a model or set a model path."))

        if self.engine is not None and self.current_model_path == model_path:
            return

        self.engine = None
        self.current_model_path = model_path
        self.engine = litert_lm.Engine(model_path, backend=litert_lm.Backend.CPU)

    def ask(self, prompt, chat, callback, error_callback):
        def thread_run():
            try:
                self.load_model()

                messages = []

                system_prompt = chat.get("system_prompt", "")
                if system_prompt:
                    messages.append({
                        "role": "system",
                        "content": [{"type": "text", "text": system_prompt}]
                    })

                for msg in chat.get("content", []):
                    role = msg.get("role", "user")
                    if role == self.app.user_name:
                        role = "user"
                    elif role == self.app.bot_name:
                        role = "assistant"
                    else:
                        role = "user"
                    content = msg.get("content", "")
                    messages.append({
                        "role": role,
                        "content": [{"type": "text", "text": content}]
                    })

                settings = self.app.model_settings
                extra_context = {
                    "max_tokens": settings.get("max_tokens", 200),
                    "temperature": settings.get("temperature", 0.7),
                    "top_p": settings.get("top_p", 0.9),
                    "top_k": settings.get("top_k", 40),
                }

                with self.engine.create_conversation(messages=messages, extra_context=extra_context) as conv:
                    stream = conv.send_message_async(prompt)
                    for chunk in stream:
                        for item in chunk.get("content", []):
                            if item.get("type") == "text":
                                GLib.idle_add(callback, item["text"])
                GLib.idle_add(callback, None)
            except Exception as e:
                GLib.idle_add(error_callback, str(e))

        t = threading.Thread(target=thread_run)
        t.start()
