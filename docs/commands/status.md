# status and show

Read what is running: the table, the extra columns, one app in detail and the daemon itself.

Source: https://oxidepm.com/docs/commands/status/

## status

*Terminal output of oxidepm status*

```text
$ oxidepm status
╭────┬──────┬──────┬─────────┬───┬────────┬──────┬───────┬────────╮
│ id │ name │ mode │ pid     │ ↺ │ status │ cpu  │ mem   │ uptime │
├────┼──────┼──────┼─────────┼───┼────────┼──────┼───────┼────────┤
│  1 │ db   │ cmd  │ 1484325 │ 0 │ online │ 0.0% │ 2.5M  │ 5s     │
│  2 │ api  │ cmd  │ 1484326 │ 0 │ online │ 0.0% │ 22.2M │ 5s     │
│  3 │ web  │ cmd  │ 1485319 │ 0 │ online │ 0.0% │ 0B    │ 0s     │
╰────┴──────┴──────┴─────────┴───┴────────┴──────┴───────┴────────╯
```

The columns are:

| Column | Meaning |
|---|---|
| `id` | The app's id. |
| `name` | The name. |
| `mode` | The runtime. |
| `pid` | The process id, or `-` when it is not running. |
| `↺` | Restarts. |
| `status` | One of the [states](https://oxidepm.com/docs/configuration/restarts/). The table calls a running app `online`. |
| `cpu`, `mem` | Sampled from the app's first process. |
| `uptime` | Time since the launch. |

## status --more

*Terminal output of oxidepm status --more*

```text
$ oxidepm status --more
╭────┬──────┬──────┬─────────┬───┬────────┬──────┬─────────────────────┬────────┬────────────╮
│ id │ name │ mode │ pid     │ ↺ │ status │ port │ cwd                 │ uptime │ policy     │
├────┼──────┼──────┼─────────┼───┼────────┼──────┼─────────────────────┼────────┼────────────┤
│  1 │ db   │ cmd  │ 1484325 │ 0 │ online │ -    │ …/shopfront/current │ 5s     │ protected  │
│  2 │ api  │ cmd  │ 1484326 │ 0 │ online │ -    │ …/shopfront/current │ 5s     │ ai-control │
│  3 │ web  │ cmd  │ 1485319 │ 0 │ online │ -    │ …/shopfront/current │ 0s     │ ai-control │
╰────┴──────┴──────┴─────────┴───┴────────┴──────┴─────────────────────┴────────┴────────────╯
```

`--more` swaps `cpu` and `mem` for `port` and `cwd` and adds `policy`, which is `-`, `protected`, `ai-control`, or both. The working directory is shortened from the left.

## status --daemon

*Terminal output of oxidepm status --daemon*

```text
$ oxidepm status --daemon
audit log:    ok
agent socket: bound
sandbox:      landlock abi 10 (restricts unix connect), seccomp, ptrace_scope 1 (launcher installed)
```

`--daemon` shows how the daemon itself is: whether the audit log is `ok` or `degraded`, whether the agent socket is bound, what the [sandbox](https://oxidepm.com/docs/adapters/sandbox/) can enforce on this machine, the state of each enabled adapter, and warnings, for example about an app whose runtime adapter is not enabled.

## show

```sh
oxidepm show api
oxidepm show api --reveal
```

`show` prints one app in detail: its state, command, working directory, arguments and last exit code. Environment values show as `<redacted>` and scripts as `<set>`. `--reveal` prints them, and the daemon writes a line to its log each time. It is a dangerous request, so an AI actor cannot make it.

`describe <name>` takes the name or id of an app that is already registered, and shows the command that would run for it, without starting anything. It does not take a file or a command to be started.
