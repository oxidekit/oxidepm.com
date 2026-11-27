## In short

PM2 and OxidePM do the same everyday job: they start your apps, restart them when they crash, keep their logs, show a status table and bring the apps back after a reboot. PM2 is written in JavaScript, runs on Node.js and has been used for a long time, especially for Node.js apps. OxidePM is a process manager written in Rust, for Linux, that is young and smaller on purpose, and it adds limits for letting AI agents work with it.

For details about PM2, see the [PM2 documentation](https://pm2.keymetrics.io/docs/usage/quick-start/).

## What each is for

- **PM2** is a process manager for Node.js, and it also runs scripts in other languages. It is a good fit when your stack is Node.js and you want clustering, zero-downtime reloads and a large ecosystem around it.
- **OxidePM** is a process manager for Linux servers whatever the app is written in. It is a good fit when you want one small native daemon that supervises processes, strict config checking, scripting output, and limits on what an AI agent may do to your processes.

## Where PM2 is the better choice

- **Zero-downtime reload for Node.js.** PM2's cluster mode can reload workers one after another so that the app keeps answering. OxidePM has no zero-downtime reload: `reload` is the same as `restart`.
- **Built-in file watching.** PM2 can restart an app when its files change. OxidePM provides file watching through the [`watch` adapter](/docs/commands/other-commands/#file-watching) on Linux.
- **Windows.** PM2 runs on Windows. OxidePM does not support Windows.
- **Age and community.** PM2 has been in use for years. OxidePM is new.
- **Deploy and hosted monitoring.** PM2 has its own deploy tooling and an optional hosted monitoring service. OxidePM provides SSH deployments through the [`deploy` adapter](/docs/commands/other-commands/#deploy-and-diff).
- **One shared port for a Node.js cluster.** PM2 cluster mode lets Node.js workers share one port. OxidePM clusters give instance `i` the port `port + i`, so you put a reverse proxy or load balancer in front.

## Where OxidePM is the better choice

- **A native manager with no JavaScript runtime.** The OxidePM daemon and CLI are Rust programs. Running them does not need Node.js on the machine. You install the runtimes your apps need, and nothing else.
- **Limits for AI agents.** The daemon decides who is asking from the connection a request arrives on. An agent on the agent socket may read everything, may only stop or restart apps you opened to it, and can never start, delete or flush. Apps can be marked `protected`, and what agents ask for is written to an audit log. See [Safe use with AI agents](/docs/ai-safety/safe-use/).
- **Rehearsals.** Most commands that change something take `--dry-run`, which answers with a plan and changes nothing.
- **Strict configuration.** A config file with an unknown key, a bad cron expression or a dependency cycle is refused as a whole, with the line of the problem, before anything starts.
- **A crash-loop breaker and a dependency wait that fails closed.** An app that restarts too often ends as `errored` until a person starts it, and an app that waits for `depends_on` fails if its dependencies never come up.
- **A small core and checked adapters.** Notifications, metrics, the web API, the dashboard and the language runtimes are adapters: separate programs that are hash-checked, show what they ask for before you enable them and, on Linux, run under Landlock and seccomp.
- **Machine-readable output.** `--json` on commands and stable `E_` error codes.

## The real differences

| | PM2 | OxidePM |
|---|---|---|
| Written in | JavaScript, runs on Node.js | Rust, native programs |
| Platforms | Linux, macOS and Windows | Linux (x86_64 and aarch64, glibc) |
| Languages of the apps | Node.js first, other interpreters by script | Any program with `cmd`. Node.js, Python, Go and Rust through runtime adapters that a release carries |
| Reload | Zero-downtime reload for cluster mode | `reload` is a restart |
| Cluster | Node.js workers can share one port | Up to 256 instances, a port each |
| Watch mode | Built in | `watch` adapter |
| Config file | A JavaScript ecosystem file, or JSON | TOML, YAML or JSON, checked strictly |
| Restart policy | Restart on crash, with options | `on-crash`, `always` or `never`, backoff that doubles up to a cap, and a crash-loop breaker |
| Health checks | None built in. An app can signal readiness during a reload | HTTP, TCP or a script, with a choice of action |
| Start order | No dependency option: start order is up to you | `depends_on`, which waits and fails closed |
| Boot | `pm2 startup` and `pm2 save` | `oxidepm startup`, `save` and `resurrect` |
| Dashboard | `pm2 monit` | `oxidepm top` in the core, and `oxidepm monit` from the `ui-tui` adapter |
| Notifications and metrics | Modules and a hosted service | The notifier and Prometheus exporter adapters |
| AI agent limits | None that are built for it | Agent socket, tiers, protected apps and an audit log |
| Licence | AGPL-3.0 | MIT or Apache-2.0 |

## Moving from PM2

The commands map closely.

| PM2 | OxidePM |
|---|---|
| `pm2 start app.js` | `oxidepm start app.js` |
| `pm2 start ecosystem.config.js` | `oxidepm start oxidepm.config.toml` |
| `pm2 list` | `oxidepm status` |
| `pm2 logs api` | `oxidepm logs api -f` |
| `pm2 restart api` | `oxidepm restart api` |
| `pm2 reload api` | `oxidepm reload api`, which is a restart |
| `pm2 stop api`, `pm2 delete api` | `oxidepm stop api`, `oxidepm delete api` |
| `pm2 save`, `pm2 resurrect` | `oxidepm save`, `oxidepm resurrect` |
| `pm2 startup` | `oxidepm startup systemd` |
| `pm2 monit` | `oxidepm monit` (needs the `ui-tui` adapter) |

A PM2 ecosystem file is JavaScript, and OxidePM does not read it. Write the same apps as a [config file](/docs/configuration/config-file/) in TOML, YAML or JSON. Apps that run on Node.js need the `runtime-node` adapter, which a release carries. [Install](/docs/getting-started/install/#runtimes) shows how it is enabled.

## Using both

Nothing stops you from running both on one machine for different apps. Keep each app under one manager only.

Next: [OxidePM and systemd](/docs/compare/oxidepm-and-systemd/).
