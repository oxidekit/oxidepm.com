## Start an app

`oxidepm start` takes a file, a directory or a config file. It starts the daemon if it is not running, and the daemon keeps your app running after you close the terminal.

```sh
oxidepm start app.py            # a script: the runtime comes from its extension
oxidepm start ./my-project      # a directory: the runtime comes from the files in it
oxidepm start oxidepm.config.toml
```

The runtime of a script comes from its extension (`.js` is node, `.py` is python, `.go` is go, `.rs` is rust) and of a directory from the file that marks it (`package.json`, `Cargo.toml`, `go.mod`, `requirements.txt`). Use `--mode` to force one: `cmd`, `node`, `npm`, `pnpm`, `yarn`, `cargo`, `rust`, `python`, `go`. `cmd` runs any program.

A config file starts every app in it, as one batch. This one is the example used on these pages. It is the file the sample output below came from, with small stand-in programs for the real ones:

```toml title="oxidepm.config.toml"
[[apps]]
name = "db"
mode = "cmd"
script = "sleep"
args = ["100000"]
protected = true

[[apps]]
name = "api"
mode = "cmd"
script = "python3"
args = ["-m", "http.server", "18080", "--bind", "127.0.0.1"]
depends_on = ["db"]
ai_control = true

[apps.health_check]
http_url = "http://127.0.0.1:18080/"

[[apps]]
name = "web"
mode = "cmd"
script = "sleep"
args = ["100000"]
depends_on = ["api"]
ai_control = true
```

```term cap="start-config" label="Terminal output of oxidepm start with a config file"
```

An app that waits for its dependencies shows as `waiting`, and the start returns at once. `api` has a health check, so it stays `starting` until its first probe passes.

## Look at it

```term cap="status-starting" label="Terminal output of oxidepm status while apps are starting"
```

The columns are `id`, `name`, `mode` (the runtime), `pid`, `↺` (restarts), `status`, `cpu`, `mem` and `uptime`. `online` is the status the table shows for an app that is running; `--json` calls it `running`. [All statuses](/docs/configuration/restarts/).

`oxidepm status --more` adds the port, the working directory and the policy markers. `oxidepm show <name>` prints one app in detail. `oxidepm status --json` prints the table as JSON.

## Read its logs

```sh
oxidepm logs api            # the last 15 lines
oxidepm logs api -f         # follow
oxidepm logs api --lines 100 --grep "error"
```

`--out` shows only stdout and `--err` only stderr. [More on logs](/docs/commands/logs/).

## Stop it

```sh
oxidepm stop api
oxidepm restart api
oxidepm delete api          # stop and remove it from the registry
oxidepm kill                # stop the daemon and every app
```

A selector is a name, an id, `all`, or `@tag`. A stopped app stays stopped and is not restarted by the daemon. `reload` is the same as `restart`: there is no zero-downtime reload.
