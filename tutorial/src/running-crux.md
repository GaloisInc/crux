# Running Crux

- More detail than the quickstart
- Explains the processing pipeline (rustc -> mir-json -> crucible -> smt, clang -> crucible -> smt, etc.)
- Note that you need a mir-json version matching your crux version
- Introduce common command-line options (not all; point to reference manual)
- Point out the distinction between symbolic execution and then discharging proof obligations afterwards
- Gently introduce the user to the idea that SMT solvers have unpredictable performance
