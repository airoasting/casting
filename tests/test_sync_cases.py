"""End-to-end test that sync_cases parses the live site to 63 cases."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.network
def test_sync_produces_63_cases(tmp_path: Path) -> None:
    out = tmp_path / "cases"
    result = subprocess.run(
        [sys.executable, "-m", "scripts.sync_cases", "--out", str(out)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Parsed 63 cases" in result.stderr
    md_files = sorted(out.glob("p*.md"))
    assert len(md_files) == 63
    index = out / "_index.md"
    assert index.exists()
    body = index.read_text(encoding="utf-8")
    # Spot-check 4 expected cases.
    for marker in ["p1", "p23", "p41", "p65"]:
        assert f"`{marker}`" in body
