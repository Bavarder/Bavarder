from .base import BaseProvider, ProviderType

import requests

from gi.repository import Gtk, Adw, GLib


class BaseImageProvider(BaseProvider):
    provider_type = ProviderType.IMAGE
    