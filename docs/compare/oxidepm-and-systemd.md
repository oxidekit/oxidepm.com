# OxidePM and systemd

Where systemd is enough, where a process manager is easier, and how the two work together.

Source: https://oxidepm.com/docs/compare/oxidepm-and-systemd/

## In short

systemd is the init system and service manager of most Linux distributions. OxidePM is a process manager written in Rust for the apps you run on a server. They are not rivals so much as two layers: `oxidepm startup systemd` writes a systemd unit so that the OxidePM daemon starts at boot, and the daemon then supervises your apps.

systemd alone is often enough to supervise apps. A dedicated process manager can make app operations more convenient.

## What each is for

- **systemd** starts the machine and the services that belong to it: the database, the web server, the system's own daemons. It orders them, isolates them, limits their resources and logs them. It is on almost every Linux server already, and a unit file for your own app is a normal way to run it.
- **OxidePM** supervises the applications of a user or a team, started and stopped from a command line without root, described in one config file, with a status table, and with limits for AI agents.

## Where systemd is the better choice

- **It is already there.** There is no second daemon to install, update or monitor.
- **System services and boot order.** `After=`, `Requires=` and targets order services across the whole machine, including mounts, networks and sockets. OxidePM's `depends_on` orders only the apps that OxidePM supervises.
- **Isolation and resource control.** Each service runs in its own control group. Memory and CPU limits (`MemoryMax=`, `CPUQuota=`), filesystem and privilege hardening (`ProtectSystem=`, `NoNewPrivileges=` and more) and killing every process of a service are systemd features. OxidePM signals the app's process group, and a child that starts its own session or detaches itself is not in it.
- **Socket activation and timers.** Starting a service on the first connection, and scheduled jobs, belong to systemd.
- **Logs.** journald collects the output of every service, with the same tools for all of them.
- **Restarts and rate limits.** `Restart=`, `RestartSec=` and `StartLimitBurst=` cover a crash and a crash loop, and the watchdog can restart a service that stops answering.

## Where OxidePM is the better choice

- **No root, and one command per app.** `oxidepm start app.js` runs as your user, and you do not write a unit file for every app or reload systemd after each change.
- **A status table and a config file for a group of apps.** `oxidepm status` shows every app with its state, restarts, CPU, memory and uptime, and one TOML, YAML or JSON file describes the group.
- **Health checks that act.** An app can be probed over HTTP, over TCP or with a script, and the daemon can restart it when the probe fails. systemd has no HTTP probe of its own.
- **Backoff, a breaker and a dependency wait that fails closed.** Restart delays that double up to a cap, an app that ends as `errored` instead of looping, and `depends_on` that fails if the dependency never comes up.
- **Limits for AI agents.** An agent on the agent socket is held to what you allow, `protected` apps cannot be changed by it, and the audit log records what it asked for. See [Safe use with AI agents](https://oxidepm.com/docs/ai-safety/safe-use/).
- **Rehearsals and JSON.** `--dry-run` on most commands that change something, and `--json` for scripts.

## The real differences

| | systemd | OxidePM |
|---|---|---|
| What it is | Init system and service manager, process 1 | A daemon you start per user, which supervises apps |
| Needs root | For system services. User units exist as well | No |
| How an app is described | A unit file | A config file, or flags to `oxidepm start` |
| Stopping an app | Kills every process in the service's control group | Signals the app's process group |
| Resource limits | Control groups, for memory, CPU and more | Memory and uptime limits that restart the app |
| Logs | journald | Per-app files, rotated by size (10 MB and 5 files by default) |
| Ordering | Across the whole system | Between the apps OxidePM supervises |
| Health checks | A watchdog the service must feed | HTTP, TCP or script probes |
| Boot | It is the boot | `oxidepm startup systemd` writes a unit for the daemon, and `resurrect` restores the apps |
| AI agent limits | None that are built for it | Agent socket, tiers, protected apps and an audit log |

## Using them together

The usual setup is both. systemd starts `oxidepmd` at boot through the unit that `oxidepm startup systemd` generates, so that the daemon comes back after a reboot, and OxidePM keeps the apps running. Keep the database and the system's own services as systemd units, and the apps you deploy and restart often under OxidePM. Keep each app under one manager only. See [Survive a reboot](https://oxidepm.com/docs/getting-started/reboot/).

Next: [OxidePM and PM2](https://oxidepm.com/docs/compare/oxidepm-and-pm2/).
