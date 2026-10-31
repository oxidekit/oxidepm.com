## save

```sh
oxidepm save
oxidepm save --force
```

`save` writes `saved.json` from the apps that should be running. It is refused when that would replace a file that lists apps with an empty list (`E_SAVE_WOULD_EMPTY`), unless you pass `--force`. The file is written atomically, with mode 0600, and carries a version number. A file from an older release is refused: run `save` again.

The markers `protected` and `ai_control` are saved too, so `delete all` followed by `resurrect` brings an app back with the markers it had.

## resurrect

```sh
oxidepm resurrect
```

`resurrect` starts the apps that should be running and are not up. An app you stopped stays stopped. It also adds apps from `saved.json` that were deleted since. Apps start the way a config file starts them: in dependency order, with their own result each.

## At boot

[Survive a reboot](/docs/getting-started/reboot/) shows how to start the daemon at boot with `oxidepm startup`.

Both commands are dangerous requests: an AI actor cannot make them. Both take [`--dry-run`](/docs/commands/dry-run/).
