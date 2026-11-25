# logs and flush

Read, follow and filter an app's logs, and truncate them.

Source: https://oxidepm.com/docs/commands/logs/

## logs

```sh
oxidepm logs api                      # the last 15 lines
oxidepm logs api -f                   # follow
oxidepm logs api --lines 100
oxidepm logs api --err                # only stderr
oxidepm logs api --grep "timeout|refused"
```

| Option | Meaning |
|---|---|
| `-f, --follow` | Follow the output. |
| `--lines <n>` | How many lines to show. 15 by default. |
| `--out`, `--err` | Only stdout, or only stderr. |
| `--grep <regex>` | Only lines that match the pattern. |

*Terminal output of oxidepm status and oxidepm logs for an errored app*

```text
$ oxidepm status
╭────┬────────┬──────┬─────┬───┬─────────┬──────┬─────┬────────╮
│ id │ name   │ mode │ pid │ ↺ │ status  │ cpu  │ mem │ uptime │
├────┼────────┼──────┼─────┼───┼─────────┼──────┼─────┼────────┤
│  1 │ mailer │ cmd  │ -   │ 3 │ errored │ 0.0% │ 0B  │ 0s     │
╰────┴────────┴──────┴─────┴───┴─────────┴──────┴─────┴────────╯
$ oxidepm logs mailer --lines 3
[2026-11-25 21:35:25.123] cannot reach smtp
[2026-11-25 21:35:25.527] cannot reach smtp
[2026-11-25 21:35:26.330] cannot reach smtp
```

## flush

```sh
oxidepm flush api
```

`flush` truncates the active log files of an app. Rotated files stay. The log contents are lost, so read them first. Log rotation is automatic ([Log files](https://oxidepm.com/docs/configuration/log-files/)), so flushing to save space is rarely needed. `flush` is a dangerous request: an AI actor cannot make it.
