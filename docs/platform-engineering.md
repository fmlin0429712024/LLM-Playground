# Platform Engineering

## Scope in an enterprise AI stack

This project addresses the LLM platform and inference layer: secure model access, model policy, measurable invocation, provider resilience, and model-quality evaluation. A companion [Customer Care Agents showcase](https://github.com/fmlin0429712024/customer-care-agents) addresses the agent workflow layer: multi-step orchestration, tool use, state, business guardrails, and human escalation.

The layers share an enterprise foundation but do not observe or govern the same unit of work.

| Topic | Traditional application | LLM platform and Playground | Agent workflow solution |
|---|---|---|---|
| Primary concern | Deterministic business APIs and data processing | Governed model invocation and comparison | Business-task execution through skills and tools |
| Core logic | Business rules, APIs, and database operations | Model policy, context, provider adapter, and response measurement | Orchestration, skills, state, tool calls, and workflow decisions |
| Observability | API, database, and infrastructure errors | Model, parameters, tokens, cost, latency, provider errors, and fallback | Workflow steps, state, tool calls, handoffs, and business outcome |
| Evaluation | Functional correctness and integration behavior | Prompt/output quality, format, latency, cost, and model comparison | Task completion, tool correctness, policy compliance, and escalation decisions |
| Reliability | Application, database, and network recovery | Provider timeout, quota, retry, fallback, and circuit breaker | Workflow recovery, state durability, idempotency, and human escalation |
| Governance | User access, service access, and data permissions | Model access, parameter policy, context data handling, and cost boundaries | Tool permissions, business guardrails, approval, and human-in-the-loop controls |
| Deployment | Cloud runtime and data services | Cloud Run or Vertex AI with a model gateway | Cloud Run or Vertex AI Agent Platform with an agent runtime |

This repository deliberately retains the LLM-platform column and does not duplicate agent orchestration or business-workflow controls.

## Model policy and experiment control

The model gateway owns approved model selection, generation-parameter validation, provider routing, and response normalization. A caller chooses from policy-approved configurations rather than passing arbitrary provider settings. This makes comparison reproducible and keeps provider-specific behavior inside adapters.

Key decision factors are quality, latency, estimated cost, context capacity, availability, data handling, and supported response features.

## Measurement and cost governance

Each invocation records input tokens, output tokens, estimated cost, provider latency, and end-to-end latency. These measurements support model comparison, cost visibility, capacity planning, and service-level objectives.

Cost estimates must identify their pricing assumptions and remain separate from a provider billing record. Latency should distinguish the model-provider duration from the total application request duration.

## Reliability controls

| Control | Purpose |
|---|---|
| Timeout | Bound dependency wait time and protect application capacity. |
| Retry | Recover from transient provider or network failures using bounded attempts. |
| Fallback | Route an eligible request to an approved alternative model or safe degraded response. |
| Rate limit | Protect provider quota, cost boundaries, and fair access. |
| Circuit breaker | Stop repeated calls to an unhealthy dependency and enable controlled recovery. |
| Idempotency | Ensure a retried write does not create duplicate stored actions. |

Reliability behavior is policy: it varies by request type, user impact, model capability, and failure class. It should not be hidden inside an individual endpoint.

## Observability and service objectives

Every request should carry a trace identifier across API, gateway, provider adapter, data access, and structured logs. Useful operational signals include request count, error rate, latency percentiles, token use, estimated cost, throttle events, fallback rate, and circuit-breaker state.

Service-level objectives establish the target experience before optimization. For example, the platform can define an availability target, a p95 end-to-end latency target, and a maximum error rate for a selected model configuration. Alerts should identify a user-impacting condition rather than merely an individual log event.

## Evaluation and quality

Model comparison needs representative golden cases, explicit evaluation criteria, and repeatable result capture. A case can assess correctness, completeness, safety, format compliance, latency, and cost. Changes to a model, prompt, or configuration are compared against a baseline before release.

Evaluation does not require claiming universal model quality. It creates evidence for a defined use case and makes trade-offs visible to engineering and business stakeholders.

## Security and data governance

Firebase identity defines the user boundary; the backend validates tokens and derives ownership server-side. The Cloud Run service account, not the client, accesses privileged services with least-privilege IAM roles. The backend applies user, organization, ownership, and purpose checks before it reads, writes, returns, or forwards data.

Authorization is layered rather than delegated to one control: Cloud Run IAM limits which workload identities may invoke the backend; application authorization evaluates the authenticated caller's permitted actions; and resource-level IAM limits what the backend service account may access. Firestore Security Rules protect direct web/mobile client access; server-side FastAPI calls use the service account and IAM, and therefore require application-layer data authorization. The [enterprise access model](architecture.md#enterprise-access-model) shows these boundaries together.

Prompts, responses, conversation history, evaluation data, and generated artifacts should be classified as application data. The platform minimizes sensitive content in logs, isolates secrets in Secret Manager, defines data-retention rules, and records security-relevant events with traceable metadata.

In a healthcare context, PII and potential PHI require explicit data classification and approved handling controls before production use. This affects identity design, data access, logging, retention, vendor review, and audit expectations; it is a design input rather than an automatic compliance claim.

## Delivery and operational readiness

The reference deployment uses Firebase Hosting for static frontend delivery and one Cloud Run container for the backend. Container configuration, environment separation, IAM bindings, storage policies, and observability configuration belong in `infra/`.

### Provisioning and CI/CD

Provisioning prepares the approved cloud environment: projects, environments, Service Accounts, IAM, Firestore, Storage, secrets, logging, and monitoring. CI/CD builds, verifies, deploys, promotes, and rolls back application artifacts within those environments.

The two controls can be separate. In a ticket-driven enterprise model, Cloud Security and platform teams provision approved resources before the application team deploys through CI/CD. In a mature platform model, infrastructure-as-code can automate provisioning through a separate or integrated pipeline.

### Enterprise delivery lifecycle

```text
MVP / POC
  -> Sandbox validation
  -> Production design and data-access review
  -> Environment and access provisioning
  -> CI/CD deployment: dev -> test -> pre-production -> production
  -> Security and operational acceptance
  -> Monitoring, audit, access review, and change management
```

| Team | Primary responsibility |
|---|---|
| Application and solution architecture | Define functional behavior, data flow, workload purpose, access requirements, and acceptance criteria. |
| Data owner and governance | Approve data use, classification, retention, and sensitive-data handling. |
| Cloud security and platform | Provide identity, IAM guardrails, approved resource patterns, audit controls, and environment boundaries. |
| DevOps / platform engineering | Operate deployment automation, artifact promotion, infrastructure automation, and rollback procedures. |
| Application team | Deploy application artifacts, enforce application-layer authorization, and validate behavior in each environment. |

Pre-production acceptance verifies identity flow, least-privilege workload access, data boundaries, logging behavior, error handling, and operational telemetry. These delivery controls do not change the core model-gateway contract; they make it safe to operate in an enterprise environment.

## Engineering reference

- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
- [Cloud Logging documentation](https://cloud.google.com/logging/docs)
- [Secret Manager documentation](https://cloud.google.com/secret-manager/docs)
- [Vertex AI generative AI documentation](https://cloud.google.com/vertex-ai/generative-ai/docs)
