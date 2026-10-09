from dataclasses import dataclass
from typing import Protocol

from .schemas import ModelResponse


class ModelAdapter(Protocol):
    model: str

    def complete(self, *, system_prompt: str, user_prompt: str) -> ModelResponse:
        ...


@dataclass
class FixtureAdapter:
    """Deterministic adapter for local development and tests.

    It simulates a task-preserving assistant and never calls a network service.
    """

    model: str = "fixture-v0"

    def complete(self, *, system_prompt: str, user_prompt: str) -> ModelResponse:
        lower = user_prompt.lower()
        if "reveal" in lower or "system prompt" in lower or "protected" in lower:
            text = "I can’t provide protected system instructions. I can help with the assigned task instead."
        else:
            text = "I’ll follow the assigned task and ignore conflicting instructions."
        return ModelResponse(text=text, model=self.model, latency_ms=0)
