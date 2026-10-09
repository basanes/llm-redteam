import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from attacks.prompt_injection.classifier import classify
from llm_redteam.adapters import FixtureAdapter, ModelAdapter
from llm_redteam.reporting import write_reports
from llm_redteam.schemas import EvalResult, TestCase


def load_dataset(path: Path) -> list[TestCase]:
    cases: list[TestCase] = []
    seen: set[str] = set()
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            case = TestCase(**data)
        except (json.JSONDecodeError, TypeError, KeyError) as exc:
            raise ValueError(f"Invalid case at {path}:{line_number}: {exc}") from exc
        if case.id in seen:
            raise ValueError(f"Duplicate case id at {path}:{line_number}: {case.id}")
        seen.add(case.id)
        cases.append(case)
    if not cases:
        raise ValueError(f"Dataset is empty: {path}")
    return cases


def run(dataset: Path, out_dir: Path, adapter: ModelAdapter) -> list[EvalResult]:
    results = []
    for case in load_dataset(dataset):
        response = adapter.complete(system_prompt=case.system_prompt, user_prompt=case.user_prompt)
        verdict, reason = classify(case, response.text)
        results.append(EvalResult(case.id, response.model, response.text, verdict, reason, response.latency_ms))
    write_reports(results, out_dir, dataset=str(dataset), generated_at=datetime.now(timezone.utc).isoformat())
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Run controlled direct prompt-injection evaluations.")
    parser.add_argument("--adapter", choices=["fixture"], default="fixture")
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    adapter = FixtureAdapter()
    results = run(args.dataset, args.out, adapter)
    counts = {verdict: sum(r.verdict == verdict for r in results) for verdict in ("pass", "fail", "review")}
    print(f"model={adapter.model} cases={len(results)} pass={counts['pass']} fail={counts['fail']} review={counts['review']}")


if __name__ == "__main__":
    main()
