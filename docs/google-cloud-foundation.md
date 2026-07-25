# Google Cloud Foundation

## Service map

| Service | Platform role |
|---|---|
| Firebase Authentication | Authenticates users and issues ID tokens to the web client |
| Firestore | Stores user-scoped conversations, experiment configurations, evaluation results, and audit events |
| Vertex AI | Provides governed access to approved Gemini models |
| Cloud Storage | Stores controlled evaluation artifacts and approved application files |
| Secret Manager | Holds provider credentials and other runtime secrets outside source code |
| IAM | Grants each runtime identity only the permissions required for its responsibility |
| Cloud Logging and Trace | Supports structured operational logs and request correlation |

## Identity and authorization flow

1. The client signs in through Firebase Authentication.
2. The client sends its Firebase ID token to the API.
3. The FastAPI service validates the token and derives the user identity server-side.
4. Firestore access is constrained to the authenticated user’s data through security rules and server-side authorization.
5. The backend runtime identity accesses Vertex AI, Storage, and secrets through narrowly scoped IAM roles.

## Security principles

- Keep secrets in Secret Manager or local environment configuration, never in source control.
- Use separate identities for client users and backend workloads.
- Apply least-privilege IAM roles and scope Storage and Firestore access to the minimum required resource.
- Treat prompts, conversation history, and evaluation data as sensitive application data.
- Record security-relevant events with trace identifiers while minimizing sensitive content in logs.

## Storage design

Firestore is the operational datastore for small, structured, user-scoped records. Cloud Storage is reserved for controlled files such as evaluation datasets and generated artifacts. Each stored record should include an owner, timestamps, and a trace or experiment identifier where relevant.

## References

- [Firebase Authentication](https://firebase.google.com/docs/auth)
- [Cloud Firestore](https://firebase.google.com/docs/firestore)
- [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)
- [Cloud Storage documentation](https://cloud.google.com/storage/docs)
- [IAM overview](https://cloud.google.com/iam/docs/overview)
- [Secret Manager documentation](https://cloud.google.com/secret-manager/docs)
- [Cloud Logging documentation](https://cloud.google.com/logging/docs)
