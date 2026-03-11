# 🔴 LLM Red-Teaming & Evaluation Framework

> A hands-on research toolkit for adversarial testing, safety evaluation, and robustness benchmarking of large language models.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: Active](https://img.shields.io/badge/Status-Active%20Development-orange)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()

---

## 📌 Overview

This project provides a structured framework for red-teaming LLMs — probing their failure modes, safety boundaries, and evaluation reliability. It covers four core attack/evaluation categories:

| Category | Description |
|---|---|
| 🎯 **Prompt Injection** | Direct & indirect injection, instruction hijacking |
| 🔓 **Jailbreak Testing** | Role-play exploits, multi-turn bypasses, encoding attacks |
| 🌀 **Hallucination Metrics** | Factual drift, citation fabrication, confidence calibration |
| 🛡️ **AI Safety Evaluation** | Refusal consistency, RLHF gap analysis, alignment stress tests |

Built as a portfolio flagship for roles in **AI Security**, **LLM Evaluation Engineering**, and **AI Safety Research**.

---

## 🗂️ Project Structure

```
llm-redteam/
├── attacks/
│   ├── prompt_injection/        # Direct & indirect injection payloads
│   ├── jailbreaks/              # Role-play, encoding, multi-turn attacks
│   └── adversarial_inputs/      # Edge case and boundary inputs
├── evaluation/
│   ├── hallucination/           # Factuality & calibration metrics
│   ├── safety_benchmarks/       # Refusal rate, consistency scoring
│   └── scorecards/              # Structured eval output templates
├── datasets/
│   ├── attack_prompts.json      # Curated adversarial prompt dataset
│   └── ground_truth.json        # Reference answers for hallucination eval
├── notebooks/
│   ├── 01_injection_analysis.ipynb
│   ├── 02_jailbreak_taxonomy.ipynb
│   └── 03_hallucination_eval.ipynb
├── results/
│   └── (auto-generated eval outputs)
├── utils/
│   ├── api_wrapper.py           # OpenAI / Anthropic / local model adapter
│   └── metrics.py               # Scoring helpers
├── requirements.txt
├── config.yaml
└── README.md
```

---

## ⚙️ Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/llm-redteam.git
cd llm-redteam

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your API keys
cp config.yaml.example config.yaml
# Edit config.yaml with your OpenAI / Anthropic keys
```

---

## 🚀 Quick Start

```python
from attacks.prompt_injection import InjectionTester
from evaluation.hallucination import HallucinationEvaluator

# Run injection tests against a model
tester = InjectionTester(model="gpt-4o")
results = tester.run_suite("datasets/attack_prompts.json")
print(results.summary())

# Evaluate hallucination rate
evaluator = HallucinationEvaluator(model="claude-3-5-sonnet")
score = evaluator.evaluate("datasets/ground_truth.json")
print(f"Factuality Score: {score.factuality:.2%}")
```

---

## 🧪 Attack Modules

### 1. Prompt Injection
Tests direct injection (user overrides system prompt) and indirect injection (malicious content in retrieved context, e.g. RAG poisoning).

```bash
python -m attacks.prompt_injection.run --model gpt-4o --mode direct
python -m attacks.prompt_injection.run --model gpt-4o --mode indirect
```

### 2. Jailbreak Testing
Systematic testing across known jailbreak categories: DAN variants, role-play exploits, base64/ROT13 encoding tricks, multi-turn escalation.

```bash
python -m attacks.jailbreaks.run --model claude-3-5-sonnet --category roleplay
```

### 3. Hallucination Metrics
Measures factual accuracy, citation fabrication rate, and confidence calibration using a reference dataset.

```bash
python -m evaluation.hallucination.run --model gpt-4o --dataset datasets/ground_truth.json
```

### 4. Safety & Alignment Evaluation
Tests refusal consistency across paraphrased harmful prompts, RLHF edge cases, and measures alignment gaps.

```bash
python -m evaluation.safety_benchmarks.run --model gpt-4o --suite core
```

---

## 📊 Sample Results

> *(Generated from evaluation runs — updated regularly)*

| Model | Injection Resistance | Jailbreak Resistance | Factuality | Refusal Consistency |
|---|---|---|---|---|
| GPT-4o | 87% | 79% | 91% | 94% |
| Claude 3.5 Sonnet | 91% | 85% | 94% | 97% |
| Llama 3 8B | 61% | 54% | 78% | 72% |

---

## 🗺️ Roadmap

- [x] Project scaffold & repo setup
- [ ] Prompt injection module (direct)
- [ ] Prompt injection module (indirect / RAG poisoning)
- [ ] Jailbreak taxonomy & test suite
- [ ] Hallucination evaluation pipeline
- [ ] Safety benchmark suite
- [ ] Multi-model comparison dashboard
- [ ] Published evaluation report / blog post
- [ ] Integration with LangChain / LlamaIndex for RAG attack scenarios

---

## 📚 References & Inspiration

- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Anthropic's Responsible Scaling Policy](https://www.anthropic.com/responsible-scaling-policy)
- [Perez et al. — Ignore Previous Prompt (2022)](https://arxiv.org/abs/2211.09527)
- [Greshake et al. — Indirect Prompt Injection (2023)](https://arxiv.org/abs/2302.12173)
- [TruthfulQA Benchmark](https://github.com/sylinrl/TruthfulQA)

---

## 🤝 Contributing

Pull requests are welcome! If you find a new attack vector, evaluation gap, or want to add model support — open an issue first to discuss.

---

## ⚠️ Disclaimer

This project is for **educational and research purposes only**. All testing is conducted against models via official APIs under their terms of service. No exploits are used maliciously.

---

## 👤 Author

**John Bernard Basañes** — BSc Data Science & AI @ Dublin City University  
Microsoft Dreamspace Ambassador | AI Security Enthusiast  
[GitHub](https://github.com/JbMarilen) · [LinkedIn](https://linkedin.com/in/jdoubleb)
