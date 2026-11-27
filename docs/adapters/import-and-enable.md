# Import and enable

Install an adapter from the signed catalogue, the release bundle or an archive you pin, read what it asks for, and enable it.

Source: https://oxidepm.com/docs/adapters/import-and-enable/

`adapter import` verifies and installs an adapter. With `--enable`, it also asks you to approve the grant. Services start when enabled, and tools start when called.

## List

`oxidepm adapter list` shows installed adapters. `oxidepm adapter list --available` lists the offers from the [signed online catalogue](https://oxidepm.com/security/#adapter-catalogue).

*Terminal output of oxidepm adapter search watch*

```text
$ oxidepm adapter search watch
NAME   KIND     VERSION   SUMMARY
watch  service  0.4.0     Restart an app when its files change.

Index https://raw.githubusercontent.com/oxidekit/oxidepm/catalogue/index.json (sequence 3), signed by key 04BF7D2A1951790C (official)
```

## Import from the catalogue

Use `info` to read the catalogue entry before importing. Once installed, `info` shows the local adapter and its grant.

```sh
oxidepm adapter info watch
oxidepm adapter import watch --enable
```

The CLI verifies the catalogue signature and the archive hash. Review the permissions and approve the grant when prompted. To get a newer version from the catalogue later, run `oxidepm adapter update watch`.

## Import from the release

The release ships all 13 adapters under `share/oxidepm/adapters`. Run `oxidepm adapter import --bundled <name> --enable` for any adapter you want to use. This command adds file watching.

```sh
oxidepm adapter import --bundled watch --enable
```

Bundled imports work offline. The CLI and daemon verify the bundle index and selected archives against `SHA256SUMS`. The installer runs `oxidepm adapter import --bundled --tag runtime --enable --yes` to enable only the four runtime adapters. To select groups, use `--tag dev` for `watch`, `check` and `init`, `--tag deploy` for `git-start` and `deploy`, `--tag ui` for `ui-web` and `ui-tui`, `--tag notifier` for `notifier`, or `--tag exporter` for `exporter-prometheus`.

Review the permissions and confirm the grant at the terminal prompt. To review before enabling, omit `--enable`. The adapter stays disabled until you approve the grant.

*Terminal output of oxidepm adapter import --bundled watch*

```text
$ oxidepm adapter import --bundled watch
Adapter   watch 0.4.0 (service)   Restart an app when its files change.
          Watches the directories an app lists under adapters.watch (paths, ignore, debounce_ms) and restarts that app, and only that app, after a trailing debounce window. It has no network, spawns no programs and writes nothing.
Source    bundle /usr/local/share/oxidepm/adapters
Trust     bundled with this release. Archive sha256 bd98b2e85e29528fde6e1b26e541b1c74197e58e0dd23b7751eb623bb61a0154 verified. Program sha256 134b3ed3a3f39847d5e86f368d8e51d9f8c8be18d0e2b67824a69fcb7187f0df
Needs     host      may stop, restart and reload apps. Only the apps that list it. Events: lifecycle.
          network   none.                                                                   Enforced on this machine: yes (seccomp)
          files     writes nothing, reads any file you can read.  [BROAD]                   Enforced on this machine: yes (Landlock 10)
          programs  none.                                                                   Enforced on this machine: yes (Landlock 10)
          memory    64 MiB.
Adds      no commands
Next      oxidepm adapter enable watch --accept 1f417029ecd44400
Again, what it needs:
  host      may stop, restart and reload apps. Only the apps that list it. Events: lifecycle.
  network   none.                                                                   Enforced on this machine: yes (seccomp)
  files     writes nothing, reads any file you can read.  [BROAD]                   Enforced on this machine: yes (Landlock 10)
  programs  none.                                                                   Enforced on this machine: yes (Landlock 10)
  memory    64 MiB.
✓ Installed watch 0.4.0 (disabled, nothing runs). Enable it with: oxidepm adapter enable watch --accept 1f417029ecd44400
```

`Needs` lists the permissions. `Again, what it needs` repeats the list after the description. `[BROAD]` marks permissions such as access to all files the current user can read. `Enforced on this machine` shows what the operating system can enforce. `Trust` identifies the source of the archive.

## Enable

```sh
oxidepm adapter enable <name> --accept <fingerprint>
```

For broader grants such as `watch`, run the printed command after reviewing the permissions if approval was deferred or the import ran without an interactive terminal. Get the fingerprint from `adapter import` or `adapter info`. It ties your consent to that adapter release. `--yes` accepts without asking only for pure adapters such as the four runtimes.

On a terminal, `oxidepm adapter enable watch` shows the permissions and asks for consent again.

*Terminal output of oxidepm adapter enable watch*

```text
$ oxidepm adapter enable watch
Adapter   watch 0.4.0 (service)   Restart an app when its files change.
          Watches the directories an app lists under adapters.watch (paths, ignore, debounce_ms) and restarts that app, and only that app, after a trailing debounce window. It has no network, spawns no programs and writes nothing.
Source    bundled installed 2026-11-26T07:30:32Z
Trust     bundled with this release. Program sha256 134b3ed3a3f39847d5e86f368d8e51d9f8c8be18d0e2b67824a69fcb7187f0df
Needs     host      may stop, restart and reload apps. Only the apps that list it. Events: lifecycle.
          network   none.                                                                   Enforced on this machine: yes (seccomp)
          files     writes nothing, reads any file you can read.  [BROAD]                   Enforced on this machine: yes (Landlock 10)
          programs  none.                                                                   Enforced on this machine: yes (Landlock 10)
          memory    64 MiB.
Adds      no commands
Next      oxidepm adapter enable watch --accept 1f417029ecd44400
Again, what it needs:
  host      may stop, restart and reload apps. Only the apps that list it. Events: lifecycle.
  network   none.                                                                   Enforced on this machine: yes (seccomp)
  files     writes nothing, reads any file you can read.  [BROAD]                   Enforced on this machine: yes (Landlock 10)
  programs  none.                                                                   Enforced on this machine: yes (Landlock 10)
  memory    64 MiB.
Enable watch with this grant? [y/N]
```

If you answer no, nothing is changed:

*Terminal output when the answer is no*

```text
Enable watch with this grant? [y/N] no
Error: Not enabled
```

If you answer yes:

*Terminal output when the answer is yes*

```text
Enable watch with this grant? [y/N] yes
✓ Enabled watch 0.4.0 (level lifecycle, scope opted-in)
  Enforced by the OS on this machine: network, fs_write, fs_read, spawn
```

You can enable with less than the adapter asks for. `--level read` or `--level lifecycle` gives a lower host level, and `--scope opted-in` limits it to the apps that list the adapter. `--allow-unenforced` accepts missing sandbox restrictions that the adapter requires.

## Update bundled adapters

After `oxidepm update`, restart the daemon and run `oxidepm adapter update --all` to refresh the adapters you imported from the release bundle. Use `oxidepm adapter update <name>` to update just one.

*Excerpt from oxidepm adapter update --all*

```text
$ oxidepm adapter update --all
✓ Updated watch 0.4.0-rc.8 to 0.4.0 (it passed its probation)
```

The update uses the bundle installed with the new release and follows the same verification and consent checks as import. If it needs a broader grant, review the permissions and run `oxidepm adapter update <name> --accept <fingerprint>` with the fingerprint from the preview. See [Upgrade](https://oxidepm.com/docs/getting-started/upgrade/#update-bundled-adapters) for when the updater prints the reminder.

## Import a self-built adapter

An adapter archive is a gzip tarball containing `manifest.json` and the executable named in `exec`. To package a local build from the [adapter sources](https://github.com/oxidekit/oxidepm-adapters), keep the core checkout in `../oxidepm` so Cargo can find the shared crates. The `ui-tui` adapter needs Rust 1.88 or newer to build from source. To build and package `watch` for x86_64 Linux, run these commands from the adapters checkout.

```sh
cargo build --release -p oxidepm-adapter-watch -p oxidepm-adapter-bundle
target/release/oxidepm-adapter-bundle --out target/watch-bundle \
  --target x86_64-unknown-linux-gnu --url-base https://example.org/adapters --sequence 1 \
  watch:target/release/oxidepm-watch
```

Use the filename and digest from your build's `target/watch-bundle/SHA256SUMS`. This example uses an archive built from the 0.4.0 sources.

```sh
oxidepm adapter import ./target/watch-bundle/watch-0.4.0.tar.gz --sha256 <digest> --allow-reserved-name --enable
```

The bundle builder requires a catalogue URL. A pinned import reads the file or HTTPS URL you pass it. Add `--allow-reserved-name` only if the adapter uses a reserved name, such as `watch` or `notifier`. A pinned archive appears as `pinned by you` with `No signature` in the preview.

## Look at it, and manage it

*Terminal output of oxidepm adapter info watch*

```text
$ oxidepm adapter info watch
watch 0.4.0 (service)  Restart an app when its files change.
State:    ready
Source:   bundled
Trust:    bundled with this release. Program sha256 134b3ed3a3f39847d5e86f368d8e51d9f8c8be18d0e2b67824a69fcb7187f0df
Installed 2026-11-26T07:30:32Z
Grant:    level lifecycle, scope opted-in
Enforced: network, fs_write, fs_read, spawn
Health:   0 crash(es), 0 protocol strike(s)

Adapter   watch 0.4.0 (service)   Restart an app when its files change.
          Watches the directories an app lists under adapters.watch (paths, ignore, debounce_ms) and restarts that app, and only that app, after a trailing debounce window. It has no network, spawns no programs and writes nothing.
Source    bundled
Trust     bundled with this release. Program sha256 134b3ed3a3f39847d5e86f368d8e51d9f8c8be18d0e2b67824a69fcb7187f0df
Needs     host      may stop, restart and reload apps. Only the apps that list it. Events: lifecycle.
          network   none.                                                                   Enforced on this machine: yes (seccomp)
          files     writes nothing, reads any file you can read.  [BROAD]                   Enforced on this machine: yes (Landlock 10)
          programs  none.                                                                   Enforced on this machine: yes (Landlock 10)
          memory    64 MiB.
Adds      no commands
Next      fingerprint 1f417029ecd44400
Again, what it needs:
  host      may stop, restart and reload apps. Only the apps that list it. Events: lifecycle.
  network   none.                                                                   Enforced on this machine: yes (seccomp)
  files     writes nothing, reads any file you can read.  [BROAD]                   Enforced on this machine: yes (Landlock 10)
  programs  none.                                                                   Enforced on this machine: yes (Landlock 10)
  memory    64 MiB.
```

| Command | Meaning |
|---|---|
| `adapter list` | Installed adapters, with state and trust. |
| `adapter list --available` | Adapters offered by the signed catalogue. |
| `adapter search <word>` | Find offers by name, summary, description or tag. |
| `adapter info <name>` | Installed adapter details, including state, source, grant, enforcement and health. For an adapter you have yet to install, shows the catalogue entry. |
| `adapter disable <name>` | Stop it and take its rights away. |
| `adapter remove <name> [--purge]` | Remove its files. Its state directory is kept unless you pass `--purge`, because it may hold tokens and keys. |
| `adapter update <name>` or `--all` | Update to a newer version. Catalogue imports use the signed catalogue, and bundled imports use the installed release bundle. `--rollback` goes back to the previous version without the network. |

`import`, `update`, `enable`, `disable` and `remove` take [`--dry-run`](https://oxidepm.com/docs/commands/dry-run/). Enabling, disabling and removing are dangerous requests, so an AI actor cannot make them.

## If the program changes

The SHA-256 of the executable is recorded at import. If it no longer matches when the daemon starts the adapter, the adapter is not started and is marked failed (`E_ADAPTER_TAMPERED`).
