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

```term cap="crash-loop" label="Terminal output of oxidepm status and oxidepm logs for an errored app"
```

## flush

```sh
oxidepm flush api
```

`flush` truncates the active log files of an app. Rotated files stay. The log contents are lost, so read them first. Log rotation is automatic ([Log files](/docs/configuration/log-files/)), so flushing to save space is rarely needed. `flush` is a dangerous request: an AI actor cannot make it.
