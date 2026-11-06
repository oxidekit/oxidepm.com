The notifier is a service adapter. It listens to the lifecycle events of the daemon and sends them to Telegram, Discord, Slack and a signed HTTP webhook. It has read access only and never touches your apps. It also adds the `oxidepm notify` command.

## Install it

The archive is not published yet. `--allow-reserved-name` is needed because the core reserves the name `notifier`.


```sh
oxidepm adapter import notifier.tar.gz --sha256 <hex> --allow-reserved-name
oxidepm adapter enable notifier
```

See [Import and enable](/docs/adapters/import-and-enable/). The manifest asks for read access to status and lifecycle events, outbound network (it names `api.telegram.org`, `discord.com` and `hooks.slack.com`), write access only to its own state directory, and the environment variable `OXIDEPM_TELEGRAM_TOKEN`.

## Events

| Event | Severity | When |
|---|---|---|
| `start` | info | An app was started. |
| `stop` | info | An app was stopped. |
| `restart` | warning | An app was restarted: after a crash, by a limit, by cron or by hand. |
| `memory_limit` | warning | An app went over its memory limit and is being restarted. |
| `crash` | critical | An app crashed or ended `errored`. The message has the exit code, the signal or the error text. |
| `crash_loop` | critical | An app crashes again and again and is no longer restarted. |
| `health_check` | critical | A health check failed. |

Messages contain app names, ids, error text and health-check endpoints. Consider that before routing alerts to a shared channel.

## Configure it

The configuration is `config.toml` in the adapter's own state directory. `oxidepm notify status` prints the path. It is not in the home directory, and `oxidepm backup` does not include it because it holds tokens.

```toml title="config.toml"
events = ["crash", "restart"]   # empty or absent: every event
min_severity = "warning"        # info | warning | critical
timeout_secs = 10               # per request, 1 to 60

[telegram]
bot_token_env = "OXIDEPM_TELEGRAM_TOKEN"   # read from the daemon's environment; or bot_token = "..."
chat_id = "-100123456789"

[discord]
webhook_url = "https://discord.com/api/webhooks/..."

[slack]
webhook_url = "https://hooks.slack.com/services/..."

[webhook]
url = "https://example.org/alerts"
secret = "..."   # signs every request
```

A webhook request carries `X-OxidePM-Timestamp` and `X-OxidePM-Signature: v1=<HMAC-SHA256 of "<timestamp>.<body>" with the secret>`. A file that does not parse is an error that `notify status` shows. It is never replaced, and nothing is sent until it is fixed. The file is read again when it changes.

## The notify command

```sh
oxidepm notify telegram --chat YOUR_CHAT_ID    # the token comes from OXIDEPM_TELEGRAM_TOKEN or bot_token, never the command line
oxidepm notify events --set crash,restart,health_check
oxidepm notify severity warning
oxidepm notify test       # sends to every channel whatever the filters say; exits non-zero if one fails
oxidepm notify status
oxidepm notify remove CHANNEL
```

```term cap="notify-status" label="Terminal output of oxidepm notify status"
```

`notify` is a caution-tier command, so an AI actor cannot run it at all, and it is audited. Without the adapter, `oxidepm notify` exits with code 2 and prints `'notify' is provided by the adapter 'notifier', which is not installed.` and the command that imports it.
