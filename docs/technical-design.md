# Technical Design

## Design principles

- Separate HTTP transport, application services, domain contracts, and provider integrations.
- Keep model selection and generation settings in explicit policy and configuration objects.
- Treat Firebase user identity as the ownership boundary for application data.
- Use the Cloud Run service account, rather than the web client, for privileged Google Cloud access.
- Return measurable, provider-neutral response metadata with every model invocation.

## Application layers

| Layer | Responsibility | Workspace location |
|---|---|---|
| Frontend | Sign-in, experiment input, comparison, and result presentation | `frontend/` |
| API | HTTP routing, authentication boundary, validation, response serialization | `app/api/` |
| Application services | Orchestration, model policy, measurement, reliability behavior | `app/services/` |
| Domain | Typed contracts for experiments, models, telemetry, and evaluation | `app/domain/` |
| Adapters | Vertex AI, Firebase, Firestore, Storage, observability integrations | `app/adapters/` |
| Core | Settings, security, shared error handling, trace context | `app/core/` |
| Infrastructure | Cloud Run, Firebase, IAM, Storage, and environment configuration | `infra/` |

## Core contracts

### Experiment request

- authenticated user identity;
- selected approved model configuration;
- prompt and generation settings;
- optional experiment label and comparison group.

### Experiment response

- generated content;
- selected model and configuration;
- input and output token usage;
- estimated cost;
- provider and end-to-end latency;
- trace identifier;
- classified error information when a request is unsuccessful.

### Stored records

| Record | Purpose |
|---|---|
| Conversation | User-scoped conversation metadata and message references |
| Experiment | Prompt configuration, selected model, response metadata, and outcome |
| Evaluation | Representative case, scoring criteria, result, and release comparison |
| Audit event | Security-relevant or operational event correlated by trace identifier |

## Security boundaries

1. Firebase Authentication signs in the user and issues an ID token.
2. The API validates the ID token and derives user identity server-side.
3. Firestore rules and backend authorization constrain data to the correct owner.
4. The Cloud Run service account receives least-privilege access to Vertex AI, Firestore, Cloud Storage, Secret Manager, and observability services.
5. The frontend never receives provider credentials or privileged service-account permissions.

## Deployment design

- **Firebase Hosting:** static frontend delivery.
- **Cloud Run:** one container for FastAPI, the model gateway, reliability logic, and provider adapters.
- **Vertex AI:** governed Gemini and approved-model access.
- **Firestore:** user-scoped operational data.
- **Cloud Storage:** evaluation datasets and controlled artifacts.
- **Secret Manager:** runtime secrets.
- **Cloud Logging and Trace:** structured logs and request correlation.

See the [architecture guide](architecture.md) for the visual request and deployment view.
