# Install

Install OxidePM with the install script, a package, a prebuilt archive or from source.

Source: https://oxidepm.com/docs/getting-started/install/

## Requirements

- Linux on x86_64 or ARM64, or macOS on Intel or Apple Silicon. macOS supports the built-in `cmd` runtime. The adapter launcher and sandbox are Linux-only in this release.
- Install the programs your apps need, such as Node.js, Python, Go or Rust.
- A Rust toolchain is required to build from source.

## The install script

*Install*

```sh
curl -fsSL https://oxidepm.com/install.sh | sh
```

The [install script](https://oxidepm.com/install.sh) installs the latest published release, 0.4.0-rc.2.

- Detects the platform with `uname`, looks up the latest release on GitHub and downloads its platform archive and `checksums.txt`.
- Checks the archive's SHA-256 against the entry for that exact filename in `checksums.txt`.
- Installs `oxidepm`, `oxidepmd` and `oxidepm-sandbox` into `/usr/local/bin`, using `sudo` when needed. Set `INSTALL_DIR` to install elsewhere.
- Copies the bundle into `share/oxidepm/adapters` under the installation prefix and checks the CLI version if `oxidepm` is on `PATH`.
- On Linux, imports and enables the runtimes offline with `oxidepm adapter import --bundled --tag runtime --enable --yes`. The CLI and daemon verify the catalog and the selected archives against the bundle's `SHA256SUMS`. If the import fails, the binaries stay installed and the script prints the command to retry.

## Other ways

The [Releases page](https://github.com/oxidekit/oxidepm/releases) has the archives and Debian packages:

| Platform | Architecture | Archive |
|---|---|---|
| Linux | x86_64 | `oxidepm-x86_64-unknown-linux-gnu.tar.gz` |
| Linux | ARM64 | `oxidepm-aarch64-unknown-linux-gnu.tar.gz` |
| macOS | Intel | `oxidepm-x86_64-apple-darwin.tar.gz` |
| macOS | Apple Silicon | `oxidepm-aarch64-apple-darwin.tar.gz` |

For Homebrew and Arch Linux instructions, see the [OxidePM README](https://github.com/oxidekit/oxidepm/blob/prod/README.md#installation).

## Runtimes

The built-in `cmd` runtime runs an executable. The `runtime-node`, `runtime-python`, `runtime-go` and `runtime-rust` adapters provide `node`, `npm`, `pnpm`, `yarn`, `python`, `go`, `rust` and `cargo`. The release archive carries them under `share/oxidepm/adapters`. On Linux, import and enable them offline with:

```sh
oxidepm adapter import --bundled --tag runtime --enable --yes
```

On Linux, serving a runtime request requires its adapter to be imported and enabled. For optional adapters, see [Import and enable](https://oxidepm.com/docs/adapters/import-and-enable/).

## From source

*Build*

```sh
git clone --branch v0.4.0-rc.2 https://github.com/oxidekit/oxidepm
cd oxidepm
cargo build --workspace --release
```

The binaries are in `target/release`. Install `oxidepm` and `oxidepmd` in the same directory on `PATH`. On Linux, place `oxidepm-sandbox` beside them. To add the bundled runtimes to a Linux source build, copy `share/oxidepm/adapters` from the release archive to the same path under your installation prefix and run the import command above.

## Check it

```sh
oxidepm --version
oxidepm status
```

If `status` reports that the daemon is down, `oxidepm start` starts it when you launch an app.
