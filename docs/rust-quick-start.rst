Rust Quick Start
================

This section demonstrates how to use Crux to test a simple Rust program. It assumes you have completed the steps in :doc:`installation`.

Our example program: a secret message encoder/decoder
-----------------------------------------------------
The Rust program that we'll test implements ROT13, an algorithm for encoding and decoding secret messages.

ROT13 takes a message (sequence of characters) as input and "rotates" or shifts each letter 13 steps forward in the Latin alphabet:

.. parsed-literal::

   **A** (letter  1)  ━━▶  **N** (1 + 13 = letter 14)
   **B** (letter  2)  ━━▶  **O** (2 + 13 = letter 15)
   ...

Letters in the latter half of the alphabet (N--Z) wrap around to the beginning. You can also think of N--Z as shifting 13 steps backward. You'll get the same result either way, because the Latin alphabet has 26 letters. For example:

.. parsed-literal::

   **Z** (letter 26)  ━━▶  **M** ((26 + 13) % 26 = 26 - 13 = letter 13)

At Galois, we sometimes use ROT13 to encrypt answers to math and logic puzzles, so that we can share answers without spoiling the puzzle for those who want to solve it themselves. Here's an example: 

(example puzzle)


The code under test
-------------------

Let's create a file called ``rot13.rs`` with a simple ROT13 implementation:

.. code-block:: rust

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

Notice that ``rot13()`` takes in a fixed-size 16-character message. Crux works best on functions with fixed-size parameters.

A property that holds
---------------------

rot13 is an involution: applying it twice returns the original input. Add a
test that verifies this for all possible 16-byte inputs:

.. code-block:: rust

   use crucible::Symbolic;
   use crucible::crucible_assert;

   #[crux::test]
   fn rot13_involution() {
       let buf: [u8; 16] = Symbolic::symbolic("buf");
       crucible_assert!(rot13(rot13(buf)) == buf);
   }

Run it:

.. code-block:: bash

   crux-mir-comp rot13.rs

You should see:

.. code-block:: text

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

Crux has proven that ``rot13(rot13(buf)) == buf`` holds for all 2^128 possible
inputs.

A property that fails
---------------------

Now add a test claiming that rot13 always changes its input:

.. code-block:: rust

   #[crux::test]
   fn rot13_always_changes() {
       let buf: [u8; 16] = Symbolic::symbolic("buf");
       crucible_assert!(rot13(buf) != buf);
   }

Run with the ``-m`` flag to print a counterexample:

.. code-block:: bash

   crux-mir-comp rot13.rs -m

Crux will find a counterexample: any input consisting entirely of
non-alphabetic bytes (like ``[0, 0, 0, ...]``) is left unchanged by rot13,
disproving the assertion.

What just happened?
-------------------

- ``Symbolic::symbolic("buf")`` creates a symbolic 16-byte array. Rather than
  taking a single concrete value, it represents all possible ``[u8; 16]``
  values simultaneously.
- ``crucible_assert!`` states the property to check. Crux uses symbolic
  execution and an SMT solver to either prove the assertion holds for all
  inputs, or find a concrete counterexample.
- The first test passes because rot13 is genuinely an involution on all byte
  values.
- The second test fails because rot13 is the identity on non-alphabetic bytes.

Running on a Cargo project
--------------------------

For larger projects, you can use ``cargo crux-test`` instead of invoking
``crux-mir-comp`` on a single file. In the root of a Cargo project:

.. code-block:: bash

   cargo crux-test --lib

This compiles the project with ``mir-json`` and runs all functions annotated
with ``#[crux::test]``.
