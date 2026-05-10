# roasting

> **5-Color Harness execution engine for Korean business leaders.**
> Auto-routes 63 white-collar cases, runs a 5-persona producer–reviewer team, and delivers
> polished Korean output — all inside Claude Code. Open Beta v0.1.

**Korean documentation:** [README.ko.md](README.ko.md)

---

## Install

```bash
/plugin marketplace add airoasting/roasting
/plugin install roasting@airoasting
```

---

## What it does

`/roasting` takes a one-line description of your task in natural Korean and:

1. **Routes** your request to the best-matching case from a library of 63 white-collar artifact types
   (emails, board memos, investor letters, legal opinions, and more).
2. **Produces** a first draft through the BLACK persona — a role-cast expert matched to the case.
3. **Reviews** the draft with four specialist reviewers (RED · SILVER · BLUE · GOLD), each evaluating
   a different dimension: logic, domain structure, empathy/tone, and reader engagement.
4. **Debates** when reviewers disagree (score spread ≥ 0.5), then iterates up to 4 rounds.
5. **Delivers** three outputs: the polished artifact, a score sheet, and an optional slide deck
   (for PPT cases, rendered from the `slide_library` template system).

The acceptance bar is an average reviewer score of **9.5 / 10**.

---

## Quick sample

```
/roasting 거래처 부장한테 8월 12일까지 회신 달라는 메일
```

Expected output: a concise B2B email, scored by 4 reviewers, ready to send.

---

## Korean only

This plugin is designed for Korean-language white-collar workflows. All case definitions,
reviewer personas, and output quality rules are written in Korean. For full documentation see
[README.ko.md](README.ko.md).

---

## Privacy

`/roasting` is designed with a privacy-first architecture:

- **Content is never transmitted.** Your input prompt, BLACK draft, and RGSB comments stay local.
- **Telemetry is opt-in and off by default.** When enabled, only anonymous metadata is sent
  (case ID, final score, round count, cost estimate). No content, no file paths, no IP.
- Full details: [docs/PRIVACY.md](docs/PRIVACY.md)

---

## Status

**Open Beta v0.1** — production-ready for individual use; Agent Teams path is experimental.
Known limitations are listed in [README.ko.md § 알려진 한계](README.ko.md).

---

## Contributing

Bug reports and feedback are welcome via GitHub Issues. To submit feedback from inside Claude:

```
/roasting --feedback
```

This opens a pre-filled GitHub Issue with session metadata attached.

---

## License

MIT — see [LICENSE](LICENSE).
