# Survive a reboot

Save the app list, generate a boot unit and bring the apps back.

Source: https://oxidepm.com/docs/getting-started/reboot/

## Save the list

```sh
oxidepm save
```

`save` writes `saved.json` in the data directory (`~/.oxidepm`, or the directory `OXIDEPM_HOME` names) from the apps that should be running. It refuses to replace a file that lists apps with an empty list, unless you pass `--force`. The file is written atomically with mode 0600.

## Bring the apps back

```sh
oxidepm resurrect
```

`resurrect` starts every app that should be running and is not up, and adds apps from `saved.json` that were deleted since. An app you stopped stays stopped. Apps are started in dependency order, and at most four build and spawn at once (the `launch_concurrency` setting), so a reboot does not run twenty builds together.

## Start the daemon at boot

```sh
oxidepm startup systemd     # or: launchd
```

This generates an autostart script for your init system. `oxidepm --dry-run startup` shows what would be written and writes nothing. The generated systemd unit has this shape (your user and paths will differ):

*oxidepmd.service*

```ini
[Unit]
Description=OxidePM Process Manager
After=network.target

[Service]
Type=simple
User=deploy
ExecStart="/usr/local/bin/oxidepmd"
Restart=on-failure
RestartSec=10
TimeoutStopSec=160
KillMode=mixed
Environment="HOME=/home/deploy"

[Install]
WantedBy=multi-user.target
```

`TimeoutStopSec` is the daemon's shutdown budget (`shutdown_budget_secs`, 120 seconds by default) plus 40 seconds, and `KillMode=mixed` makes systemd send the stop signal to the daemon alone and leave it time to stop the apps in order. Run `startup` again after you change the budget, to get the new value.

The daemon starts the apps that should be running when it starts at boot. On Linux, `pids.json` in the data directory lists the live app processes: if the daemon dies by SIGKILL, the next daemon kills what is still listed there before it starts anything. On macOS that recovery is not available, and the daemon logs a warning instead.
