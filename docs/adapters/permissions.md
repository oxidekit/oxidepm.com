# Permissions

What a manifest can ask for, and what the daemon enforces itself.

Source: https://oxidepm.com/docs/adapters/permissions/

An adapter declares what it needs in the `permissions` object of its manifest. Some of it the daemon enforces itself, some the operating system enforces, and some is only what you consent to.

## The fields

- `host` (object): `level` is `read`, `lifecycle` or `admin`. `scope` is `all` or `opted-in`. Optionally `max_in_flight`, up to 128.
- `events` (list, default: none): The event families a service receives: `lifecycle` and `adapter`. A tool receives no events.
- `env_pass` (list, default: none): Names of environment variables the adapter receives from the daemon's environment. Nothing else is passed.
- `network` (object): `mode` is `none` or `outbound`. `hosts` lists the hosts it says it uses, and `listen` the addresses it listens on.
- `fs` (object): `read` and `write` are lists of paths. `$STATE` is the adapter's own state directory. `any` means any path.
- `spawn` (object): `mode` is `none`, `named` (with `names`) or `any`.
- `memory_mb` (number, default: 128): A memory ceiling, at most 512.
- `requires_enforcement` (list, default: none): Things the OS must enforce, or the adapter is not enabled: `network`, `fs_write`, `fs_read`, `spawn`.

## What the host level allows

`read` makes safe requests: `status`, `show`, `describe`, `logs` and the daemon's status. `lifecycle` also stops, restarts and reloads apps. `admin` also starts apps and makes the dangerous and global requests: `delete`, `flush`, `save`, `resurrect`. Always only on apps that are not protected, and, with scope `opted-in`, only on apps that list the adapter under `adapters`. `kill`, changing policy markers and revealing environment values are a person's, whatever the grant.

## Who enforces what

| Layer | What it enforces |
|---|---|
| The daemon | The host level and scope, the markers, the audit log, the rate limits, the size and rate limits of the protocol, what is in an event, and the scrubbing of an app's secrets from logs. All of it holds whether or not the adapter cooperates. |
| The operating system | Which files it can read and write, which programs it can start, and its system calls. On Linux, through Landlock and seccomp. See [The sandbox](https://oxidepm.com/docs/adapters/sandbox/). |
| You | What you accepted on the consent screen. The list of hosts an adapter says it connects to is shown, but it is not enforced per host. Local Unix sockets (a session bus, an ssh agent) may also stay reachable; see [The sandbox](https://oxidepm.com/docs/adapters/sandbox/). |

## What an update may change

An update that asks for more than the installed version, in any field, shows what grew (`[GROWS]` in the list and a `Grows` section) and needs a new acceptance. Asking for less never needs one.

## Environment values in events

An event never carries an app's command, arguments, working directory, environment, hooks or log lines. `logs` that an adapter reads through the host API are scrubbed of the app's environment values (those of 6 or more characters, by exact match) and bounded at 10 000 lines and 1 MiB.
