# AI Customer Support Agent

An AI-powered customer support agent built for the Hiver backend assignment using the Customer Support on Twitter dataset.

The system performs three tasks:

1. Classifies an incoming customer message into a small set of support intents.
2. Retrieves historically similar customer-support interactions and uses them as evidence for drafting a reply.
3. Decides whether the issue should be auto-handled or escalated, with a reason.

## System Overview

```text
Customer Message
       |
       v
Intent Classification
       |
       v
Historical Retrieval
(TF-IDF + cosine similarity)
       |
       v
Reply Generation
       |
       v
Decision Layer
       |
       +-------------------+
       |                   |
       v                   v
  Auto-handle          Escalate


  ## Intent Taxonomy

The evaluation taxonomy contains 11 intents derived from recurring support issues observed in the dataset:

| Intent | Description |
|---|---|
| `delivery_delay` | Order is late or delivery is taking too long |
| `delivery_not_received` | Order is marked delivered but was not received |
| `delivery_attempt_issue` | Delivery attempt, address, carrier, or failed-delivery issue |
| `order_issue` | General order status, cancellation, or order-detail issue |
| `refund_or_return` | Refund, return, replacement, or refund issue |
| `payment_or_billing` | Payment, charge, billing, or unauthorized transaction issue |
| `prime_subscription` | Amazon Prime membership or subscription issue |
| `account_or_security` | Account, login, password, verification, or security issue |
| `product_or_digital_issue` | Product, device, app, or digital-content issue |
| `seller_or_product_complaint` | Seller, product quality, or seller-related complaint |
| `other_non_actionable` | Greetings, thanks, unclear, promotional, or non-actionable messages |

## Evaluation Setup

A fixed **200-example golden evaluation set** was created from the sampled AmazonHelp customer messages.

The examples were manually labelled using the taxonomy above.

A fixed random seed was used when creating the evaluation set so that the experiment is reproducible.

### Evaluation Metrics

For intent classification:

- Accuracy
- Macro F1
- Per-intent precision, recall, and F1

Macro F1 is particularly important because the evaluation set is imbalanced across intents.

For historical retrieval:

- Average top-1 TF-IDF cosine similarity
- Minimum and maximum similarity
- Inspection of low-similarity examples

For the operational decision layer:

- Auto-handle rate
- Escalation rate
- Inspection of low-confidence cases

For reply quality, the planned evaluation rubric contains:

- Groundedness
- Helpfulness
- Professionalism
- Overall quality


## Results

### Intent Classification

The following results were measured on the fixed 200-example golden evaluation set.

| System | Accuracy | Macro F1 |
|---|---:|---:|
| Majority-class baseline | 26.50% | 3.81% |
| Keyword baseline | 44.00% | 36.86% |
| Gemini classifier | 46.50% | 40.34% |

The majority-class baseline always predicts `other_non_actionable`, which is the most common intent in the evaluation set.

The keyword baseline uses deterministic keyword and phrase matching.

The Gemini classifier was evaluated on all 200 examples with valid predictions for every example. It achieved 46.50% accuracy and 40.34% Macro F1.

Compared with the keyword baseline, Gemini improved:

- Accuracy by 2.50 percentage points
- Macro F1 by 3.48 percentage points

### Historical Retrieval

The historical retrieval component uses TF-IDF vectors and cosine similarity over customer messages.

| Metric | Result |
|---|---:|
| Average top-1 similarity | 0.763 |
| Minimum similarity | 0.000 |
| Maximum similarity | 1.000 |

Retrieval performed well when the incoming message used wording similar to historical customer messages, but similarity dropped substantially for multilingual or differently phrased messages.

### Auto-handle vs Escalate

The decision layer was evaluated on the 200-example golden set.

| Decision | Count | Rate |
|---|---:|---:|
| Auto-handle | 154 | 77.0% |
| Escalate | 46 | 23.0% |

The decision layer escalates low-confidence retrieval cases and treats payment, account/security, and refund/return issues conservatively.

These numbers describe the current heuristic routing policy; they should not be interpreted as a measured business-optimal escalation rate.

### Reply Quality Evaluation

A 10-example reply evaluation set was generated from the golden set.

The planned LLM-as-judge rubric evaluates:

- Groundedness
- Helpfulness
- Professionalism
- Overall quality

The generated replies were successfully produced and saved for evaluation. However, the Gemini API quota was exhausted when the LLM judge was run, so the judge requests returned quota errors.

Therefore:

- LLM-judge quality score: **Not reported**
- Judge-human agreement: **Not reported**

No LLM-judge scores are fabricated or inferred from the generated replies.

## Top 5 Failure Modes

The main failure modes were identified by inspecting the confusion matrix of the keyword baseline on the 200-example golden set.

### 1. Product and digital issues missed by keyword matching

**Observed error:** `product_or_digital_issue` → `other_non_actionable` (15 cases)

Examples included app failures and Kindle/app complaints written in Japanese or German.

Example:

> "@AmazonHelp Wenn ich drauf drücke tut sich gar nichts. Weder öffnet sich die App, noch kann ich dann irgendwas anderes drücken außer 'Exit'."

**Hypothesis:** The keyword baseline depends heavily on English words such as `product` and `device`, so multilingual messages and differently worded application issues are frequently missed.

**Potential improvement:** Use multilingual embeddings or an LLM-based classifier rather than relying only on English keyword matching.

---

### 2. Delivery-agent and carrier issues missed

**Observed error:** `delivery_attempt_issue` → `other_non_actionable` (12 cases)

Example:

> "@AmazonHelp Hola. ¿Hay alguna forma de contactar con el mensajero para saber a qué hora tiene previsto hacer una entrega?"

**Hypothesis:** Some delivery problems are expressed through carrier, courier, messenger, or delivery-agent language without containing the exact keywords used by the baseline.

**Potential improvement:** Expand the intent examples and use semantic classification so that related delivery concepts are recognized even without exact keyword matches.

---

### 3. Undelivered packages expressed in varied language

**Observed error:** `delivery_not_received` → `other_non_actionable` (11 cases)

Example:

> "@AmazonHelp Yes I did but not impressed with the people on the phone. Why didn't your people ring the bell, why wasn't a card left and where is the parcel?"

**Hypothesis:** Customers describe missing deliveries using many different phrases such as "where is the parcel", "didn't arrive", "lost", or "no card was left". A small set of exact keyword rules cannot cover these variations reliably.

**Potential improvement:** Use semantic similarity/classification and add targeted examples for common missing-delivery expressions.

---

### 4. Delivery delay confused with delivery attempt issues

**Observed error:** `delivery_delay` → `delivery_attempt_issue` (11 cases)

Example:

> "@AmazonHelp I am waiting for my one day promised delivery even on the second day. PATHETIC! No response."

**Hypothesis:** The keyword `delivery` overlaps heavily between delayed deliveries and delivery-attempt problems. Rule ordering can therefore assign a generic delivery issue to the wrong intent before the delay-specific rule is applied.

**Potential improvement:** Use more specific intent boundaries and semantic classification. Delay indicators such as "late", "waiting", "promised delivery", and "second day" should receive higher priority when the complaint is specifically about lateness.

---

### 5. Seller and product complaints expressed indirectly

**Observed error:** `seller_or_product_complaint` → `other_non_actionable` (9 cases)

Example:

> "@AmazonHelp nothing was damaged, but something as delicate as a graphics card should be packaged a lot more than it was"

**Hypothesis:** Seller/product complaints are often expressed through concepts such as packaging, reviews, counterfeit products, or community guidelines without explicitly using the words `seller` or `product`.

**Potential improvement:** Add semantic features and representative examples covering packaging, reviews, counterfeit goods, listing problems, and seller behaviour.


## What Is Misleading About My Headline Number?

The 44.00% accuracy of the keyword baseline is useful as a reproducible benchmark, but it should not be interpreted as the quality of the complete support agent.

There are several reasons:

1. **The evaluation set is small.**  
   The golden set contains 200 examples, so the measured accuracy can change noticeably with a different sample.

2. **The intents are imbalanced.**  
   `other_non_actionable` is the largest class, while several support intents have relatively few examples. Accuracy can therefore hide poor performance on smaller intents. This is why Macro F1 is also reported.

3. **Intent accuracy does not measure reply quality.**  
   Correctly identifying an intent does not guarantee that the generated customer response is helpful, grounded, or professionally written.

4. **Retrieval quality is a separate component.**  
   A correct intent prediction can still produce a weak response if no sufficiently similar historical resolution is retrieved.

5. **The decision layer changes the operational risk.**  
   The system can escalate uncertain cases instead of automatically responding. Therefore, classification accuracy alone does not represent the final business behaviour of the agent.

6. **The Gemini evaluation could not be measured reliably in this run.**  
   The API quota was exhausted during evaluation, causing fallback predictions. Those results are therefore not presented as genuine Gemini performance.

For these reasons, the headline classification number should be interpreted as a **baseline benchmark**, not as an end-to-end measure of customer-support agent quality.


## One-Week Next Steps

If I had one additional week, I would focus on the following improvements:

1. **Improve intent classification**
   - Replace keyword-heavy rules with multilingual semantic embeddings or a stronger LLM-based classifier.
   - Add more labelled examples for the weaker intents.

2. **Improve historical retrieval**
   - Replace TF-IDF with multilingual sentence embeddings.
   - Add metadata such as intent and conversation context to improve retrieval quality.

3. **Improve reply grounding**
   - Require the generated response to cite or follow retrieved historical resolutions.
   - Add automated checks for unsupported claims, links, refunds, dates, and policies.

4. **Improve escalation policy**
   - Build a labelled set for `auto_handle` vs `escalate`.
   - Tune the confidence threshold using validation data rather than a manually selected threshold.
   - Evaluate false auto-handles separately because they carry higher customer-support risk.

5. **Strengthen evaluation**
   - Expand human-labelled reply evaluations beyond the initial 10 examples.
   - Re-run the LLM judge when API capacity is available.
   - Compare LLM-judge scores against human ratings to measure judge-human agreement.

6. **Production readiness**
   - Add logging, monitoring, rate-limit handling, retries, and structured error handling.
   - Add tests for classification, retrieval, reply generation, and escalation decisions.


   ## Reproducing the Results

### 1. Create the environment

```bash
python -m venv venv
venv\Scripts\activate
