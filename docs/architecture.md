# Architecture

## Purpose

The platform separates application concerns from model-provider concerns so that model selection, measurement, and reliability behavior are consistent across approved models.

## Request flow

```text
Client
  -> Firebase Authentication
  -> Cloud Run / FastAPI API (identity validation and request contract)
  -> Model gateway (policy, routing, measurement)
  -> Provider adapter (Vertex AI / Gemini)
  -> Structured response and telemetry
```

## Deployment boundary

The initial deployment topology has Firebase Hosting for the static web client and one backend container: a Cloud Run service containing the FastAPI API and model gateway. Firebase Hosting does not require a user-managed container. The Cloud Run service keeps the API contract, model-routing policy, response measurement, and provider adapter in one independently deployable service.

Firebase Authentication is used by the web client for sign-in. The Cloud Run service validates Firebase ID tokens and uses its attached service account for server-side access to Google Cloud services. The service account receives only the IAM permissions needed for Vertex AI, Firestore, Cloud Storage, Secret Manager, and observability services.

The web client is delivered to the browser through Firebase Hosting and is separate from the backend runtime. It is not trusted with provider credentials or privileged Google Cloud permissions.

## Service responsibilities

| Component | Responsibility |
|---|---|
| Web client | Sign-in, experiment input, result presentation |
| Firebase Authentication | User identity and ID tokens |
| FastAPI API | Token validation, typed API boundary, response contract |
| Model gateway | Model policy, parameter validation, token/cost/latency measurement |
| Provider adapter | Provider-specific request and response translation |
| Firestore | User-scoped conversations, experiments, evaluations, audit events |
| Cloud Storage | Controlled evaluation artifacts and approved application files |

## Response contract

Every model response should return the generated content and the measurements needed for comparison:

- selected model and configuration;
- input and output token usage;
- estimated cost;
- provider and end-to-end latency;
- trace identifier and error classification when applicable.

## Operational controls

Provider calls are governed by explicit timeout, retry, fallback, rate-limit, and circuit-breaker policies. The gateway records structured events so failures can be correlated by trace identifier without recording sensitive prompt content unnecessarily.

## References

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [Firebase Authentication documentation](https://firebase.google.com/docs/auth)
- [Cloud Firestore documentation](https://firebase.google.com/docs/firestore)
- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
