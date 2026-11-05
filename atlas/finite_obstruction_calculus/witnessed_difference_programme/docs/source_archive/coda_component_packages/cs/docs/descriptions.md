# The Continuum Shadow (CODA-CS)

A query constant on coarse fibres is constant on refined fibres. Equality of family observations is pointwise equality. A first-coordinate observation of Boolean pairs cannot recover the second coordinate.

The declared authority predicate additionally requires a local terminalizer and a nonempty authorized finite shadow tower. Missing a terminalizer makes this predicate false. It says nothing about uniqueness or existence of a mathematical answer: a constant-zero query remains uniquely defined. Authorized gluing of overlapping shadows is outside the proved scope.

## Artifacts and verification scope

The manuscript is supplied as Markdown and TeX. Exact rational computation lives in `code/`, with edge, mutation, and regression tests in `code/tests/`. Three notebooks bind their imports to the local companion and solver; no ancestor repository path is inserted. Lean sources use the pinned `lean4/lean-toolchain` and no external mathlib package. See `000_quick_start.md` for dependency installation and replay commands. Current test counts come from pytest collection, not this description.
