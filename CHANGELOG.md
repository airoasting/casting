# Changelog

This project follows [Semantic Versioning](https://semver.org/) and [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [0.1.0] - 2026-05-10 (Open Beta)

### Added

**Core pipeline (7-Phase):**
- Phase 0: Session initialization and workspace setup (`_workspace/{session}/`)
- Phase 1: Expert Pool routing — Haiku judge maps user request → top-3 case IDs from 63-case index
- Phase 2: Case seed load — lazy-loads per-case `.md` from `references/cases/`; slice limits managed
- Phase 3: BLACK draft — role-cast producer writes first artifact per case BLACK persona
- Phase 4: Anti-pattern detection — 5 detectors run before every review round
- Phase 5: RGSB review — Agent Teams primary path (TeamCreate + SendMessage + TaskCreate);
  sub-agent fallback retained for stability
- Phase 6: Loop — 4-round cap; debate triggers at σ ≥ 0.5 between any two reviewer scores
- Phase 7: Deliver — polished artifact + score sheet + slide deck (PPT cases)

**Case library (63 cases, 8 categories):**
- 외부 커뮤니케이션 (12): email, apology, crisis message, press release, newsletter, case study,
  launch message, FAQ, CS template, vision/mission, lecture deck, pitch deck, keynote
- 소셜미디어·글쓰기 (9): LinkedIn post, SNS post, blog, newspaper column, AI text polish,
  fiction, poetry, LinkedIn profile, newsletter
- 내부 커뮤니케이션 (7): company notice, job posting, difficult message, town hall, HR policy,
  1on1, workshop materials
- 분석·보고서 (12): 1-page report, meeting minutes, board report, shareholder letter, PRD,
  quarterly review, IR presentation, OKR report, investment memo, market analysis,
  expert call note, management diagnosis, narrative memo, analysis report
- 의사결정·전략 (10): business proposal, sales proposal, board report, shareholder letter,
  PRD, executive PPT, storyline, consulting deck, narrative memo
- 법무 검토·규제 대응 (7): contract review, legal opinion, complaint/answer, brief,
  audit opinion, tax opinion, due diligence, internal control report
- 마케팅 (2): copy/naming, brand guidelines
- 커리어·상담 (4): resume, cover letter, interview prep, leadership counseling

**5-Color reviewer team:**
- BLACK: Sonnet-powered producer, role-cast to case BLACK persona
- RED (이성): logic and intent clarity reviewer
- SILVER (분야 전문가): domain structure specialist
- BLUE (공감): tone, length, and empathy reviewer
- GOLD (독자 시나리오): reader scenario simulation

**Anti-pattern detection (5 types):**
- `HALLUCINATED_NUMBER`: regex extraction + Haiku source verification; exempt on p63/p64/p69
- `VAGUE_CTA`: regex sieve on last 50 chars + Haiku confirm; ~30 applicable cases
- `MISSING_GOLD_HOOK`: Haiku judge, first 200 chars vs case GOLD scenario
- `TONE_MISMATCH`: Haiku, tone match score < 6 threshold
- `LEGAL_RISK_TERM`: regex-only; legal + external comms categories
- 3-strikes counter: same pattern 3× in a row → escalate to user

**PPT / slide_library integration:**
- 35 slide templates indexed by color axis (professional/creative) × formality axis
- BLACK writes HTML deck; fallback to Markdown if template load fails
- Template confirmation flow on first call for PPT cases

**Scoring and acceptance:**
- RED·SILVER·BLUE 3-reviewer average threshold: 9.5 / 10
- GOLD reader immersion threshold: 9.5 / 10
- 4-round cap; debate auto-triggers at σ ≥ 0.5
- Score scale: 10=flawless, 9.5=pass, 9=one fix, 8=v2 candidate, ≤7=rewrite

**Telemetry and feedback:**
- Anonymous opt-in telemetry (default OFF); Supabase backend, INSERT-only RLS
- Fields: user_id (local UUID), case_id, final_score, round_count, cost estimate,
  anti_patterns_detected, debate_triggered, completion_status, timestamp
- Content (input, BLACK output, RGSB comments) never transmitted
- `/roasting --feedback`: opens pre-filled GitHub Issue with session metadata

**CLAUDE.md auto-registration:**
- `install_hook.py` registers `/roasting` pointer in `~/.claude/CLAUDE.md` on install

**Developer tooling:**
- `Makefile` targets: sync-cases, sync-slides, gen-case-catalog, test, lint, typecheck,
  package, publish, clean
- `scripts/sync_cases.py`: HTML parser for airoasting.github.io/5color (brace-counting
  state machine; no external JS engine required)
- `scripts/gen_case_catalog.py`: generates `docs/ko/case-catalog.md` from case frontmatter
- `scripts/route.py`: Haiku-backed Expert Pool router + Wilson 95% CI helper
- `scripts/anti_patterns.py`: 5 detectors + StrikeCounter
- `scripts/llm_judge.py`: HaikuJudge + fake_judge fixture for CI
- `scripts/telemetry.py`: Supabase async client + local config reader
- `scripts/deliver.py`: artifact + score sheet + HTML deck assembler
- `scripts/feedback.py`: GitHub Issue URL builder
- `scripts/build_slide_html.py`: HTML deck renderer from template JSON

**CI (GitHub Actions):**
- `test.yml`: lint (ruff + mypy), unit (no slow/network), network (main push only)
- `release.yml`: tests + `make package` + GitHub release on `v*` tag; prerelease
  auto-detected from tag name containing `-`

**Tests:**
- 50 anti-pattern unit tests (10 per detector + 5 strike counter; fake_judge in CI)
- 189 routing accuracy tests (63 cases × 3 natural-language phrasings); top-1 Wilson
  95% LB ≥ 0.90 gate

### Privacy

- User input prompt, BLACK draft, RGSB comments, and rendered output are **never** transmitted.
- Telemetry default = OFF; opt-in via `~/.claude/roasting/config.json`.
- Full policy: [docs/PRIVACY.md](docs/PRIVACY.md)

### Known limitations (v0.1 beta)

- Agent Teams path (Phase 5) uses experimental Anthropic feature; auto-falls back to
  sequential sub-agent dispatch on error.
- Case sync (`make sync-cases`) is manual; no automatic update on 5color site changes.
- HTML-only slide output; PPTX export planned for v0.2.
- Korean-language only; English input not optimized.

---

## v0.2 (planned)

- Instinct mode: fast single-reviewer path
- User-configurable Hooks for custom anti-pattern rules
- Automatic case sync with 5color site webhook
- Case validation tier labels (verified / beta)
- PPTX direct export
