Events go to a running `service` that listed the family in its manifest and was granted it. There are two families.

## lifecycle

Something happened to an app. `seq` is the daemon-wide sequence number of the event.

`kind` is one of `started`, `restarted`, `stopped`, `crashed`, `errored`, `unhealthy`, `recovered`, `backoff`, `crash_loop`, `cron_fired`, `memory_limit` and `uptime_limit`.

`app` is `{id, name, tags}`. `data` holds only these keys, and only those the event has: `cause`, `actor`, `pid`, `exit_code`, `exit_signal`, `restarts`, `memory_mb`, `limit_mb` and `reason`. `reason` is a sentence made by the daemon with the app's environment values removed and cut at 1024 characters.

`options` is the app's `adapters.<adapter name>` table for this adapter only, at most 4 KiB. No other adapter's options are ever sent.

The event never carries the app's command, arguments, working directory, environment, hooks or log lines.

```term wrap="yes" label="An event"
{hi:daemon:} {"jsonrpc":"2.0","method":"event","params":{"seq":17,"kind":"crashed","family":"lifecycle","at":"2026-11-20T10:00:00Z","app":{"id":3,"name":"web","tags":["prod"]},"data":{"exit_code":1,"restarts":2},"options":{"chat":"ops"},"dropped_before":4}}
```

## adapter

Something happened to an adapter: `started`, `exited`, `killed` or `failed`. It has no `app`, has its own `seq` counter, and `data` holds `adapter`, `version` and, for `failed`, `reason` (a short name). An adapter is not told about itself.

## Delivery

Delivery is best effort and never slows the daemon. Each service has a queue of 1024 events plus 256 critical ones (`crashed`, `errored`, `unhealthy`, `crash_loop` and `memory_limit`; `killed` and `failed` for the adapter family), at most 4 MiB. When it is full, the oldest normal event is dropped, or the oldest critical one when the critical part is full.

A service that is not running does not queue: its events are dropped. The drops are counted, and the next event delivered carries `dropped_before: n`. A gap in `seq` shows where. Events queued when the process ended are dropped, not sent to the next process. When the adapter is stopped on request, queued events are written, for up to a second, before `shutdown`.

An event line is at most 16 KiB. If one would be longer, the daemon removes `options`, then `reason`, then the tags. If it still does not fit, it is dropped and counted.
