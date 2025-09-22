from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional
from types import ModuleType

from termcolor import colored

from .config import get_config_value
from .style import style

@dataclass
class CollectorModule:
    key: str
    category: str
    module: ModuleType
    name: str
    enabled: bool
    requires: tuple[str, ...]
    description: str
    writes_text: bool

    @classmethod
    def from_module(cls, key: str, category: str, module: ModuleType) -> "CollectorModule":
        if not hasattr(module, "MODULE_NAME") or not hasattr(module, "REQUIRES"):
            raise AttributeError(
                f"Collector {module.__name__} must define MODULE_NAME and REQUIRES"
            )

        raw_name = getattr(module, "MODULE_NAME")
        requires_attr = getattr(module, "REQUIRES")

        if not isinstance(raw_name, str) or not raw_name.strip():
            raise ValueError(f"Collector {module.__name__} has invalid MODULE_NAME")
        if not isinstance(requires_attr, tuple):
            raise ValueError(f"Collector {module.__name__} REQUIRES must be a tuple")

        enabled = bool(getattr(module, "ENABLED", True))
        requires = requires_attr
        description = getattr(module, "DESCRIPTION", module.__doc__ or "")
        writes_text = bool(getattr(module, "WRITE_TEXT_FILE", False))
        name = raw_name.replace("_", " ") if isinstance(raw_name, str) else str(raw_name)
        return cls(
            key=key,
            category=category,
            module=module,
            name=name,
            enabled=enabled,
            requires=requires,
            description=description,
            writes_text=writes_text,
        )

    def missing_prerequisites(self) -> tuple[str, ...]:
        missing: list[str] = []
        for key in self.requires:
            value = get_config_value(key)
            if value is None or str(value).strip() == "":
                missing.append(key)
        return tuple(missing)

    def banner(self) -> None:
        banner_fn = getattr(self.module, "banner", None)
        if callable(banner_fn):
            print(colored(f'{style.BOLD}[>] {banner_fn()}{style.END}', 'blue'))

    def run(self, target: str) -> Optional[object]:
        main_fn = getattr(self.module, "main", None)
        output_fn = getattr(self.module, "output", None)
        if not callable(main_fn) or not callable(output_fn):
            print(colored(f"[-] Collector {self.name} is missing main/output functions. Skipping.", "red"))
            return None

        data = main_fn(target)
        if data is not None:
            output_fn(data, target)
        return data

    def write_text_report(self, target: str, data: object, output_dir: Path | None = None) -> None:
        if not self.writes_text:
            return

        output_text_fn = getattr(self.module, "output_text", None)
        if not callable(output_text_fn):
            return

        text_data = output_text_fn(data)
        if not text_data:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_name = self.name.replace(" ", "_")
        filename = f"text_report_{target}_{safe_name}_{timestamp}.txt"
        output_path = (output_dir or Path.cwd()) / filename
        output_path.write_text(text_data, encoding="utf-8")
        print(colored(f"[+] Text Report written to {output_path}", "green"))
