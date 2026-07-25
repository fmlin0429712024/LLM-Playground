# Architecture

## System view

```mermaid
flowchart TB
    BROWSER[Browser]

    subgraph CLOUD[Google Cloud]
        subgraph APP[Application Deployment]
            UI[Firebase Hosting<br/>Web Client]
            API[Cloud Run<br/>FastAPI API and Model Gateway<br/>Service Account]
        end
        AUTH[Firebase Authentication<br/>Enterprise SSO]
        MODEL[Vertex AI<br/>Gemini and Approved Models]
        DATA[(Firestore<br/>Conversations and Experiments)]
        FILES[(Cloud Storage<br/>Evaluation Artifacts)]
    end

    BROWSER --> UI
    UI --> AUTH
    UI -->|Authenticated request| API
    API --> MODEL
    API --> DATA
    API --> FILES
```

## Deployment boundary

Firebase Hosting delivers the static web client and does not require a user-managed container. One Cloud Run service contains the FastAPI API and model gateway. This boundary keeps request validation, model policy, response measurement, reliability behavior, and provider adapters together in one independently deployable backend.

The browser never receives provider credentials or privileged Google Cloud permissions. The Cloud Run service uses an attached service account with narrowly scoped IAM access to Vertex AI, Firestore, Cloud Storage, Secret Manager, and observability services.

## Request and identity flow

1. The user signs in through an enterprise identity provider federated to Firebase Authentication.
2. The web client sends the resulting Firebase ID token with the API request.
3. FastAPI validates the token and derives the user identity server-side.
4. The model gateway applies policy, calls the approved Vertex AI model, and measures the request.
5. The API returns generated content plus model, token, cost, latency, trace, and error metadata.
6. Firestore stores user-scoped conversations and experiments; Cloud Storage stores controlled artifacts.

## Enterprise access model

```mermaid
flowchart LR
    USER[Enterprise User]
    IDP[Corporate Identity Provider]
    AUTH[Firebase Authentication]
    CALLER[Approved Service Caller]

    subgraph CLOUD[Google Cloud]
        API[Cloud Run API]
        SA[Cloud Run Service Account]
        VERTEX[Vertex AI]
        FIRESTORE[(Firestore)]
        STORAGE[(Cloud Storage)]
        SECRETS[Secret Manager]
    end

    USER --> IDP --> AUTH
    AUTH -->|User ID token| API
    CALLER -->|Service-account OIDC token<br/>Cloud Run Invoker| API
    API --> SA
    SA -->|IAM-authorized access| VERTEX
    SA -->|IAM-authorized access| FIRESTORE
    SA -->|IAM-authorized access| STORAGE
    SA -->|IAM-authorized access| SECRETS
```

### Identity and authorization boundaries

| Actor | Authentication | Authorization boundary |
|---|---|---|
| Enterprise user | Corporate SSO federated to Firebase Authentication | Backend derives the user identity and applies role, organization, ownership, and purpose checks. |
| Approved service caller | Service-account OIDC token | Cloud Run IAM grants the `Invoker` permission only to approved workload identities. |
| Cloud Run backend | Attached service account | IAM grants only the resource-specific roles required for Vertex AI, Firestore, Storage, secrets, and observability. |

Fine-grained authorization is layered: Cloud Run IAM controls who may invoke the backend; application authorization controls what an authenticated caller may do; and resource-level IAM controls which managed services the backend workload can access. If a web or mobile client accesses Firestore directly, Firebase Authentication and Firestore Security Rules protect that client path. Server-side FastAPI calls use the Cloud Run service account and IAM, so the backend must enforce user, organization, ownership, and purpose checks in the application layer.

## Application layers

| Layer | Responsibility | Workspace location |
|---|---|---|
| Frontend | Sign-in, experiment input, comparison, and result presentation | `frontend/` |
| API | HTTP routing, authentication boundary, validation, response serialization | `app/api/` |
| Core | Settings, security, shared error handling, and trace context | `app/core/` |
| Domain | Provider-neutral contracts for models, experiments, telemetry, and evaluation | `app/domain/` |
| Services | Model policy, orchestration, measurement, and reliability behavior | `app/services/` |
| Adapters | Vertex AI, Firebase, Firestore, Storage, and observability integrations | `app/adapters/` |
| Infrastructure | Firebase, Cloud Run, IAM, Storage, and operational configuration | `infra/` |

## Reference backend service path

```text
POST /experiments
  -> FastAPI endpoint: verify identity and validate request
  -> Experiment service: coordinate lifecycle and persistence
  -> Model gateway: enforce model and parameter policy
  -> Provider adapter: invoke Vertex AI through a provider-neutral contract
  -> Structured response: answer, tokens, cost, latency, trace ID
```

The endpoint remains thin: it authenticates, validates, and maps domain results to HTTP. Model policy, measurement, retry/fallback behavior, and persistence belong in the service and gateway layers. This follows the same separation of concerns used by the public-safe [ESP Risk Score Service](https://github.com/fmlin0429712024/industrial-operations-ai-poc/blob/main/ml/api/app.py): typed request, reusable business function, and structured response.

## Core contracts and data

An experiment request contains authenticated identity, a selected approved model configuration, a prompt, generation settings, and optional comparison metadata. An experiment response contains generated content, selected model/configuration, input/output token usage, estimated cost, provider/end-to-end latency, trace identifier, and classified error information when applicable.

Firestore stores user-scoped conversations, experiment records, evaluation results, and audit events. Each record has an owner, timestamps, and an experiment or trace identifier where relevant. Cloud Storage holds controlled evaluation datasets and generated artifacts.

## Google Cloud responsibilities

| Service | Responsibility |
|---|---|
| Firebase Authentication and enterprise SSO | Federated user sign-in and ID tokens |
| Firebase Hosting | Static web-client delivery |
| Cloud Run | FastAPI API, model gateway, and backend runtime identity |
| Vertex AI | Governed Gemini and approved-model access |
| Firestore | User-scoped operational data |
| Cloud Storage | Controlled files and evaluation artifacts |
| IAM and Secret Manager | Least-privilege access and runtime secret isolation |
| Cloud Logging and Trace | Structured operational events and request correlation |

## References

- [Firebase Authentication](https://firebase.google.com/docs/auth)
- [Cloud Firestore](https://firebase.google.com/docs/firestore)
- [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)
- [Cloud Run documentation](https://cloud.google.com/run/docs)
- [Google Cloud IAM](https://cloud.google.com/iam/docs)
