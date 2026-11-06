# Limits and cron

Restart an app over a memory or uptime limit, or on a cron schedule.

Source: https://oxidepm.com/docs/configuration/limits-and-cron/

## Memory and uptime limits

```sh
oxidepm start ./app --max-memory 512 --max-uptime 24h
```

In a config file the keys are `max_memory_mb` and `max_uptime_secs`. An app over a limit is replaced: the daemon stops its process group, waits the restart delay and starts it again with the same plan.

- A limit restart ignores the `restart` setting and `no_autorestart`.
- A run of 5 seconds or more never counts towards `max_restarts`, so a periodic restart (`--max-uptime 24h`) cannot end in a crash loop. A limit that fires within 5 seconds of every start is counted like a crash, and the breaker ends it.
- A `stop` or `restart` by hand always wins over a limit restart that is still on its way.
- Memory is sampled every 2 seconds from the resident size of the app's first process, the one the daemon started. With `npm start` that is `npm`, not the `node` child under it, so give a wrapped app the limit of the wrapper, or start the program directly.
- Uptime counts from the launch.

`--max-uptime` takes a duration such as `30m`, `1h`, `24h`, `1d` or `1h30m`; a plain number is seconds.

## Cron restarts

*oxidepm.config.toml*

```toml
[[apps]]
name = "worker"
mode = "cmd"
script = "./worker"
restart_cron = "0 4 * * *"    # every day at 04:00 UTC
```

The expression has the usual five fields, in UTC, and Sunday is 0 or 7. A bad expression is an error when the file is loaded. A scheduled restart ignores the `restart` setting, like a limit restart, and is recorded as the daemon's own work (`system:cron`) in the audit log.
