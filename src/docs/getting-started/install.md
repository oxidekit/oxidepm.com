## Release status

The latest published release is 0.3.2, and the install script below installs it. The other pages of this documentation describe newer code that is not published yet: it is not in a release and not on a public branch. That code adds the agent socket, the audit log, the policy markers (`protected` and `ai_control`), `--dry-run` and the adapters. Release 0.3.2 has none of them: `oxidepm --dry-run status` is refused there, and notifications, the web server, the dashboard and the language runtimes are still built into the core instead of coming from adapters.

There is nothing to build from source yet to try what these pages describe: the repository's default branch builds the 0.3 line, not that code. This section goes away when a release contains it.

## Requirements

- Linux (the main platform). The process manager is also built for macOS on Apple Silicon, but it is not tested there, and adapters, the sandbox and the recovery of apps after the daemon is killed are Linux only. Windows is not supported.
- Rust 1.75 or newer, only to build from source.
- The programs your apps need, and only those: Node.js for Node, npm, pnpm and yarn apps, Python 3 for Python apps, Go 1.21 or newer for Go apps, and `rustc` or `cargo` for Rust apps. OxidePM runs them; it does not install them.
- From the next release on, the language runtimes are adapters that the release carries, and the install script enables them. See [Runtimes](#runtimes).

## The install script

```sh title="Install"
curl -fsSL https://oxidepm.com/install.sh | sh
```

The script is [install.sh](/install.sh); read it before you run it. It installs the latest published release, which is 0.3.2 today. This is everything it does:

1. Works out your platform from `uname`: Linux on x86_64 or aarch64, macOS on arm64 (Apple Silicon). Anything else stops with an error. For an Intel Mac the error says that no build is published.
2. Asks the GitHub releases API of the OxidePM repository for the tag of the latest release.
3. Downloads `oxidepm-<target>.tar.gz` and `checksums.txt` from that release on `github.com`.
4. Checks that the archive's SHA-256 is the one `checksums.txt` lists for that exact file name. This shows the file arrived whole and is the one the release lists. It is not a signature check, and there is no release signing key yet.
5. Unpacks the archive in a temporary directory and moves `oxidepm`, `oxidepmd` and, if the archive has it, `oxidepm-sandbox` into `/usr/local/bin`, using `sudo` when that directory is not writable. Set `INSTALL_DIR` to install somewhere else.
6. Runs `oxidepm --version`.

Apart from the redirects GitHub answers with to its download host, it makes no other request and installs nothing else.

A release that carries adapters (the next one does) has two more steps. The script copies the signed adapter bundle in the archive to `share/oxidepm/adapters`, next to the directory the programs went to, and then runs `oxidepm adapter import --bundled --tag runtime --enable --yes`, which imports and enables the runtime adapters from that bundle without fetching anything. If that import fails, the install stays, and the script prints the command to run again.

## Other ways

The [Releases page](https://github.com/oxidekit/oxidepm/releases) has the archives and Debian packages:

| Platform | Architecture | Archive |
|---|---|---|
| Linux | x86_64 | `oxidepm-x86_64-unknown-linux-gnu.tar.gz` |
| Linux | ARM64 | `oxidepm-aarch64-unknown-linux-gnu.tar.gz` |
| macOS | Apple Silicon | `oxidepm-aarch64-apple-darwin.tar.gz` |

There is no archive for Intel Macs. The repository README also mentions a Homebrew tap and an Arch Linux package description; they have not been checked for this site, so follow the README for them.

## Runtimes

The core runs one runtime by itself, `cmd`, which runs any program. The `node`, `npm`, `pnpm`, `yarn`, `python`, `go`, `rust` and `cargo` runtimes are provided by the adapters `runtime-node`, `runtime-python`, `runtime-go` and `runtime-rust`. A release carries them, signed, under `share/oxidepm/adapters`. The install script, the Debian and RPM packages, the Arch package and the Docker image put them there, and one command imports and enables all four with no network:

```sh
oxidepm adapter import --bundled --tag runtime --enable --yes
```

On a machine where the sandbox of adapters cannot be enforced (macOS at the moment) the command stops and says so; add `--allow-unenforced` if you accept that. Until a runtime is imported, `oxidepm start app.js` fails with the adapter's name and the command that imports it, and creates nothing. See [Provided by adapters](/docs/commands/overview/#runtimes).

## From source

```sh title="Build"
git clone https://github.com/oxidekit/oxidepm
cd oxidepm
cargo build --workspace --release
```

This builds the published 0.3 line, which does not have the features this documentation describes as not yet released. The binaries are in `target/release`. Put `oxidepm` and `oxidepmd` in one directory on your `PATH`: the CLI starts the daemon from the directory it is in. A build that includes the adapter sandbox also has `oxidepm-sandbox`, which the CLI looks for next to itself. A build from source has no runtimes: the adapters of a release come with the release archive, not with the source. Copy the archive's `share/oxidepm/adapters` next to your `bin` directory and run the import command under [Runtimes](#runtimes).

## Check it

```sh
oxidepm --version
oxidepm status
```

Before anything is started, `status` answers that the daemon is not running. The daemon starts the first time you `start` an app.
