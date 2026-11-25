On Linux, `adapter import` verifies and installs an adapter. `adapter enable` asks you to accept its permissions. Use `import --enable` to do both in one command. Services start when enabled, and tools start when called.

## List

```term cap="adapter-list" label="Terminal output of oxidepm adapter list and list --available"
```

`list` shows the installed adapters. `list --available` and `search` require a configured signed index. This release ships without a network catalog.

## Import

An archive is a gzip tarball with `manifest.json` and the executable the manifest names in `exec`, side by side. Import it from a file or an https URL, and pin it with its SHA-256:

```sh
oxidepm adapter import notifier.tar.gz --sha256 <hex> --allow-reserved-name
```

Without `--sha256` nothing is installed: the command prints the archive's hash and asks you to run it again with `--sha256` if you trust it. On a terminal, a pinned import asks you to type the first 12 digits of the hash when it is not given.

For pinned archives that use a reserved name, add `--allow-reserved-name`. That applies to `notifier`, `ui-web`, `ui-tui`, `check`, `init`, `git-start`, `deploy`, `watch` and the runtime adapters. Import `exporter-prometheus` with the digest alone.

`oxidepm adapter import <name>` looks up an adapter in a configured signed index. When the release bundle is installed, `oxidepm adapter import --bundled --tag runtime --enable --yes` verifies its `SHA256SUMS` and imports and enables the bundled runtimes offline. The install script runs this command on Linux.

```term cap="adapter-import" label="Terminal output of oxidepm adapter import"
```

Read this before you go on. `Needs` is what the adapter asks for, and `Again, what it needs` repeats it at the end so nothing in the description can push it out of sight. `[BROAD]` marks power that deserves a second look. `Enforced on this machine` says what the operating system can hold the adapter to here. `Trust` says where the archive came from: a pinned archive says `pinned by you` and `No signature`. Nothing runs yet.

## Enable

```sh
oxidepm adapter enable notifier
```

`enable` shows the permissions again and asks for consent. On a terminal you answer the question. In a script, pass `--accept <fingerprint>` with the fingerprint that `import` and `info` print, which ties your consent to exactly that release. `--yes` accepts without asking, only for an adapter that needs nothing broad.

```term cap="adapter-enable" label="Terminal output of oxidepm adapter enable: the consent screen"
```

If you answer no, nothing is changed:

```term label="Terminal output when the answer is no"
Enable notifier with this grant? [y/N] no
{ox:Error:} Not enabled
```

If you answer yes:

```term label="Terminal output when the answer is yes"
Enable notifier with this grant? [y/N] yes
{hi:✓} Enabled notifier 0.1.0 (level read, scope all)
  Enforced by the OS on this machine: fs_write, fs_read, spawn
```

You can enable with less than the adapter asks for. `--level read` or `--level lifecycle` gives a lower host level, and `--scope opted-in` limits it to the apps that list the adapter. On Linux, `--allow-unenforced` accepts missing sandbox restrictions that the adapter requires. macOS supports the built-in `cmd` runtime. The adapter launcher and sandbox are Linux-only in this release.

## Build an optional adapter

Build an archive from the [adapter sources](https://github.com/oxidekit/oxidepm-adapters). Keep the core checkout in `../oxidepm` so Cargo can find the shared crates. For the `watch` adapter on x86_64 Linux, run these commands in the adapters checkout:

```sh
cargo build --release -p oxidepm-adapter-watch -p oxidepm-adapter-bundle
target/release/oxidepm-adapter-bundle --out target/watch-bundle \
  --target x86_64-unknown-linux-gnu --url-base https://example.org/adapters --sequence 1 \
  watch:target/release/oxidepm-watch
```

Start the daemon with `oxidepm resurrect` if it is down. Use the archive's filename and its digest from `target/watch-bundle/SHA256SUMS`:

```sh
oxidepm adapter import ./target/watch-bundle/watch-0.4.0-rc.1.tar.gz --sha256 <digest> --allow-reserved-name --enable
```

For the other optional adapters, use their directory, executable and digest. The catalog URL is required by the bundle builder. A local pinned import reads the archive directly.

## Look at it, and manage it

```term cap="adapter-info" label="Terminal output of oxidepm adapter info"
```

| Command | Meaning |
|---|---|
| `adapter list` | The installed adapters, with state and trust. |
| `adapter info <name>` | Everything about one: state, source, grant, what is enforced, crashes and protocol strikes, and the last lines it wrote to stderr. |
| `adapter disable <name>` | Stop it and take its rights away. |
| `adapter remove <name> [--purge]` | Remove its files. Its state directory is kept unless you pass `--purge`, because it may hold tokens and keys. |
| `adapter update <name>` or `--all` | Update to a newer release. An update that asks for more than the installed one needs `--accept` with the new fingerprint. `--rollback` goes back to the previous version without the network. |

`import`, `update`, `enable`, `disable` and `remove` take [`--dry-run`](/docs/commands/dry-run/). Enabling, disabling and removing are dangerous requests, so an AI actor cannot make them.

## If the program changes

The SHA-256 of the executable is recorded at import. If it no longer matches when the daemon starts the adapter, the adapter is not started and is marked failed (`E_ADAPTER_TAMPERED`).
