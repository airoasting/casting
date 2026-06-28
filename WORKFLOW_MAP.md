# 50 B2B Agents → 워크플로우 오케스트레이션 맵 (초안 v0.1)

## 목적

50개의 역할(에이전트)을 그냥 나열하지 않고, **결과 중심 파이프라인 8개**로 묶는다.
- 가로축은 B2B 매출 생애주기(타겟 정의 → 발굴 → 접촉 → 수주 → 유지)다.
- 콘텐츠 엔진과 운영/계측은 이 흐름을 가로지르는(cross-cutting) 두 축이다.
- 각 워크플로우 끝의 산출물은 **5color로 검수**한다. 50 Agents가 실행, 5color가 채점.

## 전체 흐름

```
[WF6 콘텐츠·수요 엔진] ─────── 인바운드 유입 ───────┐
                                                  ▼
WF1 타겟정의 → WF2 발굴 → WF3 정제·점수 → WF4 접촉·전환 → WF5 영업·수주 → WF7 온보딩·유지
                                                  ▲
[WF8 운영·계측] ──── SOP·자동화·리포트로 전 구간 지원 ──┘
```

---

## WF1. ICP & 시장 인텔리전스 — "누구를 노릴지 정의"

| # | 에이전트 | 역할 |
|---|---|---|
| 11 | ICP Finder | 이상 고객 프로필 정의 |
| 42 | Market Research | 시장 규모·세그먼트 |
| 2 | Competitor Analysis | 경쟁 지형 |
| 35 | Industry Monitoring | 산업 동향 추적 |
| 16 | Trend Detector | 트렌드 포착 |
| 8 | Social Listening | 소셜 신호 청취 |
| 27 | Keyword Hunter | 키워드 발굴 |

**산출물**: 타겟 정의서 + 시장 지형도 → 5color 검수(전략 보고서 모드)

## WF2. 프로스펙팅 & 리드 소싱 — "리드를 찾아 긁기"

| # | 에이전트 | 역할 |
|---|---|---|
| 1 | Lead Research | 리드 리서치 |
| 5 | Lead Scraper | 리드 수집 |
| 25 | LinkedIn Prospector | 링크드인 발굴 |
| 26 | YouTube Prospector | 유튜브 발굴 |
| 23 | Instagram Lead Generator | 인스타 발굴 |
| 24 | TikTok Lead Hunter | 틱톡 발굴 |

**산출물**: 원천 리드 리스트(채널별)

## WF3. 리드 정제 & 스코어링 — "정제하고 점수 매기기"

| # | 에이전트 | 역할 |
|---|---|---|
| 14 | Inbound Lead Enrichment | 인바운드 리드 보강 |
| 37 | Lead Scoring | 점수화 |
| 33 | Lead Qualification | 자격 판별 |
| 21 | Chatbot Qualifier | 챗봇 1차 검증 |
| 22 | DM Analyzer | DM 의도 분석 |

**산출물**: 우선순위가 매겨진 리드(핫/웜/콜드)

## WF4. 아웃리치 & 전환 — "접촉해서 미팅까지"

| # | 에이전트 | 역할 |
|---|---|---|
| 6 | Hook Writer | 후킹 문구 작성 |
| 19 | Hook Analyzer | 후킹 성능 분석 |
| 17 | Cold Outreach Crafter | 콜드 아웃리치 설계 |
| 9 | Email Writer + Enricher | 이메일 작성·보강 |
| 30 | Outreach Management | 시퀀스 관리 |
| 28 | Inbox Handler | 인박스 처리 |
| 36 | Inquiry Handler | 문의 응대 |
| 45 | Meeting Prep | 미팅 준비 |
| 34 | Pitching | 피칭 |

**산출물**: 예약된 미팅 + 대화 → 5color 검수(이메일·피칭 모드)

## WF5. 영업 & 수주 — "관리하고 제안하고 클로징"

| # | 에이전트 | 역할 |
|---|---|---|
| 43 | Proposal Builder | 제안서 작성 |
| 31 | Sales Management | 영업 관리 |
| 32 | Sales Insights | 영업 인사이트 |
| 29 | Briefing | 브리핑 |
| 44 | CRM Update | CRM 갱신 |

**산출물**: 제안서·수주 + 갱신된 CRM → 5color 검수(제안서 모드)

## WF6. 콘텐츠 & 수요 엔진 (Cross-cutting) — "콘텐츠로 인바운드 만들기"

| # | 에이전트 | 역할 |
|---|---|---|
| 12 | Content Curator | 콘텐츠 큐레이션 |
| 15 | Content Repurposer | 재가공 |
| 13 | Content Reviewer | 콘텐츠 검수 |
| 18 | Social Media | 소셜 운영 |
| 20 | LinkedIn Content Engine | 링크드인 콘텐츠 |
| 38 | Marketing Copywriter | 마케팅 카피 |
| 41 | Lead Magnet Generator | 리드 마그넷 |
| 39 | Marketing Performance | 성과 측정 |

**산출물**: 발행 콘텐츠 + 인바운드 유입(→ WF3로 연결) → 5color 검수(콘텐츠 모드)

## WF7. 고객 성공 & 유지 — "온보딩·유지·확장"

| # | 에이전트 | 역할 |
|---|---|---|
| 10 | Client Onboarding | 온보딩 |
| 46 | Customer Success | 고객 성공 |
| 40 | Customer Feedback | 피드백 수집 |
| 3 | Review | 리뷰 확보 |
| 49 | Partnership Research | 파트너십 발굴 |

**산출물**: 유지·확장 + 레퍼럴/파트너십

## WF8. 운영 & 계측 (Cross-cutting) — "표준화·자동화·리포트"

| # | 에이전트 | 역할 |
|---|---|---|
| 47 | SOP Builder | 표준 운영 절차 |
| 48 | Workflow Automation | 워크플로우 자동화 |
| 50 | Reporting | 리포팅 |
| 4 | Website Analysis | 웹사이트 분석 |
| 7 | CRO Analysis | 전환율 분석 |

**산출물**: 운영 표준 + 통합 리포트(전 구간 KPI)

---

## 검증 메모

- 50개 전수 매핑(중복 없음): WF1=7, WF2=6, WF3=5, WF4=9, WF5=5, WF6=8, WF7=5, WF8=5 → 합 50.
- 9번(Email Writer + Enricher)은 enrich보다 write 비중으로 WF4에 배치. 보강 기능은 WF3 14번과 연계.
- 5color 연결점은 "사람이 읽는 산출물"이 나오는 노드(WF1·4·5·6)에 우선 건다.

## 다음 결정

1. 8개 묶음 단위가 맞는지(더 굵게 5개로? 더 잘게?) 사용자 확정.
2. 확정되면 → 이 맵을 인터랙티브 사이트 or 스킬로 구현.
