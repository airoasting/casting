import pytest

from scripts.anti_patterns import _legal_risk_term


@pytest.fixture
def _():
    return None


def test_guarantee_in_legal(_):
    assert _legal_risk_term("당사는 보장합니다.", "법무 검토·규제 대응") is not None


def test_certainly_in_external_comm(_):
    assert _legal_risk_term("확실히 답변드리겠습니다.", "외부 커뮤니케이션") is not None


def test_absolute_in_legal(_):
    assert _legal_risk_term("절대로 누설하지 않겠습니다.", "법무 검토·규제 대응") is not None


def test_100pct_in_external(_):
    assert _legal_risk_term("100% 환불해드립니다.", "외부 커뮤니케이션") is not None


def test_promise_in_legal(_):
    assert _legal_risk_term("이행을 약속드립니다.", "법무 검토·규제 대응") is not None


# --- Negative ---

def test_clean_legal(_):
    assert _legal_risk_term(
        "당사는 본 계약 조항이 적용되도록 최선의 노력을 다할 예정이다.",
        "법무 검토·규제 대응",
    ) is None


def test_clean_external(_):
    assert _legal_risk_term(
        "발생 시 신속히 회신드릴 예정입니다.",
        "외부 커뮤니케이션",
    ) is None


def test_keyword_in_internal_not_applied(_):
    # 내부 커뮤니케이션 카테고리는 규제 카테고리 아님 → 미적용.
    assert _legal_risk_term("절대로 늦지 않을게요!", "내부 커뮤니케이션") is None


def test_keyword_in_analysis_not_applied(_):
    assert _legal_risk_term("결과는 100% 신뢰할 만하다.", "분석·보고서") is None


def test_no_keyword_clean(_):
    assert _legal_risk_term(
        "본 의견서는 5월 10일 기준 검토 결과이다.",
        "법무 검토·규제 대응",
    ) is None
