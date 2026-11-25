# Overview

The core commands, selectors and global flags, the commands and runtimes that adapters provide, and what you see when one is missing.

Source: https://oxidepm.com/docs/commands/overview/

## Core commands

| Command | What it does |
|---|---|
| `start <target>` | Start a process, or every app of a config file (sent as one batch). |
| `start <target> --check` | Run preflight using the `check` adapter before starting a single file or project. |
| `stop <selector>` | Stop apps. |
| `restart <selector>` | Hard restart apps. Also starts an app that is at rest. |
| `reload <selector>` | The same as `restart`. There is no zero-downtime reload. |
| `delete <selector>` | Stop apps and remove them from the registry. |
| `status [--more\|--daemon]` | The status table. `--more` adds port, working directory and policy markers. `--daemon` shows the daemon itself. |
| `show <name> [--reveal]` | One app in detail. `--reveal` also prints environment values and hook scripts. |
| `logs <name> [-f]` | Read or follow logs. |
| `flush <selector>` | Truncate the active log files. |
| `describe <name>` | Show the command that would run for an app that is already registered, without starting anything. |
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

On Linux, [import and enable the adapter from the release bundle](https://oxidepm.com/docs/adapters/import-and-enable/#import-from-the-release) to use its commands.

| Command | Adapter | What it is |
|---|---|---|
| `notify` | [notifier](https://oxidepm.com/docs/adapters/notifier/#the-notify-command) | Show, test and configure notifications to Telegram, Discord, Slack and webhooks. |
| `web`, `web status`, `web new-key` | `ui-web` | The web API and its WebSocket. See [web](https://oxidepm.com/docs/commands/other-commands/#web). |
| `monit` | `ui-tui` | The terminal dashboard, a session command that runs on your terminal. See [monit](https://oxidepm.com/docs/commands/other-commands/#monit-and-top). |
| `check [target]` | `check` | Check project readiness. |
| `init [dir]` | `init` | Generate a starter config file. |
| `git-start <url>` | `git-start` | Clone or update a repository and start it. |
| `deploy <host>`, `diff <host>` | `deploy` | Deploy over SSH and inspect the remote checkout. |

The [exporter-prometheus](https://oxidepm.com/docs/adapters/exporter-prometheus/) service serves `/metrics`. The [`watch` service](https://oxidepm.com/docs/commands/other-commands/#file-watching) restarts opted-in apps when files change.

When an adapter is not installed, the command is refused with exit code 2 and the message names the adapter:

*Terminal output of oxidepm notify when the notifier is not installed*

```text
$ oxidepm notify status
error: unrecognized subcommand 'notify'

Usage: oxidepm [OPTIONS] <COMMAND>

For more information, try '--help'.

'notify' is provided by the adapter 'notifier', which is not installed.
Install it with: oxidepm adapter import notifier   (see: oxidepm adapter list --available)
```

The import hint uses the signed-index form. This release has no configured network catalog. Use `oxidepm adapter import --bundled notifier --enable`.

## Runtimes

The core runs one runtime itself: `cmd`, which runs any program with its arguments. The language runtimes are adapters, and a release carries them:

| Runtime names | Adapter |
|---|---|
| `node`, `npm`, `pnpm`, `yarn` | `runtime-node` |
| `python` | `runtime-python` |
| `go` | `runtime-go` |
| `rust`, `cargo` | `runtime-rust` |

On Linux, the install script runs `oxidepm adapter import --bundled --tag runtime --enable --yes` after installing the release bundle. See [Runtimes](https://oxidepm.com/docs/getting-started/install/#runtimes) for manual installs. Starting an app whose runtime is missing fails and creates nothing:

*Terminal output of oxidepm start when the runtime adapter is not enabled*

```text
$ oxidepm start /srv/app/app.js
✗ runtime 'node' is provided by the adapter 'runtime-node', which is not enabled. Run: oxidepm adapter import runtime-node --enable
Error: runtime 'node' is provided by the adapter 'runtime-node', which is not enabled. Run: oxidepm adapter import runtime-node --enable
```

Use `oxidepm adapter import --bundled runtime-node --enable` with the release bundle. If the adapter is already installed, run `oxidepm adapter enable runtime-node`. The error code is `E_ADAPTER_MISSING`.

Still in the core: `top`, a live resource monitor.

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
