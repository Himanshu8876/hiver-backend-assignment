# AI Customer Support Agent — AmazonHelp

An AI support agent for Amazon's Twitter support handle (`AmazonHelp`) that classifies incoming
customer messages, retrieves the most similar historically-resolved case, drafts a grounded reply,
and decides whether to auto-handle or escalate — with a stated reason.

Built for the Hiver SDE Intern take-home. **This README is the report.** Everything you need to
reproduce the headline numbers is in [Reproducing the Results](#reproducing-the-results), under 15 minutes.

---

## TL;DR for reviewers

- **Headline number:** 46.5% accuracy / 40.3% macro-F1 on a 200-example hand-labelled eval set —
  a modest but real 2.5–3.5 point improvement over a deterministic keyword baseline.
- **The honest part:** the LLM-judge-vs-human agreement experiment (n=6) showed 0% exact agreement
  and an MAE of 1.87 on a 1–5 scale. I'm surfacing this as a finding about judge reliability at small
  sample sizes, not hiding it. See [LLM Judge vs Human Agreement](#llm-judge-vs-human-agreement).
- **What I did *not* build:** multi-turn conversation handling, live carrier/order-status API lookups,
  or a tuned auto-handle/escalate threshold (it's currently a hand-set heuristic, stated as such).
- **Where I'd spend the next week:** semantic (not keyword) intent classification, embedding-based
  retrieval, and a properly powered judge-agreement study. See [One-Week Next Steps](#one-week-next-steps).

---

## Problem Framing

**Brand:** `AmazonHelp` — chosen for interaction volume, giving enough historical examples for
retrieval and a large enough pool to sample a balanced-ish 200-example golden set from.

**What "good" means for this agent, specifically:**
- A **correct intent** matters less on its own than whether it routes the message to a safe outcome —
  so the decision layer is evaluated separately from raw classification accuracy, and is intentionally
  conservative on payment, account/security, and refund/return intents (biases toward escalation over
  a wrong auto-reply on money- or access-sensitive issues).
- A **grounded reply** matters more than a fluent one — the reply generator is expected to draw on a
  retrieved historical resolution rather than free-generate, which is why retrieval quality (top-1
  cosine similarity) is tracked as its own metric, separate from intent accuracy and reply quality.
- **Reproducibility on a fixed, imbalanced sample** matters more than squeezing headline accuracy on a
  hand-picked, easy eval set. Macro-F1 is reported alongside accuracy specifically to expose this.

**What I chose not to build, and why:**
- **No multi-turn context.** The dataset has full threads, but scoping to single-message classification
  kept the eval set and taxonomy tractable in the time available. Real Amazon support replies often
  depend on order history the model doesn't have access to here — flagged as a known gap, not solved.
- **No live backend integration** (order status, refund APIs). The agent drafts what an agent *would*
  say based on historical resolutions; it does not execute actions. This is a support-copilot, not an
  autonomous agent.
- **No tuned escalation threshold.** The auto-handle/escalate boundary is a manually-set heuristic
  (low retrieval similarity + sensitive-intent category → escalate). It is evaluated and reported
  honestly as untuned — see [Next Steps](#one-week-next-steps) — rather than presented as optimized.

---

## System Overview

```
Customer Message
       │
       ▼
Intent Classification  (Gemini, 11-class taxonomy)
       │
       ▼
Historical Retrieval   (TF-IDF + cosine similarity over past resolutions)
       │
       ▼
Reply Generation       (grounded in the retrieved case)
       │
       ▼
Decision Layer  ──────►  Auto-handle  or  Escalate (+ reason)
```

## Dataset

**Customer Support on Twitter** (Kaggle, `thoughtvector/customer-support-on-twitter`).
`AmazonHelp` was selected for interaction volume. The raw `twcs.csv` is not committed (too large);
see [Reproducing the Results](#reproducing-the-results) for how to source it.

## Intent Taxonomy (11 classes, derived from the data)

| Intent | Description |
|---|---|
| `delivery_delay` | Order is late or delivery is taking too long |
| `delivery_not_received` | Order marked delivered but not received |
| `delivery_attempt_issue` | Delivery attempt, address, carrier, or failed-delivery issue |
| `order_issue` | General order status, cancellation, or order-detail issue |
| `refund_or_return` | Refund, return, replacement, or refund issue |
| `payment_or_billing` | Payment, charge, billing, or unauthorized transaction issue |
| `prime_subscription` | Amazon Prime membership or subscription issue |
| `account_or_security` | Account, login, password, verification, or security issue |
| `product_or_digital_issue` | Product, device, app, or digital-content issue |
| `seller_or_product_complaint` | Seller, product quality, or seller-related complaint |
| `other_non_actionable` | Greetings, thanks, unclear, promotional, or non-actionable messages |

## Golden Evaluation Set

- 200 examples, sampled from AmazonHelp customer messages with a **fixed random seed (123)** for
  reproducibility.
- Hand-labelled against the taxonomy above; validated for missing/invalid labels before use.
- Stored at `data/golden_eval.csv`.

---

## Results

### 1. Intent Classification

| System | Accuracy | Macro F1 |
|---|---:|---:|
| Majority-class baseline (`other_non_actionable`) | 26.50% | 3.81% |
| Keyword baseline (deterministic rules) | 44.00% | 36.86% |
| **Gemini classifier** | **46.50%** | **40.34%** |

Gemini improves +2.5pp accuracy / +3.48pp macro-F1 over the keyword baseline. All 200 examples
returned a valid prediction (no parsing failures).

### 2. Historical Retrieval (TF-IDF + cosine similarity)

| Metric | Result |
|---|---:|
| Average top-1 similarity | 0.763 |
| Minimum similarity | 0.000 |
| Maximum similarity | 1.000 |

Retrieval is strong when phrasing overlaps with historical messages and degrades on multilingual or
differently-phrased inputs — this is the same weakness that shows up in the failure analysis below,
which is why I flag it as one root cause rather than two unrelated problems.

### 3. Auto-handle vs Escalate

| Decision | Count | Rate |
|---|---:|---:|
| Auto-handle | 154 | 77.0% |
| Escalate | 46 | 23.0% |

The policy escalates low-similarity retrieval cases and treats payment, account/security, and
refund/return intents conservatively regardless of confidence. **This describes the current heuristic,
not a measured business-optimal rate** — no labelled auto/escalate ground truth exists yet to tune against.

### 4. Reply Quality (LLM-as-judge)

10-example reply set. The Gemini judge completed 6/10 (4 hit temporary API errors).

| Metric | Avg (n=6) |
|---|---:|
| Groundedness | 5.00 / 5 |
| Helpfulness | 3.83 / 5 |
| Professionalism | 4.67 / 5 |
| Overall | 4.33 / 5 |

### LLM Judge vs Human Agreement

The same 6 replies were scored by a human on the identical rubric.

| Metric | Result |
|---|---:|
| Evaluated replies | 6 |
| Exact agreement | 0 / 6 (0.0%) |
| Agreement within ±1 | 2 / 6 (33.3%) |
| Mean Absolute Error | 1.87 |

**Read this as a calibration finding, not a quality score.** n=6 is too small to trust as a judge
benchmark; the honest conclusion is "I don't yet know if this judge is reliable," and the fix
(bigger sample, re-run when quota allows) is in the next-steps list rather than papered over.

---

## Top 5 Failure Modes

Identified from the keyword-baseline confusion matrix on the 200-example golden set.

1. **Multilingual product/app issues missed** — `product_or_digital_issue` → `other_non_actionable`
   (15 cases). English-keyword dependence misses German/Japanese app complaints.
   *Fix: multilingual embeddings or LLM classifier.*
2. **Delivery-agent/carrier language missed** — `delivery_attempt_issue` → `other_non_actionable`
   (12 cases). "Messenger," "courier" phrasing isn't covered by keyword rules.
   *Fix: semantic classification with expanded examples.*
3. **Undelivered packages phrased indirectly** — `delivery_not_received` → `other_non_actionable`
   (11 cases). "Where is the parcel," "no card was left" aren't exact-keyword matches.
   *Fix: semantic similarity + targeted phrase examples.*
4. **Delay confused with delivery-attempt issue** — `delivery_delay` → `delivery_attempt_issue`
   (11 cases). Generic `delivery` keyword overlaps both intents; rule ordering picks the wrong one.
   *Fix: prioritize lateness signals ("late," "second day," "promised delivery") explicitly.*
5. **Indirect seller/product complaints** — `seller_or_product_complaint` → `other_non_actionable`
   (9 cases). Packaging/counterfeit/review complaints don't use the words "seller" or "product."
   *Fix: semantic features + representative examples for packaging, counterfeit, seller behavior.*

The full failure examples are available in `data/top_failure_examples.csv`.

---

## What Is Misleading About My Headline Number?

46.5% Gemini accuracy is a reproducible benchmark, **not** a measure of the whole agent's quality:

1. **Small eval set (n=200).** The number will move noticeably with a different sample.
2. **Imbalanced classes.** `other_non_actionable` dominates; accuracy can hide poor performance on
   rarer intents. Macro-F1 (40.34%) is reported specifically to counter this.
3. **Intent accuracy ≠ reply quality.** Getting the label right doesn't mean the drafted reply is useful.
4. **Retrieval is a separate failure surface.** A correct intent can still pair with a weak historical
   match (min similarity observed: 0.000).
5. **The decision layer changes real-world exposure.** 23% of cases are escalated rather than
   auto-answered, so classification accuracy alone isn't the deployed behavior.
6. **The Gemini lift is real but modest** (+2.5pp accuracy, +3.48pp macro-F1 over keyword matching) —
   there's substantial room left.
7. **Reply-quality measurement is incomplete.** Judge quota ran out at 6/10 examples; this number
   should not be read as an end-to-end quality score.

---

## One-Week Next Steps

1. **Classification:** swap keyword rules for multilingual embeddings or a stronger LLM classifier;
   add labelled examples for weak intents (esp. multilingual product/app and delivery-attempt cases).
2. **Retrieval:** move from TF-IDF to multilingual sentence embeddings; add intent/context metadata
   to retrieval scoring.
3. **Reply grounding:** require replies to cite the retrieved case; add automated checks for
   unsupported claims, dates, refund amounts, and policy statements.
4. **Escalation policy:** build a labelled auto-handle/escalate set; tune the threshold on held-out
   data instead of a hand-set heuristic; separately evaluate false auto-handles (higher-risk error type).
5. **Evaluation:** expand the reply-judge set well beyond 10 examples, re-run under sufficient API
   quota, and re-measure judge-human agreement with a sample size large enough to trust (this run's
   n=6 is a pilot, not a result).
6. **Production readiness:** logging, monitoring, retries/rate-limit handling, and tests across
   classification, retrieval, reply generation, and escalation decisions.

---

## Decision Log

15 non-obvious decisions (brand selection, taxonomy design, sampling seed, duplicate historical
pairs, retrieval method choice, escalation conservatism, sensitive-issue handling, evaluation
limitations, etc.) are in [`docs/decision_log.md`](docs/decision_log.md).

---

## Reproducing the Results

Target: under 15 minutes end to end.

### 1. Environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt # pandas, scikit-learn, python-dotenv, google-genai
```

### 2. Configure Gemini

Create a `.env` file in the project root (not committed):

```
GEMINI_API_KEY=your_api_key_here
```

### 3. Get the data

Download `twcs.csv` from the [Kaggle dataset](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter)
and place it at `data/twcs.csv` (not committed — too large for the repo).

### 4. Run baselines

```bash
python src/evaluate_trivial.py     # majority-class + keyword baselines
python src/evaluate_system.py
```
Expected: majority 26.50%/3.81% F1, keyword 44.00%/36.86% F1.

### 5. Run the Gemini classifier

```bash
python src/evaluate_gemini_full.py
```
Writes `data/gemini_predictions.csv`. Expected: 46.50% accuracy / 40.34% macro-F1.

### 6. Run retrieval evaluation

```bash
python src/evaluate_retrieval.py
```
Writes `data/golden_with_retrieval.csv`.

### 7. Run the decision layer

```bash
python src/evaluate_decisions.py
```
Writes `data/decision_results.csv`. Expected: 77.0% auto-handle / 23.0% escalate.

### 8. Run the full agent end-to-end

```bash
python src/test_agent.py
```

### 9. Run reply generation + LLM judge

```bash
python -m src.evaluate_replies   # writes data/reply_eval_results.csv
python -m src.evaluate_judge     # requires Gemini API quota; may not complete all examples
```

---

## Citations / Borrowed Code

Dataset: Axel Bruns et al., *Customer Support on Twitter*, Kaggle. TF-IDF/cosine similarity via
`scikit-learn`. LLM classification, retrieval-grounded reply generation, and judging via the Gemini
API (`google-genai`). No other external code was borrowed; ask me to walk through any file live.
