## start

```sh
oxidepm start app.js
oxidepm start ./my-project --max-memory 512
oxidepm start oxidepm.config.toml
oxidepm start ./server -i 4 --port 3000
```

`start` takes a file, a directory, or a config file. The daemon is started if it is not running. A config file starts every app in it, and each app gets its own result.

| Option | Meaning |
|---|---|
| `-n, --name <name>` | The app's name. |
| `--mode <runtime>` | Force the runtime (alias `--runtime`): `cmd`, `node`, `npm`, `pnpm`, `yarn`, `cargo`, `rust`, `python`, `go`, or one an adapter provides. |
| `--script <name>` | The package script, for `npm`, `pnpm` and `yarn`. |
| `--bin <name>` | The binary, for `cargo`. |
| `--cwd <dir>` | The working directory. |
| `--env KEY=VALUE` | An environment variable. Repeatable. |
| `--env-file <file>` | An environment file. |
| `--env-inherit` | Give the app the daemon's whole environment. |
| `--tag <tag>` | A tag for grouping. Repeatable. |
| `-i, --instances <n>` | Cluster mode, from 1 to 256. |
| `--port <n>` | The base port. Instance `i` gets `port + i`. |
| `--delay <ms>` | Wait before starting the process. |
| `--restart-delay <ms>` | Delay before the first restart. |
| `--max-restarts <n>` | Restarts before the app ends `errored`. |
| `--kill-timeout <ms>` | Time to exit after the stop signal. |
| `--no-autorestart` | Turn automatic restarts off. |
| `--max-memory <MB>`, `--max-uptime <duration>` | Limits. See [Limits and cron](/docs/configuration/limits-and-cron/). |
| `--health-check <url or script>` | An http(s) URL or a script. |
| `--on-start`, `--on-stop`, `--on-restart`, `--on-crash` | Event hooks. |
| `--protected`, `--ai-control` | The policy markers. |
| `--git <url>`, `--branch`, `--clone-dir` | Clone a repository and start it. |
| `--setup` | Install dependencies and create `.env` from a template first. |
| `--no-check` | Skip preflight checks. Not recommended. |
| `-- <args>` | Arguments passed to the program. |

`--watch` is refused with an error: file watching is not available yet.

## stop, restart, reload, delete

```sh
oxidepm stop api
oxidepm restart api
oxidepm reload api
oxidepm delete api
```

- `stop` stops the app. It stays stopped and is not restarted automatically. With several apps (`all`, a tag), dependents are stopped before their dependencies.
- `restart` stops and starts the app again. It also starts an app that is at rest.
- `reload` is the same as `restart`.
- `delete` stops the app and removes it from the registry and the database.

```term label="Terminal output of oxidepm restart"
{hi:$} oxidepm restart web
{hi:✓} Restarted 1 process(es)
```

A `start` of an app that is not at rest is refused with `E_APP_EXISTS` and changes nothing. These commands take [`--dry-run`](/docs/commands/dry-run/), except `start --git` and `start --setup`, which refuse it.
