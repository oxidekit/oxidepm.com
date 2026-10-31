## The environment an app gets

An app does not get the daemon's environment. It gets:

1. `PATH`, `HOME`, `USER`, `LOGNAME`, `SHELL`, `LANG`, `LC_*`, `TZ` and `TMPDIR`,
2. then `--env` (`env` in a config file) and `--env-file` (`env_file`),
3. and `OPM_APP_ID` and `OPM_APP_NAME` from the daemon (`OPM_INSTANCE_ID` for a cluster instance).

`--env-inherit` gives the app the daemon's whole environment instead. That is the environment of the daemon, not of the shell that ran `oxidepm start`. Build steps (`cargo build`, `rustc`) always get the daemon's environment.

## Secrets are not shown

`status`, `show`, `describe` and `env list` do not show environment values. The daemon replaces every value with `<redacted>`, and keeps the keys visible. Hook and health-check scripts show as `<set>`. `oxidepm show <name> --reveal` is the one way to see them, and the daemon writes a line to its log each time it is asked. It is a dangerous request, so an AI actor cannot make it.

Command arguments, URLs, logs, other command output and config files are not scrubbed. Keep tokens out of them: use `env_file` or environment variables.

`oxidepm env set` and `env unset` are refused. The daemon has no request that changes the environment of a saved app. Pass `--env KEY=VALUE` when starting the app, or set `env` in the config file and start the file again.

```term label="Terminal output of oxidepm env list"
{hi:$} oxidepm env list api
api: no environment variables set
```

## Event hooks

```sh
oxidepm start ./app \
  --on-start   "./notify.sh started" \
  --on-stop    "./notify.sh stopped" \
  --on-crash   "./notify.sh crashed" \
  --on-restart "./notify.sh restarted"
```

In a config file the table is `hooks`, with the same four keys and a fifth, `on_error`, which runs when the app ends `errored` or turns `unhealthy`.

A hook runs as `sh -c` in its own process group and is killed with everything it started after 30 seconds. Its output is appended to `logs/<name>-hooks.log`. It gets `PATH`, `HOME` and a few other basics from the daemon, the app's own `env`, and these variables, where they apply: `OPM_APP_ID`, `OPM_APP_NAME`, `OPM_EVENT`, `OPM_PID`, `OPM_EXIT_CODE`, `OPM_REASON` and `OPM_RESTARTS`. The daemon's other variables are not passed on, not even with `--env-inherit`.
