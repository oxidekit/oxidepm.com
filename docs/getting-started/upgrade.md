# Upgrade

Update to a newer release with `oxidepm update`, and what it checks.

Source: https://oxidepm.com/docs/getting-started/upgrade/

## Update

```sh
oxidepm update                      # the latest release
oxidepm update --version 0.3.2      # a specific one
```

`update` downloads the release archive for your platform and installs it. It is careful about it:

- The archive must match the SHA-256 in the release's `checksums.txt`. That is an integrity check. There is no release signing key yet, so authenticity is not checked.
- The asset is the one named exactly `oxidepm-<target>.tar.gz`, and it is unpacked safely.
- A running daemon is stopped, the files are replaced atomically with the old ones kept as `.pre-update`, and the new `oxidepm --version` is run. If that fails, everything is put back.
- An older version needs `--force`.

`oxidepm --dry-run update` downloads the archive into a private temporary directory, checks it against `checksums.txt`, unpacks it there, shows what it would replace and deletes the directory. Nothing is installed and no daemon is stopped.

## Keep the CLI and daemon together

The CLI and the daemon must come from the same release. A config file is sent to the daemon as one `StartBatch` request, so `oxidepm start <config file>` needs a daemon of the same release.

## State from older releases

The daemon's database is `state.db`, schema version 2. An old `oxidepm.db` is not migrated. A `saved.json` written by an older release is refused: run `oxidepm save` again. To go back to a release from before the policy markers, move `state.db` aside or put back `state.db.pre-v2`, the copy the daemon made before it migrated the file. Changes made since are lost.
