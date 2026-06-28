# CLAUDE.md — 에이전트 팀 빌더 프로젝트

이 폴더는 **에이전트 팀 빌더 (Agent Team Builder)** 웹사이트 프로젝트다.
상위 `New Projects/CLAUDE.md`(SOUL/운영 지침)를 따르고, 이 문서는 이 프로젝트 한정 규칙이다.

## 1. 무엇인가
- 한 줄: 목표를 지정하면 검증된 **50명의 범용 에이전트 팀원**이 한 팀으로 꾸려지는 카탈로그 + 워크플로우 사이트.
- 하우스 브랜드: **AI ROASTING**. 제품명: **에이전트 팀 빌더**.
- 대상: 비즈니스 리더·화이트칼라·기자·사무직·재무 분석가 등 지식 노동자 일반.
- 핵심 IP: "목표 → 부품(역할) 조합" 라우터. 50개는 단일 역할(부품), 워크플로우는 부품을 handoff로 엮은 레시피.

## 2. 파일 구조
```
20260624_50가지 스킬/
├── index.html                 # 배포본(루트). 사용자가 여는 파일
├── assets/logos/              # 로고(logo1-transparent.png 사용)
├── CLAUDE.md                  # 이 문서
├── MEMORY.md                  # 변경 로그 (갱신 시마다 append)
├── PROJECT.md / PLAN.md / WORKFLOW_MAP.md   # 기획 정본
├── guides/                    # 부품/워크플로우 셋업 가이드 md (정본)
├── assets/prompts.js          # 50개 시스템 프롬프트(`var PROMPTS`). v31부터 HTML서 분리
├── _workspace/                # 프롬프트 평가기록(RED 정적 채점 등). v32부터
│   └── 2026-06-28_프롬프트-루브릭-평가.md
└── output/agent-team-builder/
    ├── v1.html ~ v{N}.html    # 라운드별 원본(편집 대상). 최신=v31
    ├── index.html             # 빌드 폴더 사본
    ├── assets/logos/          # 로고 사본(빌드 폴더에서 열 때용)
    ├── assets/prompts.js      # prompts.js 사본(빌드 폴더에서 열 때용)
    └── EVALUATION.md          # 라운드별 평가 로그
```

## 3. 수정 규칙 (중요)
1. **원본은 `output/agent-team-builder/v{N}.html`다.** 새 변경은 최신 v를 복사해 `v{N+1}.html`을 만들고 거기서 편집한다.
2. 편집 후 **반드시 두 곳에 동기화**한다:
   ```
   cp output/agent-team-builder/v{N}.html output/agent-team-builder/index.html
   cp output/agent-team-builder/v{N}.html ./index.html
   ```
3. `index.html`을 직접 편집하지 않는다(버전 추적이 깨진다).
4. **외부 의존 없음**(Pretendard CDN + 로컬 로고·로컬 `assets/prompts.js`만). CSS·UI 로직 JS는 HTML에 인라인. **단, 50개 시스템 프롬프트(`var PROMPTS`)는 v31부터 `assets/prompts.js`로 분리**(index.html 88KB로 경량화). 프롬프트 내용 수정은 **HTML이 아니라 `assets/prompts.js`에서** 한다. 분리는 반드시 `<script src>`(동기 로드) 방식 — `fetch`+json은 file:// CORS로 막혀 더블클릭 시 프롬프트가 전멸하므로 금지. 새 v를 만들 때 prompts.js를 건드렸으면 두 `assets/` 폴더에 같이 동기화한다.
5. 로고·prompts.js 경로는 `assets/...` 상대경로. 루트·빌드 폴더 양쪽에 assets가 있어야 깨지지 않는다.

