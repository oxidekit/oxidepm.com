# Protected apps

The protected and ai_control markers, and how to change them.

Source: https://oxidepm.com/docs/ai-safety/protected-apps/

Two markers belong to an app. Both are off by default.

- `ai_control` (boolean, default: false): AI actors may stop, restart and reload the app. Set with `oxidepm start --ai-control`, or `ai_control = true` in the config file.
- `protected` (boolean, default: false): The app is read-only for every non-human actor, whatever `ai_control` says. Set with `--protected`, or `protected = true`.

A protected app can still be read: `status`, `show`, `describe` and `logs` work for an AI actor. A person is never limited by the markers.

*oxidepm.config.toml*

```toml
[[apps]]
name = "db"
mode = "cmd"
script = "postgres"
protected = true

[[apps]]
name = "web"
mode = "npm"
script = "start"
ai_control = true
```

## Change them while the app runs

*Terminal output of oxidepm policy set*

```text
$ oxidepm policy set web --protected
✓ web: protected=true ai_control=true
```

```sh
oxidepm policy set web --protected
oxidepm policy set web --protected=false --ai-control
oxidepm policy set @backend --ai-control=false
```

`policy set` changes the markers of running apps without a restart. At least one of the two flags is required. It is a dangerous request: only a person can make it. An AI cannot protect, unprotect or open an app. `oxidepm status --more` shows the markers in the `policy` column.

- For a cluster, the cluster and every instance change in one transaction. An instance created later takes the markers of its cluster.
- The markers are kept in the database (`state.db`) and in `saved.json`, so they survive a restart of the daemon, and `delete all` followed by `resurrect` brings an app back with the markers it had.
- A `start` of an app that exists keeps its stored markers, whatever the spec or config file says, so running `oxidepm start <file>` again cannot clear `protected`.

## Dry runs

`oxidepm --dry-run policy set web --protected=false` shows the change and makes none:

*Terminal output of oxidepm policy set with --dry-run*

```text
$ oxidepm policy set web --protected=false --dry-run
ℹ Dry run of 'set_policy': this is what would happen. Nothing was changed.
  set_policy  web  protected true -> false, ai_control true -> true
```

Most requests that change something can be rehearsed this way. See [Dry run](https://oxidepm.com/docs/commands/dry-run/) for the ones that cannot.
