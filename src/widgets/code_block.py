from gi.repository import Gtk, GtkSource, Adw, Xdp

from bavarder.constants import app_id, rootdir

import subprocess
from subprocess import SubprocessError, CompletedProcess
import os

GtkSource.init()

@Gtk.Template(resource_path=f"{rootdir}/ui/code_block.ui")
class CodeBlock(Gtk.Widget):
    __gtype_name__ = "CodeBlock"

    buffer = Gtk.Template.Child()
    source_view = Gtk.Template.Child()
    output_buffer = Gtk.Template.Child()
    output_source_view = Gtk.Template.Child()
    view = Gtk.Template.Child()
    box = Gtk.Template.Child()
    output = Gtk.Template.Child()

    def __init__(self, result, **kwargs):
        super().__init__(**kwargs)

        self.command = result

        self.buffer.set_text(self.command)

        if Adw.StyleManager().get_dark():
            self.buffer.set_style_scheme(GtkSource.StyleSchemeManager().get_scheme("Adwaita-dark"))
        else:
            self.buffer.set_style_scheme(GtkSource.StyleSchemeManager().get_scheme("Adwaita"))

        if Adw.StyleManager().get_dark():
            self.output_buffer.set_style_scheme(GtkSource.StyleSchemeManager().get_scheme("Adwaita-dark"))
        else:
            self.output_buffer.set_style_scheme(GtkSource.StyleSchemeManager().get_scheme("Adwaita"))
        

    @Gtk.Template.Callback()
    def run(self, widget, *args):
        command = self.buffer.props.text.split(" ")
        if self.command.startswith("$"):
            command.pop(0)

        portal = Xdp.Portal()
        is_sandboxed = portal.running_under_sandbox()
        output = self._run(command, allow_escaping=is_sandboxed)
        self.output_buffer.set_text(output)
        self.output.set_visible(True)

    def _run(self, command: list, timeout: int = None, allow_escaping: bool = False) -> CompletedProcess:
        if allow_escaping and os.environ.get('FLATPAK_ID'):
            command = ['flatpak-spawn', '--host'] + command

        try:
            process = subprocess.run(command, capture_output=True, text=True)
            if process.returncode != 0:
                output = process.stderr
            else:
                if process.stdout == "":
                    output = _("Done")
                else:
                    output = process.stdout
        except SubprocessError as e:
            output = e.stdout
        except FileNotFoundError:
            raise

        o = ""

        for line in output.split("\n"):
            if line == "":
                continue
            elif line.strip().startswith("** (flatpak-spawn:"):
                continue
            elif line.strip().startswith("(flatpak-spawn:"):
                continue
            else:
                if line.strip() == "":
                    o += _("Done") + "\n"
                else:
                    o += line + "\n"

        return o