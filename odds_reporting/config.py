import json
from pathlib import Path

from pkg_resources import resource_stream

PACKAGE_DIR = Path(__file__).parent.parent.absolute()

__config = None
with resource_stream("odds_reporting", ".authorized-config.json") as config_file:
    __config = json.load(config_file)

# ENV = (__config.get("env") or "dev").lower()
CONFIG = __config
