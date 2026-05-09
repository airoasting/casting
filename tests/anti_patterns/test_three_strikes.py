import pytest
from scripts.anti_patterns import ConsecutiveAntiPatternError, StrikeCounter


def test_one_strike_no_raise():
    sc = StrikeCounter()
    sc.record("HALLUCINATED_NUMBER")
    assert sc.counts["HALLUCINATED_NUMBER"] == 1


def test_two_strikes_no_raise():
    sc = StrikeCounter()
    sc.record("VAGUE_CTA")
    sc.record("VAGUE_CTA")
    assert sc.counts["VAGUE_CTA"] == 2


def test_three_strikes_raises():
    sc = StrikeCounter()
    sc.record("MISSING_GOLD_HOOK")
    sc.record("MISSING_GOLD_HOOK")
    with pytest.raises(ConsecutiveAntiPatternError) as exc:
        sc.record("MISSING_GOLD_HOOK")
    assert exc.value.pattern_name == "MISSING_GOLD_HOOK"


def test_reset_clears_counter():
    sc = StrikeCounter()
    sc.record("TONE_MISMATCH")
    sc.record("TONE_MISMATCH")
    sc.reset("TONE_MISMATCH")
    sc.record("TONE_MISMATCH")
    assert sc.counts["TONE_MISMATCH"] == 1


def test_independent_patterns():
    sc = StrikeCounter()
    sc.record("HALLUCINATED_NUMBER")
    sc.record("HALLUCINATED_NUMBER")
    sc.record("VAGUE_CTA")  # different pattern, no escalation
    assert sc.counts["VAGUE_CTA"] == 1
    assert sc.counts["HALLUCINATED_NUMBER"] == 2
