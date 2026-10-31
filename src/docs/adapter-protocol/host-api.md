An adapter reaches the daemon through `host.request` and nothing else. `params.request` is the object the CLI would send, for example `{"type":"stop","selector":{"by":"name","value":"web"}}`. `params.dry_run` asks for a plan instead of the action. A request that only reads ignores it. `params.end_user` is an optional label of at most 64 characters, with control characters removed, for the adapter's own end user. The answer's `result.response` is the daemon's response, exactly as the CLI would get it.

```term wrap="yes" label="host.request and its reply"
{dim:adapter:} {"jsonrpc":"2.0","id":1,"method":"host.request","params":{"request":{"type":"stop","selector":{"by":"name","value":"web"}},"dry_run":true}}
{hi:daemon:}  {"jsonrpc":"2.0","id":1,"result":{"response":{"type":"error","code":"E_POLICY_DENIED","message":"denied"}}}
```

## The daemon decides who is asking

- The request is handled as the adapter, named by the connection, under the grant the user accepted when the adapter was enabled. Nothing the adapter writes can change that. An `actor`, `reveal`, `dry_run` or any other field inside the request object, or extra fields in `params`, is not read. Only `request`, `dry_run` and `end_user` are taken from `params`.
- The request goes through the same policy, audit log and dry-run handling as a request from the CLI. A refusal is a normal response (`type: "error"`, with `E_POLICY_DENIED`, `E_PROTECTED`, `E_RATE_LIMITED`, `E_SHUTTING_DOWN` and so on), not a protocol error. Denied requests are written to the audit log with the adapter's name.
- The `end_user` label is written to the audit log as an unverified label. It is never used in a decision.

## What a grant allows

- `read`: safe requests (`status`, `show`, `describe`, `logs`, the daemon's status).
- `lifecycle`: also stops, restarts and reloads apps.
- `admin`: also starts apps and does the dangerous and global requests (`delete`, `flush`, `save`, `resurrect`).

All only on apps that are not protected, and, if the grant's scope is `opted-in`, only on apps that list the adapter under `adapters`. `kill`, `set_policy` and revealing environment values are a person's, whatever the grant.

## Logs and size

`logs` for an adapter are scrubbed of the app's environment values (those of 6 or more characters, an exact-match filter) and bounded: at most 10 000 lines and 1 MiB, the newest lines kept. An answer that would not fit in a frame is replaced by `E_REQUEST_TOO_LARGE`.

## Rates

32 requests in flight (the grant may ask for up to 128; the next one is answered with `E_ADAPTER_BUSY`, `-32029`). 50 requests a second with a burst of 100, and 5 requests that change something a minute with a burst of 10 (`E_RATE_LIMITED`). An adapter answered with `E_RATE_LIMITED` 20 times within 10 seconds commits a violation. A `params` that is not a request answers error `-32602`, and that is not a violation.

## Audit notes

`host.audit_note` takes `{"text": "..."}` and writes a line to the audit log, tagged with the adapter's name and cut at 256 characters. It counts against the same rate, and a note is dropped, not waited for, when the log's queue is full.

```term label="host.audit_note"
{dim:adapter:} {"jsonrpc":"2.0","id":2,"method":"host.audit_note","params":{"text":"sent a message"}}
```
