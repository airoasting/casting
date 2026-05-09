"""Tiny Haiku-backed LLM judge wrapper. Mockable for tests via dependency injection."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Callable, Protocol

from anthropic import Anthropic


HAIKU_MODEL = "claude-haiku-4-5-20251001"


class JudgeFn(Protocol):
    def __call__(self, system: str, user: str, schema: dict[str, Any]) -> dict[str, Any]: ...


@dataclass
class HaikuJudge:
    """Real implementation backed by Anthropic Haiku.

    Tests should pass a fake JudgeFn instead of using this.
    """
    client: Anthropic | None = None

    def __post_init__(self) -> None:
        if self.client is None:
            self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def __call__(self, system: str, user: str, schema: dict[str, Any]) -> dict[str, Any]:
        assert self.client is not None
        msg = self.client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=512,
            system=system + "\n\nReturn ONLY a JSON object matching this schema: " + json.dumps(schema),
            messages=[{"role": "user", "content": user}],
        )
        text = "".join(b.text for b in msg.content if b.type == "text")
        # Trim ```json fences if present.
        if text.strip().startswith("```"):
            text = text.strip().strip("`")
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
