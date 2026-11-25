## Daemon to adapter: requests

The adapter answers each with a `result` or an `error`.

| Method | Params | Result |
|---|---|---|
| `initialize` | `protocols`, `host`, `adapter`, `kind`, `grant`, `paths`, `limits` | `{protocol, name, version}` |
| `ping` | `{}` | `{}`. Sent every 15 seconds to a service. |
| `shutdown` | `{}` | `{}`. Sent when the adapter is stopped. |
| `runtime.prepare` | `spec`, `path_hint`, `phase` (`start` or `restart`) | `{steps, notes}` |
| `runtime.plan` | `spec`, `steps_done` | `{program, args, cwd, extra_env, binary_path}` |
| `command.invoke` | `verb`, `argv`, `cwd`, `dry_run`, `actor`, `tty` | `{exit_code, result?}` |

`runtime.prepare` and `runtime.plan` are how a runtime adapter launches an app while the core still owns the child. The adapter returns data: build steps (an `id`, an `argv`, a `cwd`, extra environment, a timeout, whether to capture output, and whether the step is optional), and then a launch plan (a program, arguments, a working directory and extra environment). The core checks and runs the steps in their own process group and spawns the plan itself. The adapter runs nothing. The `spec` it sees is a redacted view: the keys of the environment with the value `<redacted>`.

```term wrap="yes" label="runtime.prepare and its reply"
{hi:daemon:}  {"jsonrpc":"2.0","id":4,"method":"runtime.prepare","params":{"spec":{"name":"web","runtime":"node","command":"server.js","args":["--port","3000"],"cwd":"/srv/web","tags":["prod"],"ports":[3000],"instances":1,"env":{"DATABASE_URL":"<redacted>"},"options":{"node_args":["--max-old-space-size=512"]}},"path_hint":"/usr/local/bin:/usr/bin","phase":"start"}}
{dim:adapter:} {"jsonrpc":"2.0","id":4,"result":{"steps":[{"id":"install","argv":["npm","ci"],"cwd":"/srv/web","env_add":{"CI":"1"},"timeout_secs":600,"capture":"none","capture_max":65536,"optional":true,"description":"Install dependencies"}],"notes":["lockfile found"]}}
```

`command.invoke` runs a command that an adapter added to the CLI. The `actor` is the class and label of whoever asked. The `init` adapter supports dry runs and returns the generated configuration.

```term wrap="yes" label="command.invoke and its reply"
{hi:daemon:}  {"jsonrpc":"2.0","id":6,"method":"command.invoke","params":{"verb":"init","argv":[],"cwd":"/srv/web","dry_run":true,"actor":{"class":"human","label":"cli"},"tty":false}}
{dim:adapter:} {"jsonrpc":"2.0","id":6,"result":{"exit_code":0,"result":{"path":"/srv/web/oxidepm.config.toml","config":"[[apps]]\nname = \"web\"\nmode = \"npm\"\nscript = \"start\"\ncwd = \".\"\n","written":false}}}
```

## Daemon to adapter: notifications

No answer.

| Method | Params |
|---|---|
| `initialized` | `{}` |
| `event` | `{seq, kind, family, at, app?, data, options?, dropped_before?}`. See [Events](/docs/adapter-protocol/events/). |
| `cancel` | `{id}`: the request with that id was abandoned, and a late answer will be dropped. |

## Adapter to daemon

| Method | Kind | What it does |
|---|---|---|
| `host.request` | request | Asks the daemon to do something. See [The host API](/docs/adapter-protocol/host-api/). |
| `host.audit_note` | request | Writes a line to the audit log: `{"text": "..."}`. |
| `invoke.output` | notification | Streams output of a `command.invoke`: `{id, stream, text}`, with `stream` one of `stdout`, `stderr` or `status`. |
| `cancel` | notification | `{id}`. Accepted and ignored. |

The `provider.*` and `gate.*` method names are reserved.
