# Errors

Error codes in the protocol, and what fails closed or open.

Source: https://oxidepm.com/docs/adapter-protocol/errors/

An error response is `{code, message, data?}`. `data.code` is the stable name.

## Numeric codes

The numeric codes are the JSON-RPC ones, and those of OxidePM's own range.

| Code | Meaning | Name |
|---|---|---|
| `-32700` | Parse error | |
| `-32600` | Invalid request | |
| `-32601` | Method not found | |
| `-32602` | Invalid params | |
| `-32603` | Internal error | |
| `-32022` | Unsupported protocol | `E_ADAPTER_PROTOCOL` |
| `-32023` | Permission denied | `E_POLICY_DENIED` |
| `-32024` | Cancelled | |
| `-32025` | Timeout | `E_ADAPTER_TIMEOUT` |
| `-32026` | Shutting down | |
| `-32027` | Dry run unsupported | `E_DRY_RUN_UNSUPPORTED` |
| `-32028` | Rate limited | `E_RATE_LIMITED` |
| `-32029` | Busy | `E_ADAPTER_BUSY` |

*A permission error*

```text
daemon: {"jsonrpc":"2.0","id":7,"error":{"code":-32023,"message":"outside the grant","data":{"code":"E_POLICY_DENIED"}}}
```

The other stable names are listed under [Error codes](https://oxidepm.com/docs/commands/error-codes/).

## What fails closed

The operation does not happen:

- The executable's SHA-256 differs from the one recorded at install: it is not started (`E_ADAPTER_TAMPERED`).
- The handshake names another adapter or version, or no common protocol: the adapter is killed and marked failed.
- A request to an adapter that is missing, failed or not ready fails with a named error. There is no silent fallback.
- A frame that is not valid, too large or out of turn is never acted on.
- The sandbox cannot be set up as the grant says: the adapter is not started.

## What fails open

The daemon carries on:

- Events to a service are dropped, and counted, when its queue is full or it is down.
- An adapter that crashes, hangs, floods or breaks the protocol is killed and restarted with backoff. The apps the daemon supervises are not touched.
- Unknown fields, unknown notifications and floods on standard error are ignored or dropped.

The daemon never stops, restarts, signals or changes an app because an adapter failed.
