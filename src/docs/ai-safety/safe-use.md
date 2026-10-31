This is a runbook for letting an AI assistant manage processes through OxidePM. The rule of thumb: **let the AI read freely, and require a person to confirm anything that stops, restarts, deletes or truncates.**

## Commands by risk

**Safe, read-only:** `status`, `show`, `logs`, `env list`, `describe`, `check` (without `--fix`), `ping`, `monit`, `top`, `--version`.

**Caution:**

| Command | Notes |
|---|---|
| `start <target>` | Starts a process, or every app of a config file. Check the config first. An app that is already up is refused. |
| `stop`, `restart`, `reload` | Brief downtime. A stopped app stays stopped. |
| `save` | Refuses to replace a non-empty file with an empty list unless `--force`. |
| `startup` | Generates an autostart script. |
| `resurrect` | Starts everything the registry says should run. Verify the saved state first. |
| `check --fix` | Installs dependencies and creates `.env` from a template. |
| `deploy` | High: pulls code and restarts processes on a remote host. |
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
| `--watch` or `watch = true` | Refused. File watching is not available. |
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

## The web server

`oxidepm web` listens on `127.0.0.1` unless `--bind` says otherwise, and refuses a non-loopback address without `--api-key`. Without a key (loopback only) it needs no key at all, and `POST /api/processes` starts an arbitrary command. An AI must not start it without a key, and should not be given the key.
