This is how `oxidepmd` talks to an adapter: an executable it starts and supervises. This is protocol version 1. The examples on these pages are the reference frames that the daemon, its test adapter and the protocol crate's own tests all read. Changing one is a protocol change and needs a new protocol number.

## Transport and framing

- The adapter's standard input carries daemon to adapter, and its standard output adapter to daemon. Both are UTF-8, one JSON object per line, ended by `\n`. A frame never contains a raw newline.
- Each object is a JSON-RPC 2.0 message with these restrictions:
  - `"jsonrpc":"2.0"` is required. There are no batches: an array is a violation.
  - `id` is an unsigned 64-bit integer. Each side numbers its own requests from 1 and never reuses a number.
  - `params` and `result` are objects. A missing `params` means `{}`.
  - `method` is 1 to 64 characters of letters, digits, `.`, `_` and `-`.
  - A response has `result` or `error`, never both. An error is `{code: integer, message: string, data?}`.
  - A line that is empty, contains a NUL byte or is not valid UTF-8 is not a frame.
- Unknown fields are ignored. An unknown request method is answered with error `-32601`. An unknown notification is ignored.
- Standard output carries protocol and nothing else. Standard error is the adapter's log: lines are cut at 8 KiB, rate limited to 1 MiB per second, kept in the adapter's own rotated file (1 MiB, 5 files) and never mixed into the daemon's log.

## The environment

The adapter is started with a cleared environment: a short base (`PATH`, `LANG`, `HOME` set to its state directory), the names its manifest lists in `env_pass`, and `OXIDEPM_ADAPTER_PROTOCOLS`, the comma-separated protocol numbers the daemon speaks. A process that finds that variable missing was not started by the daemon.

## Kinds

`service` is resident and receives events. `tool` is started on demand and exits when idle. The kind is set in the manifest and sent in `initialize`. Only a `tool` can run a session verb, a command that owns the terminal, so its standard input and output are not the protocol channel. See [Session verbs](/docs/adapter-protocol/lifecycle/#session-verbs).

## Where to read on

- [Messages](/docs/adapter-protocol/messages/): every method.
- [Handshake and lifecycle](/docs/adapter-protocol/lifecycle/): starting, checking, stopping and session verbs.
- [The host API](/docs/adapter-protocol/host-api/): how an adapter asks the daemon to act.
- [Events](/docs/adapter-protocol/events/): what a service is told.
- [Limits and timeouts](/docs/adapter-protocol/limits/) and [Errors](/docs/adapter-protocol/errors/).
- [Write an adapter](/docs/adapter-protocol/write-an-adapter/): the manifest and the archive.
