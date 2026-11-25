## Requirements

- Linux on x86_64 or ARM64, or macOS on Intel or Apple Silicon. macOS supports the built-in `cmd` runtime. The adapter launcher and sandbox are Linux-only in this release.
- Install the programs your apps need, such as Node.js, Python, Go or Rust.
- Building from source requires Rust 1.85 or newer.

## The install script

Install `minisign` before running the script to verify the release signature.

```sh title="Install"
curl -fsSL https://oxidepm.com/install.sh | sh
```

The [install script](/install.sh) installs the latest published release. Set `OXIDEPM_VERSION` to select a specific version or tag.

- Detects the platform with `uname` and downloads its archive and `checksums.txt` from GitHub.
- When `minisign` is on `PATH`, verifies `checksums.txt.minisig` against the [release signing keys](/security/#release-signing) and requires the trusted comment to match the release tag. Without `minisign`, the script reports that it skipped signature verification.
- Checks the archive's SHA-256 against the entry for that exact filename in `checksums.txt`.
- Installs `oxidepm`, `oxidepmd` and `oxidepm-sandbox` into `/usr/local/bin`, using `sudo` when needed. Set `INSTALL_DIR` to install elsewhere.
- Copies all 13 adapter archives into `share/oxidepm/adapters` under the installation prefix and checks the CLI version if `oxidepm` is on `PATH`.
- Attempts to import and enable only the four runtime adapters with `oxidepm adapter import --bundled --tag runtime --enable --yes`. On Linux, this works offline, and the CLI and daemon verify the catalog and the selected archives against the bundle's `SHA256SUMS`. If the import fails, the binaries stay installed and the script prints the command to retry.

With `minisign` installed, the script allows a missing signature only when you explicitly select a release older than 0.4.0-rc.4 and the signature URL returns HTTP 404. It still checks SHA-256.

## Other ways

The [{{release_version}} release]({{release_url}}) has archives for these platforms:

| Platform | Architecture | Archive |
|---|---|---|
| Linux | x86_64 | `oxidepm-x86_64-unknown-linux-gnu.tar.gz` |
| Linux | ARM64 | `oxidepm-aarch64-unknown-linux-gnu.tar.gz` |
| macOS | Intel | `oxidepm-x86_64-apple-darwin.tar.gz` |
| macOS | Apple Silicon | `oxidepm-aarch64-apple-darwin.tar.gz` |

[Verify your download](/docs/getting-started/install/#verify-a-release-download) before extracting an archive or installing a package. On Debian or Ubuntu, install the package for your architecture with `dpkg`.

```sh
# x86_64
sudo dpkg -i oxidepm_{{deb_version}}_amd64.deb
# ARM64
sudo dpkg -i oxidepm_{{deb_version}}_arm64.deb
```

On Linux, run the runtime import below after installing manually.

For Homebrew and Arch Linux instructions, see the [OxidePM README](https://github.com/oxidekit/oxidepm/blob/prod/README.md#installation).

## Verify a release download

0.4.0-rc.4 is the first signed release. Download the exact archive or Debian package for your platform, `checksums.txt` and `checksums.txt.minisig` from the same release tag. Get the public key from the [release signing policy](/security/#release-signing). For `v{{release_version}}`, use the current key below and require the command to succeed and print exactly `oxidepm release checksums tag=v{{release_version}}`.

```sh
PUBLIC_KEY='RWQMeVEZKn2/BHzgJLldWbECE2BqKV4a0rmNXEzn5N0lxrSi/dDuFjHC'
minisign -V -H -Q -P "$PUBLIC_KEY" -m checksums.txt -x checksums.txt.minisig
```

For another signed release, require the trusted comment to match its full tag, including the `v` prefix and any release candidate suffix. Set `ARCHIVE` to the exact filename you downloaded and compute its SHA-256.

```sh
ARCHIVE=oxidepm-x86_64-unknown-linux-gnu.tar.gz
sha256sum "$ARCHIVE"       # Linux
shasum -a 256 "$ARCHIVE"  # macOS
```

Compare the digest with the entry for that exact filename in the verified `checksums.txt` before extracting the archive or installing the package. For a verified archive, put `oxidepm`, `oxidepmd` and `oxidepm-sandbox` in your installation prefix's `bin` directory and copy `share/oxidepm/adapters` to the same path under that prefix.

## Runtimes

The built-in `cmd` runtime runs an executable. The `runtime-node`, `runtime-python`, `runtime-go` and `runtime-rust` adapters provide `node`, `npm`, `pnpm`, `yarn`, `python`, `go`, `rust` and `cargo`. The release archive carries them under `share/oxidepm/adapters`. On Linux, import and enable them offline with:

```sh
oxidepm adapter import --bundled --tag runtime --enable --yes
```

On Linux, serving a runtime request requires its adapter to be imported and enabled. To use any of the other nine adapters, [import and enable it from the release bundle](/docs/adapters/import-and-enable/#import-from-the-release).

## From source

```sh title="Build"
git clone --branch v{{release_version}} https://github.com/oxidekit/oxidepm
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
