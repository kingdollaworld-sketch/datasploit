# Changelog

## Modernisation (2025-03-19)

**Core architecture**
- Introduced a `core` package with shared orchestration helpers:
  - `core.collector.CollectorModule` wraps existing collectors with metadata and text-report support.
  - `core.registry.CollectorRegistry` performs auto-discovery per target category and ensures the project root is on `sys.path` before imports.
  - `core.runner.CollectorRunner` handles prerequisite checks, banner execution, and optional text report writing.
  - `core.style` centralises ANSI styling; collectors import `style` instead of defining local classes.
  - `core.input_classifier` offers unified target classification (`domain`, `email`, `ip`, `username`) and private-IP detection.
  - `core.config` loads values from `config.ini` (falling back to legacy `config.py`) once and exposes `get_config_value` for collectors.
- `datasploit.py` now uses the classifier + runner and skips private IPs automatically.
- Legacy entry points (`domainOsint.py`, `emailOsint.py`, `ipOsint.py`, `usernameOsint.py`) have been removed in favour of a single `datasploit.py` entrypoint. Older workflows should switch to `python datasploit.py -i <target>`.

**Collector requirements**
- Every collector module must define:
  - `ENABLED`: boolean flag to toggle execution.
  - `MODULE_NAME`: user-facing name (derived from filename when omitted).
  - `REQUIRES`: tuple of config keys required before execution (empty tuple if none).
- `banner()` implementations now return a plain string; the runner handles consistent formatting via the shared `style` helper.
- Modules missing `MODULE_NAME` or `REQUIRES` are skipped with an explanatory warning.
- Many collectors now declare prerequisites (GitHub tokens, Shodan API key, etc.) so the runner can skip them gracefully when credentials are absent.

**Configuration access**
- `vault.py` is deprecated; calling `vault.get_key` raises an error instructing authors to use `core.config.get_config_value`.
- All collectors use `get_config_value` instead of rolling their own config parsing.
- The user-facing configuration moved to `config.ini` to align with a familiar INI-style template and avoid name clashes with `core/config.py`.

**Package cleanup**
- Module packages now auto-import their collectors so library users can access them via attributes like `datasploit.username.username_gitscrape`.
- Removed the `base.py` shim from all module packages (`domain`, `emails`, `ip`, `username`). Discovery now relies on the registry’s path injection.
 - Package `__init__` files perform lightweight auto-imports instead of remaining empty stubs, preserving backwards-compatible attribute access.
- Documentation (`docs/Writing_Modules.md`) updated to reflect the new structure—no base helper or auto-import glue; collectors live directly in the package with the required metadata.

**Dependency updates**
- `requirements.txt` and `Pipfile` list the exact dependencies used at runtime; obsolete Python 2 packages dropped, and version floors set for Python 3 compatibility.
- Optional integrations (e.g., `emails/email_hacked_emails.py`) now handle missing optional dependencies gracefully (`cfscrape`).

**Contributor guidance**
- When adding a new collector:
  1. Place it under the appropriate package (`domain/`, `emails/`, `ip/`, `username/`).
  2. Name the file `category_source.py` (e.g., `domain_newservice.py`).
  3. Define `ENABLED`, `MODULE_NAME`, `REQUIRES`, and optionally `WRITE_TEXT_FILE` and `DESCRIPTION`.
  4. Implement `banner()`, `main(target)`, `output(data, target)`; `output_text(data)` if you set `WRITE_TEXT_FILE = True`.
  5. The shared runner auto-discovers it—no manual registry changes needed.
- `config.ini` should contain any new keys referenced in `REQUIRES`; users populate them with their credentials.

Refer to `core/collector.py` and `docs/Writing_Modules.md` for detailed examples.
