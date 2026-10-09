import json
import os
import time
import urllib.error
import urllib.request
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


@dataclass
class OpenAIAdapter:
    """Opt-in adapter for the OpenAI Chat Completions API.

    The API key is read only from ``OPENAI_API_KEY``. No request is made during
    construction; network access occurs only when ``complete`` is called.
    """

    model: str = "gpt-4o-mini"
    base_url: str | None = None
    timeout_seconds: float = 60.0

    def __post_init__(self) -> None:
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is required for --adapter openai; "
                "use --adapter fixture for offline runs"
            )
        self.base_url = (self.base_url or os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")

    def complete(self, *, system_prompt: str, user_prompt: str) -> ModelResponse:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        started = time.perf_counter()
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"OpenAI API request failed with HTTP {exc.code}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"OpenAI API request failed: {exc.reason}") from exc
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise RuntimeError("OpenAI API returned invalid JSON") from exc

        try:
            text = body["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("OpenAI API response did not contain message content") from exc
        if not isinstance(text, str):
            raise RuntimeError("OpenAI API message content was not text")
        latency_ms = round((time.perf_counter() - started) * 1000)
        return ModelResponse(text=text, model=self.model, latency_ms=latency_ms)
