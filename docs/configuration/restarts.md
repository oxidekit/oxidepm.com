# Restarts and states

Restart policy, backoff, the crash-loop breaker and the states an app moves through.

Source: https://oxidepm.com/docs/configuration/restarts/

## States

`oxidepm status` shows one of these for each app. In `--json` output `online` is called `running`.

| Status | Meaning |
|---|---|
| `waiting` | A start was accepted and waits for `depends_on` or a startup delay. |
| `building` | Building from source. |
| `starting` | Spawned, and with a health check, until the first probe has passed. |
| `online` | Running. |
| `unhealthy` | Alive, but the health check failed `retries` times in a row. |
| `backoff` | Crashed. An automatic restart is scheduled. |
| `stopping` | Shutting down. |
| `stopped` | Stopped by a person. It stays stopped. |
| `errored` | A crash loop, a launch that failed, an exit that is not restarted, or a failed dependency. |

A `stop` acts on every state except `stopped` and `errored`: it also cancels a pending start, a build and a pending restart. A `start` of an app that is not at rest (anything but `stopped` and `errored`, `backoff` and `waiting` included) is refused with `E_APP_EXISTS` and changes nothing.

## The restart policy

A crashed app waits in `backoff` and is restarted automatically unless `--no-autorestart` or the config key `restart` says otherwise. `restart` is one of:

- `on-crash` (the default): a non-zero exit or a death by a signal is restarted. An exit with code 0 is not, and leaves the app `errored`.
- `always`: any exit is restarted.
- `never`: nothing is restarted.

A restart caused by a memory or uptime limit, by a health check with `action = "restart"`, or by a launch that failed during a restart ignores both settings. A manual `stop` is never restarted automatically.

## Backoff and the crash-loop breaker

The delay before the first restart is `restart_delay` (500 ms by default) and doubles for every crash in a row, up to `max_restart_delay` (60 000 ms). A run of `stable_uptime` seconds (60 by default) starts the delay over.

More than `max_restarts` restarts (15 by default) inside any `crash_window` seconds (600 by default) are a crash loop. The app ends `errored` and stays `errored` until a person starts it. `start` and `restart` by hand give the app a fresh budget.

A launch that fails during an automatic restart (the program is gone, a log file cannot be opened) is one more attempt with a longer delay, not the end.

*Terminal output: an app in a crash loop, then its logs*

```text
$ oxidepm status
╭────┬────────┬──────┬─────┬───┬─────────┬──────┬─────┬────────╮
│ id │ name   │ mode │ pid │ ↺ │ status  │ cpu  │ mem │ uptime │
├────┼────────┼──────┼─────┼───┼─────────┼──────┼─────┼────────┤
│  1 │ mailer │ cmd  │ -   │ 3 │ errored │ 0.0% │ 0B  │ 0s     │
╰────┴────────┴──────┴─────┴───┴─────────┴──────┴─────┴────────╯
$ oxidepm logs mailer --lines 3
[2026-11-25 21:35:25.123] cannot reach smtp
[2026-11-25 21:35:25.527] cannot reach smtp
[2026-11-25 21:35:26.330] cannot reach smtp
```

Here the app was started with `max_restarts = 3` and `restart_delay = 200`. The `↺` column counts restarts. Read the logs before you restart an errored app: the cause is usually there.

## Reload is a restart

`oxidepm reload` is the same as `restart`: the process is stopped and started again. There is no zero-downtime reload.
