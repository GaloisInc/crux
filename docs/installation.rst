Installing Crux
===============

This chapter covers installing ``crux-mir-comp`` from a pre-built binary
distribution. If you'd like to build ``crux-mir-comp`` from source instead, see
:doc:`building-from-source`.

Supported platforms
-------------------

Crux is developed and tested on Linux and macOS (including Apple Silicon).
Windows is not officially supported.

Prerequisites
-------------

You will need a `Rust <https://rust-lang.org/>`_ compiler, which you can
install via the `rustup <https://rustup.rs/>`_ tool.

1. Download the SAW release
----------------------------

``crux-mir-comp`` is distributed as part of the
`SAW <https://github.com/GaloisInc/saw-script>`_ release. Download the latest
release from the `SAW releases page
<https://github.com/GaloisInc/saw-script/releases>`_. Choose the
``-with-solvers`` variant for your platform to get bundled SMT solvers.

For macOS on Apple Silicon:

.. code-block:: bash

   gh release download v1.5.1 --repo GaloisInc/saw-script \
     --pattern "saw-1.5.1-macos-15-ARM64-with-solvers.tar.gz"
   tar xzf saw-1.5.1-macos-15-ARM64-with-solvers.tar.gz

Add the ``bin/`` directory to your PATH:

.. code-block:: bash

   export PATH=$(pwd)/saw-1.5.1-macos-15-ARM64-with-solvers/bin:$PATH

Verify that the binary works:

.. code-block:: bash

   crux-mir-comp --version

2. Install mir-json
-------------------

``mir-json`` translates Rust code into an intermediate representation (IR)
called MIR for Crux to consume. ``mir-json`` requires a specific nightly Rust
toolchain and must match the SAW release version you downloaded.

For SAW v1.5.1, the matching ``mir-json`` commit is
``7e12cecee9aceefd903191f4bd888d68e9a9cc0a`` and the required toolchain is
``nightly-2025-09-14``:

.. code-block:: bash

   rustup toolchain install nightly-2025-09-14 --component rustc-dev,rust-src
   git clone https://github.com/GaloisInc/mir-json.git
   cd mir-json
   git checkout 7e12cecee9aceefd903191f4bd888d68e9a9cc0a
   cargo +nightly-2025-09-14 install --path . --locked

These commands install ``mir-json``, ``crux-rustc``, ``cargo-crux-test``, and
related tools into ``~/.cargo/bin/``.

**Finding the correct mir-json version for other SAW releases:** ``mir-json``
is a submodule of the saw-script repository at ``deps/mir-json``. To find the
matching commit for a given SAW release tag, run:

.. code-block:: bash

   git ls-tree <saw-release-tag> deps/mir-json

The nightly toolchain version is specified in ``rust-toolchain.toml`` within
the ``mir-json`` repository at that commit.

3. Translate the standard libraries
------------------------------------

Crux needs pre-translated versions of the Rust standard library. From the
directory where you cloned ``mir-json``, run:

.. code-block:: bash

   mir-json-translate-libs

This command creates an ``rlibs_real`` directory containing the translated
libraries.

4. Set environment variables
-----------------------------

Point Crux at the translated libraries. The path depends on your platform:

.. code-block:: bash

   export CRUX_RUST_LIBRARY_PATH=$(pwd)/rlibs_real/lib/rustlib/aarch64-apple-darwin/lib

On Linux, replace ``aarch64-apple-darwin`` with your target triple (e.g.,
``x86_64-unknown-linux-gnu``).

We recommend adding this line to your shell configuration (``.bashrc``,
``.zshrc``, etc.).

5. Verify the installation
---------------------------

Create a small test file to confirm that the full toolchain (``mir-json``,
translated libraries, and solver) works end-to-end:

.. code-block:: rust

   // test.rs
   use crucible::Symbolic;
   use crucible::crucible_assert;

   #[crux::test]
   fn simple_test() {
       let x = u8::symbolic("x");
       crucible_assert!(x.wrapping_add(1) != 0 || x == 255);
   }

Run it:

.. code-block:: bash

   crux-mir-comp test.rs

You should see output ending with ``Overall status: Valid.``, indicating that
the assertion wrapped in ``crucible_assert!()`` holds for all possible values
of ``x``. In other words, we've proven via symbolic testing that for any ``x``
of type ``u8``, the logical OR of ``x`` and 0 is equal to ``x``.
