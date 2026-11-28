# The sandbox

Landlock and seccomp: what they limit, where they apply and where they stop.

Source: https://oxidepm.com/docs/adapters/sandbox/

## What runs

`oxidepm-sandbox` sits next to `oxidepmd` and sets restrictions before launching an adapter. It uses Landlock and seccomp where the kernel supports them:

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

## What is enforced on each kernel

Before running an adapter, `oxidepm-sandbox` always applies a baseline set of process limits: it closes inherited file descriptors above the executable descriptor, sets `PR_SET_NO_NEW_PRIVS`, applies resource limits (`RLIMIT_NOFILE`, `RLIMIT_FSIZE`, `RLIMIT_CORE = 0`, and `RLIMIT_DATA` from `memory_mb`), lowers priority (`nice`), and sets `oom_score_adj` so the kernel kills an adapter before an app.

On top of that baseline, Landlock and seccomp enforce as much of the adapter's grant as the running kernel supports. Rights a kernel does not support are dropped from the Landlock ruleset; the self-test then measures what actually held.

| Kernel feature | Linux kernel | What OxidePM enforces with it |
| --- | --- | --- |
| No Landlock | — | No filesystem, program execution, TCP bind, or Unix-socket scoping rules. |
| Landlock ABI 1 | 5.13+ | File read, write, create, and remove rules (`fs.read`, `fs.write`), and execution allowlisting (`spawn = none` or `named`). |
| Landlock ABI 2–3 | 5.19+ / 6.2+ | Cross-directory link and rename rules (ABI 2) and file truncation rules (ABI 3). |
| Landlock ABI 4 | 6.7+ | TCP bind port rules (`network.listen`). Outbound TCP connections are not filtered per host. |
| Landlock ABI 5 | 6.10+ | Device `ioctl` restrictions. |
| Landlock ABI 6 | 6.12+ | Abstract Unix socket scoping and signal scoping: blocks connecting to abstract `AF_UNIX` sockets or signalling processes outside the sandbox. |
| Landlock ABI 9+ | 7.1+ | Pathname Unix socket connect rules: blocks connecting to pathname `AF_UNIX` sockets (such as the daemon socket, session bus, ssh-agent, or display server) unless explicitly allowed through `connect_env_socket`. |

### seccomp

The seccomp filter runs on `x86_64` and `aarch64` Linux (and rejects non-native syscall ABIs and x32 syscalls on `x86_64`).

- **Always denied** (with `EPERM`): `ptrace`, `process_vm_readv`, `process_vm_writev`, `pidfd_getfd`, `kcmp`, `io_uring_setup`/`enter`/`register`, mount and filesystem-context calls, `kexec_load`/`kexec_file_load`, `bpf`, `perf_event_open`, `userfaultfd`, keyring calls, `unshare`, `setns`, `chroot`, `pivot_root`, `reboot`, and kernel module calls.
- `network = none`: blocks `socket(2)` for every address family other than `AF_UNIX`.
- `spawn = none`: blocks `fork` and `vfork` (on `x86_64`), returns `ENOSYS` for `clone3` so glibc falls back to `clone` for threads, and blocks `clone` calls that do not set `CLONE_THREAD`.

## When a level is missing

When you run `oxidepm adapter enable`, the daemon runs `oxidepm-sandbox selftest` under the adapter's exact profile and saves the measured result as the adapter's enforcement record.

- **What the enforcement record says**: It stores the items the self-test observed as refused (`network`, `fs_read`, `fs_write`, `spawn`), the `AF_UNIX` services the self-test could still connect to (`daemon_socket`, `session_bus`, `abstract_socket`, `pathname_socket`), the probed kernel capabilities, and whether `--allow-unenforced` was accepted. `network` counts as enforced when `AF_INET` sockets are refused and `io_uring_setup` is not allowed; if the adapter requires `network` enforcement, `network` is removed from `enforced` whenever the kernel is below Landlock ABI 9 or any probed `AF_UNIX` service is reachable. Without the `oxidepm-sandbox` launcher, `enforced` is empty. `oxidepm adapter info <name>` shows this record.
- **When enable refuses**: If the manifest lists items in `requires_enforcement` that the self-test did not enforce — including `network` on a kernel below Landlock ABI 9 or where an `AF_UNIX` service remained reachable — `adapter enable` refuses unless you pass `--allow-unenforced`. On every launch, `oxidepm-sandbox` also refuses to start the adapter if Landlock or seccomp cannot enforce a required item and `--allow-unenforced` was not accepted.
- **Automatic consent vs explicit consent**: `--yes` is only honoured for adapters with limited permissions (read-only host access, `network = none`, `spawn = none`, no `env_pass` or `connect_env_socket`, writes limited to `$STATE`, and reads limited to `$STATE` and a regular `/etc/hosts`). Broader permissions require interactive confirmation or `--accept <fingerprint>`, and `admin` host access always requires an interactive terminal. Official adapters (bundled with the release or signed by an official key) can still use `--yes` when they provide runtimes or programs, or when `AF_UNIX` services remain reachable on a kernel below Landlock ABI 9 (provided `requires_enforcement` is met). Self-built and third-party adapters cannot use `--yes` if they provide runtimes or programs or if any `AF_UNIX` service is reachable; they require `--accept <fingerprint>`.
- **Accepting missing enforcement**: Passing `--allow-unenforced` tells `adapter enable` to accept missing `requires_enforcement` items, records `allow_unenforced` on the adapter, and tells `oxidepm-sandbox` to log a warning and continue instead of refusing to start when Landlock or seccomp fails or cannot enforce a required rule. It does not disable the baseline limits or skip consent, and `oxidepm adapter list` and `oxidepm adapter info` mark any adapter enabled with `--allow-unenforced`.

If the kernel has no Landlock or no seccomp, or the launcher is not installed, the consent screen says `no (this kernel has no Landlock)`, `no (this kernel has no seccomp)`, or `no (the sandbox launcher is not installed)` for that part.

## What it does and does not do

Adapters run as the same Linux user as `oxidepmd` and your apps. The sandbox is a policy layer to limit mistakes and reduce blast radius, not a hard isolation wall against hostile code running under the same user account.

It keeps a buggy adapter out of the rest of the file system and stops it from starting programs it did not declare. It does not fully contain a hostile adapter. In particular:

- Network access is not enforced per host. The manifest names the hosts, and the consent screen says `Not enforceable per host`.
- It does not take back what you approved.
- Local Unix sockets may stay reachable below Landlock ABI 9: the session bus, an ssh agent, or the display server. `adapter info` prints `AF_UNIX services reachable:` with the ones its self-test could connect to. On a kernel with Landlock ABI 9 or later, which `status --daemon` shows as `restricts unix connect`, pathname socket connections are blocked unless granted.
- Same-user boundaries still depend on host settings such as Yama `ptrace_scope` (shown by `oxidepm status --daemon`).

That is why an adapter is also checked against a hash, why you see what it asks for first, and why the daemon enforces the host level on its own. Only install adapters you trust.
