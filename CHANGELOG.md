# Changelog

This project follows [Semantic Versioning](https://semver.org/) and [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [0.1.0] - 2026-XX-XX (Open Beta)

### Added

- Initial release with 63 cases routed via Expert Pool pattern.
- 5-Color Harness Producer-Reviewer team (BLACK + RED·SILVER·BLUE·GOLD).
- Agent Teams mode for Phase 5 RGSB debate; sub-agent fallback retained.
- Anti-pattern detection (5 types): HALLUCINATED_NUMBER, VAGUE_CTA, MISSING_GOLD_HOOK, TONE_MISMATCH, LEGAL_RISK_TERM.
- slide_library binding for PPT cases (35 templates, color × formality axes).
- 9.5 acceptance threshold + 4-round cap.
- Anonymous opt-in telemetry; `/roasting --feedback` GitHub Issue prefilled.
- CLAUDE.md auto-registration on install.

### Privacy

- Content (user input prompt, BLACK output, RGSB comments) never transmitted.
- Telemetry default = OFF; opt-in via `~/.claude/roasting/config.json`.
