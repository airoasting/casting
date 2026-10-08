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
    # 스크립트는 표준입력으로 넘긴다. -e 인자로 넘기면 prompts.js가 커질 때 인자 길이 한도(ARG_MAX)를 넘는다.
    out = subprocess.run(
        ["node", "-"], input=script, capture_output=True, text=True, check=True
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


INLINE_ID_TARGETS = [
    "SKILL.md",
    "references/harnesses.md",
    "references/execution-modes.md",
    "references/deliverable-specs.md",
    "platforms/codex/SETUP.md",
    "README.md",
]

INLINE_ID_PATTERN = re.compile(r"([가-힣A-Za-z·\s]{2,14}?)\((\d{1,2})\)")


def check_inline_ids(roles):
    """본문에 손으로 적은 '직책(id)' 표기가 카탈로그와 맞는지 본다.

    생성되는 세 파일과 달리 SKILL.md·harnesses.md 머리 부분은 사람이 직접 쓴다.
    여기서 번호가 어긋나면 라우터가 엉뚱한 팀원을 뽑는데, 파일만 봐서는 눈에 띄지 않는다.
    """
    by_name = {r["ko"]: r["id"] for r in roles.values()}

    def resolve(label):
        label = label.strip()
        if label in by_name:
            return by_name[label]
        for match in (
            [n for n in by_name if n.startswith(label) or label.startswith(n)],
            [n for n in by_name if label in n or n in label],
        ):
            if len(match) == 1:
                return by_name[match[0]]
        return None

    problems = []
    for rel in INLINE_ID_TARGETS:
        path = ROOT / rel
        if not path.exists():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for m in INLINE_ID_PATTERN.finditer(line):
                label, wrote = m.group(1).strip(), int(m.group(2))
                right = resolve(label)
                if right is not None and right != wrote:
                    problems.append(
                        "%s:%d 에 '%s(%d)' 라고 적혀 있지만 카탈로그에서는 %d 입니다."
                        % (rel, lineno, label, wrote, right)
                    )
    return problems


SECTION_RANGE_PATTERN = re.compile(r"([가-힣A-Za-z·]{2,16})\((\d{1,2})~(\d{1,2})\)")


def check_section_ranges(roles, sections):
    """본문에 적은 '본부(a~b)' 범위가 카탈로그의 실제 번호 구간과 맞는지 본다.

    '직책(id)' 검사는 범위 표기를 읽지 못해서, 본부 번호가 바뀐 뒤에도 옛 범위가 남는다.
    """
    ranges = {}
    for idx, name in enumerate(sections):
        ids = sorted(r["id"] for r in roles.values() if r["sec"] == idx)
        if ids:
            ranges[name] = (ids[0], ids[-1])

    problems = []
    for rel in INLINE_ID_TARGETS:
        path = ROOT / rel
        if not path.exists():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for m in SECTION_RANGE_PATTERN.finditer(line):
                label, lo, hi = m.group(1), int(m.group(2)), int(m.group(3))
                names = [n for n in ranges if n == label or n.startswith(label) or label.startswith(n)]
                if len(names) == 1 and ranges[names[0]] != (lo, hi):
                    right = ranges[names[0]]
                    problems.append(
                        "%s:%d 에 '%s(%d~%d)' 라고 적혀 있지만 카탈로그에서는 %d~%d 입니다."
                        % (rel, lineno, label, lo, hi, right[0], right[1])
                    )
    return problems


PROMPT_SECTIONS = [
    "## Role · 역할",
    "## Rubric · 합격 기준",
    "## Workflow · 작업 순서",
    "## Tools · 도구",
    "## Context · 맥락",
    "## Guardrail · 금지선",
]
SECTION_FIELDS = {
    "## Role · 역할": ["- 맡는 일:", "- 맡지 않는 일:", "- 끝의 기준:", "- 판단 기준:"],
    "## Rubric · 합격 기준": ["문체:", "출력 형식", "점검 질문", "점수 기준", "예시 (형식 참고용입니다.", "자기평가:"],
    "## Workflow · 작업 순서": ["넘기는 곳:"],
    "## Tools · 도구": ["- 도구가 없을 때:"],
    "## Context · 맥락": [
        "- 받는 것:", "- 꼭 있어야 할 입력:", "- 빠졌을 때:", "- 독자와 쓰임:",
        "- 사람과 대화할 때:", "- 팀 안에서",
    ],
    "## Guardrail · 금지선": ["- "],
}
# 예전에 쓰던 역할 이름. 핸드오프가 없는 역할을 가리키게 된다.
STALE_ROLE_NAMES = [
    "자동화 아키텍트", "업무·일정 오케스트레이션", "SOP·프로세스", "비즈니스 케이스",
    "데이터·분석 담당", "문서 작성가", "커뮤니케이션·SNS 담당", "경리 담당",
]
# 표지는 [확인 필요]·추정·가정·미정·(제안) 다섯 가지만 쓴다. 아래는 같은 자리에 쓰이던 다른 표지다.
BANNED_MARKERS = [
    '"자료 없음"', '"검증 필요"', '"추측"', '"가정 기반"', '"확인 중"', '"추가 자료 필요"', "[자료 필요]",
    "[고객 입력 필요]", '"사례 보강 필요"', '"추후 안내"', '"확인 필요"', "[사례 보강 필요]", "한 끗",
]
ROLE_REF_PATTERN = re.compile(r"\((\d{1,2})\)")
QUESTION_PATTERN = re.compile(r"^\d+\. \(출력 ([\d, ]+)\) .+\?$")
ANCHOR_LABELS = ["8점: ", "9점: ", "9.5점(합격선): ", "10점(대표작): "]


def _numbered(block):
    return [l for l in block.strip().split("\n") if re.match(r"^\d+\. ", l)]


def harness_neighbors(harness):
    """팀 구성에서 역할마다 바로 앞·뒤 단계 역할을 모은다(게이트 검토자는 빼고)."""
    prev, nxt = {}, {}
    for h in harness["HARNESS"]:
        steps = [s["p"] for s in h["steps"]]
        for i, p in enumerate(steps):
            if i > 0:
                prev.setdefault(p, set()).add(steps[i - 1])
            if i + 1 < len(steps):
                nxt.setdefault(p, set()).add(steps[i + 1])
    return prev, nxt


def check_prompt_structure(roles, prompts, harness=None):
    """50역할과 팀장 프롬프트가 6칸(Role·Rubric·Workflow·Tools·Context·Guardrail) 틀을 지키는지 본다.

    - 6칸 머리글이 이 순서로 하나씩만 있고, 다른 '## ' 머리글이 없다. 본문에 '---' 줄이 없다
      (SKILL.md의 sed 구간 추출이 거기서 끊긴다).
    - 칸마다 필수 항목이 있다. Tools 에는 '도구가 없을 때' 줄이 있다.
    - 점검 질문은 4~7개이고, 모두 '(출력 N) …?' 꼴이며, 출력 형식의 모든 항목이 질문 하나 이상에 걸린다.
    - 점수 기준은 8·9·9.5·10점 네 줄이고 합니다체로 끝난다.
    - '직책(id)'로 부른 팀원은 그 번호의 실제 직책이다. 옛 역할 이름과 폐기한 표지를 쓰지 않는다.
    - 팀 구성에서 바로 뒤 단계 역할은 '넘기는 곳'에, 바로 앞 단계 역할은 '받는 것'에 있다.
    """
    problems = []
    prev, nxt = harness_neighbors(harness) if harness else ({}, {})
    keys = [str(r) for r in sorted(roles)] + ["lead"]
    for key in keys:
        body = prompts.get(key)
        if not body:
            problems.append("프롬프트 %s 가 없습니다." % key)
            continue
        where = "프롬프트 [%s]" % key
        if key != "lead":
            r = roles[int(key)]
            want = "# %s (%s)" % (r["ko"], r["en"])
            if body.split("\n", 1)[0].strip() != want:
                problems.append("%s 제목이 '%s' 가 아닙니다." % (where, want))
        heads = [l for l in body.split("\n") if l.startswith("## ")]
        if heads != PROMPT_SECTIONS:
            problems.append("%s 의 칸 순서가 6칸 틀과 다릅니다: %s" % (where, " / ".join(heads)))
            continue
        if any(l.strip() == "---" for l in body.split("\n")):
            problems.append("%s 에 '---' 줄이 있습니다." % where)
        parts = re.split(r"(?m)^(## .+)$", body)
        sections = dict(zip(parts[1::2], parts[2::2]))
        for head, fields in SECTION_FIELDS.items():
            text = sections.get(head, "")
            for f in fields:
                if f not in text:
                    problems.append("%s 의 %s 에 '%s' 가 없습니다." % (where, head[3:], f.strip()))
        rubric = sections.get("## Rubric · 합격 기준", "")
        outs = _numbered(rubric.split("출력 형식", 1)[-1].split("점검 질문", 1)[0])
        qs = _numbered(rubric.split("점검 질문", 1)[-1].split("점수 기준", 1)[0])
        if not 4 <= len(qs) <= 7:
            problems.append("%s 의 점검 질문이 %d개입니다(4~7개)." % (where, len(qs)))
        covered = set()
        for q in qs:
            m = QUESTION_PATTERN.match(q)
            if not m:
                problems.append("%s 의 점검 질문이 '(출력 N) …?' 꼴이 아닙니다: %s" % (where, q[:40]))
                continue
            for n in re.findall(r"\d+", m.group(1)):
                if not 1 <= int(n) <= len(outs):
                    problems.append("%s 의 점검 질문이 없는 출력 %s 를 가리킵니다." % (where, n))
                covered.add(int(n))
        missing = [str(i) for i in range(1, len(outs) + 1) if i not in covered]
        if missing:
            problems.append("%s 의 출력 %s 에 걸린 점검 질문이 없습니다." % (where, ", ".join(missing)))
        anchors = [l[2:] for l in rubric.split("점수 기준", 1)[-1].split("\n\n", 1)[0].strip().split("\n")]
        if len(anchors) != 4 or any(not a.startswith(lab) for a, lab in zip(anchors, ANCHOR_LABELS)):
            problems.append("%s 의 점수 기준이 8·9·9.5·10점 네 줄이 아닙니다." % where)
        elif any(not a.rstrip().endswith("니다.") for a in anchors):
            problems.append("%s 의 점수 기준이 합니다체로 끝나지 않습니다." % where)
        guard = sections.get("## Guardrail · 금지선", "")
        if len(re.findall(r"(?m)^- ", guard)) < 2:
            problems.append("%s 의 금지선에 역할 고유 줄이 없습니다." % where)
        for marker in BANNED_MARKERS:
            if marker in body:
                problems.append("%s 에 폐기한 표지 '%s' 가 있습니다." % (where, marker))
        if "`python " in body or "python scripts/" in body:
            problems.append("%s 이 python3 대신 python 을 부릅니다." % where)
        for m in ROLE_REF_PATTERN.finditer(body):
            rid = int(m.group(1))
            if rid in roles and not body[: m.start()].endswith(roles[rid]["ko"]):
                problems.append(
                    "%s 에서 '(%d)' 앞의 이름이 '%s' 가 아닙니다: …%s(%d)"
                    % (where, rid, roles[rid]["ko"], body[max(0, m.start() - 12): m.start()], rid)
                )
        for stale in STALE_ROLE_NAMES:
            if stale in body:
                problems.append("%s 에 옛 역할 이름 '%s' 가 남아 있습니다." % (where, stale))
        if key != "lead":
            handoff = next((l for l in sections["## Workflow · 작업 순서"].split("\n") if l.startswith("넘기는 곳:")), "")
            recv = next((l for l in sections["## Context · 맥락"].split("\n") if l.startswith("- 받는 것:")), "")
            for rid in sorted(nxt.get(int(key), ())):
                if "%s(%d)" % (roles[rid]["ko"], rid) not in handoff:
                    problems.append("%s 의 넘기는 곳에 팀 구성의 다음 단계 %s(%d) 가 없습니다." % (where, roles[rid]["ko"], rid))
            for rid in sorted(prev.get(int(key), ())):
                if "%s(%d)" % (roles[rid]["ko"], rid) not in recv:
                    problems.append("%s 의 받는 것에 팀 구성의 앞 단계 %s(%d) 가 없습니다." % (where, roles[rid]["ko"], rid))
    return problems


REBUTTAL_ID = 47


def check_harness_rules(harness):
    """팀 구성이 SKILL.md의 규칙을 어기는지 본다.

    - 비판적 검토자(47)는 게이트 자리에 두지 않는다(반박은 실행 단계에서, 반박 검토 토글로).
    - 분석 강화(deepAdd)는 이미 단계에 있는 역할을 다시 넣지 않고, 47을 넣지 않는다.
    """
    problems = []
    for h in harness["HARNESS"]:
        steps = [s["p"] for s in h["steps"]]
        if h["review"]["p"] == REBUTTAL_ID:
            problems.append("팀 구성 '%s' 가 비판적 검토자(47)를 게이트 자리에 둡니다." % h["name"])
        deep = h.get("deepAdd")
        if deep in steps:
            problems.append("팀 구성 '%s' 의 분석 강화(%s)가 이미 단계에 있는 역할입니다." % (h["name"], deep))
        if deep == REBUTTAL_ID:
            problems.append("팀 구성 '%s' 의 분석 강화가 비판적 검토자(47)입니다. 반박은 반박 검토 토글로 켭니다." % h["name"])
    return problems


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

    problems += check_inline_ids(roles)
    problems += check_section_ranges(roles, sections)
    problems += check_harness_rules(harness)
    problems += check_prompt_structure(roles, prompts, harness)

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
