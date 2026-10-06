# Codex에서 쓰기

`/casting`은 Claude Code 스킬이지만 SKILL.md 표준을 따르기 때문에, 같은 파일을 그대로 Codex CLI에 설치해 쓸 수 있다.

## 설치

```bash
git clone https://github.com/airoasting/casting.git
mkdir -p ~/.codex/skills/casting
cp -r casting/{SKILL.md,README.md,LICENSE,NOTICE,references,platforms,scripts} ~/.codex/skills/casting/
```

프로젝트 하나에서만 쓰려면 `~/.codex/skills/casting` 대신 `<your-project>/.codex/skills/casting`에 둔다. 새 세션을 시작하면 Codex가 SKILL.md의 `description`을 읽고, 요청이 걸릴 때 알아서 불러온다.

설치를 확인한다.

```bash
ls ~/.codex/skills/casting/SKILL.md
```

## Claude Code와 다른 점

| | Claude Code | Codex |
|---|---|---|
| 발동 | `/casting` 또는 설명 매칭 | 설명 매칭 |
| 팀원 실행 | `Agent` 도구로 서브에이전트 | Codex 서브에이전트(GPT-5.6부터) |
| 워크스페이스 | `_workspace/`에 파일로 배치 | 같음(파일시스템 있음) |
| 리서치 | WebSearch·WebFetch | Codex의 검색 도구 |
| 병렬 결과 회수 | 포그라운드 `Agent`(`run_in_background: false`) | 서브에이전트 결과를 기다려 받는 방식 |
| 2차 검토 | 새 `Agent` 호출 | 새 서브에이전트 |

도구 이름만 다르고 하는 일은 같다. 서브에이전트를 쓸 수 없는 Codex 환경이면 폴백(순차 역할극)으로 떨어지고, 이때 검토는 독립이 아니므로 검토 줄에 `(자기검토 · 독립 아님)`이 붙는다. 스킬의 "실행 모드"는 그 환경에서 쓸 수 있는 도구를 위에서부터 고르게 되어 있어서, Codex에서는 서브에이전트 모드로 걸린다. 팀원 50명과 팀 구성 28개, 9.5 게이트는 동일하다.

## 업데이트

저장소를 다시 받아 같은 경로에 덮어쓴다. `references/`는 사이트 정본에서 생성되므로 따로 손대지 않는다. 설치본에는 `docs/`가 없으므로 `scripts/sync_refs.py`는 설치본에서 돌리지 않고 저장소 원본에서만 돌린다.
