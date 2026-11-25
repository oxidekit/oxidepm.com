On Linux, `adapter import` verifies and installs an adapter. With `--enable`, it also asks you to approve the grant. Services start when enabled, and tools start when called.

## List

```term cap="adapter-list" label="Terminal output of oxidepm adapter list and list --available"
```

`list` shows the installed adapters. `list --available` and `search` require a configured signed index. This release ships without a network catalog.

## Import from the release

The release ships all 13 adapters under `share/oxidepm/adapters`. On Linux, run `oxidepm adapter import --bundled <name> --enable` for any adapter you want to use. This command adds file watching.

```sh
oxidepm adapter import --bundled watch --enable
```

Bundled imports work offline. The CLI and daemon verify the catalog and selected archives against `SHA256SUMS`. The installer runs `oxidepm adapter import --bundled --tag runtime --enable --yes` to enable only the four runtime adapters. To select groups, use `--tag dev` for `watch`, `check` and `init`, `--tag deploy` for `git-start` and `deploy`, `--tag ui` for `ui-web` and `ui-tui`, `--tag notifier` for `notifier`, or `--tag exporter` for `exporter-prometheus`.

Review the permissions and confirm the grant at the terminal prompt. To review before enabling, omit `--enable`. The adapter stays disabled until you approve the grant.

```term cap="adapter-import" wrap="yes" label="Terminal output of oxidepm adapter import --bundled watch"
```

`Needs` lists the permissions. `Again, what it needs` repeats the list after the description. `[BROAD]` marks permissions such as access to all files the current user can read. `Enforced on this machine` shows what the operating system can enforce. `Trust` identifies the source of the archive.

`oxidepm adapter import <name>` uses a configured signed index. This release ships without a network catalog.

## Enable

```sh
oxidepm adapter enable <name> --accept <fingerprint>
```

For broader grants such as `watch`, run the printed command after reviewing the permissions if approval was deferred or the import ran without an interactive terminal. Get the fingerprint from `adapter import` or `adapter info`. It ties your consent to that adapter release. `--yes` accepts without asking only for pure adapters such as the four runtimes.

On a terminal, `oxidepm adapter enable watch` shows the permissions and asks for consent again.

```term cap="adapter-enable" wrap="yes" label="Terminal output of oxidepm adapter enable watch"
```

If you answer no, nothing is changed:

```term label="Terminal output when the answer is no"
Enable watch with this grant? [y/N] no
{ox:Error:} Not enabled
```

If you answer yes:

```term label="Terminal output when the answer is yes"
Enable watch with this grant? [y/N] yes
{hi:✓} Enabled watch {{release_version}} (level lifecycle, scope opted-in)
  Enforced by the OS on this machine: network, fs_write, fs_read, spawn
```

You can enable with less than the adapter asks for. `--level read` or `--level lifecycle` gives a lower host level, and `--scope opted-in` limits it to the apps that list the adapter. On Linux, `--allow-unenforced` accepts missing sandbox restrictions that the adapter requires. macOS supports the built-in `cmd` runtime. The adapter launcher and sandbox are Linux-only in this release.

## Update bundled adapters

After `oxidepm update`, restart the daemon and run `oxidepm adapter update --all` to refresh the adapters you imported from the release bundle. Use `oxidepm adapter update <name>` to update just one.

```term cap="adapter-update" wrap="yes" label="Excerpt from oxidepm adapter update --all"
```

The update uses the bundle installed with the new release and follows the same verification and consent checks as import. If it needs a broader grant, review the permissions and run `oxidepm adapter update <name> --accept <fingerprint>` with the fingerprint from the preview. See [Upgrade](/docs/getting-started/upgrade/#update-bundled-adapters) for when the updater prints the reminder.

## Import a self-built adapter

An adapter archive is a gzip tarball containing `manifest.json` and the executable named in `exec`. To package a local build from the [adapter sources](https://github.com/oxidekit/oxidepm-adapters), keep the core checkout in `../oxidepm` so Cargo can find the shared crates. For example, build and package `watch` for x86_64 Linux from the adapters checkout.

```sh
cargo build --release -p oxidepm-adapter-watch -p oxidepm-adapter-bundle
target/release/oxidepm-adapter-bundle --out target/watch-bundle \
  --target x86_64-unknown-linux-gnu --url-base https://example.org/adapters --sequence 1 \
  watch:target/release/oxidepm-watch
```

Use the filename and digest from your build's `target/watch-bundle/SHA256SUMS`. This example uses an archive built from the {{release_version}} sources.

```sh
oxidepm adapter import ./target/watch-bundle/watch-{{release_version}}.tar.gz --sha256 <digest> --allow-reserved-name --enable
```

The bundle builder requires a catalog URL. A pinned import reads the file or HTTPS URL you pass it. Add `--allow-reserved-name` only if the adapter uses a reserved name, such as `watch` or `notifier`. A pinned archive appears as `pinned by you` with `No signature` in the preview.

## Look at it, and manage it

```term cap="adapter-info" wrap="yes" label="Terminal output of oxidepm adapter info watch"
```

| Command | Meaning |
|---|---|
| `adapter list` | The installed adapters, with state and trust. |
| `adapter info <name>` | Everything about one: state, source, grant, what is enforced, crashes and protocol strikes, and the last lines it wrote to stderr. |
| `adapter disable <name>` | Stop it and take its rights away. |
| `adapter remove <name> [--purge]` | Remove its files. Its state directory is kept unless you pass `--purge`, because it may hold tokens and keys. |
| `adapter update <name>` or `--all` | Update to a newer version. Bundled adapters use the installed release bundle. `--rollback` goes back to the previous version without the network. |

`import`, `update`, `enable`, `disable` and `remove` take [`--dry-run`](/docs/commands/dry-run/). Enabling, disabling and removing are dangerous requests, so an AI actor cannot make them.

## If the program changes

The SHA-256 of the executable is recorded at import. If it no longer matches when the daemon starts the adapter, the adapter is not started and is marked failed (`E_ADAPTER_TAMPERED`).
