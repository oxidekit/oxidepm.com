# Permission tiers

Safe, caution and dangerous requests, and what an AI actor may ask for.

Source: https://oxidepm.com/docs/ai-safety/permission-tiers/

Every request has a tier. A person (class `human`, any label) may make every request. An `ai` actor, whether it declared itself or came in on `agent.sock`, is held to the tier.

| Tier | Requests | An `ai` actor |
|---|---|---|
| safe | `status`, `show`, `describe`, `logs`, `ping`, `hello` | Yes, on every app, protected ones too. |
| caution | `stop`, `restart`, `reload` | Only on an app marked `ai_control` and not `protected`. |
| dangerous | `start` (and a config file: a spec is arbitrary code), `delete`, `flush`, `kill`, `save`, `resurrect`, `show --reveal` | Never. |

## Rules for caution requests

- An `ai` actor must name its apps: a name or an id, at most 10. `all` and `@tag` are refused for `stop`, `restart` and `reload`.
- The check is all or nothing. If one app of the request (an instance of a cluster counts) is not open to the actor, nothing runs, and the error names the apps that are not.
- The apps that passed the check are the ones acted on. An app that gains a tag or is created while the request is being checked is not touched.
- `restart` also starts an app that is at rest. That is how an AI brings back what it may control.

*Terminal output of an agent's requests*

```text
agent$ oxidepm stop web --dry-run
ℹ Dry run of 'stop': this is what would happen. Nothing was changed.
  stop  web [step 0]  status running

agent$ oxidepm restart db
✗ ai:assistant may not restart protected app(s): db. A protected app is read-only for anything but a person
Error: ai:assistant may not restart protected app(s): db. A protected app is read-only for anything but a person

agent$ oxidepm delete api
✗ ai:assistant may not make the request 'delete': it is a dangerous request. Ask a person to run it
Error: ai:assistant may not make the request 'delete': it is a dangerous request. Ask a person to run it
```

The CLI prints the message. The code (`E_PROTECTED`, `E_POLICY_DENIED`) is in the [audit log](https://oxidepm.com/docs/ai-safety/audit-log/).

## Rate limits

An `ai` actor can restart or reload the same app once every 10 seconds and five times in ten minutes (`E_RATE_LIMITED`), so a looping agent cannot keep an app down. More generally, a non-human actor is limited to 50 requests a second (a burst of 100), and requests that change something, or are refused for being dangerous, to 5 a minute (a burst of 10). An `ai` actor's allowance is shared by every `ai` actor on the same socket, so changing the label in the claim does not buy a new one.

## What the markers do not limit

The markers limit requests, not the daemon's own work. A crash restart, a `restart_cron` restart, a limit restart and the boot resurrect treat a protected app like any other.

## Adapters

An adapter is held to its [grant](https://oxidepm.com/docs/adapters/permissions/) on top of this: `read`, `lifecycle` or `admin`. `kill`, changing the markers and revealing environment values are a person's, whatever the grant.
