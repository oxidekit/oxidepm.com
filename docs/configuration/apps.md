# Apps

Every key an app can have in a config file.

Source: https://oxidepm.com/docs/configuration/apps/

Every key an app can have in a config file. Times are in the unit the key names: `_ms` and the restart and kill delays are milliseconds, `_secs`, `stable_uptime` and `crash_window` are seconds.

## What to run

- `name` (string): The app's name. Required. A name is also what a selector matches, so it is limited in charset and length (a cluster name to 59 characters).
- `mode` (string, alias: runtime): How to run it: `cmd` (any program, the only runtime in the core), or a runtime an enabled adapter provides: `node`, `npm`, `pnpm`, `yarn` (`runtime-node`), `python` (`runtime-python`), `go` (`runtime-go`), `rust` and `cargo` (`runtime-rust`). An app whose runtime adapter is missing is refused with `E_ADAPTER_MISSING` and the command that imports it. If you leave it out, a `script` gets its mode from its extension, and the file is refused if that is not possible.
- `script` (string): What to run. For `cmd` it is the program; for `npm`, `pnpm` and `yarn` the name of the package script; for `node` and `python` the file.
- `bin` (string): The binary name, for `cargo`.
- `binary` (string): The path to a binary, as an alternative to `script` or `bin`.
- `args` (list of strings, default: none): Arguments passed to the program.
- `cwd` (string): The working directory.

## Environment and tags

- `env` (table, default: empty): Environment variables for the app, for example `env = { RUST_LOG = "info" }`.
- `env_file` (string): A file of `KEY=VALUE` lines. A missing file is an error.
- `tags` (list of strings, default: none): Group apps, and select them with `@tag`.

## Restarts

- `restart` (string, default: "on-crash"): `on-crash`, `always` or `never`. See [Restarts and states](/docs/configuration/restarts/).
- `no_autorestart` (boolean, default: false): Turn automatic restarts off.
- `restart_delay` (number, default: 500): Milliseconds before the first restart. It doubles for every crash in a row.
- `max_restart_delay` (number, default: 60000): The cap on that delay, in milliseconds.
- `max_restarts` (number, default: 15): More than this many restarts inside `crash_window` end the app `errored`.
- `crash_window` (number, default: 600): Seconds. See `max_restarts`.
- `stable_uptime` (number, default: 60): A run this long, in seconds, starts the delay over.
- `kill_timeout` (number, default: 3000): Milliseconds the app has to exit after the stop signal.

## Dependencies, limits and schedules

- `depends_on` (list of app names, default: none): Apps that must be running before this one starts. See [Dependencies](/docs/configuration/dependencies/).
- `depends_timeout` (seconds, default: 60): How long to wait for them, from 1 to 3600.
- `depends_fail_open` (boolean, default: false): Launch anyway, with a warning, when the wait times out. Discouraged.
- `max_memory_mb` (number): Restart the app when it is over this resident size. See [Limits and cron](/docs/configuration/limits-and-cron/).
- `max_uptime_secs` (number): Restart the app after this many seconds of uptime.
- `restart_cron` (string): A cron expression for scheduled restarts. Five fields, UTC; Sunday is 0 or 7.

## Clusters

- `instances` (number, default: 1): How many instances, up to 256. See [Clusters](/docs/configuration/clusters/).
- `port` (number): The base port. Instance `i` gets `port + i`.
- `port_range` (table): `{ start = 3000, end = 3010 }`. The range must hold every instance. `port` and `port_range` together are refused.

## Checks, hooks and logs

- `health_check` (table): Exactly one of `http_url`, `tcp` or `script`, plus optional settings. See [Health checks](/docs/configuration/health-checks/).
- `hooks` (table): `on_start`, `on_stop`, `on_restart`, `on_crash`, `on_error`. See [Environment and hooks](/docs/configuration/environment-and-hooks/).
- `log_max_size` (string, default: "10mb"): Rotate a log file at this size, for example `"50mb"`.
- `log_max_files` (number, default: 5): How many rotated files to keep.
- `log_compress` (boolean, default: false): Compress rotated files with gzip.

## Safety markers

- `protected` (boolean, default: false): Read-only for AI actors and other non-human callers. See [Protected apps](/docs/ai-safety/protected-apps/).
- `ai_control` (boolean, default: false): AI actors may stop, restart and reload the app. They can never start or delete it.

## Accepted, with no effect

- `watch` (boolean, default: false): `true` is an error: file watching is not available yet. `false` is accepted.
- `ignore` (list of strings): Ignore patterns for watching. They have no effect while watching is refused.
- `adapters` (table): Reserved. It must be empty.
