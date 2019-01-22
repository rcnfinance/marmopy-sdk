from .intent import Intent, IntentGeneric, SignedIntent
from .intent_action import IntentAction
from .wallet import Wallet
from .conf import DefaultConf, Conf, global_conf
from .provider import Provider, global_provider
import warnings

# Disable deprecation warnings
og_warn = warnings.warn
def warn(*args, **kwargs):
    if not isinstance(args[0], DeprecationWarning) and not kwargs["category"] == DeprecationWarning:
        og_warn(*args, **kwargs)

warnings.warn = warn
