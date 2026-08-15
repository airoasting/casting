#!/usr/bin/env python3
"""references/ 를 사이트 정본(docs/assets)에서 생성한다.

정본은 하나다.
  docs/index.html   의 A 배열      = 50역할 id·직책·본부·설명
  docs/assets/prompts.js 의 PROMPTS = 50역할 + 팀장 시스템 프롬프트 전문
  docs/assets/router.js  의 HARNESS = 28개 팀 구성

여기서 아래 세 파일을 생성한다.
  references/catalog.md
  references/agent-prompts.md
  references/harnesses.md  (손으로 쓰는 머리 부분은 보존, "## 팀 구성 목록" 아래만 생성)

사용법
  python3 scripts/sync_refs.py           # 생성(덮어쓰기)
  python3 scripts/sync_refs.py --check   # 어긋난 곳만 보고, 파일은 건드리지 않음(종료코드 1)

역할을 고치거나 번호를 바꿀 때는 docs/assets 쪽만 고치고 이 스크립트를 돌린다.
손으로 references를 고치면 다음 실행에서 지워진다.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "docs" / "index.html"
PROMPTS_JS = ROOT / "docs" / "assets" / "prompts.js"
ROUTER_JS = ROOT / "docs" / "assets" / "router.js"
CATALOG = ROOT / "references" / "catalog.md"
AGENT_PROMPTS = ROOT / "references" / "agent-prompts.md"
HARNESSES = ROOT / "references" / "harnesses.md"

RECIPE_HEADER = "## 팀 구성 목록"


def run_js(source: str, expr: str):
    """JS 소스를 실행해 expr 결과를 JSON으로 받는다."""
    script = (
        "const src=%s;"
        "const fn=new Function(src+';return %s;');"
        "process.stdout.write(JSON.stringify(fn()));" % (json.dumps(source), expr)
    )
    out = subprocess.run(
        ["node", "-e", script], capture_output=True, text=True, check=True
    )
    return json.loads(out.stdout)


def load_roles():
    html = INDEX.read_text(encoding="utf-8")
    arr = re.search(r"var A=\[(.*?)\n\s*\];", html, re.S)
    if not arr:
        sys.exit("index.html 에서 A 배열을 찾지 못했습니다.")
    rows = run_js("var A=[%s];" % arr.group(1), "A")
    secs = re.search(r"var SECTIONS=(\[[^\]]*\]);", html)
    if not secs:
        sys.exit("index.html 에서 SECTIONS 를 찾지 못했습니다.")
    sections = run_js("var S=%s;" % secs.group(1), "S")
    roles = {}
    for rid, ko, desc, sec, _type, en in rows:
        roles[rid] = {"id": rid, "ko": ko, "desc": desc, "sec": sec, "en": en}
    return roles, sections


def load_prompts():
    return run_js(PROMPTS_JS.read_text(encoding="utf-8"), "PROMPTS")


def load_harness():
    return run_js(
        ROUTER_JS.read_text(encoding="utf-8"),
        "{HARNESS:HARNESS,CATS:HARNESS_CATS,MODS:MODIFIERS}",
    )


def build_catalog(roles, sections):
    out = [
        "# 에이전트 팀원 카탈로그 — 50명",
        "",
        "> 목적에 맞는 팀원을 고를 때 쓰는 표. 실행용 전체 시스템 프롬프트는 `agent-prompts.md`에 id로 들어 있다.",
        "> 회사형 10개 본부로 나뉜다. **이 파일은 `scripts/sync_refs.py`가 사이트 정본(`docs/assets`)에서 생성한다. 직접 고치지 않는다.**",
        "",
    ]
    for idx, name in enumerate(sections):
        members = [r for r in roles.values() if r["sec"] == idx]
        if not members:
            continue
        out.append("## %d. %s" % (idx + 1, name))
        out.append("")
        out.append("| id | 직책 | English | 설명 |")
        out.append("|---|---|---|---|")
        for r in sorted(members, key=lambda x: x["id"]):
            out.append("| %d | %s | %s | %s |" % (r["id"], r["ko"], r["en"], r["desc"]))
        out.append("")
    out += [
        "> 팀장(오케스트레이터)은 이 50명과 별개다. `agent-prompts.md`의 `## [lead]` 구간에 있다.",
        "> 전문가 역할(회계사·노무사·변호사·감사인)은 실무 초안과 1차 검토 보조이며 자격 자문이 아니다.",
        "",
    ]
    return "\n".join(out)


def build_agent_prompts(roles, sections, prompts):
    out = [
        "# 50명 시스템 프롬프트(실행용)",
        "",
        "> 선발된 팀원의 id 구간만 뽑아 읽는다: `## [N]`부터 다음 `---` 직전까지. 회사형 10개 본부. 팀장 프롬프트는 맨 끝 `## [lead]`.",
        "> **이 파일은 `scripts/sync_refs.py`가 `docs/assets/prompts.js`에서 생성한다. 직접 고치지 않는다.**",
        "",
    ]
    blocks = []
    for rid in sorted(roles):
        r = roles[rid]
        body = prompts.get(str(rid)) or prompts.get(rid)
        if not body:
            sys.exit("prompts.js 에 id %s 프롬프트가 없습니다." % rid)
        blocks.append(
            "## [%d] %s (%s) · %s\n\n%s\n"
            % (rid, r["ko"], r["en"], sections[r["sec"]], body.strip())
        )
    lead = prompts.get("lead")
    if lead:
        blocks.append(
            "## [lead] 팀장 · 오케스트레이터 (Team Lead · Orchestrator)\n\n%s\n"
            % lead.strip()
        )
    return "\n".join(out) + "\n---\n\n".join(blocks)


def build_harness_section(roles, harness):
    cats = harness["CATS"]
    out = [RECIPE_HEADER, "", "> `docs/assets/router.js`에서 생성된다. 직접 고치지 않는다.", ""]

    def label(pid):
        r = roles.get(pid)
        return "%s(%d)" % (r["ko"], pid) if r else "id %s(카탈로그에 없음)" % pid

    for h in harness["HARNESS"]:
        out.append("### %s" % h["name"])
        out.append("- 분야: %s · %s" % (cats[h["cat"]], h["desc"]))
        out.append("- 팀장 지침: %s" % h["lead"])
        out.append("- 단계:")
        for i, step in enumerate(h["steps"], 1):
            out.append("  %d. %s — %s" % (i, label(step["p"]), step["io"]))
        out.append("- 검토: %s — %s" % (label(h["review"]["p"]), h["review"]["io"]))
        deep = h.get("deepAdd")
        out.append(
            "- deepAdd: %s · 가능 토글: %s"
            % (label(deep) if deep else "없음", ",".join(h.get("mods", [])))
        )
        out.append("- 키워드: %s" % ",".join(h.get("kw", [])))
        out.append("")
    return "\n".join(out)


def build_harnesses(roles, harness):
    old = HARNESSES.read_text(encoding="utf-8")
    if RECIPE_HEADER not in old:
        sys.exit("harnesses.md 에서 '%s' 머리글을 찾지 못했습니다." % RECIPE_HEADER)
    head = old.split(RECIPE_HEADER)[0]
    return head + build_harness_section(roles, harness)


def main():
    check = "--check" in sys.argv
    roles, sections = load_roles()
    prompts = load_prompts()
    harness = load_harness()

    targets = [
        (CATALOG, build_catalog(roles, sections)),
        (AGENT_PROMPTS, build_agent_prompts(roles, sections, prompts)),
        (HARNESSES, build_harnesses(roles, harness)),
    ]

    # 팀 구성이 카탈로그에 없는 id를 부르는지 교차 검사
    problems = []
    for h in harness["HARNESS"]:
        ids = [s["p"] for s in h["steps"]] + [h["review"]["p"]]
        if h.get("deepAdd"):
            ids.append(h["deepAdd"])
        for pid in ids:
            if pid not in roles:
                problems.append("팀 구성 '%s' 가 없는 id %s 를 부릅니다." % (h["name"], pid))
    for name, mod in harness["MODS"].items():
        add = mod.get("add")
        if isinstance(add, list):
            for pid in add:
                if pid not in roles:
                    problems.append("토글 '%s' 가 없는 id %s 를 부릅니다." % (name, pid))

    stale = []
    for path, content in targets:
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != content:
            stale.append(path)
            if not check:
                path.write_text(content, encoding="utf-8")

    rel = lambda p: p.relative_to(ROOT)
    if check:
        for p in stale:
            print("어긋남: %s (사이트 정본과 다릅니다)" % rel(p))
        for msg in problems:
            print("오류: %s" % msg)
        if stale or problems:
            print("\n고치려면: python3 scripts/sync_refs.py")
            sys.exit(1)
        print("정합 확인. references 3개 파일이 사이트 정본과 일치합니다.")
    else:
        for p in stale:
            print("생성: %s" % rel(p))
        if not stale:
            print("변경 없음. 이미 정본과 일치합니다.")
        for msg in problems:
            print("오류: %s" % msg)
        if problems:
            sys.exit(1)


if __name__ == "__main__":
    main()
