from gi.repository import Gtk, Adw, Gio, GLib, Pango, GtkSource

import re

from bavarder.constants import app_id, rootdir
from bavarder.widgets.code_block import CodeBlock


H1="H1"
H2="H2"
H3="H3"
UL="BULLET"
OL="LIST"
CODE="CODE"
BOLD="BOLD"
EMPH="EMPH"
PRE="PRE"
LINK="LINK"
m2p_sections = [
    { "name": H1, "re": re.compile(r"^(#\s+)(.*)(\s*)$"), "sub": r"<big><big><big>\2</big></big></big>" },
    { "name": H2, "re": re.compile(r"^(##\s+)(.*)(\s*)$"), "sub": r"<big><big>\2</big></big>" },
    { "name": H3, "re": re.compile(r"^(###\s+)(.*)(\s*)$"), "sub": r"<big>\2</big>" },
    { "name": UL, "re": re.compile(r"^(\s*[\*\-]\s)(.*)(\s*)$"), "sub": r" • \2" },
    { "name": OL, "re": re.compile(r"^(\s*[0-9]+\.\s)(.*)(\s*)$"), "sub": r" \1\2" },
    { "name": CODE, "re": re.compile(r"^```[a-z_]*$"), "sub": "<tt>" },
]

m2p_styles = [
    { "name": BOLD, "re": re.compile(r"(^|[^\*])(\*\*)(.*)(\*\*)"), "sub": r"\1<b>\3</b>" },
    { "name": BOLD, "re": re.compile(r"(\*\*)(.*)(\*\*)([^\*]|$)"), "sub": r"<b>\3</b>\4" },
    { "name": EMPH, "re": re.compile(r"(^|[^\*])(\*)(.*)(\*)"), "sub": r"\1<i>\3</i>" },
    { "name": EMPH, "re": re.compile(r"(\*)(.*)(\*)([^\*]|$)"), "sub": r"<i>\3</i>\4" }, 
    { "name": PRE, "re": re.compile(r"(`)([^`]*)(`)"), "sub": r"<tt>\2</tt>" },
    { "name": LINK, "re": re.compile(r"(!)?(\[)(.*)(\]\()(.+)(\))"), "sub": r"<a href='\5'>\3</a>" },
    { "name": LINK, "re": re.compile(r"(!)?(\[)(.*)(\]\(\))"), "sub": r"<a href='\3'>\3</a>" },
]

re_comment = re.compile(r"^\s*<!--.*-->\s*$")
re_color = re.compile(r"^(\s*<!--\s*(fg|bg)=(#?[0-9a-z_A-Z-]*)\s*((fg|bg)=(#?[0-9a-z_A-Z-]*))?\s*-->\s*)$")
re_reset = re.compile(r"(<!--\/-->)")
re_uri = re.compile(r"http[s]?:\/\/[^\s']*")
re_href = re.compile(r"href='(http[s]?:\\/\\/[^\\s]*)'")
re_atag = re.compile(r"<a\s.*>.*(http[s]?:\\/\\/[^\\s]*).*</a>")
re_h1line = re.compile(r"^===+\s*$")
re_h2line = re.compile(r"^---+\s*$")

m2p_escapes = [
    [re.compile(r"<!--.*-->"), ''],
    [re.compile(r"&"), '&amp;'],
    [re.compile(r"<"), '&lt;'],
    [re.compile(r">"), '&gt;'],
]


