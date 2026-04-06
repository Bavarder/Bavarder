import litert_lm
from .base import BaseProvider, ProviderType
from gi.repository import Gtk, Adw, GLib
from huggingface_hub import hf_hub_download
import os
import threading


class LiteRTLMProvider(BaseProvider):
    name = "LiteRT-LM"
    description = _("Run local LLMs using LiteRT-LM")
    provider_type = ProviderType.CHAT
    url = "https://ai.google.dev/edge/litert-lm"

    def __init__(self, app, window):
        super().__init__(app, window)
        self.model = None
        self.conversation = None

    def get_settings_rows(self):
        rows = []

        self.hf_model_row = Adw.EntryRow()
        self.hf_model_row.connect("apply", self.on_apply)
        self.hf_model_row.props.title = _("HuggingFace Model (e.g., litert-community/gemma-4-E2B-it-litert-lm)")
        if "hf_model" in self.data:
            self.hf_model_row.props.text = str(self.data["hf_model"])
        else:
            self.hf_model_row.props.text = ""
        self.hf_model_row.set_show_apply_button(True)
        rows.append(self.hf_model_row)

        self.download_button = Gtk.Button()
        self.download_button.set_label(_("Download Model"))
        self.download_button.connect("clicked", self.on_download_clicked)
        rows.append(self.download_button)

        self.model_path_row = Adw.EntryRow()
        self.model_path_row.connect("apply", self.on_apply)
        self.model_path_row.props.title = _("Model Path (or leave empty to use HF model)")
        if "model_path" in self.data:
            self.model_path_row.props.text = str(self.data["model_path"])
        else:
            self.model_path_row.props.text = ""
        self.model_path_row.set_show_apply_button(True)
        rows.append(self.model_path_row)

        return rows

    def on_apply(self, widget):
        hf_model = self.hf_model_row.get_text()
        model_path = self.model_path_row.get_text()
        self.data["hf_model"] = hf_model
        self.data["model_path"] = model_path
        self.model = None
        self.conversation = None

    def on_download_clicked(self, widget):
        def thread_run():
            try:
                hf_model = self.hf_model_row.get_text()
                if not hf_model:
                    GLib.idle_add(self.show_error, _("Please enter a HuggingFace model ID"))
                    return

                toast = Adw.Toast()
                toast.set_timeout(0)
                toast.set_title(_("Downloading model from HuggingFace..."))
                GLib.idle_add(self.window.add_toast, toast)

                model_file = hf_hub_download(
                    repo_id=hf_model,
                    filename="*.litertlm",
                    cache_dir=self.app.user_cache_dir
                )

                self.data["model_path"] = model_file
                GLib.idle_add(self.model_path_row.set_text, model_file)
                GLib.idle_add(toast.dismiss)

                toast = Adw.Toast()
                toast.set_title(_("Model downloaded successfully!"))
                GLib.idle_add(self.window.add_toast, toast)

            except Exception as e:
                GLib.idle_add(self.show_error, str(e))

        t = threading.Thread(target=thread_run)
        t.start()

    def show_error(self, message):
        toast = Adw.Toast()
        toast.set_title(message)
        self.window.add_toast(toast)

    def get_model_path(self):
        model_path = self.data.get("model_path", "")
        if model_path and os.path.exists(model_path):
            return model_path

        hf_model = self.data.get("hf_model", "")
        if hf_model:
            try:
                return hf_hub_download(
                    repo_id=hf_model,
                    filename="*.litertlm",
                    cache_dir=self.app.user_cache_dir
                )
            except Exception:
                pass

        return None

    def load_model(self):
        if self.model is not None:
            return

        model_path = self.get_model_path()
        if not model_path:
            raise ValueError("No model available. Please download a model or set a model path.")

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
