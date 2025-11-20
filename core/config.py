from __future__ import annotations

from configobj import ConfigObj
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable


CONFIG_DIR = Path(__file__).resolve().parent.parent
CONFIG_CANDIDATES: Iterable[Path] = (
    CONFIG_DIR / "config.ini",
    CONFIG_DIR / "config.py",
)


@lru_cache(maxsize=1)
def load_config() -> Dict[str, str]:
    """Load the user configuration once and cache the result."""
    for config_path in CONFIG_CANDIDATES:
        if not config_path.exists():
            continue

        config = ConfigObj(str(config_path))
        # ConfigObj returns a ConfigObj instance with string keys and values.
        # Normalise to a simple dictionary to avoid leaking ConfigObj specific
        # behaviour into the rest of the code base.
        return {key: value for key, value in config.items()}

    return {}


def get_config_value(key: str) -> str | None:
    """Fetch a value from the cached configuration, if available."""
    return load_config().get(key)
