`--dry-run` previews an operation. It is a global flag, and most commands that change something accept it.

```term cap="stop-all-dry" label="Terminal output of oxidepm stop all --dry-run"
```

## Which commands

- **The daemon answers with a plan:** `start`, `stop`, `restart`, `reload`, `delete`, `flush`, `save`, `resurrect`, `kill` and `policy set`, and `adapter enable`, `disable` and `remove`. The daemon runs the policy exactly as for the real request, records the rehearsal in the audit log (the lines say `"dry_run": true`), and answers with the apps it would reach, the step each happens in (stop and kill go dependents first), and for a refusal the error code.
- **The command rehearses itself:** `startup`, `update`, `backup` and `restore`, and `adapter import` and `adapter update`. A rehearsal never starts a daemon.
- **Adapters with previews:** `init`, `git-start`, `deploy` and `diff` preview through a running daemon after their adapters are enabled. For example, `oxidepm --dry-run init ./my-project` prints the configuration it would write.
- **Reads:** a command that only reads ignores the flag.
- **Unsupported:** `start --check`, `env set` and `env unset` refuse the flag. The `check`, `web`, `notify` and `monit` adapter commands have no dry run. Use plain `oxidepm check` to report findings without changing the project.

## What a plan is

A daemon plan uses the registry and files to report the intended operations. A rehearsed restart leaves an AI actor's restart allowance intact. Use `--json` for machine-readable output.

A request that the policy refuses is answered with the refusal as the plan (`E_POLICY_DENIED`, `E_PROTECTED`, `E_RATE_LIMITED`). A request that is invalid for a reason the daemon can see without side effects (a bad spec, a missing dependency, an unusable saved file) is answered with the real error.

`update --dry-run` downloads the archive into a private temporary directory, checks it against `checksums.txt`, unpacks it there, shows what it would replace and deletes the directory.

## For agents

An AI actor can use a rehearsal to see what a stop or restart would reach before it asks for it. A rehearsal gives it nothing a `status` does not, and a `start`, `delete`, `save` and the other dangerous requests are refused for it as plans, like the real ones.
