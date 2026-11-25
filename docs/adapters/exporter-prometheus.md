# The Prometheus exporter

Prometheus metrics from the daemon's status, served by an adapter.

Source: https://oxidepm.com/docs/adapters/exporter-prometheus/

The exporter is a service adapter with read access only. On each scrape it asks the daemon for the status of the apps, at most once a second however many scrapers there are, and never touches them.

## Install it

On Linux, [build the exporter archive](https://oxidepm.com/docs/adapters/import-and-enable/#build-an-optional-adapter) and use its filename and digest from `SHA256SUMS`.

```sh
oxidepm adapter import ./exporter-prometheus-0.4.0-rc.1.tar.gz --sha256 <digest> --enable
```

The manifest asks for read access to status, to listen on `127.0.0.1:9616`, to read its own state directory, and for outbound network without naming any host; the consent screen marks that last one `[BROAD]`. It serves the Prometheus text format on `/metrics`, and nothing else.

*prometheus.yml*

```yaml
scrape_configs:
  - job_name: oxidepm
    static_configs:
      - targets: ["127.0.0.1:9616"]
```

## What it exports

*Metrics served by the exporter*

```text
$ curl -s 127.0.0.1:9616/metrics
# HELP oxidepm_up Whether the exporter could read the process list from the daemon (1) or not (0)
# TYPE oxidepm_up gauge
oxidepm_up 1
# HELP oxidepm_processes_total Total number of managed processes
# TYPE oxidepm_processes_total gauge
oxidepm_processes_total 4
# HELP oxidepm_process_up Whether the process is running (1) or not (0)
# TYPE oxidepm_process_up gauge
oxidepm_process_up{name="db",id="1",mode="cmd"} 1
oxidepm_process_up{name="worker",id="4",mode="cmd"} 0
# HELP oxidepm_process_restarts_total Total number of process restarts
# TYPE oxidepm_process_restarts_total counter
oxidepm_process_restarts_total{name="worker",id="4",mode="cmd"} 3
```

That is a part of the real output. The other families are `oxidepm_process_uptime_seconds`, `oxidepm_process_memory_bytes` and `oxidepm_process_cpu_percent`, each per app with the labels `name`, `id` and `mode`. Label values are escaped.

If the daemon cannot be asked (it is stopped, busy, or refused the request), the answer is HTTP 503 with only `oxidepm_up 0`, never an empty list that looks healthy.

## Configuration

An optional `config.toml` in the adapter's state directory, read when the adapter starts. Disable and enable it again after a change.

*config.toml*

```toml
listen = "127.0.0.1:9616"       # an IP address and a port; the default
key = "at least 16 characters"  # required for any address that is not loopback
```

- An address that is not loopback (`0.0.0.0` included) without a `key` is refused: the adapter listens nowhere, and `adapter info` shows why.
- With a key, every request needs `Authorization: Bearer <key>`, and so does a loopback bind that has a key.
- Without a key (loopback only), the `Host` header must be `localhost` or a loopback address with the port that is bound, so a web page whose name was re-pointed at `127.0.0.1` cannot read the metrics.
- There is no TLS. Put a proxy in front of it for anything but a trusted network.
- The sandbox lets the adapter bind the ports its manifest lists, which is 9616 as shipped. Another port needs a build whose manifest lists it, and a new consent at `enable`.
