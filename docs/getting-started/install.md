# Install

Install OxidePM with the install script, a package, a prebuilt archive or from source.

Source: https://oxidepm.com/docs/getting-started/install/

## Requirements

- Linux only (x86_64 and aarch64, glibc).
- Install the programs your apps need, such as Node.js, Python, Go or Rust.
- Building OxidePM from source requires Rust 1.85 or newer. Building the `ui-tui` adapter from source requires Rust 1.88 or newer.

## The install script

Install `minisign` before running the script to verify the release signature.

*Install*

```sh
curl -fsSL https://oxidepm.com/install.sh | sh
```

The [install script](https://oxidepm.com/install.sh) uses `OXIDEPM_VERSION` to select a version or tag. It defaults to the latest published release.

- Detects the platform with `uname` and downloads its archive and `checksums.txt` from GitHub.
- When `minisign` is on `PATH`, verifies `checksums.txt.minisig` against the [release signing keys](https://oxidepm.com/security/#release-signing) and requires the trusted comment to match the release tag. Without `minisign`, the script reports that it skipped signature verification.
- Checks the archive's SHA-256 against the entry for that exact filename in `checksums.txt`.
- Installs `oxidepm`, `oxidepmd` and `oxidepm-sandbox` into `/usr/local/bin`, using `sudo` when needed. Set `INSTALL_DIR` to install elsewhere.
- Copies all 13 adapter archives into `share/oxidepm/adapters` under the installation prefix and checks the CLI version if `oxidepm` is on `PATH`.
- Attempts to import and enable only the four runtime adapters with `oxidepm adapter import --bundled --tag runtime --enable --yes`. This works offline, and the CLI and daemon verify the catalog and the selected archives against the bundle's `SHA256SUMS`. If the import fails, the binaries stay installed and the script prints the command to retry.

With `minisign` installed, the script allows a missing signature only when you explicitly select a release older than 0.4.0-rc.4 and the signature URL returns HTTP 404. It still checks SHA-256.

## Other ways

The [0.4.0 release](https://github.com/oxidekit/oxidepm/releases/tag/v0.4.0) has archives for these platforms:

| Platform | Architecture | Archive |
|---|---|---|
| Linux | x86_64 | `oxidepm-x86_64-unknown-linux-gnu.tar.gz` |
| Linux | ARM64 | `oxidepm-aarch64-unknown-linux-gnu.tar.gz` |

[Verify your download](https://oxidepm.com/docs/getting-started/install/#verify-a-release-download) before extracting an archive or installing a package. On Debian or Ubuntu, install the package for your architecture with `dpkg`.

```sh
# x86_64
sudo dpkg -i oxidepm_0.4.0_amd64.deb
# ARM64
sudo dpkg -i oxidepm_0.4.0_arm64.deb
```

Run the runtime import below after installing manually.

For Arch Linux instructions, see the [OxidePM README](https://github.com/oxidekit/oxidepm/blob/prod/README.md#installation).

## Verify a release download

0.4.0-rc.4 is the first signed release. Download the exact archive or Debian package for your platform, `checksums.txt` and `checksums.txt.minisig` from the same release tag. The checksums also cover the standalone `oxidepm-adapter-<name>-<target>.tar.gz` archives published for each platform. Get the public key from the [release signing policy](https://oxidepm.com/security/#release-signing). For `v0.4.0`, use the current key below and require the command to succeed and print exactly `oxidepm release checksums tag=v0.4.0`.

```sh
PUBLIC_KEY='RWQMeVEZKn2/BHzgJLldWbECE2BqKV4a0rmNXEzn5N0lxrSi/dDuFjHC'
minisign -V -H -Q -P "$PUBLIC_KEY" -m checksums.txt -x checksums.txt.minisig
```

For another signed release, require the trusted comment to match its full tag, including the `v` prefix and any release candidate suffix. Set `ARCHIVE` to the exact filename you downloaded and compute its SHA-256.

```sh
ARCHIVE=oxidepm-x86_64-unknown-linux-gnu.tar.gz
sha256sum "$ARCHIVE"
```

Compare the digest with the entry for that exact filename in the verified `checksums.txt` before extracting the archive or installing the package. For a verified archive, put `oxidepm`, `oxidepmd` and `oxidepm-sandbox` in your installation prefix's `bin` directory and copy `share/oxidepm/adapters` to the same path under that prefix.

## Runtimes

The built-in `cmd` runtime runs an executable. The `runtime-node`, `runtime-python`, `runtime-go` and `runtime-rust` adapters provide `node`, `npm`, `pnpm`, `yarn`, `python`, `go`, `rust` and `cargo`. The release archive carries them under `share/oxidepm/adapters`. Import and enable them offline with:

```sh
oxidepm adapter import --bundled --tag runtime --enable --yes
```

Serving a runtime request requires its adapter to be imported and enabled.

## Add optional adapters

Use the signed online catalogue to find and install an adapter by name.

```sh
oxidepm adapter search watch
oxidepm adapter import watch --enable
```

For an offline install, run `oxidepm adapter import --bundled watch --enable`. Review the permissions and approve the grant at the prompt. See [Import and enable](https://oxidepm.com/docs/adapters/import-and-enable/) for more commands.

## From source

*Build*

```sh
git clone --branch v0.4.0 https://github.com/oxidekit/oxidepm
cd oxidepm
cargo build --workspace --release
```

The binaries are in `target/release`. Install `oxidepm`, `oxidepmd` and `oxidepm-sandbox` in the same directory on `PATH`. To add the bundled runtimes to a source build, copy `share/oxidepm/adapters` from the release archive to the same path under your installation prefix and run the import command above.

## Check it

```sh
oxidepm --version
oxidepm status
```

If `status` reports that the daemon is down, `oxidepm start` starts it when you launch an app.
