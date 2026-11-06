# Agent connections

How the daemon decides who is asking, and the agent socket.

Source: https://oxidepm.com/docs/ai-safety/agent-connections/

## Who is asking

The daemon decides who is asking from the connection a request arrives on. What a client writes about itself is only a claim, and a claim can make a request stricter, never looser.

| Where the request comes in | Class | Label |
|---|---|---|
| `daemon.sock`, no claim | human | `cli` |
| `daemon.sock`, claim `human:<label>` | human | the label |
| `daemon.sock`, claim `ai:<label>` | ai | the label |
| `daemon.sock`, any other claim (`adapter:*` and `system:*` may never be claimed by a client, and a label must be 1 to 32 characters of `A-Z a-z 0-9 . _ -`) | ai | `invalid-claim` |
| `agent.sock`, whatever the claim | ai | the label of an `ai:<label>` claim, otherwise `agent` |

The CLI sends `OXIDEPM_ACTOR` as its claim:

```sh
OXIDEPM_ACTOR=ai:assistant oxidepm status
```

Set it for every agent you run. `OXIDEPM_SOCKET` names the socket the CLI talks to. Pointing an agent at `agent.sock` gives it class `ai` whatever it claims, so it does not depend on the agent being honest about itself:

```sh
OXIDEPM_SOCKET=~/.oxidepm/agent.sock oxidepm status
```

## The agent socket

`agent.sock` is created in the data directory with mode 0600. `agent_socket = false` in `daemon.toml` turns it off. It is tighter than the main socket:

- lines of at most 1 MiB,
- at most 32 connections at once (the 33rd is closed),
- a connection that is idle for 60 seconds is closed,
- a write the client does not read is abandoned after 10 seconds.

If it cannot be bound (a path that is too long, a file in the way), the daemon starts without it and says so in its log.

## What the daemon records

The daemon writes every request to its log with the actor, the class and the socket. Reads are at debug level. The lifecycle events of an app are credited to the actor of the request that caused them, or to `system:crash`, `system:limit`, `system:cron`, `system:health` and `system:resurrect` when the daemon acted on its own.

## What this gives and what it does not

- It binds an AI that goes through the agent socket or that declares itself. It makes a confused or over-eager agent safe.
- It does not stop a hostile or careless process that runs as the same user and calls `oxidepm` without declaring anything. That process reaches the main socket and is a person as far as the kernel can tell. Code that runs as you is you.
- A class decides what a request may do ([Permission tiers](https://oxidepm.com/docs/ai-safety/permission-tiers/)). A refused request is answered `E_POLICY_DENIED` or `E_PROTECTED`, the message names the actor, the request and the apps, and nothing changes.

To contain an agent that runs in a container, run it as the same user inside the container (for example rootless Podman with `--userns=keep-id`), bind-mount only `agent.sock` into it and set `OXIDEPM_SOCKET` to the mounted path. The container then cannot reach `daemon.sock`.

## An adapter that starts the CLI

A process in an adapter's process tree that opens the daemon's main socket itself, for example the CLI started by the adapter, is handled as that adapter under its grant, whatever it claims. The daemon looks at the peer once, when the connection is accepted. A peer that cannot be looked at then is treated as an AI, not as a person.
