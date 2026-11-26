## The handshake

The daemon speaks first. The adapter stays silent until it receives `initialize`; a frame sent before that is a violation.

```term wrap="yes" label="initialize and its reply"
{hi:daemon:}  {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocols":[1],"host":{"name":"oxidepmd","version":"{{release_version}}"},"adapter":{"name":"notifier","version":"{{release_version}}"},"kind":"service","grant":{"level":"read","scope":"all"},"paths":{"state":"/home/u/.oxidepm/adapters/state/notifier"},"limits":{"max_line":262144,"max_in_flight":32,"event_queue":1024}}}
{dim:adapter:} {"jsonrpc":"2.0","id":1,"result":{"protocol":1,"name":"notifier","version":"{{release_version}}"}}
{hi:daemon:}  {"jsonrpc":"2.0","method":"initialized","params":{}}
```

The version numbers in this example are illustrative. The daemon puts its own version in `host.version`.

- The adapter must answer within 10 seconds, with the highest protocol it shares with `protocols`, and its own `name` and `version`.
- The daemon compares `name` and `version` with what it has on record. A difference means the executable is not what was installed: the adapter is killed and marked failed (`tampered`) and does not start again.
- A protocol that is not in the offered list, or an error `-32022` (optionally with `data.supported`), marks the adapter failed (`incompatible`).
- After a good reply, the daemon sends the notification `initialized`. A `service` then receives events. A `tool` is idle until a request arrives.
- A silent or broken handshake ends the process. It counts as a crash, and the supervisor restarts it with a growing delay until it gives up.

```term wrap="yes" label="A reply that refuses the protocol"
{dim:adapter:} {"jsonrpc":"2.0","id":1,"error":{"code":-32022,"message":"unsupported protocol","data":{"supported":[1],"code":"E_ADAPTER_PROTOCOL"}}}
```

## Staying alive

A service is sent `ping` every 15 seconds and has 5 seconds to answer. Three misses in a row kill it. A tool is not pinged: it is started for a request, kept warm for 30 seconds, and asked to exit when idle.

```term label="ping"
{hi:daemon:}  {"jsonrpc":"2.0","id":2,"method":"ping","params":{}}
{dim:adapter:} {"jsonrpc":"2.0","id":2,"result":{}}
```

## Timeouts and cancellation

- Every wait for an adapter is a timer in the daemon. The adapter's cooperation is not needed.
- When a deadline passes, or the caller goes away, the daemon forgets the request at once, sends `cancel {id}` and remembers the id. A reply with that id (a late answer, or error `-32024` from an adapter that obeyed the cancel) is dropped and counted, without a strike. An id that was never issued is a strike.
- When the connection ends for any reason, every request in flight fails with `E_ADAPTER_CRASHED`.

## Shutdown

When the adapter is stopped, the daemon sends `shutdown` and waits up to 2 seconds. It then closes the adapter's standard input (the adapter must also exit when its input closes), waits until 2 seconds are over, sends SIGTERM to the adapter's process group, waits until 5 seconds are over in all, and then sends SIGKILL. The total is fixed. Queued events are written first, for up to a second.

## Session verbs

A verb whose manifest entry says `"mode": "session"` needs the terminal (a dashboard) or the pipes of the program that started `oxidepm` (an MCP server over stdio). Only a `tool` can run one. Its standard input and output then belong to the terminal or the pipes, so they cannot carry the protocol. A session verb has no `--dry-run`.

1. `oxidepm <verb>` asks the daemon for a session. The daemon applies the policy and answers with the path of a fresh socket and a token. The CLI connects only if that socket belongs to the same user and sits in a directory only that user can write to. With its first line it hands over its own standard input and output as open descriptors, then it waits.
2. The daemon starts the adapter as for any other call: the same launcher and profile, and the executable checked against the digest recorded at import. The adapter's standard input and output are the descriptors the CLI handed over. Standard error is still its log and never reaches the terminal.
3. The adapter finds `OXIDEPM_SESSION_SOCKET` (a path under 100 bytes) and `OXIDEPM_SESSION_TOKEN` in its environment. The token works for 60 seconds from the moment the session was opened. In that time the adapter connects to the socket and sends one line: `{"session":"adapter","token":"<token>"}`. Nothing else may come first. The token works once, and the socket is removed as soon as the adapter is connected.
4. From then on the protocol runs over that connection instead of standard input and output. The daemon sends `initialize`, then `initialized`, then `command.invoke` with `tty` set when the CLI's standard input is a terminal. The adapter's `host.request` calls are handled as `adapter:<name>` and recorded in the audit log with the channel `adapter_session`.
5. The answer to `command.invoke` ends the session. Its `exit_code` is the exit code of `oxidepm <verb>`, and the daemon then stops the adapter as it does after any call. An error ends the session too, and the CLI prints it with its code.

The session also ends when the CLI goes away (the adapter's process group is killed), when the adapter is disabled or the daemon stops, and after 12 hours at most. At most 4 sessions exist at once, pending ones included. A fifth request fails with `E_ADAPTER_BUSY`.

### The terminal

The adapter runs in the daemon's session, not in the terminal's, so it cannot count on `/dev/tty`: it reads and writes its standard input and output. A Ctrl-C typed at a terminal that is not in raw mode reaches the CLI, which ends the session and exits with 130. A terminal in raw mode delivers Ctrl-C as a key. When the window changes size, the CLI tells the daemon, which sends `SIGWINCH` to the adapter's process group. The size is read with `TIOCGWINSZ` on descriptor 1. The CLI puts back the terminal settings it found when the session ends, whatever the adapter left.

### Who may open one

A person may open any session verb. An AI actor may open one only for a verb of an adapter whose manifest says `ai_driven`, and only while that adapter's grant is `read`. What such a session writes is limited to the adapter's state directory. An adapter can never open one.
