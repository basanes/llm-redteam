import json

import pytest

from attacks.prompt_injection.runner import load_dataset, run
from llm_redteam.adapters import FixtureAdapter


DATASET = "datasets/direct_injection_v0.jsonl"


def test_dataset_has_ten_unique_cases():
    cases = load_dataset(__import__("pathlib").Path(DATASET))
    assert len(cases) == 10
    assert len({case.id for case in cases}) == 10


def test_duplicate_ids_are_rejected(tmp_path):
    path = tmp_path / "duplicate.jsonl"
    row = {"id": "same", "category": "x", "system_prompt": "s", "user_prompt": "u", "expected_behavior": "remain_on_task"}
    path.write_text(json.dumps(row) + "\n" + json.dumps(row) + "\n")
    with pytest.raises(ValueError, match="Duplicate case id"):
        load_dataset(path)


def test_fixture_run_writes_reports(tmp_path):
    results = run(__import__("pathlib").Path(DATASET), tmp_path, FixtureAdapter())
    assert len(results) == 10
    assert all(result.verdict == "pass" for result in results)
    assert (tmp_path / "results.json").exists()
    assert (tmp_path / "scorecard.md").exists()
