"""Test fixtures shared across anti-pattern tests."""
from __future__ import annotations

from typing import Any, Callable

import pytest


@pytest.fixture
def fake_judge() -> Callable[[Any], Callable[..., Any]]:
    """Return a builder that produces a deterministic fake JudgeFn.

    Usage:
        judge = fake_judge({"unsourced_numbers": ["23%"]})
    """
    def make(payload: dict[str, Any]):
        def inner(system: str, user: str, schema: dict[str, Any]) -> dict[str, Any]:
            return payload
        return inner
    return make
