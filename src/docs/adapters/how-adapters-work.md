## What an adapter is

An adapter is a separate executable that `oxidepmd` starts and supervises. It talks to the daemon over its standard input and output, one JSON-RPC message per line. The protocol is documented, so an adapter can be written in any language. The daemon itself does not fetch anything: importing is done by the CLI.

There are two kinds, named by the `kind` field of the manifest:

- **service**: resident. It starts when you enable it, receives events about the apps, and the supervisor restarts it if it dies. The notifier and the Prometheus exporter are services.
- **tool**: started on demand to answer a request, kept warm for 30 seconds, then asked to exit. Runtimes and commands that run once are tools.

## What an adapter can add

An adapter can listen to lifecycle events, ask the daemon to do things within a grant, add a command to the CLI (the notifier adds `oxidepm notify`), and provide a runtime for apps. Whatever it provides is named in its manifest, and is shown before you enable it.

An adapter never starts, stops or changes an app on its own authority. When it asks the daemon, the request goes through the same policy, audit log and rate limits as a person's or an agent's, as the adapter and under the grant you accepted. A request an adapter makes is written to the audit log with its name.

## When one fails

- A crash, a hang, a flood of output or a broken protocol gets the adapter killed and restarted with a growing delay. Three protocol violations in 60 seconds count as a crash.
- Events for a service that is down or slow are dropped and counted, never queued without limit.
- A request to an adapter that is missing, failed or not ready fails with a named error (`E_ADAPTER_MISSING`, `E_ADAPTER_UNAVAILABLE`, `E_ADAPTER_TIMEOUT`, `E_ADAPTER_CRASHED`). There is no silent fallback.
- The daemon never stops, restarts, signals or changes an app because an adapter failed.

## Which adapters exist

Two are built and tested today: the [notifier](/docs/adapters/notifier/) and the [Prometheus exporter](/docs/adapters/exporter-prometheus/). The core reserves the names of adapters that are planned to take over the web API, the dashboard, the language runtimes, project checks, deploys and file watching. See the [list](/adapters/).

## Where they come from

An adapter is imported from an archive. You can pin an archive by its SHA-256 (a file or an https URL), take one from the bundle a release carries, or take one from a signed index. The signing code is in the CLI and the daemon, but this build has no index address and no official signing key embedded, so there is no index to search yet. See [Import and enable](/docs/adapters/import-and-enable/).
