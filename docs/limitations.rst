Limitations
===========

Crux has some important limitations to be aware of:

- **Bounded analysis**: Crux works best when the state space is finite or can
  be bounded. Programs with deeply nested loops or large recursive
  data structures may cause the solver to time out.
- **Concurrency**: Crux does not currently support concurrent code.
- **SMT solver unpredictability**: Crux relies on SMT solvers, so verification
  times can be unpredictable. Small changes to code can sometimes cause large
  changes in solver performance.
- **Partial language/library support**: There exist idioms, compiler intrinsics,
  and standard library functions that Crux does not support. Unsupported
  constructs will produce error messages during verification.

Despite these limitations, Crux is effective for verifying core algorithmic
code, data structure implementations, and protocol logic where the computation
is bounded and the properties are expressible as assertions.
