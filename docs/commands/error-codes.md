# Error codes

The stable E_ codes, where you can see them, and what they mean.

Source: https://oxidepm.com/docs/commands/error-codes/

Errors carry a stable name that starts with `E_`. The CLI prints the message, and exits with a non-zero code. The name is what a program should match on. You can see it in the daemon's JSON responses on the socket, in the `deny` part of the [audit log](https://oxidepm.com/docs/ai-safety/audit-log/), and in the [adapter protocol](https://oxidepm.com/docs/adapter-protocol/errors/).

A crash loop is not an error code. An app in a crash loop is in the `errored` state. The reason is in the logs and in the daemon's status data.

## Requests and apps

| Code | Meaning |
|---|---|
| `E_BAD_REQUEST` | Malformed JSON or an unknown request type. |
| `E_PROTOCOL_VERSION` | The request's protocol is outside the supported range. |
| `E_REQUEST_TOO_LARGE` | A request line over the size limit. |
| `E_INVALID_SPEC` | A spec failed validation. The message names the field. |
| `E_INVALID_NAME` | An app name with a bad charset or length, or a reserved one. |
| `E_INVALID_SELECTOR` | A selector that cannot be parsed or is not allowed for the operation. |
| `E_UNSUPPORTED` | A feature that is not available: removed, or not built yet. |
| `E_APP_NOT_FOUND` | A selector matched nothing. |
| `E_APP_EXISTS` | The name is taken, or the app is already active. |
| `E_BUILD_FAILED` | The build step failed. |
| `E_SPAWN_FAILED` | The program did not resolve or could not be spawned. |
| `E_CANCELLED` | A pending start was cancelled by a stop or delete. |
| `E_SHUTTING_DOWN` | The daemon is shutting down. |
| `E_BUSY` | An app's mailbox stayed full. |
| `E_TIMEOUT` | A bounded wait expired. |

## Dependencies

| Code | Meaning |
|---|---|
| `E_DEPENDENCY_MISSING` | A dependency is not registered. |
| `E_DEPENDENCY_CYCLE` | The dependencies form a cycle. The message names it. |
| `E_DEPENDENCY_FAILED` | A dependency is `stopped` or `errored`, or failed while the app waited. |
| `E_DEPENDENCY_TIMEOUT` | The wait for dependencies passed `depends_timeout`. |

## Storage

| Code | Meaning |
|---|---|
| `E_DB` | A database error. |
| `E_IO` | A file error. |
| `E_STATE_INCOMPATIBLE` | Stored state was written by an incompatible OxidePM. |
| `E_SAVE_WOULD_EMPTY` | `save` would replace a non-empty file with an empty one. |
| `E_INTERNAL` | A bug, or an internal task died. The daemon log has the details. |

## Policy

| Code | Meaning |
|---|---|
| `E_POLICY_DENIED` | The policy refused the request for this actor. The message names the tier, the actor and the apps. |
| `E_PROTECTED` | The app is protected and the actor is not a person. |
| `E_RATE_LIMITED` | A non-human actor asked too often. |
| `E_AUDIT_UNAVAILABLE` | A non-human actor's caution or dangerous request was refused because the audit log could not record it first. |
| `E_DRY_RUN_UNSUPPORTED` | A verb or command has no dry run. |

## Adapters

| Code | Meaning |
|---|---|
| `E_ADAPTER_MISSING` | The named adapter or runtime is not imported or not enabled. |
| `E_ADAPTER_UNAVAILABLE` | Enabled but not running, failed, still starting, or its circuit breaker is open. |
| `E_ADAPTER_TIMEOUT` | A call to an adapter timed out. |
| `E_ADAPTER_CRASHED` | The adapter exited during a call. |
| `E_ADAPTER_PROTOCOL` | The adapter broke the protocol, or speaks another version. |
| `E_ADAPTER_BUSY` | The adapter's in-flight limit was reached. |
| `E_ADAPTER_INVALID` | A manifest, plan or name is invalid, or a command collides with a built-in one. |
| `E_ADAPTER_TAMPERED` | The executable's SHA-256 no longer matches the one recorded at import. |
| `E_CHECKSUM_MISMATCH` | A downloaded file does not match the checksum published for it. |
| `E_SIGNATURE_INVALID` | A signature is wrong. |
| `E_INDEX_STALE` | The index is expired or older than the last one seen. |
