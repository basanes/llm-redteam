import json
from pathlib import Path
from dataclasses import asdict

from .schemas import EvalResult


def write_reports(results: list[EvalResult], out_dir: Path, *, dataset: str, generated_at: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": {"dataset": dataset, "generated_at": generated_at, "count": len(results)},
        "results": [asdict(result) for result in results],
    }
    (out_dir / "results.json").write_text(json.dumps(payload, indent=2) + "\n")
    counts = {verdict: sum(result.verdict == verdict for result in results) for verdict in ("pass", "fail", "review")}
    pass_rate = counts["pass"] / len(results) if results else 0
    lines = [
        "# Direct Prompt-Injection Evaluation",
        "",
        f"- Dataset: `{dataset}`",
        f"- Cases: {len(results)}",
        f"- Pass rate: {pass_rate:.1%}",
        f"- Pass / fail / review: {counts['pass']} / {counts['fail']} / {counts['review']}",
        "",
        "| Case | Model | Verdict | Reason |",
        "|---|---|---|---|",
    ]
    for result in results:
        reason = result.reason.replace("|", "\\|")
        lines.append(f"| `{result.case_id}` | `{result.model}` | **{result.verdict}** | {reason} |")
    (out_dir / "scorecard.md").write_text("\n".join(lines) + "\n")
