from __future__ import annotations

from pathlib import Path
from typing import Optional

from termcolor import colored

from .collector import CollectorModule
from .config import load_config
from .registry import CollectorRegistry
from .types import TargetType


class CollectorRunner:
    def __init__(self, registry: Optional[CollectorRegistry] = None):
        self.registry = registry or CollectorRegistry()
        self._config = load_config()

    def run(self, category: TargetType, target: str, output: Optional[str] = None) -> None:
        collectors = self.registry.get_collectors(category)
        if not collectors:
            print(colored(f"[-] No collectors found for {category.value} targets.", "yellow"))
            return
        print(colored(f"[+] Running {len(collectors)} collectors for {category.value} target '{target}'.", "green"))

        for collector in collectors:
            self._run_collector(collector, target, output)

    def _run_collector(self, collector: CollectorModule, target: str, output: Optional[str]) -> None:
        if not collector.enabled:
            print(colored(f"[-] Skipping {collector.name} (disabled).", "yellow"))
            return

        missing = collector.missing_prerequisites()
        if missing:
            missing_list = ", ".join(missing)
            print(colored(f"[-] Skipping {collector.name}: missing config keys [{missing_list}].", "yellow"))
            return

        collector.banner()
        data = collector.run(target)

        if data and output and output.lower() == "text":
            collector.write_text_report(target, data)


_runner: Optional[CollectorRunner] = None


def get_runner() -> CollectorRunner:
    global _runner
    if _runner is None:
        _runner = CollectorRunner()
    return _runner
