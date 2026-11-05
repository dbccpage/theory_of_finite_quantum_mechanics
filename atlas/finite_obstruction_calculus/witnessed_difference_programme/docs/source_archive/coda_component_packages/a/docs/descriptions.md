# CODA-A: Residuals of Projections, Kernels, and Cokernels

For a linear correction, `residual(C, x) = x - Cx`. If `C² = C`, the residual lies in `ker(C)`, and equal residuals identify classes modulo `im(C)`. Commuting linear maps transport residuals.

A-T1–A-T7 are algebraic statements. The Lean model uses additive groups; A-T7 proves the unique underlying quotient function, while scalar linearity is proved in the manuscript and checked in finite rational matrix examples. A-T8 is a declared commitment without a proof. A-T9 assumes finite rational coordinate spaces with the coordinate l1 norm and `im(C) = im(d0)`.

The finite classifier calls a closed cochain with positive quotient distance `ClosedResidual` (the project-specific Anomalon). A residual supplies diagnostic data; it supplies no authorization or causal provenance.

## Artifacts and verification scope

The manuscript is supplied as Markdown and TeX. Exact rational computation lives in `code/`, with edge, mutation, and regression tests in `code/tests/`. Three notebooks bind their imports to the local companion and solver; no ancestor repository path is inserted. Lean sources use the pinned `lean4/lean-toolchain` and no external mathlib package. See `000_quick_start.md` for dependency installation and replay commands. Current test counts come from pytest collection, not this description.

The current `lean4/axiom_report.txt` census covers the explicitly queried declarations and lists standard kernel dependencies including `propext` and `Quot.sound`. It records standard kernel dependencies and does not claim that every theorem is axiom-free.
