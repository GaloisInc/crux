# Rust Quick Start

This section walks through running Crux on a simple Rust example. It assumes you have completed the steps in [Installing Crux](./installing.md).

## A first example

Create a file `test.rs`:

```rust
extern crate crucible;
use crucible::*;

#[crux::test]
fn crux_test() {
    let x = u8::symbolic("x");
    let y = u8::symbolic("y");
    crucible_assume!(x < 10);
    crucible_assume!(y < 10);
    crucible_assert!(x + y < 20);
}
```

Run it (from the saw-script directory):

```bash
cabal exec -- crux-mir-comp test.rs --solver=z3
```

You should see output like:

```
test test/abcd1234::crux_test[0]: [Crux] Attempting to prove verification conditions.
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

If you have Yices installed, you can omit `--solver=z3` (Yices is the default).

## What just happened?

- `u8::symbolic("x")` creates a symbolic 8-bit unsigned integer. Rather than taking a single concrete value, it represents all possible `u8` values simultaneously.
- `crucible_assume!` constrains the symbolic values. Here, both `x` and `y` are restricted to the range 0..9.
- `crucible_assert!` states the property to check. Crux will try to find any assignment of `x` and `y` (within the assumptions) that violates the assertion.
- Since the maximum value of `x + y` under these constraints is 18, which is less than 20, the assertion holds for all valid inputs and Crux reports "Valid."

## An example that fails

Change the assertion to something that doesn't hold:

```rust
extern crate crucible;
use crucible::*;

#[crux::test]
fn crux_test() {
    let x = u8::symbolic("x");
    let y = u8::symbolic("y");
    crucible_assume!(x < 10);
    crucible_assume!(y < 10);
    crucible_assert!(x + y < 15);
}
```

Run with `-m` to print a counterexample:

```bash
cabal exec -- crux-mir-comp test.rs --solver=z3 -- -m
```

Crux will report a counterexample showing concrete values of `x` and `y` that violate the assertion (e.g., `x = 9` and `y = 9`, giving a sum of 18).

## Running on a Cargo project

For larger projects, you can use `cargo crux-test` instead of invoking `crux-mir-comp` on a single file. In the root of a Cargo project:

```bash
cargo crux-test --lib -- --solver=z3
```

This compiles the project with `mir-json` and runs all functions annotated with `#[crux::test]`.

## Demo video

There is a [2-minute demo video](https://www.youtube.com/watch?v=dCNQFHjgotU) showing Crux's basic functionality. Everything in the video is also covered in this tutorial.
