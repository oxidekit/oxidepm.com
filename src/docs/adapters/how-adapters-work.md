## What an adapter is

An adapter is a separate executable that `oxidepmd` starts and supervises. It talks to the daemon over its standard input and output, one JSON-RPC message per line. The protocol is documented, so an adapter can be written in any language. The daemon itself does not fetch anything: importing is done by the CLI.

There are two kinds, named by the `kind` field of the manifest:

- **service**: resident. It starts when you enable it, receives events about the apps, and the supervisor restarts it if it dies. The notifier, the Prometheus exporter and the web API (`ui-web`) are services.
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

Built and tested: the [notifier](/docs/adapters/notifier/), the [Prometheus exporter](/docs/adapters/exporter-prometheus/), `ui-web` (the web API and WebSocket), `ui-tui` (the terminal dashboard) and the four runtime adapters, `runtime-node`, `runtime-python`, `runtime-go` and `runtime-rust`. The runtime adapters are carried, signed, by each release. The other built adapters have no published archive yet.

Planned and not built: adapters for project checks and `init` (`check`, `init`), `start --git` (`git-start`), `deploy` and `diff` (`deploy`), file watching (`watch-rebuild`) and, later, adapters for AI agents. The core reserves the names of the official adapters, so only a signed adapter can use one. See the [list](/adapters/).

## Where they come from

An adapter is imported from an archive. You can pin an archive by its SHA-256 (a file or an https URL), take one from the bundle a release carries (`oxidepm adapter import --bundled`), or take one from a signed index. The signing code is in the CLI and the daemon, but there is no index address configured in a build yet, so there is no index to search. See [Import and enable](/docs/adapters/import-and-enable/).
