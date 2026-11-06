# The sandbox

Landlock and seccomp: what they limit, where they apply and where they stop.

Source: https://oxidepm.com/docs/adapters/sandbox/

## What runs

An adapter is started through a small launcher, `oxidepm-sandbox`, that sits next to `oxidepmd`. The launcher limits itself and then runs the adapter. It uses two Linux mechanisms:

- **Landlock** limits the files the adapter can read and write, and the programs it can start, to what its manifest lists.
- **seccomp** limits the system calls it can make, which is how network use is limited.

`oxidepm status --daemon` shows what this machine can do.

*Terminal output of oxidepm status --daemon*

```text
$ oxidepm status --daemon
audit log:    ok
agent socket: bound
sandbox:      landlock abi 10 (restricts unix connect), seccomp, ptrace_scope 1 (launcher installed)
```

Here Landlock is at ABI 10 (which also restricts connecting to Unix sockets), seccomp is available, `ptrace_scope` is 1 and the launcher is installed. The import and enable screens say, line by line, what is enforced on this machine.

## When it cannot be set up

If the sandbox cannot be set up the way the grant says, the adapter is not started. If the kernel has no Landlock or no seccomp, or the launcher is not installed, the consent screen says `no (this kernel has no Landlock)` or `no (the sandbox launcher is not installed)` for that part. An adapter that requires enforcement is then not enabled, unless you accept that with `--allow-unenforced`.

## What it does and does not do

It limits the damage a buggy adapter can do: it keeps it out of the rest of the file system, and from starting programs it did not declare. It does not fully contain a hostile adapter. In particular:

- Network access is not enforced per host. The manifest names the hosts, and the consent screen says `Not enforceable per host`.
- It does not take back what you approved.
- Local Unix sockets may stay reachable: the session bus, an ssh agent or the display server. `adapter info` prints `AF_UNIX services reachable:` with the ones its self-test could connect to. On a kernel with Landlock ABI 10, which `status --daemon` shows as `restricts unix connect`, this can be closed.
- It is Linux only. Adapters are started only on Linux; on macOS there are no adapters and no sandbox, because Landlock and seccomp are Linux features.

That is why an adapter is also checked against a hash, why you see what it asks for first, and why the daemon enforces the host level on its own. Only install adapters you trust.
