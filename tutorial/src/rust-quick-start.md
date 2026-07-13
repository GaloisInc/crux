# Rust Quick Start

This section walks through running Crux on a simple Rust example. It assumes you have completed the steps in [Installing Crux](./installing.md).

## The code under test

Create a file `rot13.rs` with a simple rot13 implementation:

```rust
fn rot13(buf: [u8; 16]) -> [u8; 16] {
    let mut out = [0u8; 16];
    let mut i = 0;
    while i < 16 {
        out[i] = match buf[i] {
            b'a'..=b'm' | b'A'..=b'M' => buf[i] + 13,
            b'n'..=b'z' | b'N'..=b'Z' => buf[i] - 13,
            _ => buf[i],
        };
        i += 1;
    }
    out
}
```

## A property that holds

rot13 is an involution: applying it twice returns the original input. Add a test that verifies this for all possible 16-byte inputs:

```rust
use crucible::Symbolic;
use crucible::crucible_assert;

#[crux::test]
fn rot13_involution() {
    let buf: [u8; 16] = Symbolic::symbolic("buf");
    crucible_assert!(rot13(rot13(buf)) == buf);
}
```

Run it:

```bash
crux-mir-comp rot13.rs
```

You should see:

```
test test/..::rot13_involution[0]: [Crux] Attempting to prove verification conditions.
[0Kok

[Crux-MIR] ---- FINAL RESULTS ----
[Crux] Goal status:
[Crux]   Total: 1
[Crux]   Proved: 1
[Crux]   Disproved: 0
[Crux]   Incomplete: 0
[Crux]   Unknown: 0
[Crux] Overall status: Valid.
```

Crux has proven that `rot13(rot13(buf)) == buf` holds for all 2^128 possible inputs.

## A property that fails

Now add a test claiming that rot13 always changes its input:

```rust
#[crux::test]
fn rot13_always_changes() {
    let buf: [u8; 16] = Symbolic::symbolic("buf");
    crucible_assert!(rot13(buf) != buf);
}
```

Run with the `-m` flag to print a counterexample:

```bash
crux-mir-comp rot13.rs -m
```

Crux will find a counterexample: any input consisting entirely of non-alphabetic bytes (like `[0, 0, 0, ...]`) is left unchanged by rot13, disproving the assertion.

## What just happened?

- `Symbolic::symbolic("buf")` creates a symbolic 16-byte array. Rather than taking a single concrete value, it represents all possible `[u8; 16]` values simultaneously.
- `crucible_assert!` states the property to check. Crux uses symbolic execution and an SMT solver to either prove the assertion holds for all inputs, or find a concrete counterexample.
- The first test passes because rot13 is genuinely an involution on all byte values.
- The second test fails because rot13 is the identity on non-alphabetic bytes.

## Running on a Cargo project

For larger projects, you can use `cargo crux-test` instead of invoking `crux-mir-comp` on a single file. In the root of a Cargo project:

```bash
cargo crux-test --lib
```

This compiles the project with `mir-json` and runs all functions annotated with `#[crux::test]`.
