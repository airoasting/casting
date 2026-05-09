# TONE_MISMATCH

**검출 방법:** Haiku judge — BLACK 캐스팅 톤 vs 산출물 첫 문장 어휘 거리.

**트리거:** tone_match_score < 6 (1-10 척도, 10 = 완벽 일치).

**적용 범위:** 전 케이스.

**검출 시 BLACK 재작성 지시:**
> "BLACK 캐스팅 톤은 '{black_tone}'이다. 산출물 첫 문장의 어휘가 이 톤과 일치하도록 재작성하라."
