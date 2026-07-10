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

At Galois, we sometimes use ROT13 to encrypt answers to math and logic puzzles, so that we can share answers without revealing spoilers to those who don't want them. Here's a fun one with a ROT13-encoded solution:

.. dropdown:: Fun Diversion (and example of ROT13 encoding)
   :icon: light-bulb

   .. tab-set::

      .. tab-item:: Puzzle

         There are 100 coins on a table. 10 coins are heads-up, and 90 coins are tails-up. You're blindfolded and can't see which coins are heads-up and which are tails-up, but you're allowed to flip coins over. How can you partition these coins into two groups such that each group has the same number of heads facing up?

      .. tab-item:: ROT13-Encoded Solution

         Chg 10 pbvaf va Tebhc N. Yrg'f fnl gung *K* vf gur ahzore bs urnqf va Tebhc N; gung zrnaf gurer ner 10-*K* gnvyf va Tebhc N.

         Abj chg gur erznvavat pbvaf va Tebhc O. Tebhc O zhfg unir 10-*K* urnqf, orpnhfr gurer ner 10 urnqf va gbgny naq jr chg *K* bs gurz va Tebhc N.

         Svanyyl, syvc nyy pbvaf va Tebhc N. Tebhc N abj unf *K* gnvyf naq 10-*K* urnqf: gur fnzr ahzore bs urnqf nf Tebhc O!

      .. tab-item:: Decoded Solution

         Put 10 coins in Group A. Let's say that *X* is the number of heads in Group A; that means there are 10-*X* tails in Group A.

         Now put the remaining coins in Group B. Group B must have 10-*X* heads, because there are 10 heads in total and we put *X* of them in Group A.

         Finally, flip all coins in Group A. Group A now has *X* tails and 10-*X* heads: the same number of heads as Group B!

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

A neat property of ROT13 is that it's *involutive*. That's a fancy way of saying that if you apply ROT13 to any message *m*, and then you apply ROT13 to the result, you'll get back your original *m*. This property makes ROT13 a suboptimal choice for guarding your deepest secrets, but a good choice for encrypting messages that you want to be decipherable with just a little bit of friction (like puzzle solutions).

Let's use Crux to check that this involutive property holds for our implementation of ROT13. Below, we'll provide code for a Crux test that checks the property, run the test to see what output it produces, and then explain the structure of the test, line by line.

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

Here's a property that might seem true if you don't think about it too hard: the output of ``rot13()`` always differs from its input. After all, the function changes every letter of its input message, so it should never return the message unchanged, right?

We can encode that property as the following Crux test:

.. code-block:: rust

   #[crux::test]
   fn rot13_output_neq_input) {
       let buf: [u8; 16] = <[u8; 16]>::symbolic("buf");
       crucible_assert!(rot13(buf) != buf);
   }

Now we'll run Crux on the file like this:

.. code-block:: bash

   crux-mir-comp rot13.rs -m

The ``-m`` flag makes Crux print a model (another name for a counterexample) when it finds one.

Your output should contain something like this:

.. code-block:: text

   failures:

   ---- rot13_test/51948743::rot13_output_neq_input[0] counterexamples ----
   Model:
   buf = 0x60 (signed), 0x60 (unsigned), 96 (decimal)
   buf = 0x60 (signed), 0x60 (unsigned), 96 (decimal)
   ... (repeats 14 more times)

It turns out that this property is false! On line 8 of the ``rot13()`` definition above, you'll see that the function simply copies any non-alphabetic input characters to the output. Therefore, when the input is entirely non-alphabetic, the output of ``rot13()`` is equal to its input.

In this case, the model that Crux found is a 16-byte array in which each byte is 0x60: the backtick (`````) character. When ``rot13()`` takes this array as an argument, its behavior violates the assertion in our ``rot13_output_neq_input()`` test.

Of course, this model isn't the only one that disproves the assertion. Depending on which version of Crux you run and which SMT solver it calls, your Crux installation might find a different model.

A property with a precondition
------------------------------

As we just discovered, the property "ROT13's output always differs from its input" isn't true. However, it *is* true for a subset of inputs: inputs that contain at least one alphabetic character. ROT13 will shift at least that one character, making the output message unequal to the input.

Here's another way of stating this fact: for inputs that satisfy the *precondition* "contains an alphabetic character," ROT13's output is guaranteed to differ from its input.

Up to this point in the tutorial, we've only asked Crux to check *postconditions*: properties that hold after a piece of code executes. For example, we proved above that ``rot13(rot13(buf)) == buf`` for *any* input buffer; we didn't place any preconditions on the buffer. But Crux can check properties that include both pre- and postconditions, which is handy because we can state all kinds of useful function properties in terms of these two elements.

Let's write a more constrained version of ``rot13_output_neq_input()`` that only considers inputs with an alphabetic character.

First, we'll define a predicate that checks whether a buffer contains at least one ASCII letter:

.. code-block:: rust

   fn contains_a_letter(buf: &[u8; 16]) -> bool {
       buf.iter().any(|b| b.is_ascii_alphabetic())
   }

Now we can use this predicate as a precondition in a Crux test. The ``crucible_assume!()`` macro tells Crux to consider only those inputs that satisfy the assumption.

.. code-block:: rust

   use crucible::crucible_assume;

   #[crux::test]
   fn rot13_output_neq_input_with_letter() {
       let buf: [u8; 16] = <[u8; 16]>::symbolic("buf");
       crucible_assume!(contains_a_letter(&buf));
       crucible_assert!(rot13(buf) != buf);
   }

When we run Crux on the file...

.. code-block:: bash

   crux-mir-comp rot13.rs

...we see that this time the property passes:

.. code-block:: text

   test rot13/...::rot13_output_neq_input_with_letter[0]: [Crux] Attempting to prove verification conditions.
   ok

   [Crux-MIR] ---- FINAL RESULTS ----
   [Crux] Goal status:
     Total: 241
     Proved: 241
     Disproved: 0
     Incomplete: 0
     Unknown: 0
   [Crux] Overall status: Valid.

With the precondition in place, Crux only explores messages that contain at least one letter. For all such messages, ``rot13()`` produces output that differs from its input.

Running Crux on a Cargo project
-------------------------------

For larger projects, you can use the command ``cargo crux-test`` instead of invoking ``crux-mir-comp`` on a single file. In the root of a Cargo project, run:

.. code-block:: bash

   cargo crux-test --lib

This command compiles the project with ``mir-json`` and runs all functions annotated with ``#[crux::test]``.
