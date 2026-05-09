from scripts.anti_patterns import _missing_gold_hook


def test_missing_preview_two_lines(fake_judge):
    judge = fake_judge({"gold_hook_alive": False, "missing_aspect": "미리보기 두 줄에 의도 없음"})
    result = _missing_gold_hook(
        text="안녕하세요. 잘 지내십니까. 다름이 아니라 지난 미팅에서 말씀드린 건과 관련하여 ...",
        gold_scenario="화요일 오후 4시, 거래처 부장이 미리보기 두 줄로 답을 정한다.",
        judge=judge,
    )
    assert result is not None
    assert result.name == "MISSING_GOLD_HOOK"


def test_missing_decision_request(fake_judge):
    judge = fake_judge({"gold_hook_alive": False, "missing_aspect": "결정 요청 없음"})
    result = _missing_gold_hook(
        "분기 결과를 정리했습니다. 자세한 내용은 다음과 같습니다 ...",
        "보드 멤버가 첫 슬라이드로 의사결정 안건을 인지한다.",
        judge,
    )
    assert result is not None


def test_three_more_positive(fake_judge):
    """Add 3 more positive variants — board memo opening that buries lede,
    investor letter without quarter snapshot, internal announcement without action."""
    judge = fake_judge({"gold_hook_alive": False, "missing_aspect": "리드 묻힘"})
    for text, scenario in [
        ("회사 전반에 대해 말씀드리고 싶은 것이 있어 ...",
         "보드 멤버가 1분 안에 결론 인지"),
        ("Dear LP, hope this finds you well. We have many updates ...",
         "LP가 첫 단락에 분기 핵심 수치를 본다"),
        ("동료 여러분, 늘 수고가 많으십니다. 다름이 아니라 ...",
         "사원이 첫 줄에 변경 사항 인지"),
    ]:
        result = _missing_gold_hook(text, scenario, judge)
        assert result is not None


def test_two_clean_cases(fake_judge):
    judge = fake_judge({"gold_hook_alive": True, "missing_aspect": ""})
    for text, scenario in [
        ("[8/12 회신 요망] 8월 출시 전 계약 조항 1번 승인 여부 회신 부탁드립니다.",
         "거래처 부장이 미리보기 두 줄로 답을 정한다."),
        ("Q2 ARR 12.4M (+34% YoY). 2가지 결정 안건. ...",
         "보드 멤버가 1분 안에 결론 인지"),
    ]:
        assert _missing_gold_hook(text, scenario, judge) is None


def test_three_more_clean(fake_judge):
    judge = fake_judge({"gold_hook_alive": True, "missing_aspect": ""})
    for text, scenario in [
        ("Dear LP — Q2 IRR 18.2%. Three portfolio updates inside.",
         "LP가 첫 단락에 분기 핵심 수치를 본다"),
        ("[조직개편 공지] 5/15부 영업본부 → 사업본부로 통합. 본인 소속 변동 표는 본문 1번.",
         "사원이 첫 줄에 변경 사항 인지"),
        ("'우리는 이길 수 있다' — Q2 결산 전 모든 팀이 봐야 할 한 페이지.",
         "임원이 첫 슬라이드 한 줄로 동기 부여"),
    ]:
        assert _missing_gold_hook(text, scenario, judge) is None
