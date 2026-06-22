Introduction
============

What is Crux?
-------------

Crux is a symbolic testing tool for C/C++ and Rust programs, developed by
`Galois, Inc <https://www.galois.com/>`_.

Crux tests are similar to unit tests, but Crux can check your test assertions exhaustively, on all possible inputs within a
given scope. If an assertion has any *counterexamples*---inputs that cause the
assertion to fail---Crux will find one of these counterexamples. If Crux does
not find a counterexample, you have a proof that the assertion always holds.

Crux currently comes in several variants:

- **crux-llvm**: verifies C and C++ code compiled to LLVM bitcode.
- **crux-mir**: verifies Rust code compiled to Mid-level Intermediate
  Representation (MIR).
- **crux-mir-comp**: extends ``crux-mir`` with *compositional verification*,
  enabling you to verify large programs piece by piece.

Despite these variants, the workflow is the same: you write test functions with
symbolic inputs and assertions, and Crux exhaustively checks those assertions
using symbolic execution and SMT solving.

Tutorial examples will focus on ``crux-mir-comp``, the most mature variant.

What can I use Crux for?
------------------------

Crux is designed for verifying functional correctness properties of code.
Common use cases include:

- Verifying that a function's output satisfies a postcondition for all valid
  inputs.
- Checking that an optimized implementation matches a reference implementation
  for all inputs.
- Checking equivalence between a Rust implementation and a Cryptol
  specification.

Crux can also detect (or prove the absence of) generic safety violations such
as arithmetic overflows, out-of-bounds accesses, and other undefined behavior.

Crux works best on code with bounded loops and finite data structures. It can
handle unbounded loops to some extent, but its strength is exhaustive analysis
of bounded computations.
