This is a runbook for letting an AI assistant manage processes through OxidePM. The rule of thumb: **let the AI read freely, and require a person to confirm anything that stops, restarts, deletes or truncates.**

## Commands by risk

**Safe, read-only:** `status`, `show`, `logs`, `env list`, `describe`, `ping`, `top` and `--version`.

**Caution:**

| Command | Notes |
|---|---|
| `start <target>` | Starts a process, or every app of a config file. Check the config first. An app that is already up is refused. |
| `stop`, `restart`, `reload` | Brief downtime. A stopped app stays stopped. |
| `save` | Refuses to replace a non-empty file with an empty list unless `--force`. |
| `startup` | Generates an autostart script. |
| `resurrect` | Starts everything the registry says should run. Verify the saved state first. |
| `check` | The adapter command is caution-tier. `--fix` can install Node dependencies and create `.env`, and `--set-env` can edit `.env`. |
| `init` | The adapter command is caution-tier. It writes a starter `oxidepm.config.toml` into the project and leaves an existing one alone. |
| `git-start` | The adapter command is caution-tier. It clones or updates a repository into its own state directory and starts the app, which runs project code. `--install` opts into installing Node dependencies. |
| `deploy` | Pulls code and restarts processes on a remote host. |
| `diff` | Reads recent commits, working-tree status and a diff summary on a remote host. |
| `monit` | The adapter command is caution-tier. The terminal dashboard can stop and restart apps, and asks `y`/`n` first. An AI actor cannot open it, because `ui-tui` does not allow AI driving. |
| `update` | Replaces the installed binaries and stops a running daemon. |

**Dangerous:** `kill` (stops the daemon and every app), `delete`, `flush` (the log contents are lost), `restore`, `policy set`, and `show --reveal` (its output ends up in the conversation).

Treat `all` as a higher-risk variant of every command that accepts it.

## Mistakes agents make

| Mistake | What happens |
|---|---|
| A wrong `mode` | The process is run with the wrong runtime. |
| Guessed field names | The file is refused and the unknown key is named, so nothing starts. `restart` is the key for the restart mode, not `restart_mode`. |
| `restart = "always"` for a process that exits normally | It is restarted over and over, with a growing delay, until more than `max_restarts` exits fall inside `crash_window`. |
| A very high `max_restarts` | A crash loop can run for a long time. |
| Editing the config while the app runs | The running process keeps the spec it was started with. Stop it, then start the file again. |
| `env set` or `env unset` | Both are refused. Use `--env` or the config file. |
| `--watch` or `watch = true` | The CLI refuses these legacy settings. Use `[apps.adapters.watch]` to [opt in to file watching](/docs/commands/other-commands/#file-watching). |
| `pkill` or `kill -9` instead of `oxidepm stop` | OxidePM's state no longer matches the real processes. |
| `flush` to clean up | It destroys the diagnostic history. Rotation is already automatic. |
| Restarting an `errored` app without reading its logs | You find the cause first, then restart. |
| `all` when one app was meant | Unrelated services are stopped or deleted. |
| A loop of its own (`while true`, cron, a watcher) | Let OxidePM restart apps. |

## Rules

1. Review a config an AI wrote before it is started. Confirm `mode`, `script` or `bin`, `cwd`, `env`, ports and the restart policy.
2. Confirm before a destructive command: `kill`, `delete`, `flush`, or anything with `all`.
3. Read the logs before you restart. `oxidepm logs <name>` first.
4. Keep secrets out of prompts and configs. `status`, `show`, `describe` and `env list` do not show environment values, but command arguments, URLs, logs and config files are not scrubbed.
5. Put the agent on `agent.sock` and set `OXIDEPM_ACTOR`, so the limits apply whatever it does. Mark the apps it may restart `ai_control`, and the ones it must not touch `protected`.
6. Run `oxidepm describe <name>` after any config change.

## Commands that adapters provide

`web`, `monit`, `notify`, `deploy` and the other commands that [adapters provide](/docs/commands/overview/#provided-by-adapters) are caution or dangerous requests, and they go through the same policy and audit log as every other command. A session command such as `monit`, which takes over a terminal, is refused for an AI actor unless its adapter says it may be driven by one.

## The web API

The `ui-web` adapter listens on `127.0.0.1` by default and requires an access key for its API, with an exception for `/api/health`. The default grant shows all apps and permits stops and restarts only for apps that list `ui-web` under `adapters`. Keep the access key private. The daemon applies policy to requests from `adapter:ui-web` and records them in the audit log.
