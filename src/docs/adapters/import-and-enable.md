Installing an adapter is two steps that you do separately: `import` fetches and checks it and installs it switched off, and `enable` asks you to accept what it needs and starts it.

## List

```term cap="adapter-list" label="Terminal output of oxidepm adapter list and list --available"
```

`list` shows the installed adapters. `list --available` and `search` read the signed index, and this build has none configured, so they say so and point at the other ways.

## Import

An archive is a gzip tarball with `manifest.json` and the executable the manifest names in `exec`, side by side. Import it from a file or an https URL, and pin it with its SHA-256:

```sh
oxidepm adapter import notifier.tar.gz --sha256 <hex> --allow-reserved-name
```

Without `--sha256` nothing is installed: the command prints the archive's hash and asks you to run it again with `--sha256` if you trust it. On a terminal, a pinned import asks you to type the first 12 digits of the hash when it is not given.

`--allow-reserved-name` is needed only for a name the core reserves for adapters signed by an official key: `notifier`, `ui-web`, `ui-tui`, `check`, `init`, `git-start`, `deploy` and the `runtime-` adapters for node, python, go and rust. The Prometheus exporter is not reserved, so it needs no flag. Pass the flag, as in the example, for `notifier`. Other forms are `oxidepm adapter import --bundled [names] [--tag runtime]`, which takes adapters from the bundle that a release carries (a `cargo install` build has none), and `oxidepm adapter import <name>` from the signed index. `--enable` enables the adapter right after it is installed, with the same consent.

```term cap="adapter-import" label="Terminal output of oxidepm adapter import"
```

Read this before you go on. `Needs` is what the adapter asks for, and `Again, what it needs` repeats it at the end so nothing in the description can push it out of sight. `[BROAD]` marks power that deserves a second look. `Enforced on this machine` says what the operating system can hold the adapter to here. `Trust` says where the archive came from: a pinned archive says `pinned by you` and `No signature`. Nothing runs yet.

## Enable

```sh
oxidepm adapter enable notifier
```

`enable` shows the same list again, asks, and starts the adapter. On a terminal you answer the question. In a script, pass `--accept <fingerprint>` with the fingerprint that `import` and `info` print, which ties your consent to exactly that release. `--yes` accepts without asking, only for an adapter that needs nothing broad.

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

You can enable with less than the adapter asks for: `--level read|lifecycle` gives a lower host level, and `--scope opted-in` limits it to the apps that list the adapter. If the OS cannot enforce something the adapter requires to be enforced, `enable` refuses unless you pass `--allow-unenforced`.

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
