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

The letters N--Z shift past the end of the alphabet and wrap around to the beginning, which is the same as shifting backwards because the Latin alphabet has 26 letters. For example:

.. parsed-literal::

   **Z** (letter 26)  ━━▶  **M** ((26 + 13) % 26 = 26 - 13 = letter 13)

At Galois, we sometimes use ROT13 to encrypt answers to math and logic puzzles, so that we can share answers without spoiling the puzzle for those who are still solving it.


The code under test
-------------------

Let's create a file called ``rot13.rs`` with a simple ROT13 implementation:

.. code-block:: rust
   :linenos:

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

Notice that ``rot13()`` takes in a fixed-size 16-character message. As we discussed in the introduction, Crux works best with code that manipulates finite data structures.

A property that holds
---------------------

A neat property of ROT13 is that it's *involutive*. That's a fancy way of saying that if you apply ROT13 to any message *m*, and then you apply ROT13 to the result, you'll get back your original *m*. This property means that ROT13 can be used to encrypt and decrypt the same message!

Let's use Crux to check that this property holds for our implementation of ROT13. Below, we'll provide code for a Crux test that checks the property, run the test to see what output it produces, and then explain the structure of the test, line by line.

First, add this code to your ``rot13.rs`` file:

.. code-block:: rust
  :linenos:

   use crucible::Symbolic;
   use crucible::crucible_assert;

   #[crux::test]
   fn rot13_involutive() {
       let buf: [u8; 16] = <[u8; 16]>::symbolic("buf");
       crucible_assert!(rot13(rot13(buf)) == buf);
   }

Now run Crux on the file:

.. code-block:: bash

   crux-mir-comp rot13.rs

You should see:

.. code-block:: text

   test rot13/...::rot13_involutive[0]: [Crux] Attempting to prove verification conditions.
   ok

   [Crux-MIR] ---- FINAL RESULTS ----
   [Crux] Goal status:
   [Crux]   Total: 721
   [Crux]   Proved: 721
   [Crux]   Disproved: 0
   [Crux]   Incomplete: 0
   [Crux]   Unknown: 0
   [Crux] Overall status: Valid.

Success! Crux has proven that ``rot13()`` is involutive for all possible 16-character inputs.

Now let's break down the structure of the test we just ran:

- The ``#[crux::test]`` directive on line 4 tells Crux to run the test below when Crux is invoked on this file.
- Line 5 is the beginning of a Crux test called ``rot13_involutive()``. Crux tests are ordinary Rust functions.
- Line 6 creates a symbolic 16-byte array called ``buf``. Rather than taking a single concrete value, the array represents all possible ``[u8; 16]`` values simultaneously.
- The ``crucible_assert!()`` call on line 7 states the property Crux should check: that ``rot13(rot13(buf)) == buf`` (i.e., that ``rot13()`` is involutive).

When Crux runs this test, it uses symbolic execution and an SMT solver to either (a) prove that the assertion holds for all inputs, or (b) find a concrete counterexample. The test passes, so ``rot13()`` is truly an involution on all inputs.

A property that fails
---------------------

Now let's see what happens when we use Crux to check a property of ``rot13()`` that *doesn't* hold.

Here's a property that might seem true if you don't think about it too hard: the output of ``rot13()`` is never equal to its input. After all, the function changes every letter of its input message, so it should never return the message unchanged, right?

We can encode that property as the following Crux test:

.. code-block:: rust

   #[crux::test]
   fn rot13_always_changes() {
       let buf: [u8; 16] = <[u8; 16]>::symbolic("buf");
       crucible_assert!(rot13(buf) != buf);
   }

Now we'll run Crux on the file and pass it the ``-m`` flag, which makes Crux print a counterexample when it finds one:

.. code-block:: bash

   crux-mir-comp rot13.rs -m

Crux will find a counterexample: any input consisting entirely of
non-alphabetic bytes (like ``[0, 0, 0, ...]``) is left unchanged by rot13,
disproving the assertion.

- The second test fails because rot13 is the identity on non-alphabetic bytes.

Running on a Cargo project
--------------------------

For larger projects, you can use ``cargo crux-test`` instead of invoking
``crux-mir-comp`` on a single file. In the root of a Cargo project:

.. code-block:: bash

   cargo crux-test --lib

This compiles the project with ``mir-json`` and runs all functions annotated
with ``#[crux::test]``.
