from gi.repository import Adw, Gtk, Gio

from bavarder.constants import app_id, build_type

MAX_WIDTH = 400

@Gtk.Template(resource_path="/io/github/Bavarder/Bavarder/ui/message_bubble.ui")
class MessageBubble(Gtk.Box):
    __gtype_name__ = "MessageBubble"

    sender_label = Gtk.Template.Child()
    message_reply_bin = Gtk.Template.Child()
    prefix_bin = Gtk.Template.Child()
    message_label = Gtk.Template.Child()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = Gtk.Application.get_default()


    # def measure(self, orientation, , for_size):
    #     # Limit the widget width
    #     if orientation == Gtk.Orientation.HORIZONTAL:
    #         minimum, natural, minimum_baseline, natural_baseline = \
    #             self.overlay.measure(orientation, for_size)

    #         return (
    #             minimum.min(MAX_WIDTH),
    #             natural.min(MAX_WIDTH),
    #             minimum_baseline,
    #             natural_baseline,
    #         )
    #     else:
    #         adjusted_for_size = for_size.min(MAX_WIDTH);
    #         self.overlay.measure(orientation, adjusted_for_size)
    #     
    # 

    # def size_allocate(self, width, height, baseline):
    #     self.overlay.allocate(width, height, baseline, None)
    # 

    # def request_mode(self):
    #     return Gtk.SizeRequestMode.HEIGHT_FOR_WIDTH

    def set_label(self, label):
        if label.is_empty():
            self.message_label.set_label("")
            self..message_label.set_visible(false)

            self.remove_css_class("with-label")
        else:
            self.message_label.set_label(label)
            self.message_label.set_visible(true)

            self.add_css_class("with-label")
    