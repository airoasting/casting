from scripts.anti_patterns import _tone_mismatch


def test_friendly_against_consulting_tone(fake_judge):
    judge = fake_judge({"tone_match_score": 3, "reason": "친근체와 컨설팅 단정 톤 거리 큼"})
    result = _tone_mismatch(
        "안녕하세요~ 오랜만이에요!",
        "베인 컨설턴트 응답 메일 톤. 본론 한 줄로 시작.",
        judge,
    )
    assert result is not None
    assert result.name == "TONE_MISMATCH"


def test_casual_against_legal_tone(fake_judge):
    judge = fake_judge({"tone_match_score": 2, "reason": "캐주얼 vs 법무 격식"})
    result = _tone_mismatch(
        "음 이거 좀 봐줘",
        "사외 변호사 18년차. 격식 격조 유지.",
        judge,
    )
    assert result is not None


def test_overformal_against_internal_announce(fake_judge):
    judge = fake_judge({"tone_match_score": 4, "reason": "사내 공지에 과한 격식"})
    result = _tone_mismatch(
        "삼가 알려드립니다. 부복(俯伏)하건대 ...",
        "사내 공지 — 동료에게 말하듯 솔직하고 가까운 톤",
        judge,
    )
    assert result is not None


def test_two_more_mismatches(fake_judge):
    judge = fake_judge({"tone_match_score": 3, "reason": "톤 거리"})
    for text, tone in [
        ("Yo team, what's up?", "분기 IR 정중·격조"),
        ("쩌는 결과가 나왔어요!", "감사 의견서 — 객관·중립 톤"),
    ]:
        assert _tone_mismatch(text, tone, judge) is not None


# --- Negative cases (matching tone) ---

def test_consulting_match_clean(fake_judge):
    judge = fake_judge({"tone_match_score": 9, "reason": ""})
    assert _tone_mismatch(
        "결론: 1안 승인 부탁드립니다.",
        "베인 컨설턴트 응답 메일 톤. 본론 한 줄로 시작.",
        judge,
    ) is None


def test_legal_match_clean(fake_judge):
    judge = fake_judge({"tone_match_score": 8, "reason": ""})
    assert _tone_mismatch(
        "본 의견서는 2026.5.10. 검토 결과를 정리한다.",
        "사외 변호사 18년차. 격식 격조 유지.",
        judge,
    ) is None


def test_internal_match_clean(fake_judge):
    judge = fake_judge({"tone_match_score": 8, "reason": ""})
    assert _tone_mismatch(
        "팀, 이번 주에 한 가지 정해야 할 게 있어.",
        "사내 공지 — 동료에게 말하듯 솔직하고 가까운 톤",
        judge,
    ) is None


def test_two_more_clean(fake_judge):
    judge = fake_judge({"tone_match_score": 9, "reason": ""})
    for text, tone in [
        ("Q2 ARR 12.4M (+34% YoY).", "분기 IR 정중·격조"),
        ("당사는 다음 사항을 확인하였다.", "감사 의견서 — 객관·중립 톤"),
    ]:
        assert _tone_mismatch(text, tone, judge) is None
