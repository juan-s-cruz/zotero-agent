# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added `user_config.json` and a template `user_config.json.template` at the workspace root to store research topics, evaluation criteria, and target web sources.
- Added `initialize.py` script to dynamically compile user configuration into the agent's prompts and instruction files.
- Added template files `.agents/AGENTS.md.template` and `.agents/skills/web-news-expander/SKILL.md.template` containing placeholder tags.
- Added a `CHANGELOG.md` following standard practices.
- Added `requirements.txt` to track workspace dependencies (`markdown`).
- Added the `newsletter-persister` skill (`SKILL.md.template` and `scripts/persist.py`) to manage Zotero report and note persistence.

### Changed

- Generalized `.agents/AGENTS.md` and `.agents/skills/web-news-expander/SKILL.md` to be dynamically generated instead of containing hardcoded configuration.
- Updated `.gitignore` to untrack and ignore generated agent instructions and user configurations (`user_config.json`).
- Updated `README.md` to document the new configuration setup and `initialize.py` script execution.
- Tightened fallback web search behavior: Restricted explicit web searches for arXiv papers to Zotero RSS feed unavailability and explicit user approval.
- Added early newsletter existence check: The agent now checks if the summary report for the current day already exists before running and prompts the user to cancel or overwrite.
- Updated `initialize.py` to compile new persister templates, manage a local `.venv`, and clean up unused replacements.
- Simplified `.agents/AGENTS.md.template` to merge goals/guide sections, skip redundant verifications, and route search/persist tasks to skills/subagents.
- Polished the `newsletter-persister` skill to run directly under `.venv`, validate file content size, restrict fallbacks, and request sandbox bypass.

### Removed

- Removed hardcoded Zotero credentials, collection keys, and specific quant blogs from synced instructions to prevent configuration leakage.
