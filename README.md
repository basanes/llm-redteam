# LLM Red-Teaming & Evaluation Framework

A controlled, reproducible toolkit for evaluating LLM instruction-following and safety boundaries through authorized model APIs.

## Current milestone: direct prompt-injection evaluation

The repository now includes a deterministic offline evaluator with:

- 10 controlled direct-injection cases in `datasets/direct_injection_v0.jsonl`;
- a fixture adapter that makes no network calls;
- an opt-in OpenAI Chat Completions adapter;
- transparent `pass`, `fail`, and `review` classification;
- JSON results and a Markdown scorecard;
- unit tests for loading, classification, and reporting.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
```

## Run the offline evaluation

```bash
python -m attacks.prompt_injection.runner \
  --adapter fixture \
  --dataset datasets/direct_injection_v0.jsonl \
  --out results/demo
```

The command writes `results/demo/results.json` and `results/demo/scorecard.md`.

## Run an authorized live evaluation

The live adapter is **opt-in**. It makes network requests only when you select
`--adapter openai`, and it requires `OPENAI_API_KEY` from the environment. The
key is never read from a file in the repository or written to evaluation output.

```bash
export OPENAI_API_KEY="your-key-in-your-shell"
python -m attacks.prompt_injection.runner \
  --adapter openai \
  --model gpt-4o-mini \
  --dataset datasets/direct_injection_v0.jsonl \
  --out results/openai-baseline
```

For OpenAI-compatible gateways, optionally set `OPENAI_BASE_URL`. Use only
models and endpoints that you are authorized to evaluate. The fixture adapter
remains the default and is the recommended path for tests and development.

Run tests with:

```bash
pytest
```

## Scope and authorization

This project is for educational and research use against models and applications you are authorized to evaluate. The first milestone tests whether a model preserves its assigned task and avoids revealing protected system instructions. It does not attempt to bypass real access controls or generate operationally harmful content.

## Project structure

```text
attacks/prompt_injection/  # classifier and CLI runner
llm_redteam/               # schemas, fixture/live adapters, reporting
 datasets/                 # versioned JSONL cases
 tests/                    # offline tests
 results/                  # generated outputs (ignored by git)
```

See [START_HERE.md](START_HERE.md) for the staged roadmap and next milestones.
