# Introduction

## What is Crux?

Crux is a symbolic testing tool for C/C++ and Rust programs, developed by Galois, Inc. It checks your test assertions exhaustively, on all possible inputs within a given scope. If an assertion can fail for any input, Crux will find a counterexample. If no counterexample exists, you have a proof that the assertion always holds.

Crux currently comes in several variants:

- **crux-llvm**: verifies C and C++ code compiled to LLVM bitcode.
- **crux-mir**: verifies Rust code compiled to MIR (Mid-level Intermediate Representation).
- **crux-mir-comp**: extends crux-mir with *compositional verification*, allowing you to verify large programs piece by piece.

Despite these variants, the workflow is the same: you write test functions with symbolic inputs and assertions, then Crux exhaustively checks those assertions using symbolic execution and SMT solving.

## What do I use Crux for?

Crux is designed for verifying functional correctness properties of code. Common use cases include:

- Checking that an optimized implementation matches a reference implementation for all inputs.
- Proving absence of arithmetic overflows, out-of-bounds accesses, or other undefined behavior.
- Verifying that a function's output satisfies a postcondition for all valid inputs.
- Checking equivalence between a Rust implementation and a Cryptol specification.

Crux works best on code with bounded loops and finite data structures. It can handle unbounded loops to some extent (via path saturation checks), but its strength is exhaustive analysis of bounded computations.

## When do I use Crux vs. SAW?

Crux and SAW (the Software Analysis Workbench) are both developed by Galois and share much of the same underlying technology (Crucible, What4, and SMT solvers). They differ in how you interact with them:

- **Crux** uses *in-source annotations*. You write `#[crux::test]` functions directly in your Rust or C code, using the same language you're already working in. This makes it easy to integrate into an existing development workflow.

- **SAW** uses an *external scripting language* (SAWScript). Verification specifications are written separately from the code under test, giving SAW more flexibility for complex multi-step proofs, but requiring you to learn an additional language.

In general, if you want to add symbolic tests alongside your existing code with minimal friction, use Crux. If you need more sophisticated proof engineering (chaining together lemmas, rewriting terms, or working with multiple verification backends), use SAW.

The crux-mir-comp variant bridges this gap somewhat by supporting compositional verification (proving properties of functions in terms of specs for their callees) while keeping everything in Rust source annotations.

## How does Crux compare to other verification tools?

### Kani

[Kani](https://github.com/model-checking/kani) is an open-source model checker for Rust backed by the CBMC bounded model checker. Like Crux, it lets you write proof harnesses in Rust. Key differences:

- **Backend**: Kani uses bounded model checking (CBMC). Crux uses symbolic execution with SMT solving (via What4 and solvers like Yices and Z3). This leads to different performance characteristics on different kinds of code.
- **Loop handling**: Kani requires explicit loop unwinding bounds. Crux can use path saturation (`--path-sat`) to automatically determine when loop exploration is complete.
- **Compositional verification**: Crux (via crux-mir-comp) supports compositional verification with method specs. Kani does not currently have an equivalent feature.
- **Maturity of standard library support**: Both tools have partial support for the Rust standard library. Coverage varies by domain.

### Verus

[Verus](https://github.com/verus-lang/verus) is a verification tool for Rust that uses a different approach: you annotate your code with pre/postconditions and loop invariants in a specification language embedded in Rust, and Verus verifies these annotations using an SMT solver (Z3). Key differences:

- **Approach**: Verus is a *deductive verifier*: you provide a proof outline (invariants, pre/postconditions) and the solver fills in the details. Crux is a *symbolic tester*: you provide test harnesses and Crux exhaustively explores them.
- **Annotation burden**: Verus requires more annotations (especially loop invariants) but can verify unbounded computations. Crux requires less annotation but is limited to bounded analysis.
- **Language integration**: Verus uses a custom Rust dialect with specification syntax. Crux uses standard Rust with a small helper crate.

### Other tools

- **CBMC** (for C): Similar in spirit to Crux's C/LLVM mode, but uses bounded model checking rather than symbolic execution.
- **KLEE**: A symbolic execution engine for LLVM. Unlike Crux, KLEE is primarily aimed at bug-finding (generating test cases that increase coverage) rather than proving properties.
- **Creusot** (for Rust): A deductive verifier similar in philosophy to Verus, translating Rust to Why3 for verification.

## Limitations

Crux has some important limitations to be aware of:

- **Bounded analysis**: Crux works best when the state space is finite or can be effectively bounded. Programs with deeply nested loops or large recursive data structures may cause the solver to time out.
- **Unsafe code**: Crux has limited support for `unsafe` Rust code. Many standard library functions that use `unsafe` internally have been reimplemented as safe overrides, but coverage is incomplete.
- **Concurrency**: Crux does not currently support concurrent code.
- **SMT solver unpredictability**: Crux relies on SMT solvers, so verification times can be unpredictable. Small changes to code can sometimes cause large changes in solver performance.
- **Partial standard library support**: Not all standard library functions are supported. Unsupported functions will produce error messages during verification.

Despite these limitations, Crux is effective for verifying core algorithmic code, data structure implementations, and protocol logic where the computation is bounded and the properties are expressible as assertions.
