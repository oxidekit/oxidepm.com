# Handshake and lifecycle

How an adapter starts, is checked and is stopped.

Source: https://oxidepm.com/docs/adapter-protocol/lifecycle/

## The handshake

The daemon speaks first. The adapter stays silent until it receives `initialize`; a frame sent before that is a violation.

*initialize and its reply*

```text
daemon:  {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocols":[1],"host":{"name":"oxidepmd","version":"0.4.0"},"adapter":{"name":"notifier","version":"0.1.0"},"kind":"service","grant":{"level":"read","scope":"all"},"paths":{"state":"/home/u/.oxidepm/adapters/state/notifier"},"limits":{"max_line":262144,"max_in_flight":32,"event_queue":1024}}}
adapter: {"jsonrpc":"2.0","id":1,"result":{"protocol":1,"name":"notifier","version":"0.1.0"}}
daemon:  {"jsonrpc":"2.0","method":"initialized","params":{}}
```

The version numbers in this example are illustrative. The daemon puts its own version in `host.version`.

- The adapter must answer within 10 seconds, with the highest protocol it shares with `protocols`, and its own `name` and `version`.
- The daemon compares `name` and `version` with what it has on record. A difference means the executable is not what was installed: the adapter is killed and marked failed (`tampered`) and does not start again.
- A protocol that is not in the offered list, or an error `-32022` (optionally with `data.supported`), marks the adapter failed (`incompatible`).
- After a good reply, the daemon sends the notification `initialized`. A `service` then receives events. A `tool` is idle until a request arrives.
- A silent or broken handshake ends the process. It counts as a crash, and the supervisor restarts it with a growing delay until it gives up.

*A reply that refuses the protocol*

```text
adapter: {"jsonrpc":"2.0","id":1,"error":{"code":-32022,"message":"unsupported protocol","data":{"supported":[1],"code":"E_ADAPTER_PROTOCOL"}}}
```

## Staying alive

A service is sent `ping` every 15 seconds and has 5 seconds to answer. Three misses in a row kill it. A tool is not pinged: it is started for a request, kept warm for 30 seconds, and asked to exit when idle.

*ping*

```text
daemon:  {"jsonrpc":"2.0","id":2,"method":"ping","params":{}}
adapter: {"jsonrpc":"2.0","id":2,"result":{}}
```

## Timeouts and cancellation

- Every wait for an adapter is a timer in the daemon. The adapter's cooperation is not needed.
- When a deadline passes, or the caller goes away, the daemon forgets the request at once, sends `cancel {id}` and remembers the id. A reply with that id (a late answer, or error `-32024` from an adapter that obeyed the cancel) is dropped and counted, without a strike. An id that was never issued is a strike.
- When the connection ends for any reason, every request in flight fails with `E_ADAPTER_CRASHED`.

## Shutdown

When the adapter is stopped, the daemon sends `shutdown` and waits up to 2 seconds. It then closes the adapter's standard input (the adapter must also exit when its input closes), waits until 2 seconds are over, sends SIGTERM to the adapter's process group, waits until 5 seconds are over in all, and then sends SIGKILL. The total is fixed. Queued events are written first, for up to a second.
