# Other commands

Update, backup and restore, env, top, completions, and the commands that adapters provide: web, monit, init, check, deploy and diff.

Source: https://oxidepm.com/docs/commands/other-commands/

## update

`oxidepm update [--version X] [--force]` updates to a release. See [Upgrade](https://oxidepm.com/docs/getting-started/upgrade/).

## backup and restore

```sh
oxidepm backup --output my-server-backup.tar.gz
scp my-server-backup.tar.gz user@newserver:~
ssh user@newserver "oxidepm restore my-server-backup.tar.gz && oxidepm resurrect"
```

`backup` exports the config and the process list to a tarball. `restore` restores it, and the daemon must not be running. `-y` overwrites existing files without asking. A backup does not include the notifier's configuration, because it holds tokens.

## env

`oxidepm env list <name>` lists the keys of an app's environment. `env set` and `env unset` are refused. See [Environment and hooks](https://oxidepm.com/docs/configuration/environment-and-hooks/).

## adapter

`oxidepm adapter import`, `list`, `info`, `search`, `enable`, `disable`, `update` and `remove`. See [Import and enable](https://oxidepm.com/docs/adapters/import-and-enable/).

## Commands that come from adapters

The commands below are not in the core. Each one is provided by an adapter you import and enable, and the core only knows the name. Without the adapter, the command is refused with exit code 2 and a message such as `'web' is provided by the adapter 'ui-web', which is not installed.` followed by the `oxidepm adapter import` command to run. See [Provided by adapters](https://oxidepm.com/docs/commands/overview/#provided-by-adapters).

## init and check

Provided by the `init` and `check` adapters, which are planned and not published yet.

```sh
oxidepm init ./my-project          # scan a directory and write oxidepm.config.toml
oxidepm check ./my-app             # is the project ready to run?
oxidepm check ./my-app --fix       # install dependencies, create .env
oxidepm start ./my-app --setup     # the same, then start
```

`init` detects Node.js (npm, pnpm, yarn), Cargo, Python and Go projects. `check` looks for `node_modules/` and a lockfile for Node.js, `Cargo.lock` for Cargo, and a `.env` file for all of them (`--fix` copies it from `.env.example`).

## deploy and diff

Provided by the `deploy` adapter, which is planned and not published yet. `start --git <url>` is provided by the `git-start` adapter.

```sh
oxidepm deploy user@myserver --cwd /srv/myapp --post "npm run build" --restart api
oxidepm deploy user@myserver --cwd /srv/myapp --branch main --dry-run
oxidepm diff user@myserver --cwd /srv/myapp --count 10
```

`deploy` pulls code on the remote host over SSH and restarts processes. It needs SSH key authentication: no password prompts. `diff` shows the remote git history since the last deploy. Both are dangerous: an AI actor should never run `deploy` without a person confirming it.

## web

Provided by the `ui-web` adapter. It is built and tested; its archive is not published yet.

```sh
oxidepm adapter import ui-web --enable
oxidepm web              # where it listens, and its access key (shown once)
oxidepm web new-key      # replace the key
```

The adapter serves a REST API and a WebSocket on `127.0.0.1:9615`. Every request, loopback included, needs the access key in the `X-API-Key` header. Only `/api/health` needs none. The first start makes a random key in the adapter's `config.toml`, and a browser WebSocket sends the key as a subprotocol, never in the URL. The `Host` header must be the address it is bound to, and `Origin` must be absent or the one set in `config.toml`, so a web page you visit cannot drive the API.

By default it works on the apps that list `ui-web` under `adapters`, at the `lifecycle` level: it shows every app and can restart, stop and reload the opted-in ones. It cannot create or delete apps or flush logs. There is no TLS: put a reverse proxy in front for anything but a trusted network. The daemon sees each request as the actor `adapter:ui-web`, so its policy and audit log apply.

| Endpoint | Method | Key | Description |
|---|---|---|---|
| `/api/health` | GET | No | `{"ok":true}`. |
| `/api/processes` | GET | Yes | All apps. |
| `/api/processes/:selector` | GET | Yes | One app. |
| `/api/processes/:selector/stop` | POST | Yes | Stop. |
| `/api/processes/:selector/restart` | POST | Yes | Restart. |
| `/api/processes/:selector/logs` | GET | Yes | Logs. |
| `/api/ping` | GET | Yes | Ask the daemon whether it is alive. |
| `/api/save`, `/api/resurrect` | POST | Yes | Save, and start the saved apps. |
| `/ws` | WebSocket | Yes | The daemon's lifecycle events as they happen. |

`POST /api/processes` (start an app) and `DELETE` need the adapter to hold the `admin` level, and answer 403 otherwise. The adapter has no `/metrics`: use the [Prometheus exporter](https://oxidepm.com/docs/adapters/exporter-prometheus/).

## monit and top

`oxidepm monit` is the terminal dashboard of the `ui-tui` adapter: the apps with state, CPU and memory, the selected app in detail and a log viewer. It can stop and restart apps, and asks for `y` or `n` first. It is a session command: the daemon starts the adapter on your terminal for as long as the dashboard is open, and it needs a terminal for input and output. The adapter is built and tested; its archive is not published yet.

```sh
oxidepm adapter import ui-tui --enable
oxidepm monit
```

`oxidepm top`, a live resource monitor, is still in the core.

## completions and man

```sh
oxidepm completions bash > /etc/bash_completion.d/oxidepm
oxidepm completions zsh > ~/.zfunc/_oxidepm
oxidepm completions fish > ~/.config/fish/completions/oxidepm.fish
oxidepm man
```
