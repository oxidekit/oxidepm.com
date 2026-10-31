::: note Release status
These docs describe the code on the development branch of OxidePM, which is ahead of the latest published release (0.3.2). That release has no adapters, no agent socket, no audit log and no policy markers. Until a release includes them, build from source to try what these pages describe.
:::

## Requirements

- Linux (the main platform) or macOS. macOS: works, without the OS sandbox. Windows is not supported.
- Rust 1.75 or newer, only to build from source.
- The runtimes of the apps you want to run, and only those: Node.js for Node, npm, pnpm and yarn apps, Python 3 for Python apps, Go 1.21 or newer for Go apps.

## The install script

```sh title="Install"
curl -fsSL https://oxidepm.com/install.sh | sh
```

The script is [install.sh](/install.sh); read it before you run it. This is everything it does:

1. Works out your platform from `uname`: Linux on x86_64 or aarch64, macOS on x86_64 or arm64. Anything else stops with an error.
2. Asks the GitHub API (`api.github.com/repos/oxidekit/oxidepm/releases/latest`) for the tag of the latest release.
3. Downloads `oxidepm-<target>.tar.gz` and `checksums.txt` from that release on `github.com`.
4. Checks that the archive's SHA-256 is the one `checksums.txt` lists for that exact file name. This shows the file arrived whole and is the one the release lists. It is not a signature check, and there is no release signing key yet.
5. Unpacks the archive in a temporary directory and moves `oxidepm`, `oxidepmd` and, if the archive has it, `oxidepm-sandbox` into `/usr/local/bin`, using `sudo` when that directory is not writable. Set `INSTALL_DIR` to install somewhere else.
6. Runs `oxidepm --version`.

It makes no other request and installs nothing else.

## Other ways

The [Releases page](https://github.com/oxidekit/oxidepm/releases) has the archives and Debian packages:

| Platform | Architecture | Archive |
|---|---|---|
| Linux | x86_64 | `oxidepm-x86_64-unknown-linux-gnu.tar.gz` |
| Linux | ARM64 | `oxidepm-aarch64-unknown-linux-gnu.tar.gz` |
| macOS | Intel | `oxidepm-x86_64-apple-darwin.tar.gz` |
| macOS | Apple Silicon | `oxidepm-aarch64-apple-darwin.tar.gz` |

The repository README also lists a Homebrew tap (`brew tap oxidekit/homebrew-tap`, then `brew install oxidepm`) and an Arch Linux package description in `dist/aur`.

## From source

```sh title="Build"
git clone https://github.com/oxidekit/oxidepm
cd oxidepm
cargo build --workspace --release
```

The binaries are in `target/release`. Put `oxidepm`, `oxidepmd` and `oxidepm-sandbox` in one directory on your `PATH`. The CLI starts the daemon from the directory it is in, and looks for the sandbox launcher next to itself.

## Check it

```sh
oxidepm --version
oxidepm status
```

Before anything is started, `status` answers that the daemon is not running. The daemon starts the first time you `start` an app.
