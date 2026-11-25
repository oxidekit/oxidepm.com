# Write an adapter

The manifest file, the archive layout and a minimal adapter.

Source: https://oxidepm.com/docs/adapter-protocol/write-an-adapter/

## The archive

An adapter is a gzip tarball with two files at its top level: `manifest.json`, and the executable that the manifest names in `exec`. `exec` must be a relative path, with no `.` or `..` components. The executable must be a native program for the machine it runs on.

```text
notifier.tar.gz
├── manifest.json
└── oxidepm-notifier
```

## The manifest

`manifest.json` declares who the adapter is and what it asks for. It is validated at import and again at every load in the daemon. This is the whole manifest of the Prometheus exporter:

*manifest.json*

```json
{
  "schema": 1,
  "name": "exporter-prometheus",
  "version": "0.4.0-rc.4",
  "kind": "service",
  "summary": "Prometheus metrics for the apps OxidePM manages.",
  "description": "Serves /metrics in the Prometheus text format on 127.0.0.1:9616. On each scrape it asks the daemon for the status of the apps (read access only) and never touches them. It listens on loopback unless its config.toml says otherwise, and any other address needs an access key in that file. If the daemon cannot be reached the answer is HTTP 503 and oxidepm_up 0.",
  "tags": ["exporter"],
  "protocol": [1],
  "min_daemon": "0.1.0",
  "exec": "oxidepm-exporter-prometheus",
  "provides": {},
  "permissions": {
    "host": {"level": "read", "scope": "all"},
    "events": [],
    "env_pass": [],
    "network": {"mode": "outbound", "hosts": [], "listen": ["127.0.0.1:9616"]},
    "fs": {"read": ["$STATE"], "write": []},
    "spawn": {"mode": "none"},
    "memory_mb": 64,
    "requires_enforcement": []
  }
}
```

- `schema` (number): Always `1`.
- `name` (string): 2 to 32 characters. Start with a lowercase letter and use lowercase letters, digits and hyphens. Names such as `core`, `oxidepm`, `oxidepmd`, `all`, `adapter`, `daemon`, `cmd`, `system` and `host` are reserved. See [Import and enable](/docs/adapters/import-and-enable/) for the rules on official adapter names.
- `version` (string): A semantic version.
- `kind` (string): `service` or `tool`.
- `summary` (string): One line, at most 120 characters. Required.
- `description` (string, default: empty): At most 4096 characters. It is shown on the consent screen, followed by the permissions again so it cannot push them out of sight.
- `tags` (list, default: none): At most 10, for listing and search.
- `protocol` (list of numbers): The protocol versions the adapter speaks. At least one must be one the daemon speaks.
- `min_daemon` (string): The oldest daemon version it works with.
- `exec` (string): The executable, relative to the archive.
- `provides` (object, default: empty): `runtimes`, `verbs`, `serves`, `programs`, `capture_programs` and `env_set`.
- `permissions` (object): What it asks for. See [Permissions](/docs/adapters/permissions/).

## Verbs and runtimes

`provides.verbs` adds commands to the CLI. Each has a `name` (2 to 24 characters), a `summary`, a `tier` (`safe`, `caution` or `dangerous`), a `mode` (`relayed` or `session`), whether it `writes`, whether it supports `dry_run`, `max_runtime_secs` (1 to 3600, 600 by default) and an `args_summary`. A verb must not collide with a built-in command or another adapter's verb. A verb that writes cannot be `safe`, and an adapter that may spawn programs or use the network cannot declare a `safe` verb.

`provides.runtimes` names runtimes the adapter provides (a tool only, and never `cmd`), and then must list `provides.programs`, the bare program names it runs.

A `service` may list events, and provides no runtimes. A `tool` receives no events.

## What you write

The program reads one JSON object per line on standard input, and writes protocol on standard output and logs on standard error. It waits for `initialize`, answers it, handles `ping`, and exits on `shutdown` or when standard input closes. A service then handles `event` notifications, and may call `host.request` within its grant. The frames on these pages are the reference.

The [adapter sources](https://github.com/oxidekit/oxidepm-adapters) include `oxidepm-adapter-sdk`, a Rust crate that handles the handshake, `ping`, events, relayed verbs and `shutdown`.

## Try it

```sh
oxidepm adapter import ./my-adapter.tar.gz --sha256 <hex>
oxidepm adapter enable my-adapter
oxidepm adapter info my-adapter
```

`--allow-reserved-name` is only needed for a reserved name. `adapter info` shows the last lines the adapter wrote to standard error, its crashes and its protocol strikes.
