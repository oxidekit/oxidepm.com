# Import and enable

Install an adapter from an archive you pin, read what it asks for, and enable it.

Source: https://oxidepm.com/docs/adapters/import-and-enable/

Installing an adapter is two steps that you do separately: `import` fetches and checks it and installs it switched off, and `enable` asks you to accept what it needs and starts it.

## List

*Terminal output of oxidepm adapter list and list --available*

```text
$ oxidepm adapter list
No adapters are installed. `oxidepm adapter list --available` shows what the index offers.
$ oxidepm adapter list --available
Error: no index is configured in this build. Import by a pinned hash (`oxidepm adapter import <file or url> --sha256 <hex>`) or from the bundle of a release (`oxidepm adapter import --bundled`)
```

`list` shows the installed adapters. `list --available` and `search` read the signed index, and this build has none configured, so they say so and point at the other ways.

## Import

An archive is a gzip tarball with `manifest.json` and the executable the manifest names in `exec`, side by side. Import it from a file or an https URL, and pin it with its SHA-256:

```sh
oxidepm adapter import notifier.tar.gz --sha256 <hex> --allow-reserved-name
```

Without `--sha256` nothing is installed: the command prints the archive's hash and asks you to run it again with `--sha256` if you trust it. On a terminal, a pinned import asks you to type the first 12 digits of the hash when it is not given.

`--allow-reserved-name` is needed only for a name the core reserves for adapters signed by an official key: `notifier`, `ui-web`, `ui-tui`, `check`, `init`, `git-start`, `deploy` and the `runtime-node`, `runtime-python`, `runtime-go` and `runtime-rust` adapters. The Prometheus exporter is not reserved, so it needs no flag. Pass the flag, as in the example, for `notifier`. Other forms are `oxidepm adapter import --bundled [names] [--tag runtime]`, which takes adapters from the bundle that a release carries (a build from source has none). The bundle holds the runtime adapters, and `oxidepm adapter import --bundled --tag runtime --enable --yes` imports and enables them with no network, which is what the install script runs, and `oxidepm adapter import <name>` from the signed index. `--enable` enables the adapter right after it is installed, with the same consent.

*Terminal output of oxidepm adapter import*

```text
$ oxidepm adapter import notifier.tar.gz --sha256 fa85a17e321cfbb84e5af87835ea399def9cd0d6670df6f8f16746d0149cb203 --allow-reserved-name
Adapter   notifier 0.1.0 (service)   Telegram, Discord, Slack and webhook notifications.
          Sends a message to the channels you configure when an app starts, stops, restarts, crashes, loops, goes over its memory limit or fails its health check. It reads only those events and its own config.toml, and it never touches your apps.
Source    notifier.tar.gz (pinned by you)
Trust     pinned by you: sha256 fa85a17e321cfbb84e5af87835ea399def9cd0d6670df6f8f16746d0149cb203. Program sha256 d57290e957af80897bea384066311d07cf4bfb1d9da4e314760e35503b85fe77. No signature
Needs     host      read only (status). Events: lifecycle.
          network   outbound. It says it uses api.telegram.org, discord.com, hooks.slack.com. Not enforceable per host.  [BROAD]  Enforced on this machine: yes (seccomp)
          files     writes only its own directory, reads /etc/resolv.conf, /etc/hosts, /etc/nsswitch.conf, /etc/host.conf, /etc/gai.conf.  Enforced on this machine: yes (Landlock 10)
          programs  none.                                                                   Enforced on this machine: yes (Landlock 10)
          environment receives OXIDEPM_TELEGRAM_TOKEN from your environment.  [BROAD]
          memory    128 MiB.
Adds      commands: notify (caution, writes)
Next      oxidepm adapter enable notifier --accept 33926d31eb91080f
Again, what it needs:
  host      read only (status). Events: lifecycle.
  network   outbound. It says it uses api.telegram.org, discord.com, hooks.slack.com. Not enforceable per host.  [BROAD]  Enforced on this machine: yes (seccomp)
  files     writes only its own directory, reads /etc/resolv.conf, /etc/hosts, /etc/nsswitch.conf, /etc/host.conf, /etc/gai.conf.  Enforced on this machine: yes (Landlock 10)
  programs  none.                                                                   Enforced on this machine: yes (Landlock 10)
  environment receives OXIDEPM_TELEGRAM_TOKEN from your environment.  [BROAD]
  memory    128 MiB.
✓ Installed notifier 0.1.0 (disabled, nothing runs). Enable it with: oxidepm adapter enable notifier --accept 33926d31eb91080f
```

Read this before you go on. `Needs` is what the adapter asks for, and `Again, what it needs` repeats it at the end so nothing in the description can push it out of sight. `[BROAD]` marks power that deserves a second look. `Enforced on this machine` says what the operating system can hold the adapter to here. `Trust` says where the archive came from: a pinned archive says `pinned by you` and `No signature`. Nothing runs yet.

## Enable

```sh
oxidepm adapter enable notifier
```

`enable` shows the same list again, asks, and starts the adapter. On a terminal you answer the question. In a script, pass `--accept <fingerprint>` with the fingerprint that `import` and `info` print, which ties your consent to exactly that release. `--yes` accepts without asking, only for an adapter that needs nothing broad.

*Terminal output of oxidepm adapter enable: the consent screen*

