from __future__ import annotations

def get_key(key: str):
    raise RuntimeError(
        "vault.get_key is deprecated. Use core.config.get_config_value instead."
    )
