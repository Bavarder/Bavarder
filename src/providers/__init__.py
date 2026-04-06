from .local import LocalProvider
from .litert_lm import LiteRTLMProvider

PROVIDERS = {
    LocalProvider,
    LiteRTLMProvider,
}
