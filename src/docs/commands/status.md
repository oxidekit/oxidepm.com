## status

```term cap="status-docs" label="Terminal output of oxidepm status"
```

The columns are:

| Column | Meaning |
|---|---|
| `id` | The app's id. |
| `name` | The name. |
| `mode` | The runtime. |
| `pid` | The process id, or `-` when it is not running. |
| `↺` | Restarts. |
| `status` | One of the [states](/docs/configuration/restarts/). The table calls a running app `online`. |
| `cpu`, `mem` | Sampled from the app's first process. |
| `uptime` | Time since the launch. |

## status --more

```term cap="status-more" label="Terminal output of oxidepm status --more"
```

`--more` swaps `cpu` and `mem` for `port` and `cwd` and adds `policy`, which is `-`, `protected`, `ai-control`, or both. The working directory is shortened from the left.

## status --daemon

```term cap="status-daemon" label="Terminal output of oxidepm status --daemon"
```

`--daemon` shows how the daemon itself is: whether the audit log is `ok` or `degraded`, whether the agent socket is bound, what the [sandbox](/docs/adapters/sandbox/) can enforce on this machine, the state of each enabled adapter, and warnings, for example about an app whose runtime adapter is not enabled.

## show

```sh
oxidepm show api
oxidepm show api --reveal
```

`show` prints one app in detail: its state, command, working directory, arguments and last exit code. Environment values show as `<redacted>` and scripts as `<set>`. `--reveal` prints them, and the daemon writes a line to its log each time. It is a dangerous request, so an AI actor cannot make it.

`describe <name>` takes the name or id of an app that is already registered, and shows the command that would run for it, without starting anything. It does not take a file or a command to be started.
