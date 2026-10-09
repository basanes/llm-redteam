from dataclasses import dataclass
from typing import Literal


ExpectedBehavior = Literal["remain_on_task", "refuse_disclosure"]
Verdict = Literal["pass", "fail", "review"]


@dataclass(frozen=True)
class TestCase:
    id: str
    category: str
    system_prompt: str
    user_prompt: str
    expected_behavior: ExpectedBehavior
    severity: str = "low"
    notes: str = ""


@dataclass(frozen=True)
class ModelResponse:
    text: str
    model: str
    latency_ms: int = 0


@dataclass(frozen=True)
class EvalResult:
    case_id: str
    model: str
    response_text: str
    verdict: Verdict
    reason: str
    latency_ms: int
