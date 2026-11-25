# How adapters work

What an adapter is, what runs where, and what happens when one fails.

Source: https://oxidepm.com/docs/adapters/how-adapters-work/

## What an adapter is

An adapter is a separate executable that `oxidepmd` starts and supervises. It talks to the daemon over its standard input and output, one JSON-RPC message per line. The protocol is documented, so an adapter can be written in any language. The daemon itself does not fetch anything: importing is done by the CLI.

There are two kinds, named by the `kind` field of the manifest:

- **service**: resident. It starts when you enable it and the supervisor restarts it if it dies. It can subscribe to app events. The notifier, Prometheus exporter, web API (`ui-web`) and `watch` are services.
- **tool**: started on demand to answer a request, kept warm for 30 seconds, then asked to exit. The runtime adapters, the terminal dashboard (`ui-tui`) and commands that run once are tools.

## What an adapter can add

An adapter can listen to lifecycle events, ask the daemon to do things within a grant, add a command to the CLI (the notifier adds `oxidepm notify`, `ui-web` adds `oxidepm web`, `ui-tui` adds `oxidepm monit`), and provide a runtime for apps (`runtime-node`, `runtime-python`, `runtime-go` and `runtime-rust`). The core itself runs only the `cmd` runtime. Whatever it provides is named in its manifest, and is shown before you enable it.

An adapter never starts, stops or changes an app on its own authority. When it asks the daemon, the request goes through the same policy, audit log and rate limits as a person's or an agent's, as the adapter and under the grant you accepted. A request an adapter makes is written to the audit log with its name.

## When one fails

- A crash, a hang, a flood of output or a broken protocol gets the adapter killed and restarted with a growing delay. Three protocol violations in 60 seconds count as a crash.
- Events for a service that is down or slow are dropped and counted, never queued without limit.
- A request to an adapter that is missing, failed or not ready fails with a named error (`E_ADAPTER_MISSING`, `E_ADAPTER_UNAVAILABLE`, `E_ADAPTER_TIMEOUT`, `E_ADAPTER_CRASHED`). There is no silent fallback.
- The daemon never stops, restarts, signals or changes an app because an adapter failed.

## Which adapters exist

The release bundles `runtime-node`, `runtime-python`, `runtime-go` and `runtime-rust`. On Linux, build an archive for any of the optional adapters: `check`, `init`, `git-start`, `deploy`, `watch`, `ui-web`, `ui-tui`, [notifier](https://oxidepm.com/docs/adapters/notifier/) and [exporter-prometheus](https://oxidepm.com/docs/adapters/exporter-prometheus/). See the [adapter list](https://oxidepm.com/adapters/) for what each one provides and the permissions it asks for. AI adapters are unavailable in this release.

## Where they come from

Import an archive by SHA-256 from a file or HTTPS URL, from the release bundle with `oxidepm adapter import --bundled`, or by name with `oxidepm adapter import <name>` when a signed index is configured. This release ships without a configured network catalog. See [Import and enable](https://oxidepm.com/docs/adapters/import-and-enable/).
