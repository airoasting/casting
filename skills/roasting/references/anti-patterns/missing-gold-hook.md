# MISSING_GOLD_HOOK

**검출 방법:** Haiku judge.

**트리거:** 케이스 정의의 GOLD 합격선 장면이 산출물 첫 200자(또는 슬라이드 1장)에 살아있지 않음.

**적용 범위:** 전 케이스.

**검출 시 BLACK 재작성 지시:**
> "이 케이스의 GOLD 합격선 장면은 '{gold_scenario}'이다. 첫 200자/슬라이드 1장에 그 장면이 살아있게 다시 쓰라. 누락된 측면: {missing_aspect}."
