# Daemon settings

The optional daemon.toml and the files in the data directory.

Source: https://oxidepm.com/docs/configuration/daemon-settings/

## daemon.toml

`daemon.toml` in the data directory holds the daemon's own settings. The file is optional. An unknown key, or a value out of range, keeps the daemon from starting, and the error names it.

- `shutdown_budget_secs` (number, default: 120): Seconds the daemon spends stopping its apps on shutdown, from 10 to 900. The apps are stopped in dependency layers and the budget is shared between the layers. `oxidepm startup` uses it for `TimeoutStopSec`.
- `launch_concurrency` (number, default: 4): How many apps may build and spawn at once, from 1 to 64.
- `agent_socket` (boolean, default: true): Bind `agent.sock`, the socket whose every connection is an AI agent. See [Agent connections](/docs/ai-safety/agent-connections/).
- `reuse_plan` (boolean, default: true): An app whose runtime an adapter provides keeps the launch plan the adapter made, and a resurrect at boot or an automatic launch may start from it when the app, the adapter and its executable are unchanged: at once if the plan had no build steps, otherwise only when the adapter cannot be asked, and then with a warning. `false` always asks the adapter. A start or restart by a person never uses a stored plan.

## The data directory

Everything is in `~/.oxidepm`. The `OXIDEPM_HOME` environment variable names another directory.

```text
~/.oxidepm/
├── daemon.sock     # the CLI's socket (mode 0600)
├── agent.sock      # the socket for AI agents; every connection is class ai
├── oxidepmd.lock   # held by the running daemon: one daemon per home
├── daemon.toml     # optional daemon settings
├── state.db        # SQLite: full app specs and the two policy markers
├── daemon.log      # what the daemon wrote to stderr while it started (fatal startup errors)
├── daemon.log.DATE # the daemon's log, one file a day, the last 7 days kept
├── saved.json      # the saved process list
├── pids.json       # live app processes
├── audit/          # audit.jsonl and audit-security.jsonl
├── adapters.db     # SQLite: installed adapters, grants and consent (with -wal and -shm files while it is open)
├── adapter-pids.json # live adapter processes
├── adapters/       # installed adapters and their state (index, installed, staging, state, trash, verbs.json)
├── adapter-logs/   # each adapter's stderr log
└── logs/           # app logs
```

## The sockets

The CLI and the daemon talk over `daemon.sock`, with mode 0600. The daemon drops connections from any other user. `OXIDEPM_SOCKET` names another socket for the CLI. A request is one line of JSON in an envelope that carries the protocol version (2) and a request id, and the answer is one line. A line may be up to 10 MiB, and a connection that sends nothing for 5 minutes is closed.

`agent.sock` is tighter: lines of at most 1 MiB, at most 32 connections at once, and a connection that is idle for 60 seconds is closed.
