## Declare a dependency

List the names of the apps this one needs. Here `api` needs the database, and `web` needs `api`.

```toml title="oxidepm.config.toml"
[[apps]]
name = "db"
mode = "cmd"
script = "postgres"
args = ["-D", "/srv/pg/data"]

[[apps]]
name = "api"
mode = "cmd"
script = "./target/release/api"
depends_on = ["db"]

[apps.health_check]
http_url = "http://127.0.0.1:8080/health"

[[apps]]
name = "web"
mode = "npm"
script = "start"
depends_on = ["api"]
```

## What happens at start

The checks run when the app is started:

- A name that is not registered is refused at once (`E_DEPENDENCY_MISSING`), and so is a cycle (`E_DEPENDENCY_CYCLE`, and the message names it).
- A single `start` of an app whose dependency is `stopped` or `errored` right now is refused with the remedy (`E_DEPENDENCY_FAILED`).
- Otherwise the start is accepted and the app shows `waiting` until every dependency is `online`. The start returns at once and nothing else is blocked. A `stop` cancels the wait.

```term cap="start-config" label="Terminal output of oxidepm start: api and web wait for their dependencies"
```

If a dependency has a health check, it is `online` only once its first probe has passed. Until then it is `starting`, and the apps that wait for it keep waiting.

```term label="Terminal output of refused starts"
{hi:$} oxidepm start api-only.toml
{ox:✗} Failed to start api: dependency 'db' is stopped; start it first

Started: 0, Failed: 1
{ox:Error:} 1 of 1 apps failed to start (started: none; failed: api)

{hi:$} oxidepm start cycle.toml
{ox:Error:} Config error: depends_on cycle: a -> b -> a
```

## The wait fails closed

A dependency that ends `errored`, or is deleted, fails the dependent at once. So does `depends_timeout` (1 to 3600 seconds, 60 by default): the app ends `errored` with the reason `dependency 'db' not running after 60s` (`E_DEPENDENCY_TIMEOUT`) and is never launched. It does not start anyway and fail in a confusing way.

`depends_fail_open = true` turns that timeout into a warning and a launch. It is discouraged.

Once an app is running, a later failure of its dependency does not touch it.

## When the wait applies

The wait applies to a start or restart by hand of an app that was at rest. A `restart` of an app that is up, and every automatic restart (crash, limit, cron, health), skip it: a crashed app comes back through the normal backoff even while its dependency is down.

An app that waits holds no build slot. At most `launch_concurrency` apps (4 by default, a [daemon setting](/docs/configuration/daemon-settings/)) build and spawn at once.

## Stop order

`stop all`, and a stop by tag, stops dependents before their dependencies, layer by layer. The daemon's shutdown does the same within its time budget. A `stop` of one app stops that app only: its dependents keep running.

```term cap="stop-all-dry" label="Terminal output of oxidepm stop all --dry-run"
```

`--dry-run` shows the order without stopping anything. `restart db --dry-run` on a running app says the dependency gate is skipped because the app is up.

## Fields

::: fields
depends_on | list of app names | default: none
: Apps that must be running before this one starts. A name must be in the same file or already registered.
depends_timeout | seconds | default: 60
: How long to wait for them, from 1 to 3600, before the app ends `errored`.
depends_fail_open | boolean | default: false
: Launch anyway, with a warning, when the wait times out.
:::
