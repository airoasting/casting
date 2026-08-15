# Casting · 에이전트 팀 빌더 (실행 엔진)

**한국어** · [English](./README.en.md)

![Version](https://img.shields.io/badge/Version-1.1.1-2ea44f)
![License](https://img.shields.io/badge/License-Apache%202.0-1f6feb)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-8957e6)
![Agents](https://img.shields.io/badge/Agents-50%20Verified-d2691e)
![Mode](https://img.shields.io/badge/Mode-Agent%20Teams-2ea44f)
![Native](https://img.shields.io/badge/Native-Claude%20Code-8957e6)
![Also on](https://img.shields.io/badge/Also%20on-ChatGPT-555555)
[![Live](https://img.shields.io/badge/Live-50agents.airoasting.com-FF6FB5)](https://50agents.airoasting.com)

[![에이전트 팀 빌더 미리보기](docs/assets/thumbnail/preview.png)](https://50agents.airoasting.com)

> 하고 싶은 일을 한 줄로 말하면 50명 중에서 팀을 짭니다. 그 팀을 **실제로 돌려서** 검토를 통과한 결과물까지 냅니다. Claude Code 스킬입니다.
>
> **v1.1.1 (2026-08-15)** · 역할 번호를 한 곳에서만 관리합니다. `scripts/sync_refs.py`가 `references/`를 만듭니다. 팀원 이미지 고지와 외부 에셋 출처(`NOTICE`)를 넣었습니다.
>
> **v1.1.0 (2026-07-12)** · 회사처럼 10개 본부로 개편했습니다. 디자인·마케팅·법무·감사·인사 직군을 새로 넣었고, 디자인 역할은 실제 이미지를 냅니다.

**라이브 데모**: [50agents.airoasting.com](https://50agents.airoasting.com). 50명 카탈로그와 팀 빌더를 브라우저에서 바로 봅니다.

AI ROASTING이 5색 다관점 채점으로 검증한 역할 프롬프트 50개와 팀 레시피 28개가 들어 있습니다. 사용자는 무엇을 만들지만 말합니다. 누가 어떤 순서로 할지는 팀장이 정하고 끝까지 끌고 갑니다.

**Claude Code에서 가장 잘 돕니다.** 팀원이 각각 독립 에이전트로 돌고 검토자도 따로 뜹니다. 그래서 9.5 게이트가 제일 세게 걸립니다. [ChatGPT에서도 쓸 수 있습니다](#chatgpt에서-쓰기). 이때는 한 모델이 역할을 순서대로 맡습니다.

## 무엇을 하나

목적 입력 → ① 목적 파악 → ② 팀 설계 → ③ 팀 구조 제시 → ④ 실행 → ⑤ 검토(9.5 게이트) → 최종 결과.

- **부품(Agent) 50개**. 역할 하나짜리 시스템 프롬프트입니다. 전부 9.5 합격선을 넘겼습니다.
- **레시피(Harness) 28개**. 부품을 이어 붙인 팀입니다. 리서치 보고서, 시장 분석, 재무 리뷰, 발표자료, 전략, 회의 정리 같은 것들이 있습니다.
- **라우터**. 목적을 받아 레시피를 고르거나 부품을 새로 조합합니다. 여기가 이 스킬의 핵심입니다.

## 팀원 50명 (부품 카탈로그)

목적에 따라 아래 50개 역할에서 팀을 뽑습니다. 회사처럼 **10개 본부**로 나눴고, 번호는 본부 순서를 따릅니다.

> 사이트와 이 문서에 나오는 팀원 얼굴은 **ChatGPT로 만든 가상 인물**입니다. 실제 사람이 아닙니다.

### 1. 전략기획실
| # | 직책 | English | 하는 일 |
|---|---|---|---|
| 1 | 경영전략가 | Management Strategist | 전사·경쟁 전략과 시장 포지셔닝을 설계합니다 |
| 2 | 신규사업 개발 | New Business Developer | 신사업 기회를 발굴하고 사업모델을 설계합니다 |
| 3 | 사업 타당성 분석가 | Feasibility Analyst | 수익성·리스크로 사업 타당성을 검증합니다 |
| 4 | 제품 기획자 | Product Manager | 요구사항과 로드맵을 PRD로 정리합니다 |
| 5 | 프로젝트·목표 기획자 | Project & OKR Planner | 실행 계획·일정·OKR을 설계합니다 |

### 2. 리서치랩
| # | 직책 | English | 하는 일 |
|---|---|---|---|
| 6 | 리서치 어시스턴트 | Research Assistant | 주제를 조사해 핵심을 정리합니다 |
| 7 | 팩트·출처 검증가 | Fact & Source Checker | 주장·수치의 사실과 출처를 검증합니다 |
| 8 | 마켓 리서처 | Market Researcher | 시장과 산업 동향을 조사합니다 |
| 9 | 경쟁·동향 분석가 | Competitor Analyst | 경쟁·유사 사례를 분석합니다 |
| 10 | 데이터 분석가 | Data Analyst | 데이터에서 패턴과 인사이트를 찾습니다 |
| 11 | 트렌드·인사이트 분석가 | Trend & Insight Analyst | 흐름과 인사이트를 짚어냅니다 |

### 3. 마케팅본부
| # | 직책 | English | 하는 일 |
|---|---|---|---|
| 12 | 콘텐츠 마케터 | Content Marketer | 오가닉 콘텐츠 주제와 서사를 기획합니다 |
| 13 | SEO·GEO 전략가 | SEO & GEO Strategist | 검색·AI 노출을 최적화합니다 |
| 14 | 소셜미디어 전략가 | Social Media Strategist | 채널 운영과 콘텐츠 캘린더를 짭니다 |
| 15 | 퍼포먼스·광고 전략가 | Performance Ad Strategist | 유료 광고와 전환을 설계합니다 |
| 16 | 카피라이터 | Copywriter | 광고·세일즈 카피를 벼립니다 |
| 17 | 이메일·CRM 마케터 | Email & CRM Marketer | 뉴스레터·리텐션을 설계합니다 |
| 18 | VOC·설문 분석가 | VOC & Survey Analyst | 고객의 목소리와 설문을 분석합니다 |

### 4. 디자인본부
| # | 직책 | English | 하는 일 |
|---|---|---|---|
| 19 | 슬라이드 디자이너 | Slide Designer | 발표 슬라이드 비주얼을 생성합니다 |
| 20 | 인포그래픽·차트 디자이너 | Infographic Designer | 데이터를 시각화합니다 |
| 21 | 카드뉴스 제작자 | Card News Creator | SNS 카드뉴스를 만듭니다 |
| 22 | 브랜드·비주얼 가디언 | Brand & Visual Guardian | 톤·아이덴티티와 비주얼을 지킵니다 |
| 23 | 이미지 생성 | Image Generator | 필요한 이미지를 생성합니다 |
> 디자인본부 5명은 gpt-image로 프롬프트를 만들고 OpenAI 이미지 API로 실제 이미지 파일을 냅니다. API 키가 없으면 완성된 프롬프트만 줍니다.

### 5. 콘텐츠제작본부
| # | 직책 | English | 하는 일 |
|---|---|---|---|
| 24 | 보고서 작성가 | Report Writer | 보고서 초안을 작성합니다 |
| 25 | 제안서·지원사업 작성가 | Proposal & Grant Writer | 제안서·지원사업 양식을 작성합니다 |
| 26 | 이메일·업무 서신 작성 | Business Correspondence Writer | 업무 이메일과 서신을 작성합니다 |
| 27 | 요약·브리핑 담당 | Summarizer | 긴 문서를 핵심만 요약합니다 |
| 28 | 교정·윤문 담당 | Copy Editor | 문장을 다듬고 교정합니다 |
| 29 | 번역·현지화 담당 | Translator | 번역하고 자연스럽게 다듬습니다 |

### 6. 커뮤니케이션·PR본부
| # | 직책 | English | 하는 일 |
|---|---|---|---|
| 30 | PR·언론 홍보 | PR & Media Relations | 보도자료와 미디어 대응을 맡습니다 |
| 31 | 대외 응대 | Customer Response | 문의와 클레임에 답변을 작성합니다 |
| 32 | 사내 커뮤니케이션 | Internal Comms | 사내 공지와 안내를 작성합니다 |
| 33 | 발표·스피치 작성 | Speech Writer | 발표·연설문을 씁니다 |
| 34 | 협상·이해관계자 대응 | Negotiation & Stakeholder | 협상 시나리오를 준비합니다 |

### 7. 재무본부
| # | 직책 | English | 하는 일 |
|---|---|---|---|
| 35 | 재무 분석가 | Financial Analyst | 재무제표를 읽고 시나리오를 모델링합니다 |
| 36 | 예산·비용 관리 | Budget & Cost Manager | 예산을 편성하고 비용 구조를 봅니다 |
| 37 | IR·투자자 리포트 | Investor Reporter | 투자자·이사회용 보고를 작성합니다 |
| 38 | KPI 추적 | KPI Tracker | 핵심 지표를 추적하고 정리합니다 |
| 39 | 리스크 분석가 | Risk Analyst | 재무·사업 위험을 식별하고 평가합니다 |
| 40 | 회계사 | Certified Accountant | 세무·회계 처리를 돕습니다 |

### 8. 인사본부
| # | 직책 | English | 하는 일 |
|---|---|---|---|
| 41 | 채용 담당 | Recruiter | 채용 공고와 면접 질문을 준비합니다 |
| 42 | 노무사 | Labor Attorney | 인사·근로·노무를 돕습니다 |
| 43 | 성과·보상 설계 | Comp & Performance Designer | 평가·보상 제도를 설계합니다 |

### 9. 법무·감사실
| # | 직책 | English | 하는 일 |
|---|---|---|---|
| 44 | 변호사 | Legal Counsel | 계약·법률 리스크를 검토합니다 |
| 45 | 감사인 | Auditor | 내부감사·준법·통제를 점검합니다 |
| 46 | 문서·품질 검수 | Document & Quality Reviewer | 계약·문서·산출물을 검수합니다 |
| 47 | 비판적 검토자 | Devil's Advocate | 결론을 반박해 약점을 찾습니다 |
> 회계사·변호사·감사인·노무사는 초안과 1차 검토를 돕습니다. 법률·세무·노무 자문이 아닙니다. 최종 판단은 자격을 가진 전문가에게 확인하십시오.

### 10. 운영자동화본부
| # | 직책 | English | 하는 일 |
|---|---|---|---|
| 48 | 프로세스 설계자 | SOP & Process Designer | 표준 업무 절차를 문서화합니다 |
| 49 | 자동화 설계자 | Automation Architect | 반복 업무·리포트를 자동화합니다 |
| 50 | 업무·일정 조율가 | Work & Schedule Orchestrator | 일정·할일·메일을 조율합니다 |

> 팀장(오케스트레이터)은 이 50명에 들어가지 않습니다. 부품을 고르고 순서를 정하고 실행과 검토를 지휘합니다.

## 설치

저장소를 클론하고 스킬 파일만 Claude Code 스킬 폴더로 복사합니다. 스킬 파일은 저장소 루트에 있습니다. 데모 웹사이트는 `docs/`에 있습니다.

```bash
git clone https://github.com/airoasting/casting.git
# 모든 프로젝트에서 쓰려면 사용자 레벨(~/.claude/skills)
mkdir -p ~/.claude/skills/casting
cp -r casting/{SKILL.md,README.md,LICENSE,NOTICE,references,platforms,scripts} ~/.claude/skills/casting/
```

프로젝트 하나에서만 쓰려면 `~/.claude/skills/casting` 대신 `<your-project>/.claude/skills/casting`에 복사합니다. Claude Code를 다시 켜면 `/casting`으로 부를 수 있습니다.

## 사용법

```
/casting 경쟁사 3곳을 분석해서 이사회용 보고서 만들어줘
```

"팀 짜줘", "이거 팀으로 해줘"라고 해도 되고, 보고서·분석·발표자료·제안서·재무검토·회의정리 같은 결과물을 만들어 달라고 해도 됩니다. 누가 필요한지는 몰라도 됩니다.

## 실행 모드 (티어드)

쓸 수 있는 도구에 따라 위에서부터 고릅니다.

1. **에이전트 팀**. `TeamCreate`·`SendMessage`·`TaskCreate`를 쓸 수 있을 때입니다. 팀원이 공유 작업목록으로 알아서 조율합니다.
2. **서브에이전트**. `Agent` 도구만 있으면 됩니다. 이어지는 단계는 순서대로, 서로 상관없는 단계는 한꺼번에 돌립니다. 기본값입니다.
3. **순차 역할극**. 에이전트 도구가 아예 없을 때만 씁니다. 팀장이 역할을 순서대로 맡습니다.

중요한 건 팀원이 **각자 다른 맥락**을 갖는다는 점입니다. 그래서 검토자가 자기 글을 채점하지 않습니다. 상관없는 단계는 동시에 돌아갑니다.

## 품질 게이트

검토자는 그 산출물을 만들지 않은 **별도 에이전트**입니다. 사용자의 원래 목적과 자료에 대고 결함부터 찾습니다. 결함이 하나라도 있으면 9.5를 주지 않고 그 단계로 돌려보냅니다. 한 번 보강한 뒤에 다시 봅니다. 실제 테스트에서 게이트는 첫 산출물을 6.5로 떨어뜨리고 다시 만들라고 했습니다.

## 실행 결과 (워크스페이스)

Claude Code에서 돌리면 그 실행의 팀과 산출물이 파일로 남습니다.

```
_workspace/
└── 20260628_01/             # {YYYYMMDD}_NN, 같은 날 재호출 시 _02·_03
    ├── team.md              # 빌드 시트: 목적·팀 구조·순서·토글
    ├── lead/                # 팀장(오케스트레이터)
    │   └── lead.md
    ├── agents/              # 배치된 팀원(역할 프롬프트 + 이번 io)
    │   ├── 1-research-assistant.md
    │   ├── 2-summarizer.md
    │   └── review-copy-editor.md
    └── output/              # 단계별 산출물 + 최종결과.md
```

팀이 한 번 쓰고 사라지지 않습니다. 나중에 다시 보거나 그대로 재사용합니다. ChatGPT 호환 모드는 파일시스템이 없어서 화면에만 보여 줍니다.

## ChatGPT에서 쓰기 (호환 모드)

기본은 Claude Code지만 **ChatGPT(Custom GPT)** 로도 같은 동작을 씁니다. 셋업은 `platforms/chatgpt/`에 있습니다.

- `platforms/chatgpt/INSTRUCTIONS.md`. Custom GPT의 Instructions 칸에 붙여 넣을 본문입니다.
- `platforms/chatgpt/SETUP.md`. 5분 셋업 안내입니다. Instructions를 붙여 넣습니다. `references/` 4개를 Knowledge로 올립니다. 브라우징을 켭니다.

ChatGPT에는 서브에이전트가 없습니다. 그래서 한 모델이 순서대로 돌고, 게이트는 냉정하게 다시 읽는 방식으로 걸립니다. 50 부품과 28 레시피, 9.5 게이트는 같습니다.

## 장착 도구

팀원 일부는 AI ROASTING이 만든 도구를 역할별로 들고 있습니다.

| 도구 | 용도 | 받는 팀원 |
|---|---|---|
| [전략 도구 갤러리](https://airoasting-strategy.vercel.app/) | 70개 컨설팅 프레임워크 | 경영전략·신규사업·사업 타당성 |
| [5color](https://5color.vercel.app/) | 5인 페르소나 검토 지침 생성 | 문서·품질 검수·비판적 검토·교정 |
| [슬라이드 라이브러리](https://airoasting-slide.vercel.app/) | 35개 HTML 슬라이드 템플릿 | 슬라이드 디자인·제안서 |
| [AI ROASTING 블로그](https://airoasting-blog.vercel.app/) | 글로벌 리서치 인사이트 | 리서치·트렌드·마켓 |
| [Hound](https://github.com/airoasting/hound) | 16개 채널 끈질긴 다채널 검색 | 리서치·팩트체크·마켓·경쟁분석·출처검증 |
| [스킬 라이브러리](https://airoasting-skill.vercel.app/) | 엄선된 실무 AI 스킬 | 자동화 설계자·프로세스 |
| [`dart` 스킬 (`/dart`)](https://github.com/airoasting/dart) | 상장사 DART 공시 재무 데이터 조회 → 인터랙티브 애널리스트 HTML 리포트(13인 투자자 평가) | 재무 분석가·IR·투자자 리포트·회계사·사업 타당성 |

## 구조

스킬 파일은 저장소 루트에, 데모 웹사이트는 `docs/`에 있습니다. `docs/`는 GitHub Pages로도 열리고, 라이브 도메인 [50agents.airoasting.com](https://50agents.airoasting.com)으로도 열립니다.

```
SKILL.md                   # 트리거 · 라우터 결정 사다리 · 실행 프로토콜 · 9.5 게이트
README.md                  # 이 문서 (한국어)
README.en.md               # 영어판
LICENSE                    # Apache License 2.0
NOTICE                     # 외부 폰트·아이콘 출처, 인용 출처, 생성 이미지 고지
references/                # scripts/sync_refs.py 가 docs/assets 에서 생성 (직접 수정 금지)
├── catalog.md             # 50명 부품 표(선발용)
├── harnesses.md           # 28 레시피 + 라우터 결정 사다리 + 토글
├── agent-prompts.md       # 50명 전체 시스템 프롬프트(실행용, id 구간으로 선택)
└── execution-modes.md     # 실행 모드 3종 · 실제 도구 호출 문법 · 검토자 템플릿
scripts/
├── sync_refs.py           # references/ 를 사이트 정본에서 재생성 (--check 로 정합 검사)
└── gen_image.py           # 디자인본부 역할의 실제 이미지 산출
platforms/
└── chatgpt/
    ├── INSTRUCTIONS.md    # Custom GPT Instructions 본문
    └── SETUP.md           # ChatGPT 셋업 가이드
docs/                      # GitHub Pages 데모 웹사이트 · 데이터 정본
├── index.html            # 팀 빌더 · 50명 카탈로그 · A 배열(역할 정본)
└── assets/               # prompts.js(프롬프트 정본) · router.js(레시피 정본) · agents · logos
```

## 데이터 정본과 동기화

역할 번호가 문서마다 다르면 엉뚱한 사람이 팀에 들어옵니다. 그래서 한 곳만 정본으로 두고 나머지는 거기서 만듭니다.

| 무엇 | 정본 |
|---|---|
| 50역할 번호·직책·본부·설명 | `docs/index.html`의 `A` 배열 |
| 50역할 + 팀장 시스템 프롬프트 | `docs/assets/prompts.js`의 `PROMPTS` |
| 28개 팀 레시피 | `docs/assets/router.js`의 `HARNESS` |

`references/`의 catalog·agent-prompts·harnesses는 위 정본에서 만듭니다. 역할이나 번호, 레시피를 고칠 때는 `docs/assets`만 고치고 아래를 돌립니다.

```bash
python3 scripts/sync_refs.py
```

어긋난 곳만 보려면 이렇게 씁니다. 어긋나 있으면 종료 코드 1로 알려 줍니다.

```bash
python3 scripts/sync_refs.py --check
```

카드 이미지 `docs/assets/agents/agent-N.png`는 역할 번호에 묶여 있습니다. 번호를 바꾸면 이미지도 같이 옮깁니다.

## 라이선스

Copyright 2026 AI ROASTING (Jayden Kang). [Apache License 2.0](./LICENSE)으로 배포합니다.

외부 폰트와 아이콘, 인용 출처, 생성 이미지 고지는 [NOTICE](./NOTICE)에 적어 두었습니다.
