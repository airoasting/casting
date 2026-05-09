from scripts.anti_patterns import _vague_cta


def test_detects_review_please(fake_judge):
    judge = fake_judge({"has_clear_verb": False})
    result = _vague_cta("내용 첨부드리니 검토 부탁드립니다.", judge)
    assert result is not None
    assert result.name == "VAGUE_CTA"


def test_detects_for_reference(fake_judge):
    judge = fake_judge({"has_clear_verb": False})
    result = _vague_cta("자료를 보냅니다. 참고 바랍니다.", judge)
    assert result is not None


def test_detects_consider_please(fake_judge):
    judge = fake_judge({"has_clear_verb": False})
    result = _vague_cta("의견 주시면 좋겠습니다. 고민 부탁.", judge)
    assert result is not None


def test_detects_confirm_please(fake_judge):
    judge = fake_judge({"has_clear_verb": False})
    result = _vague_cta("초안을 공유합니다. 확인 부탁드립니다.", judge)
    assert result is not None


def test_detects_yangyae(fake_judge):
    judge = fake_judge({"has_clear_verb": False})
    result = _vague_cta("일정 변경에 대해 양해 부탁드립니다.", judge)
    assert result is not None


# --- Negative cases ---

def test_explicit_approval_request_clean(fake_judge):
    judge = fake_judge({"has_clear_verb": True})
    assert _vague_cta("초안 공유합니다. 금요일까지 승인 회신 부탁드립니다.", judge) is None


def test_deadline_clean(fake_judge):
    judge = fake_judge({"has_clear_verb": True})
    assert _vague_cta("8월 12일 마감으로 회신 부탁드립니다.", judge) is None


def test_decision_phrase_clean(fake_judge):
    judge = fake_judge({"has_clear_verb": True})
    assert _vague_cta("두 안 중 1안으로 결정 부탁드립니다.", judge) is None


def test_no_vague_keyword_clean(fake_judge):
    judge = fake_judge({"has_clear_verb": True})
    assert _vague_cta("8/12까지 회신 주세요.", judge) is None


def test_clear_action_verb_clean(fake_judge):
    judge = fake_judge({"has_clear_verb": True})
    assert _vague_cta("이번 주 안에 확정 회신 부탁드립니다.", judge) is None
