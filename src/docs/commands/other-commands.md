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

## Commands that come from adapters

On Linux, [build, import and enable the optional adapter](/docs/adapters/import-and-enable/#build-an-optional-adapter) before using its commands. The CLI names the adapter when a command is unavailable. See [Provided by adapters](/docs/commands/overview/#provided-by-adapters).

## init and check

Import the `init` and `check` adapters to generate a project config and check project readiness.

```sh
oxidepm init ./my-project          # scan a directory and write oxidepm.config.toml
oxidepm check ./my-app             # is the project ready to run?
oxidepm check ./my-app --fix       # install dependencies, create .env
oxidepm start ./my-app --check     # check before starting one app
oxidepm --dry-run init ./my-project
```

`init` detects Node.js, Cargo, Python and Go projects and preserves existing configs. `check` reports on dependencies, lockfiles, environment files and port availability. With `--strict`, warnings make it fail. `--fix` can install Node dependencies and create `.env` from a template, and `--set-env KEY=VALUE` edits `.env`. Both write options are limited to projects within the current directory.

## git-start

The `git-start` adapter prepares a Git checkout in its own state directory and starts it. Use `--offline` to reuse a local checkout or `--no-start` to prepare it without launching. `--install` opts into Node dependency installation. Add `--allow-scripts` to allow dependency lifecycle scripts.

```sh
oxidepm git-start https://github.com/user/repo --branch main
oxidepm --dry-run git-start https://github.com/user/repo
```

## deploy and diff

The `deploy` adapter provides both commands.

```sh
oxidepm deploy user@myserver --cwd /srv/myapp --post "npm run build" --restart api
oxidepm --dry-run deploy user@myserver --cwd /srv/myapp --branch main
oxidepm diff user@myserver --cwd /srv/myapp --count 10
```

`deploy` pulls from `origin` on the remote branch, or the branch selected by `--branch`. It runs the optional `--post` command and restarts processes using the remote `oxidepm` executable, which `--remote-bin` can override. A restart failure returns exit status 3. `diff` shows recent commits, working-tree status and a diff summary. Both use noninteractive SSH and require a known-hosts entry. Both support `--dry-run`.

## File watching

Import and enable the `watch` service on Linux. Add this table to each app you want to restart when its files change:

```toml
[apps.adapters.watch]
paths = ["src"]
ignore = ["generated/*"]
debounce_ms = 200
```

Paths are relative to the app's working directory. If `paths` is omitted, the adapter watches that directory. Your ignore patterns extend the defaults, which include `.git`, `node_modules` and `target`.

## web

Build and import the `ui-web` adapter before using these commands.

```sh
oxidepm web              # where it listens, and its access key (shown once)
oxidepm web new-key      # replace the key
```

The adapter serves a REST API and a WebSocket on `127.0.0.1:9615`. API endpoints other than `/api/health` require the `X-API-Key` header, even on loopback. The first start makes a random key in the adapter's `config.toml`. A browser WebSocket can send it through the `oxidepm-key.<key>` subprotocol alongside `oxidepm.v1`. The adapter validates `Host`. For writes and WebSocket upgrades, `Origin` must be absent or match the configured origin.

With the default `lifecycle` grant, it shows every app and can restart or stop the ones that list `ui-web` under `adapters`. The daemon applies its policy to each request from `adapter:ui-web` and records it in the audit log. Use a TLS reverse proxy when exposing the service outside a trusted network.

| Endpoint | Method | Key | Description |
|---|---|---|---|
| `/api/health` | GET | No | `{"ok":true}`. |
| `/api/processes` | GET | Yes | All apps. |
| `/api/processes/:selector` | GET | Yes | One app. |
| `/api/processes/:selector/stop` | POST | Yes | Stop. |
| `/api/processes/:selector/restart` | POST | Yes | Restart. |
| `/api/processes/:selector/logs` | GET | Yes | Logs. |
| `/api/ping` | GET | Yes | Ask the daemon whether it is alive. |
| `/api/save`, `/api/resurrect` | POST | Yes | Save or start the saved apps. Requires `admin`. |
| `/ws` | WebSocket | Yes | The daemon's lifecycle events as they happen. |

`POST /api/processes` (start an app) and `DELETE` require the `admin` level and return 403 under the default grant. Use the [Prometheus exporter](/docs/adapters/exporter-prometheus/) for `/metrics`.

## monit and top

`oxidepm monit` is the terminal dashboard from the `ui-tui` adapter. It shows app state, CPU and memory, details and logs. It asks for `y` or `n` before stopping or restarting an app. The session needs a terminal for input and output and takes no arguments.

```sh
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
