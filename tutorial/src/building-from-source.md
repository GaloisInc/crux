# Appendix B: Building from Source

This appendix covers building `crux-mir-comp` from source. This is useful if you need the latest development version or want to modify the tools yourself.

## Prerequisites

You will need:

- **GHC 9.6, 9.8, or 9.10** and **cabal** (install via [ghcup](https://www.haskell.org/ghcup/))
- **Rust** (install via [rustup](https://rustup.rs/))
- **An SMT solver**: either [Z3](https://github.com/Z3Prover/z3/releases) or [Yices](http://yices.csl.sri.com/)
- Standard build tools (`cc`, `make`, etc.)

On macOS, Z3 can be installed with Homebrew:

```bash
brew install z3
```

## Building

### 1. Clone the repository and initialize submodules

```bash
git clone https://github.com/GaloisInc/saw-script.git
cd saw-script
git submodule update --init --recursive
```

### 2. Generate version information

The build requires generated version files. From the saw-script root:

```bash
bash saw-version/src/SAWVersion/savegitinfo.sh
```

### 3. Build crux-mir-comp

```bash
cabal build crux-mir-comp
```

This compiles `crux-mir-comp` and all its Haskell dependencies (crucible, what4, cryptol, etc.). The first build takes a while.

### 4. Install mir-json

mir-json translates Rust code into MIR for Crux to consume. It requires a specific nightly Rust toolchain. Check the required version in `deps/mir-json/rust-toolchain.toml`, then:

```bash
rustup toolchain install nightly-2025-09-14 --component rustc-dev,rust-src
cd deps/mir-json
cargo +nightly-2025-09-14 install --path . --locked
```

This installs `mir-json`, `crux-rustc`, `cargo-crux-test`, and related tools into `~/.cargo/bin/`.

### 5. Translate the standard libraries

Crux needs pre-translated versions of the Rust standard library. From the `deps/mir-json` directory:

```bash
mir-json-translate-libs
```

This creates an `rlibs_real` directory containing the translated libraries.

### 6. Set environment variables

Point Crux at the translated libraries. The path depends on your platform:

```bash
export CRUX_RUST_LIBRARY_PATH=$(pwd)/rlibs_real/lib/rustlib/aarch64-apple-darwin/lib
```

On Linux, replace `aarch64-apple-darwin` with your target triple (e.g., `x86_64-unknown-linux-gnu`).

Adding this to your shell configuration (`.bashrc`, `.zshrc`, etc.) is recommended.

## Verifying the build

Check that `crux-mir-comp` runs:

```bash
cabal exec -- crux-mir-comp --version
```

To verify the full toolchain works end-to-end (mir-json, rlibs, and the solver), see the [Rust Quick Start](./rust-quick-start.md).

## Notes

- The nightly toolchain version required by mir-json changes periodically. Always check `deps/mir-json/rust-toolchain.toml` for the current requirement.
- Your mir-json version must match your `crux-mir-comp` version. If you update one, rebuild the other.
- After updating mir-json, re-run `mir-json-translate-libs` to regenerate the rlibs.

## TODO

- Validate these installation steps in a clean environment (Docker container or CI workflow) to confirm they work end-to-end without implicit dependencies.
