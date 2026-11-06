# Log files

Where an app's output goes, and how the files rotate.

Source: https://oxidepm.com/docs/configuration/log-files/

## Where the logs are

The daemon captures each app's output in its data directory (`~/.oxidepm/logs`, or under `OXIDEPM_HOME`):

```text
logs/
├── api-out.log      # stdout
├── api-err.log      # stderr
└── api-hooks.log    # output of the app's event hooks
```

Every line is timestamped when the daemon writes it. Read them with `oxidepm logs <name>`, [described here](https://oxidepm.com/docs/commands/logs/).

## Rotation

Logs rotate by size, per app. The defaults are 10 MB per file, 5 files, and no compression. Change them in the config file:

*oxidepm.config.toml*

```toml
[[apps]]
name = "api"
mode = "cmd"
script = "./api"
log_max_size = "50mb"
log_max_files = 10
log_compress = true
```

`log_max_size` accepts values such as `"10mb"`, `"500kb"` or a number of bytes, and a bad value is an error when the file is loaded. `log_compress` compresses rotated files with gzip.

## Truncating

`oxidepm flush <selector>` truncates the active log files of an app. Rotated files stay. A file that cannot be emptied is reported for that app. The contents are lost, so read the logs before you flush them: a crashed app's logs are the evidence of why it crashed.
