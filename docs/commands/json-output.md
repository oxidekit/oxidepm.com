# JSON output

The --json flag, and what it prints.

Source: https://oxidepm.com/docs/commands/json-output/

Most commands take `--json` and print JSON instead of a table.

*Terminal output of oxidepm --json status*

```text
$ oxidepm --json status
[
  {
    "id": 1,
    "name": "mailer",
    "mode": "cmd",
    "pid": null,
    "restarts": 3,
    "status": "errored",
    "cpu_percent": 0.0,
    "memory_bytes": 0,
    "uptime_secs": 0
  }
]
```

A running app has `"status": "running"`: the table calls it `online`. `tags` is present when the app has any.

## Other output

- `oxidepm --json show <name>` prints the same fields plus the command, working directory, arguments, `last_exit_code`, `healthy` and the two policy markers.
- `oxidepm --json <command> --dry-run` prints the plan: `op`, a `decision`, an `items` list with one entry per app (`id`, `name`, `action`, `detail`, `order`) and `warnings`.
- `oxidepm --json audit` prints one audit record per line.

An error is printed as text, with a non-zero exit code, in `--json` mode too. The stable `E_` code of an error is on the daemon's socket, in the audit log and in the adapter protocol; see [Error codes](https://oxidepm.com/docs/commands/error-codes/).
