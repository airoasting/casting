# ChatGPT에서 쓰기 (Custom GPT 셋업)

`/casting`은 Claude Code 스킬이지만, ChatGPT에서는 **Custom GPT**로 같은 동작을 쓸 수 있다. ChatGPT엔 서브에이전트가 없어 실행은 단일 모델 순차 모드로 돌아가고(스킬의 폴백 모드), 게이트는 "냉정 재독" 독립 검토로 동작한다.

## 5분 셋업

1. chatgpt.com → 왼쪽 사이드바 **GPT 탐색 → 만들기**(또는 Projects의 사용자 지정 지침). ChatGPT Plus/Team/Enterprise 필요.
2. **Configure 탭**으로 간다.
   - **Name**: `에이전트 팀 빌더 (Casting)`
   - **Description**: 목적을 주면 검증된 50명으로 팀을 짜 실행하고 9.5 검토를 통과한 결과물을 내는 빌더.
   - **Instructions**: `INSTRUCTIONS.md`의 `---` 아래 본문 전체를 붙여 넣는다.
3. **Knowledge** 에 아래 4개 파일을 업로드한다(repo `references/`에서 가져옴):
   - `catalog.md` — 50명 부품 표
   - `harnesses.md` — 12 레시피 + 토글
   - `agent-prompts.md` — 50명 전체 시스템 프롬프트(실행용)
   - `execution-modes.md` — 실행·검토 가이드
4. **Capabilities**: **Web Search(브라우징)** 를 켠다. 리서치·팩트 단계가 실제 출처를 달 수 있게 하는 핵심이다. (Code Interpreter는 선택.)
5. 저장(Create) → Only me 또는 공유 범위 선택.

## 쓰는 법

대화창에 목적만 적으면 된다.

```
경쟁사 3곳을 분석해서 이사회용 보고서 만들어줘. 우리는 상업용 부동산 디벨로퍼야.
```

GPT가 팀을 설계해 보여 주고, 각 역할을 순서대로 수행한 뒤, 검토 통과본을 낸다.

## Claude와 다른 점 (정직하게)

| | Claude Code (`/casting`) | ChatGPT (Custom GPT) |
|---|---|---|
| 실행 | 팀원이 **독립 에이전트**(서브에이전트/팀), 병렬 가능 | 단일 모델이 역할을 **순차 연기** |
| 검토 게이트 | **독립 검토자 에이전트**(진짜 독립) | 같은 모델이 입장 바꿔 "냉정 재독"(독립성은 약함, 그래서 더 깐깐히) |
| 참조 로딩 | `references/` 온디맨드 | Knowledge 파일 검색 |
| 리서치 | WebSearch/WebFetch | 브라우징(켰을 때) |

핵심 가치(검증된 50 부품·레시피·9.5 게이트·자사 도구 안내)는 두 플랫폼에서 동일하다. 차이는 "실행을 진짜 여러 에이전트가 나눠 하느냐, 한 모델이 순서대로 하느냐"다.

## 업데이트

repo의 `references/` 4개 파일이 바뀌면, Custom GPT의 Knowledge 파일도 다시 올리면 된다. Instructions가 바뀌면 `INSTRUCTIONS.md`를 다시 붙여 넣는다.
