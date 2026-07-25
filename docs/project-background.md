# Project Background and Learning Scope

## Background

This repository is an independent reconstruction and extension of a multi-model LLM Playground initiative completed for DaVita in January–February 2026. The original application source was not retained. This project therefore documents and re-establishes the reusable engineering patterns: a secure model-access boundary, model comparison, measured responses, authenticated user data, and a Google Cloud application foundation.

The repository contains only independently created material. It does not reproduce client source code, private data, credentials, or internal implementation details.

## Learning scope

The project is organized around two connected areas of engineering practice.

### LLM foundations

- Model capabilities and selection trade-offs: quality, latency, cost, context window, availability, and data handling.
- Request configuration: system instructions, temperature, output-token limit, stop sequences, and structured-output expectations.
- Response measurement: input tokens, output tokens, estimated cost, provider latency, end-to-end latency, errors, and trace identifiers.
- Evaluation: representative test cases, scoring rubrics, regression comparison, and release criteria.
- Reliability: timeouts, retries, fallbacks, rate limits, circuit breakers, and safe error responses.

### Google Cloud foundation

- Firebase Authentication: client sign-in, ID tokens, backend validation, and user identity propagation.
- Firestore: user-scoped conversation and experiment records, security rules, indexes, data ownership, and retention.
- Vertex AI and Gemini: approved model access, generation configuration, safety configuration, quotas, regions, and provider response metadata.
- Cloud Storage: bucket access boundaries, artifact organization, retention, and lifecycle policies.
- IAM and Secret Manager: service accounts, least-privilege roles, secret access, key avoidance, and environment separation.
- Operations: structured logging, trace correlation, monitoring, alerting, and audit-ready event records.

## Dry-run workflow

Each topic is approached through a small, controlled exercise:

1. Define the application boundary and success criteria.
2. Configure the relevant service with a least-privilege design.
3. Trace the request, identity, data, and telemetry flow end to end.
4. Capture the resulting contract, configuration decision, and failure behavior in this repository.

## Reference material

- [Google Cloud foundation](google-cloud-foundation.md)
- [Platform architecture](architecture.md)
- [Engineering reference](knowledge-gap-cheatsheet.md)
- [Vertex AI generative AI documentation](https://cloud.google.com/vertex-ai/generative-ai/docs)
- [Firebase security rules documentation](https://firebase.google.com/docs/rules)
- [Google Cloud IAM documentation](https://cloud.google.com/iam/docs)
