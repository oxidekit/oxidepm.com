# Upgrade

Update to a newer release with `oxidepm update`, and what it checks.

Source: https://oxidepm.com/docs/getting-started/upgrade/

## Update

```sh
oxidepm update                      # the latest release
oxidepm update --version 0.4.0-rc.2    # a specific version
```

`update` downloads the release archive for your platform and installs it. It is careful about it:

- The archive must match the SHA-256 in the release's `checksums.txt`. That is an integrity check. There is no release signing key yet, so authenticity is not checked.
- The asset is the one named exactly `oxidepm-<target>.tar.gz`, and it is unpacked safely.
- A running daemon is stopped, the files are replaced atomically with the old ones kept as `.pre-update`, and the new `oxidepm --version` is run. If that fails, everything is put back.
- An older version needs `--force`.

`oxidepm --dry-run update` downloads the archive into a private temporary directory, checks it against `checksums.txt`, unpacks it there, shows what it would replace and deletes the directory. Nothing is installed and no daemon is stopped.

The update installs the release's adapter bundle alongside the executables. On Linux, run `oxidepm adapter import --bundled --tag runtime --enable --yes` to import and enable the bundled runtimes. macOS supports the built-in `cmd` runtime. The adapter launcher and sandbox are Linux-only in this release.

## Keep the CLI and daemon together

The CLI and the daemon must come from the same release. A config file is sent to the daemon as one `StartBatch` request, so `oxidepm start <config file>` needs a daemon of the same release.

## State from older releases

When upgrading from 0.3.2, keep a copy of your app configuration and stop the old daemon before installing. The new daemon uses `state.db` and a versioned `saved.json`. Start your apps from their configs and run `oxidepm save` to record the new state.
