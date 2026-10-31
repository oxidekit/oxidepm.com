## Core commands

| Command | What it does |
|---|---|
| `start <target>` | Start a process, or every app of a config file (sent as one batch). |
| `stop <selector>` | Stop apps. |
| `restart <selector>` | Hard restart apps. Also starts an app that is at rest. |
| `reload <selector>` | The same as `restart`. There is no zero-downtime reload. |
| `delete <selector>` | Stop apps and remove them from the registry. |
| `status [--more\|--daemon]` | The status table. `--more` adds port, working directory and policy markers. `--daemon` shows the daemon itself. |
| `show <name> [--reveal]` | One app in detail. `--reveal` also prints environment values and hook scripts. |
| `logs <name> [-f]` | Read or follow logs. |
| `flush <selector>` | Truncate the active log files. |
| `describe <target>` | Show the command that would run, without starting it. |
| `policy set <selector>` | Change the `protected` and `ai_control` markers of running apps. |
| `audit` | Read the audit log. |
| `save [--force]`, `resurrect` | Write and restore the list of apps that should run. |
| `startup [systemd\|launchd]` | Generate an autostart script. |
| `ping` | Check that the daemon is alive. |
| `kill` | Stop the daemon and every app. |
| `env list` | The keys of an app's environment. |
| `update [--version X] [--force]` | Update to a release. |
| `backup`, `restore <file>` | Export and restore the config and process list. |
| `adapter` | Find, import, enable and manage adapters. |
| `completions <shell>`, `man` | Shell completions and the man page. |

## Provided by adapters

| Command | Adapter |
|---|---|
| `notify status\|test\|events\|severity\|telegram\|remove` | The [notifier](/docs/adapters/notifier/). Without it, `oxidepm notify` prints how to install it, and no notifications are sent. |

The Prometheus `/metrics` endpoint is no longer part of the web server: the [exporter-prometheus](/docs/adapters/exporter-prometheus/) adapter serves it.

## Still in the core today

These commands are built into the core now. The core already reserves the names of the adapters that are planned to take them over, so expect them to move: `web` (the Web API and WebSocket), `monit` (the terminal dashboard), `check` and `init`, `start --git` and `start --setup`, `deploy` and `diff`, and the Node.js, Python, Go and Cargo runtimes. `top` is a live resource monitor.

## Selectors

A selector is an app name, an id, `all`, or `@tag` for a group. A cluster (`web`) and its instances (`web-0`, `web-1`) are selected as one when a tag or `all` matches both. An AI actor may not use `all` or a tag with `stop`, `restart` or `reload`.

## Global flags

| Flag | Meaning |
|---|---|
| `--json` | Print machine-readable output instead of tables. |
| `--dry-run` | Say what the command would do and change nothing. |
| `-v` | More logging (`-vv`, `-vvv`). |

## Environment variables

| Variable | Meaning |
|---|---|
| `OXIDEPM_HOME` | Use this data directory instead of `~/.oxidepm`. |
| `OXIDEPM_SOCKET` | The socket the CLI talks to. |
| `OXIDEPM_ACTOR` | The actor the CLI claims to be, such as `ai:assistant`. A claim can only make a request stricter. |
