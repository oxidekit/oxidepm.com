# Health checks

HTTP, TCP and script checks, and what the daemon does when one fails.

Source: https://oxidepm.com/docs/configuration/health-checks/

## Add a check

```sh
oxidepm start ./server --health-check http://localhost:3000/health   # HTTP
oxidepm start ./server --health-check ./check-health.sh              # a script
```

In a config file a check is a table with exactly one of `http_url`, `tcp` or `script`:

*oxidepm.config.toml*

```toml
[[apps]]
name = "api"
mode = "cmd"
script = "./target/release/api"

[apps.health_check]
http_url = "http://127.0.0.1:8080/health"
expected_status = [200, 204]
interval_secs = 30
retries = 3
action = "restart"
```

## How a check runs

An app with a check is `starting` until its first probe has passed. The first probe runs `start_period_secs` after the launch, then one runs every `interval_secs`. A probe times out after `timeout_secs`.

- An HTTP check passes on status 200 unless `expected_status` lists others. It does not follow redirects: a 301 is a failure unless it is listed.
- A `tcp` check (`"host:port"`) passes when the connection is accepted.
- A `script` check runs in the app's directory, as `sh -c`, with the same limited environment as a hook.

After `retries` failures in a row the app is `unhealthy`, the `on_error` hook fires once for that streak, and the `health_check` notification is sent if the notifier adapter is enabled. It goes back to `online` when a probe passes again.

The child is left alone unless the check sets `action = "restart"`, which replaces it with an automatic restart.

## Fields

- `http_url` (string): The URL to request. Exactly one of `http_url`, `tcp` and `script` is required.
- `tcp` (string): `"host:port"`.
- `script` (string): A script or command.
- `expected_status` (list of numbers, default: [200]): The HTTP status codes that count as healthy.
- `interval_secs` (number, default: 30): Seconds between probes.
- `timeout_secs` (number, default: 5): Seconds before a probe fails. 5, or the interval if that is shorter.
- `retries` (number, default: 3): Failures in a row before the app is `unhealthy`.
- `start_period_secs` (number, default: 5): Seconds after the launch before the first probe.
- `action` (string, default: "notify"): `notify` leaves the child alone. `restart` replaces it.
