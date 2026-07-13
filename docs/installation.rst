Installing Crux
===============

This chapter covers installing ``crux-mir-comp`` from a pre-built binary
distribution. If you'd like to build ``crux-mir-comp`` from source instead, see
:doc:`building-from-source`.

Supported platforms
-------------------

Crux is developed and tested on Linux and macOS, including Apple Silicon.

We do not yet officially support Windows. See `this GitHub issue
<https://github.com/GaloisInc/mir-json/issues/275/>`_ for a description of
what's involved in adding Windows support.

Prerequisites
-------------

You'll need a `Rust <https://rust-lang.org/>`_ compiler, which you can
install via the `rustup <https://rustup.rs/>`_ tool.

Step 1: Download saw-suite
-----------------------------

``crux-mir-comp`` is distributed as part of `saw-suite
<https://github.com/GaloisInc/saw-suite>`_, a bundle of open-source tools for
verifying software and hardware. You can download the latest saw-suite release
from the `releases page <https://github.com/GaloisInc/saw-suite/releases>`_, or
from the command line as follows:

For macOS on Apple Silicon:

.. code-block:: bash

   curl -o saw-suite-macos-15-ARM64.zip -L \
     https://github.com/GaloisInc/saw-suite/releases/download/snapshot-20260420/saw-suite-macos-15-ARM64.zip
   unzip saw-suite-macos-15-ARM64.zip

For Ubuntu 24.04 on x86_64:

.. code-block:: bash

   curl -o saw-suite-ubuntu-24.04-X64.zip -L \
     https://github.com/GaloisInc/saw-suite/releases/download/snapshot-20260420/saw-suite-ubuntu-24.04-X64.zip
   unzip saw-suite-ubuntu-24.04-X64.zip

Step 2: Set environment variables
---------------------------------

Add the saw-suite ``bin/`` directory to your PATH, and point Crux at a
copy of the Rust standard library that has been translated into a Crux-ready
format:

.. code-block:: bash

   export PATH=$(pwd)/saw-suite/bin:$PATH
   export CRUX_RUST_LIBRARY_PATH=$(pwd)/saw-suite/rlibs

We recommend adding these lines to your shell configuration (``.bashrc``,
``.zshrc``, etc.), using absolute paths.

Step 3: Verify the installation
-------------------------------

Check that the binary works:

.. code-block:: bash

   crux-mir-comp --version

Then create a small test file to confirm that the full toolchain works end-to-end:

.. code-block:: rust

   // test.rs
   use crucible::Symbolic;
   use crucible::crucible_assert;

   #[crux::test]
   fn simple_test() {
       let x = u8::symbolic("x");
       crucible_assert!(x.saturating_add(1) >= x);
   }

Run it:

.. code-block:: bash

   crux-mir-comp test.rs

You should see output ending with ``Overall status: Valid.``, indicating that
the assertion holds for all possible values of ``x``.
