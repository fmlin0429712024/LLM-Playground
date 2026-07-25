# Knowledge-Gap Cheat Sheet

This is a study backlog, not a claim of implemented functionality.

## 1. Model policy and LLMOps

- Model selection: quality, latency, cost, privacy, context window, availability.
- RAG changes knowledge; fine-tuning changes stable behavior.
- Golden cases, rubric, regression evaluation, release gates.
- Token usage, estimated cost, p50/p95 latency, error rate.

## 2. Resilience

| Pattern | Purpose |
|---|---|
| Timeout | Stop waiting indefinitely for a dependency. |
| Retry | Recover from transient network or provider errors. |
| Fallback | Use an approved alternate model or safe degraded experience. |
| Circuit breaker | Stop repeatedly calling a failing dependency. |
| Idempotency | Ensure a retried write operation does not create a duplicate action. |

## 3. RAG and vector search

- Parse, clean, chunk, embed, store metadata, retrieve, filter, rerank, cite, evaluate.
- Common failures: weak source quality, poor chunks, missing metadata, irrelevant retrieval, unsupported answer.

## 4. Fine-tuning

- Start with prompt and RAG baselines.
- Consider fine-tuning for stable classification, format, behavior, or domain language patterns.
- Require labeled data, train/validation/test splits, reproducibility, privacy review, and production monitoring.

## 5. Tool boundaries - implemented separately in customer-care-agents

- Narrow typed tools; least privilege; read/write distinction.
- Authorization, approval, idempotency, audit, traceability.
- High-consequence actions are not executed by an LLM alone.

## 6. Production engineering

```text
FastAPI client -> endpoint -> service/business function
Docker -> CI/CD -> Artifact Registry -> Cloud Run
Terraform -> IAM, secrets, service configuration, monitoring
Tests -> unit, integration, contract, evaluation regression
```
