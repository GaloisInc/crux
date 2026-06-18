Limitations
===========

Crux has some important limitations to be aware of:

- **Bounded analysis**: Crux works best when the state space is finite or can
  be effectively bounded. Programs with deeply nested loops or large recursive
  data structures may cause the solver to time out.
- **Unsafe code**: Crux has limited support for ``unsafe`` Rust code. Many
  standard library functions that use ``unsafe`` internally have been
  reimplemented as safe overrides, but coverage is incomplete.
- **Concurrency**: Crux does not currently support concurrent code.
- **SMT solver unpredictability**: Crux relies on SMT solvers, so verification
  times can be unpredictable. Small changes to code can sometimes cause large
  changes in solver performance.
- **Partial standard library support**: Not all standard library functions are
  supported. Unsupported functions will produce error messages during
  verification.

Despite these limitations, Crux is effective for verifying core algorithmic
code, data structure implementations, and protocol logic where the computation
is bounded and the properties are expressible as assertions.
