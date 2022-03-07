"""
load production settings with optional dev and test settings
"""

from config.settings.prod import *

try:
    from config.settings.dev import *

    if os.environ.get("TEST_ENV"):
        from config.settings.test import *
except (ImportError,):
    pass