@Gtk.Template(resource_path=f"{rootdir}/ui/item.ui")
class Item(Gtk.Box):
    __gtype_name__ = "Item"

    user = Gtk.Template.Child()
    content = Gtk.Template.Child()
    timestamp = Gtk.Template.Child()
    popover = Gtk.Template.Child()
    avatar = Gtk.Template.Child()
    message_bubble = Gtk.Template.Child()
    model = Gtk.Template.Child()

    def __init__(self, parent, chat, item, **kwargs):
        super().__init__(**kwargs)

        self.chat = chat
        self.item = item

        self.content_text = self.item["content"]

        self.convert_content_to_pango()

        result = ""
        for line in self.content_markup:
            if isinstance(line, str): 
                result += f"{line}\n"
            else: # code
                label = Gtk.Label()
                label.set_use_markup(True)
                label.set_wrap(True)
                label.set_xalign(0)
                label.set_wrap_mode(Pango.WrapMode.WORD)
                label.set_markup(result)
                label.set_justify(Gtk.Justification.LEFT)
                label.set_valign(Gtk.Align.START)
                label.set_hexpand(True)
                label.set_halign(Gtk.Align.START)
                self.content.append(label)

                result = "\n".join(line)

                self.content.append(CodeBlock(result))
                result = ""
        else:
            if not result.strip() == "<tt></tt>`":
                label = Gtk.Label()
                label.set_use_markup(True)
                label.set_wrap(True)
                label.set_xalign(0)
                label.set_wrap_mode(Pango.WrapMode.WORD)
                label.set_markup(result)
                label.set_justify(Gtk.Justification.LEFT)
                label.set_valign(Gtk.Align.START)
                label.set_hexpand(True)
                label.set_halign(Gtk.Align.START)
                self.content.append(label)

        t = self.item["role"].capitalize()

        if t == "User":
            self.message_bubble.add_css_class("message-bubble-user")
            self.avatar.add_css_class("avatar-user")
            role = _("User")
        elif t == "Assistant":
            self.avatar.set_icon_name("bot-symbolic")
            self.user.add_css_class("warning")
            role = _("Assistant")
        else:
            role = t

        self.timestamp.set_text(self.item.get("time", ""))
        self.model.set_text(self.item.get("model", ""))

        self.avatar.set_text(role)
        self.user.set_text(role)

        self.parent = parent
        self.settings = parent.settings

        self.app = self.parent.get_application()
        self.win = self.app.get_active_window()

        self.setup()

    def setup(self):
        self.setup_signals()

        evk = Gtk.GestureClick.new()
        evk.connect("pressed", self.show_menu)
        evk.set_button(3)
        self.add_controller(evk)

    def show_menu(self, gesture, data, x, y):
        self.popover.set_parent(self)
        self.popover.popup()

    def setup_signals(self):
        self.action_group = Gio.SimpleActionGroup()
        self.create_action("delete", self.on_delete)
        self.create_action("edit", self.on_edit)
        self.insert_action_group("event", self.action_group);

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.action_group.add_action(action)

        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def on_delete(self, *args, **kwargs):
        self.chat["content"].remove(self.item)
        self.win.threads_row_activated_cb()

    def on_edit(self, *args):
        self.win.message_entry.get_buffer().set_text(self.item["content"])

    def convert_content_to_pango(self):
        lines = self.content_text.split("\n")

        is_code = False
        code_lines = []

        output = []
        self.color_span_open = False
        tt_must_close = False

        def try_close_span():
            if self.color_span_open:
                output.append('</span>')
                self.color_span_open = False
            
        def try_open_span():
            if not self.color_span_open:
                output.append('</span>')
                self.color_span_open = False

        def escape_line(line):
            for escape in m2p_escapes:
                line = re.sub(escape[0], escape[1], line)
            return line

        # def pad(lines, start=1, end=1):
        #     length = 0
        #     for line in lines:
        #         if len(line) > 0:
        #             length += len(line)
        #         else:
        #             length += 0
        #     for line in lines:
        #         line.rjust()
        #     return lines.map((l) => l.padEnd(len + end, ' ').padStart(len + end + start, ' '))


        for line in lines:
            if not is_code:
                colors = re_color.match(line)
                if colors or re_reset.match(line):
                    try_close_span()
                

                if colors:
                    try_close_span()
                    if self.color_span_open:
                        try_close_span()

                    if colors[2] == 'fg':
                        fg = colors[3]
                    elif colors[5] == 'fg':
                        fg = colors[6]
                    else:
                        fg = ""
                    
                    if colors[2] == 'bg':
                        fg = colors[3]
                    elif colors[5] == 'bg':
                        fg = colors[6]
                    else:
                        fg = ""
                    
                    attrs = ''

                    if fg != '':
                        attrs += f" foreground='{fg}'"
                    

                    if bg != '':
                        attrs += f" background='{bg}'"

                    if attrs != '':
                        output.append("<span {attrs}>")
                        self.color_span_open = True
            
            if re_comment.match(line):
                continue

            code_start = False

            if is_code:
                result = line
            else:
                result = escape_line(line)

            for exp in m2p_sections:
                name = exp["name"]
                regexp = exp["re"]
                sub = exp["sub"]
                if regexp.match(line):
                    if name == CODE:
                        if not is_code:
                            code_start = True
                            is_code = True

                            result = ""

                            #if self.color_span_open:
                            #    result = '<tt>'
                            #    tt_must_close = False
                            #else:
                            #    result = "<span foreground='#bbb' background='#222'>" + '<tt>'
                            #    tt_must_close = True
                        else:
                            is_code = False
                            #output.append(...pad(code_lines).map(escape_line))
                            output.append(code_lines)
                            code_lines = []
                            #result = '</tt>'
                            if tt_must_close:
                                result += '</span>'
                                tt_must_close = False
                    else:
                        if is_code:
                            result = line
                        else:
                            result = re.sub(regexp, sub, line)

            if is_code and not code_start:
                code_lines.append(result)
                continue
            

            if re_h1line.match(line):
                output.append(re.sub(m2p_sections[0]["re"], m2p_sections[0]["sub"], f"# {output.pop()}"))
                continue
            

            if re_h2line.match(line):
                output.append(re.sub(m2p_sections[1]["re"], m2p_sections[1]["sub"], f"# {output.pop()}"))
                continue
            
            for style in m2p_styles:
                regexp = style["re"]
                sub = style["sub"]
                result = re.sub(regexp, sub, result)
            

            uri = re_uri.match(result)     # look for any URI
            href = re_href.match(result)   # and for URIs in href=''
            atag = re_atag.match(result)   # and for URIs in <a></a>

            if uri and (href or atag):
                result = result.replace(uri, f"<a href='{uri}'>{uri}</a>")

            output.append(result)

        try_close_span()

        self.content_markup = output