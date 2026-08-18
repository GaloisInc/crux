Equivalence Checking
====================

In the :doc:`previous section <rust-quick-start>`, we used Crux to prove properties of a single function. Another common use case for Crux is proving that two implementations of a function produce equal outputs on all possible inputs. This property is sometimes called *extensional equivalence*.

Proving extensional equivalence is useful when there's an "obviously correct" way to implement a function, and another implementation that (a) is harder to reason about and (b) has a nice property, like being more efficient or more secure. In these cases, Crux gives you the best of both worlds. You can use Crux to prove that the reference implementation is equivalent to the optimized version, and then deploy the optimized version with the knowledge that its observable behavior matches that of the reference.

Example: conditional select
---------------------------------------------

We'll illustrate this Crux use case with an example based on the *conditional select* operation. This operation chooses between two inputs (of type ``u32`` in our example) based on the value of a Boolean flag.

A natural way to implement conditional select is with an ``if`` statement:

.. code-block:: rust
   :linenos:

   fn ct_select_ref(flag: bool, a: u32, b: u32) -> u32 {
       if flag { a } else { b }
   }

This function clearly implements the conditional select operation correctly. However, it is ill-suited to cryptographic applications because its branching structure may expose a *timing side-channel*. In other words, an attacker who can observe the function's timing behavior might be able to infer which branch was taken, thereby obtaining secret data. For example, if the attacker knows which branch was taken, they know whether the flag was ``true`` or ``false``, and the flag might be one bit of a secret key.

For this reason, cryptographic engineers use a *constant-time* version of conditional select that always executes the same instructions regardless of the flag's value. The trick is to encode conditional behavior in terms of bitwise operations instead of using explicit branches.

There are several ways to define branchless conditional select; here's one version:

.. code-block:: rust
   :linenos:

   fn ct_select_opt(flag: bool, a: u32, b: u32) -> u32 {
       let mask = 0u32.wrapping_sub(flag as u32);
       b ^ (mask & (a ^ b))
   }

Informal equivalence proof
--------------------------

In just a minute, we'll use Crux to verify that the constant-time function ``ct_select_opt()`` is extensionally equivalent to the reference implementation ``ct_select_ref()``. But first, here's an informal proof that the two functions compute the same result given equal inputs.

Consider the two cases of the constant-time version:

- When ``flag`` is ``true``, ``flag as u32`` is ``1``, and ``0u32.wrapping_sub(1)`` evaluates to ``0xFFFFFFFF`` (all bits are one).
- When ``flag`` is ``false``, ``flag as u32`` is ``0``, and ``0u32.wrapping_sub(0)`` evaluates to ``0x00000000`` (all bits are zero).

So ``mask`` is either all ones or all zeros. Then:

- If ``mask`` is all ones: ``b ^ (0xFFFFFFFF & (a ^ b))`` simplifies to ``b ^ (a ^ b)`` which is ``a``.
- If ``mask`` is all zeros: ``b ^ (0x00000000 & (a ^ b))`` simplifies to ``b ^ 0`` which is ``b``.

Therefore, ``ct_select_opt()`` returns ``a`` if ``flag`` is ``true`` and ``b`` otherwise, which is the same behavior as ``ct_select_ref()``.

Crux equivalence test
---------------------

TODO
