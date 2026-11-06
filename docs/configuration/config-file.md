# The config file

Where an app's settings live, which formats are read and how strictly.

Source: https://oxidepm.com/docs/configuration/config-file/

## Writing one

A config file lists apps. It is a TOML file by default; YAML and JSON are read too, chosen by the file extension (`.toml`, `.yaml`, `.yml`, `.json`). The documented names are `oxidepm.config.toml` and `ecosystem.config.toml`, but any file name with a known extension works.

*oxidepm.config.toml*

```toml
[[apps]]
name = "api"
mode = "cargo"
cwd = "./api"
env = { RUST_LOG = "info" }
tags = ["backend"]

[[apps]]
name = "web"
mode = "npm"
script = "start"
cwd = "./web"
env_file = ".env"
instances = 2
port = 3000

[[apps]]
name = "worker"
mode = "node"
script = "worker.js"
max_restarts = 5
restart_delay = 2000
depends_on = ["api"]              # wait for the api to be running first
restart_cron = "0 4 * * *"        # restart daily at 4am UTC

log_max_size = "50mb"
log_max_files = 10
log_compress = true
```

The `cargo`, `npm` and `node` modes in this example are provided by the `runtime-rust` and `runtime-node` adapters that a release carries. With `mode = "cmd"` the app needs no adapter. See [Runtimes](https://oxidepm.com/docs/getting-started/install/#runtimes).

Start everything in it with:

```sh
oxidepm start oxidepm.config.toml
```

The file is sent to the daemon as one batch, so an app may be listed before the apps it depends on. Each app gets its own result: an app that cannot start does not stop the others, but the apps that depend on it are refused too.

## Checked strictly

A config file is checked when it is loaded, and nothing is started if it fails. A file that does not parse is reported with its name and the line of the problem; the other errors name the app, the key or the file they are about. These are all errors:

- an unknown key (a typo such as `restart_mode`, which is spelled `restart`),
- a bad cron expression or log size,
- a health check that is not exactly one of `http_url`, `tcp` or `script`,
- an `env_file` that does not exist,
- a `script` whose runtime cannot be inferred from its extension (set `mode`),
- `watch = true`, because file watching is not available yet,
- a dependency on an app that is not in the file or the registry, or a dependency cycle.

*Terminal output of oxidepm start with a config file that has an unknown key*

```text
$ oxidepm start bad.toml
Error: Config error: bad.toml: TOML parse error at line 5, column 1
  |
5 | restart_mode = "always"
  | ^^^^^^^^^^^^
unknown field `restart_mode`, expected one of `name`, `mode`, `runtime`, `script`, `bin`, `cwd`, `args`, `env`, `env_file`, `watch`, `ignore`, `restart_delay`, `max_restarts`, `max_restart_delay`, `stable_uptime`, `crash_window`, `kill_timeout`, `no_autorestart`, `instances`, `port`, `port_range`, `health_check`, `max_memory_mb`, `hooks`, `tags`, `max_uptime_secs`, `restart`, `binary`, `depends_on`, `depends_timeout`, `depends_fail_open`, `restart_cron`, `log_max_size`, `log_max_files`, `log_compress`, `adapters`, `protected`, `ai_control`
```

## The daemon keeps its own copy

A config file is read only by `oxidepm start <file>`. The daemon keeps the spec an app was started with: `restart` and `reload` reuse it, and `start` of an app that is already up is refused with `E_APP_EXISTS`. To apply a changed file, stop the app and start the file again. An app that is at rest takes the new spec.

A config file has no key for the startup delay or for `env_inherit`. Those are `--delay` and `--env-inherit` of a single `start`.

## Reserved tables

The top-level tables `adapters` and `policy` are reserved and must be empty, and so is a per-app `adapters` table (`[apps.adapters]`). A file that fills one is refused.

The keys of an app are on the next page.
