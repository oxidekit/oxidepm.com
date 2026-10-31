## update

`oxidepm update [--version X] [--force]` updates to a release. See [Upgrade](/docs/getting-started/upgrade/).

## backup and restore

```sh
oxidepm backup --output my-server-backup.tar.gz
scp my-server-backup.tar.gz user@newserver:~
ssh user@newserver "oxidepm restore my-server-backup.tar.gz && oxidepm resurrect"
```

`backup` exports the config and the process list to a tarball. `restore` restores it, and the daemon must not be running. `-y` overwrites existing files without asking. A backup does not include the notifier's configuration, because it holds tokens.

## env

`oxidepm env list <name>` lists the keys of an app's environment. `env set` and `env unset` are refused. See [Environment and hooks](/docs/configuration/environment-and-hooks/).

## adapter

`oxidepm adapter import`, `list`, `info`, `search`, `enable`, `disable`, `update` and `remove`. See [Import and enable](/docs/adapters/import-and-enable/).

## init and check

These two are still built into the core.

```sh
oxidepm init ./my-project          # scan a directory and write oxidepm.config.toml
oxidepm check ./my-app             # is the project ready to run?
oxidepm check ./my-app --fix       # install dependencies, create .env
oxidepm start ./my-app --setup     # the same, then start
```

`init` detects Node.js (npm, pnpm, yarn), Cargo, Python and Go projects. `check` looks for `node_modules/` and a lockfile for Node.js, `Cargo.lock` for Cargo, and a `.env` file for all of them (`--fix` copies it from `.env.example`).

## deploy and diff

These two are still built into the core.

```sh
oxidepm deploy user@myserver --cwd /srv/myapp --post "npm run build" --restart api
oxidepm deploy user@myserver --cwd /srv/myapp --branch main --dry-run
oxidepm diff user@myserver --cwd /srv/myapp --count 10
```

`deploy` pulls code on the remote host over SSH and restarts processes. It needs SSH key authentication: no password prompts. `--dry-run` prints the commands without running them. `diff` shows the remote git history since the last deploy. Both are dangerous: an AI actor should never run `deploy` without a person confirming it.

## web

```sh
oxidepm web --port 9615 --api-key your-secret-key
```

The Web API and WebSocket server is still built into the core. It listens on `127.0.0.1` by default. `--bind <ip>` picks another address, and an address that is not loopback (`0.0.0.0` included) is refused with exit code 2 unless `--api-key` is set. With a key on a loopback address everything except `/api/health` needs the key; without a key every route is open to anything that can reach the port on this machine, and that includes starting a command. The key travels in cleartext, so put TLS in front of the server for anything but loopback.

| Endpoint | Method | Key | Description |
|---|---|---|---|
| `/api/health` | GET | No | Health and version. |
| `/api/processes` | GET, POST | Yes | List all, or start an app. |
| `/api/processes/:selector` | GET, DELETE | Yes | One app, or delete it. |
| `/api/processes/:selector/stop` | POST | Yes | Stop. |
| `/api/processes/:selector/restart` | POST | Yes | Restart. |
| `/api/processes/:selector/logs` | GET | Yes | Logs. |
| `/api/ping` | GET | Yes | Ask the daemon whether it is alive. |
| `/api/save`, `/api/resurrect` | POST | Yes | Save, and start the saved apps. |
| `/ws` | WebSocket | Yes | Real-time updates. |

The key is the `X-API-Key` header. The web server has no `/metrics`: use the [Prometheus exporter](/docs/adapters/exporter-prometheus/).

## monit and top

`oxidepm monit` is a terminal dashboard with a process list, a log viewer and start, stop and restart controls. `oxidepm top` is a live resource monitor. `monit` is still built into the core.

## completions and man

```sh
oxidepm completions bash > /etc/bash_completion.d/oxidepm
oxidepm completions zsh > ~/.zfunc/_oxidepm
oxidepm completions fish > ~/.config/fish/completions/oxidepm.fish
oxidepm man
```
