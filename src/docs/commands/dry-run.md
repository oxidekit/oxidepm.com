`--dry-run` makes a command say what it would do, and change nothing. It is a global flag, and most commands that change something take it. The ones that do not are listed below.

```term cap="stop-all-dry" label="Terminal output of oxidepm stop all --dry-run"
```

## Which commands

- **The daemon answers with a plan:** `start`, `stop`, `restart`, `reload`, `delete`, `flush`, `save`, `resurrect`, `kill` and `policy set`, and `adapter enable`, `disable` and `remove`. The daemon runs the policy exactly as for the real request, records the rehearsal in the audit log (the lines say `"dry_run": true`), and answers with the apps it would reach, the step each happens in (stop and kill go dependents first), and for a refusal the error code.
- **The command rehearses itself:** `startup`, `update`, `backup` and `restore`, and `adapter import` and `adapter update`. A rehearsal never starts a daemon.
- **Reads:** a command that only reads ignores the flag.
- **No rehearsal:** `env set`, and the commands that adapters provide, such as `web`, `init`, `check --fix`, `start --git`, `start --setup` and `notify`, refuse the flag with exit code 2, instead of ignoring it, unless the adapter declares a rehearsal. A command an adapter adds may also be refused with `E_DRY_RUN_UNSUPPORTED`.

## What a plan is

A plan is built from what the daemon already knows and the files. It starts, stops, writes and calls nothing, and a rehearsed restart does not use up an AI actor's restart allowance. With `--json` the output is the plan.

A request that the policy refuses is answered with the refusal as the plan (`E_POLICY_DENIED`, `E_PROTECTED`, `E_RATE_LIMITED`). A request that is invalid for a reason the daemon can see without side effects (a bad spec, a missing dependency, an unusable saved file) is answered with the real error.

`update --dry-run` downloads the archive into a private temporary directory, checks it against `checksums.txt`, unpacks it there, shows what it would replace and deletes the directory.

## For agents

An AI actor can use a rehearsal to see what a stop or restart would reach before it asks for it. A rehearsal gives it nothing a `status` does not, and a `start`, `delete`, `save` and the other dangerous requests are refused for it as plans, like the real ones.
