"""One-shot helper: read references/cases/p*.md frontmatter and emit 3 phrasing
templates per case. Author then hand-edits to make them natural Korean.
"""
from __future__ import annotations

import json
import re
from pathlib import Path


CASES_DIR = Path("skills/roasting/references/cases")
OUT = Path("tests/routing/cases_phrasings.seed.json")


def parse_fm(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip().strip('"')
    return out


def main() -> None:
    rows = []
    for p in sorted(CASES_DIR.glob("p*.md")):
        fm = parse_fm(p.read_text(encoding="utf-8"))
        cid = fm.get("id", p.stem)
        title = fm.get("title", "")
        sub = fm.get("subhead", "")
        # Strip emphasis markers for cleaner natural phrasings.
        title_clean = re.sub(r"</?em>", "", title)
        rows.append({"case_id": cid, "phrasing": f"{title_clean} 작성", "intent_tag": "natural_intent"})
        rows.append({"case_id": cid, "phrasing": title_clean, "intent_tag": "direct_keyword"})
        rows.append({"case_id": cid, "phrasing": sub[:60], "intent_tag": "audience_clue"})
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(rows)} phrasings to {OUT}")


if __name__ == "__main__":
    main()