```text
$ oxidepm adapter enable notifier
Adapter   notifier 0.1.0 (service)   Telegram, Discord, Slack and webhook notifications.
          Sends a message to the channels you configure when an app starts, stops, restarts, crashes, loops, goes over its memory limit or fails its health check. It reads only those events and its own config.toml, and it never touches your apps.
Source    pinned:notifier.tar.gz installed 2026-10-31T04:06:41Z
Trust     pinned by you. Program sha256 d57290e957af80897bea384066311d07cf4bfb1d9da4e314760e35503b85fe77. No signature
Needs     host      read only (status). Events: lifecycle.
          network   outbound. It says it uses api.telegram.org, discord.com, hooks.slack.com. Not enforceable per host.  [BROAD]  Enforced on this machine: yes (seccomp)
          files     writes only its own directory, reads /etc/resolv.conf, /etc/hosts, /etc/nsswitch.conf, /etc/host.conf, /etc/gai.conf.  Enforced on this machine: yes (Landlock 10)
          programs  none.                                                                   Enforced on this machine: yes (Landlock 10)
          environment receives OXIDEPM_TELEGRAM_TOKEN from your environment.  [BROAD]
          memory    128 MiB.
Adds      commands: notify (caution, writes)
Next      oxidepm adapter enable notifier --accept 33926d31eb91080f
Again, what it needs:
  host      read only (status). Events: lifecycle.
  network   outbound. It says it uses api.telegram.org, discord.com, hooks.slack.com. Not enforceable per host.  [BROAD]  Enforced on this machine: yes (seccomp)
  files     writes only its own directory, reads /etc/resolv.conf, /etc/hosts, /etc/nsswitch.conf, /etc/host.conf, /etc/gai.conf.  Enforced on this machine: yes (Landlock 10)
  programs  none.                                                                   Enforced on this machine: yes (Landlock 10)
  environment receives OXIDEPM_TELEGRAM_TOKEN from your environment.  [BROAD]
  memory    128 MiB.
Enable notifier with this grant? [y/N] 
```

If you answer no, nothing is changed:

*Terminal output when the answer is no*

```text
Enable notifier with this grant? [y/N] no
Error: Not enabled
```

If you answer yes:

*Terminal output when the answer is yes*

```text
Enable notifier with this grant? [y/N] yes
✓ Enabled notifier 0.1.0 (level read, scope all)
  Enforced by the OS on this machine: fs_write, fs_read, spawn
```

You can enable with less than the adapter asks for: `--level read|lifecycle` gives a lower host level, and `--scope opted-in` limits it to the apps that list the adapter. If the OS cannot enforce something the adapter requires to be enforced, `enable` refuses unless you pass `--allow-unenforced`.

## Look at it, and manage it

*Terminal output of oxidepm adapter info*

```text
$ oxidepm adapter info notifier
notifier 0.1.0 (service)  Telegram, Discord, Slack and webhook notifications.
State:    ready
Source:   pinned:notifier.tar.gz
Trust:    pinned by you. Program sha256 d57290e957af80897bea384066311d07cf4bfb1d9da4e314760e35503b85fe77. No signature
Installed 2026-10-31T04:06:41Z
Grant:    level read, scope all
Enforced: fs_write, fs_read, spawn
Health:   0 crash(es), 0 protocol strike(s)

Adapter   notifier 0.1.0 (service)   Telegram, Discord, Slack and webhook notifications.
          Sends a message to the channels you configure when an app starts, stops, restarts, crashes, loops, goes over its memory limit or fails its health check. It reads only those events and its own config.toml, and it never touches your apps.
Source    pinned:notifier.tar.gz
Trust     pinned by you. Program sha256 d57290e957af80897bea384066311d07cf4bfb1d9da4e314760e35503b85fe77. No signature
Needs     host      read only (status). Events: lifecycle.
          network   outbound. It says it uses api.telegram.org, discord.com, hooks.slack.com. Not enforceable per host.  [BROAD]  Enforced on this machine: yes (seccomp)
          files     writes only its own directory, reads /etc/resolv.conf, /etc/hosts, /etc/nsswitch.conf, /etc/host.conf, /etc/gai.conf.  Enforced on this machine: yes (Landlock 10)
          programs  none.                                                                   Enforced on this machine: yes (Landlock 10)
          environment receives OXIDEPM_TELEGRAM_TOKEN from your environment.  [BROAD]
          memory    128 MiB.
Adds      commands: notify (caution, writes)
Next      fingerprint 33926d31eb91080f
Again, what it needs:
  host      read only (status). Events: lifecycle.
  network   outbound. It says it uses api.telegram.org, discord.com, hooks.slack.com. Not enforceable per host.  [BROAD]  Enforced on this machine: yes (seccomp)
  files     writes only its own directory, reads /etc/resolv.conf, /etc/hosts, /etc/nsswitch.conf, /etc/host.conf, /etc/gai.conf.  Enforced on this machine: yes (Landlock 10)
  programs  none.                                                                   Enforced on this machine: yes (Landlock 10)
  environment receives OXIDEPM_TELEGRAM_TOKEN from your environment.  [BROAD]
  memory    128 MiB.
```

| Command | Meaning |
|---|---|
| `adapter list` | The installed adapters, with state and trust. |
| `adapter info <name>` | Everything about one: state, source, grant, what is enforced, crashes and protocol strikes, and the last lines it wrote to stderr. |
| `adapter disable <name>` | Stop it and take its rights away. |
| `adapter remove <name> [--purge]` | Remove its files. Its state directory is kept unless you pass `--purge`, because it may hold tokens and keys. |
| `adapter update <name>` or `--all` | Update to a newer release. An update that asks for more than the installed one needs `--accept` with the new fingerprint. `--rollback` goes back to the previous version without the network. |

`import`, `update`, `enable`, `disable` and `remove` take [`--dry-run`](https://oxidepm.com/docs/commands/dry-run/). Enabling, disabling and removing are dangerous requests, so an AI actor cannot make them.

## If the program changes

The SHA-256 of the executable is recorded at import. If it no longer matches when the daemon starts the adapter, the adapter is not started and is marked failed (`E_ADAPTER_TAMPERED`).
