"""Domain collectors for DataSploit."""

from importlib import import_module
import pkgutil
from pathlib import Path

__all__ = []

_PACKAGE_PATH = Path(__file__).resolve().parent

for module_info in pkgutil.iter_modules([str(_PACKAGE_PATH)]):
    if module_info.ispkg:
        continue

    module_name = module_info.name
    if module_name.startswith(("_", "template")):
        continue

    module = import_module(f"{__name__}.{module_name}")
    globals()[module_name] = module
    __all__.append(module_name)
