"""Routing test helpers."""
from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def phrasings() -> list[dict[str, str]]:
    return json.loads(Path("tests/routing/cases_phrasings.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def index_md() -> str:
    return Path("skills/roasting/references/cases/_index.md").read_text(encoding="utf-8")
