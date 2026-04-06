import litert_lm
import os
import threading
from gi.repository import GLib


class LLM:
    def __init__(self, app):
        self.app = app
        self.model = None
        self.engine = None

    def get_data(self):
        return self.app.data.get("models", {})

    def get_model_path(self):
        data = self.get_data()
        
        model_path = data.get("model_path", "")
        if model_path and os.path.exists(model_path):
            return model_path

        models_dir = os.path.join(self.app.user_cache_dir, "bavarder", "models")
        if os.path.exists(models_dir):
            for f in os.listdir(models_dir):
                if f.endswith(".litertlm"):
                    return os.path.join(models_dir, f)

        hf_model = data.get("hf_model", "")
        if hf_model:
            try:
                from huggingface_hub import hf_hub_download
                from huggingface_hub import list_repo_files
                files = list_repo_files(hf_model, repo_type="model")
                litertlm_files = [f for f in files if f.endswith('.litertlm')]
                if litertlm_files:
                    return hf_hub_download(
                        repo_id=hf_model,
                        filename=litertlm_files[0],
                        cache_dir=self.app.user_cache_dir
                    )
            except Exception:
                pass

        return None

    def load_model(self):
        if self.engine is not None:
            return

        model_path = self.get_model_path()
        if not model_path:
            raise ValueError("No model available. Please download a model or set a model path.")

        self.engine = litert_lm.Engine(model_path, backend=litert_lm.Backend.CPU)

    def ask(self, prompt, chat, callback, error_callback):
        def thread_run():
            try:
                self.load_model()

                messages = []
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

                with self.engine.create_conversation(messages=messages) as conv:
                    response = conv.send_message(prompt)
                    GLib.idle_add(callback, response["content"][0]["text"])
            except Exception as e:
                GLib.idle_add(error_callback, str(e))

        t = threading.Thread(target=thread_run)
        t.start()

    def ask_async(self, prompt, chat, callback, error_callback):
        def thread_run():
            try:
                self.load_model()

                messages = []
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

                with self.engine.create_conversation(messages=messages) as conv:
                    stream = conv.send_message_async(prompt)
                    for chunk in stream:
                        for item in chunk.get("content", []):
                            if item.get("type") == "text":
                                GLib.idle_add(callback, item["text"])
            except Exception as e:
                GLib.idle_add(error_callback, str(e))

        t = threading.Thread(target=thread_run)
        t.start()
