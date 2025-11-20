# Repository Guidelines

## Project Structure & Module Organization
`datasploit.py` is the single entry point. It classifies the target (domain/email/ip/username) and delegates to the shared runner in `core/`, which auto-discovers collectors under `domain/`, `emails/`, `ip/`, and `username/`. Each collector lives in the matching package as `<category>_<source>.py` and defines `ENABLED`, `MODULE_NAME`, and `REQUIRES`. Keep shared settings in `config.ini` or `datasploit_config.py`, contributor docs in `docs/`, and generated output under `reports/`. Cached avatars and similar assets belong in `profile_pic/`.

## Build, Test, and Development Commands
Target Python 3.12 as declared in `Pipfile`. Preferred workflow: `pipenv install` to resolve dependencies, then `pipenv shell` to run tools. Virtualenv is also fine: `python3 -m venv .venv && source .venv/bin/activate` followed by `pip install -r requirements.txt`. Exercise scripts before opening a pull request, e.g. `python datasploit.py -i example.com` for the full domain sweep or `python domain/domain_subdomains.py example.com` for a single collector. Append `-o text` when validating report writers.

## Coding Style & Naming Conventions
Follow PEP 8 with four-space indentation, lowercase module names, and descriptive function names. New collectors must live in the matching module folder and keep the `<module>_<source>.py` prefix so discovery stays consistent. Implement the `banner`, `main`, and `output` trio from the templates; let `main` return data and gate unfinished work with the `ENABLED` flag. Secrets stay outside the codebase—use config files, `.env`, or runtime variables.

## Testing Guidelines
There is no automated suite yet, so rely on targeted manual verification. Run the collector directly to confirm input handling, then trigger the orchestrator (`python datasploit.py -i test.tld`) to confirm integration. Inspect files created in `reports/` and keep console output readable. Document the targets and commands you used in the pull request so reviewers can repeat them.

## Commit & Pull Request Guidelines
Write concise, imperative commit summaries that mirror the existing history (`domain: scan domain with urlscan.io`). Squash noisy work-in-progress commits before review. Pull requests should explain the motivation, list configuration or dependency changes, and note verification steps or artifacts. Link to issues when relevant, and include screenshots only when they meaningfully illustrate UI or report changes.

## Configuration & Security Notes
Mirror changes between `config.template.ini` and `config.ini`, and flag new options in the docs. Never commit API tokens or target data; load them via environment variables or local config files. Review third-party integrations for rate limits and legal considerations, and highlight modules that may require elevated or commercial access.
