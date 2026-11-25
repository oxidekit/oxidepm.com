## Update

```sh
oxidepm update                      # the latest release
oxidepm update --version {{release_version}}    # a specific version
```

Starting with 0.4.0-rc.4, `oxidepm update` authenticates the release before downloading the archive.

- The CLI verifies `checksums.txt.minisig` against its built-in [release signing keys](/security/#release-signing). It refuses a missing or invalid signature and requires the trusted comment to match the exact release tag.
- The archive must have the exact filename `oxidepm-<target>.tar.gz` and match the SHA-256 listed for that name in the verified `checksums.txt`. The CLI then unpacks it safely.
- A running daemon is stopped, the files are replaced atomically with the old ones kept as `.pre-update`, and the new `oxidepm --version` is run. If that fails, everything is put back.
- A downgrade requires both `--version` and `--force`, and the requested release must be signed.

`oxidepm --dry-run update` performs the same verification, downloads and unpacks the archive in a private temporary directory, shows what it would replace and deletes the directory. Nothing is installed and no daemon is stopped.

The update installs the release bundle with all 13 adapters alongside the executables. macOS supports the built-in `cmd` runtime. The adapter launcher and sandbox are Linux-only in this release.

## Update bundled adapters

On Linux, restart the daemon after `oxidepm update`, then run `oxidepm adapter update --all` to update the adapters you imported from the release bundle.

```term cap="adapter-update" wrap="yes" label="Excerpt from oxidepm adapter update --all"
```

When you run `oxidepm update` with 0.4.0-rc.6 or later, it lists installed bundled adapters that are older than the new bundle and suggests `oxidepm adapter update --all`. When upgrading from an older CLI, run the adapter update command yourself after restarting the daemon.

To update one adapter, run `oxidepm adapter update <name>`. If an update needs a broader grant, review the permissions and update that adapter with `--accept <fingerprint>`. See [Update bundled adapters](/docs/adapters/import-and-enable/#update-bundled-adapters).

To add runtimes for the first time, run `oxidepm adapter import --bundled --tag runtime --enable --yes` to import and enable all four. See [Import from the release](/docs/adapters/import-and-enable/#import-from-the-release) for the other adapters.

## Keep the CLI and daemon together

The CLI and the daemon must come from the same release. A config file is sent to the daemon as one `StartBatch` request, so `oxidepm start <config file>` needs a daemon of the same release.

## Upgrade from older releases

From 0.4.0-rc.1 through 0.4.0-rc.3, run `oxidepm update` to install {{release_version}}. Those clients check SHA-256 for that upgrade. The new CLI verifies signatures on subsequent updates. To verify the initial download yourself, follow the [manual verification and installation instructions](/docs/getting-started/install/#verify-a-release-download).

From 0.3.x, use the manual verification and installation instructions.

### State from older releases

When upgrading from 0.3.2, keep a copy of your app configuration and stop the old daemon before installing. The new daemon uses `state.db` and a versioned `saved.json`. Start your apps from their configs and run `oxidepm save` to record the new state.