## 4. 디자인 시스템 — 컬러 블록(네오브루탈리즘) · v25부터
(v24까지는 "람보르기니 라이트": 흰 배경·골드 #FFC000·둥근 모서리였음. v25에서 사용자 지시로 전면 교체.)
- 색: **파스텔 네온 5색** + 흑/백/오프화이트만. `--pink:#FE90E8 / --blue:#C0F7FE / --green:#99E885 / --yellow:#F7CB46 / --cream:#FFDC8B`, `--black:#000 / --white:#fff / --offwhite:#FFFDF5`. fill 위에 검정 글자만(다크 섹션=footer만 흰 글자). 새 hex·그라데이션 금지.
- 시그니처 토큰: 보더 **`4px solid #000`**(소형 3px), 그림자 **`8px 8px 0 #000`**(소형 `4px 4px 0`, blur 0 검정), **radius 0(직각)**. 모든 카드/박스/버튼은 보더+오프셋 그림자+직각.
- 폰트: 디스플레이/본문 **Pretendard**(weight 800~900), 모노 라벨 **Space Grotesk**(이미 Google Fonts import됨, line 17). 영문 라벨·메타·번호는 모노+대문자+자간.
- 헤딩은 포스터 디스플레이(짧고 굵게, 음수 자간). 풀쿼트 밴드는 **핑크 블록 + 흰 quote-frame**.
- 본문 가로 폭 **1200px**(`.wrap max-width`).
- 권위 레이어: `</head>` 직전 마지막 `<style>` 블록이 컬러 블록 스킨을 `!important`로 전부 덮는다. 람보르기니 블록의 `border-radius:*!important` 4줄은 0으로 바꿔 둠. 색 변경은 이 마지막 블록과 `:root`에서.
- 카드 배경색은 JS에서 `(id-1)%5`로 5색 순환(렌더 시 inline). 팀 노드는 `i%4`로 4색 순환.

## 5. 인터랙션
- 버튼/카드 호버: 네오브루탈 **눌림**(`transform:translate(-2~3px)` + 그림자 확대), active는 반대로 눌러 그림자 축소.
- 마우스 **다운**: 잉크 리플(`.ripple`), **오버**: 물결(`.hripple`) + 로고 회전은 기존 스크립트 유지(컬러 블록과 충돌 없음).
- `prefers-reduced-motion`이면 모두 비활성.

## 6. 콘텐츠
- 50 에이전트는 JS의 `A` 배열 `[id, 한국어직책, 설명, 섹션idx, type(A/B), 영문명]`.
- 8섹션: 리서치·정보 / 분석·인사이트 / 재무·숫자 / 글쓰기·문서 / 커뮤니케이션 / 기획·전략 / 생산성·자동화 / 검토·품질.
- 워크플로우는 `WORKFLOWS`(목표명 → id 배열). 대표: "리서치 보고서 완성".
- A/B(혼자/도구) 표시는 화면에서 제거됨. type 필드는 데이터에만 남김.
- v25부터 카드·모달의 **픽셀 아바타 제거**(인물 일러스트 없음). `pixelAvatar()` 함수는 코드에 남아 있으나 미사용. 카드는 번호 배지(01~50)+직책+영문 모노+설명+섹션 라벨 구조. (현재 카드·모달은 `assets/agents/agent-N.png` 실제 캐릭터 흉상을 함께 표시.)
- **팀장 · 오케스트레이터(v36)**: 카탈로그 50명 그리드 **바로 위**에 단독 스포트라이트 블록(`#leadSpot`, `.lead-spot`). `assets/agents/lead.png`(반신·노트북 구도) + 특성 1문단 + 클릭 시 `openLeadModal()`로 팀장 프롬프트 모달. 팀장 프롬프트는 `assets/prompts.js`의 **`lead` 키**(숫자 1~50과 분리). **원칙: 50=부품(흉상 그리드), lead=라우터/오케스트레이터(별도 블록). 둘을 같은 그리드에 섞지 않는다 — lead를 51번째 카탈로그 카드로 넣지 않는다.**

## 7. 품질 루프
- 제작=PINK/BLACK, 평가=RED. `EVALUATION.md`에 라운드별 기록.
- UIUX 평가는 MECE 5차원(정보구조·내비 / 시각·타이포 / 인터랙션·피드백 / 콘텐츠·카피 / 접근성·반응형), 합격선 9.5.
- **프롬프트 품질 루프(v33부터)**: 각 프롬프트의 `## 품질 기준`은 **공통 5차원** 0~10 채점표다(정확성·근거 / 목적·완결성 / 구조·형식 / 실행력 / 언어·톤, 50개 전원 동일). 총점=5평균, 합격선 9.5, 9.5 미만이면 자가수정 후 산출물 끝에 `자기평가:` 줄로 점수를 남긴다. 프롬프트 자체의 정적 RED 채점 기록은 `_workspace/`에 둔다(런타임 산출물 점수와 구분). (v32에서 역할 고유 6번째 차원을 썼다가 v33에서 5차원으로 통일.)

## 8. MEMORY.md 규칙
- **변경할 때마다 `MEMORY.md` 맨 위 로그에 한 줄 추가**한다(날짜 + 버전 + 무엇을 바꿨는지). 과거 기록은 지우지 않는다.
