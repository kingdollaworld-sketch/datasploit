from __future__ import annotations

try:
    from core import TargetType, get_runner
except ModuleNotFoundError:  # Imported via the datasploit package
    from .core import TargetType, get_runner

CATEGORY_MAP = {
    "domain": TargetType.DOMAIN,
    "email": TargetType.EMAIL,
    "ip": TargetType.IP,
    "username": TargetType.USERNAME,
}


def run(component: str, module_dir: str, m_input: str, output=None):
    """Backward compatible entry point for legacy scripts."""
    target_type = CATEGORY_MAP.get(component)
    if target_type is None:
        raise ValueError(f"Unsupported component '{component}'.")

    runner = get_runner()
    runner.run(target_type, m_input, output)
