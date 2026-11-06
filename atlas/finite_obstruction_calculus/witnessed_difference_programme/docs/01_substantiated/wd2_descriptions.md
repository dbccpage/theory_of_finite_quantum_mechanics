# Finite Distinction Carriers and History Escape

Version 1.1.0, dated 2026-10-08. Author-review prose preprint; not an external publication.

A finite deterministic system has a declared observation map and an input
alphabet of permitted updates. States with the same present observation
can become distinguishable after an input sequence. This paper identifies
finite-horizon observational equivalence with recursive partition refinement,
bounds stabilization by the available increase in the number of classes,
and constructs shortest separating words. The stabilized relation is the
largest observation-preserving update congruence, and its quotient is the
smallest deterministic quotient preserving all states' future readouts.

Reports attached to updates add no distinction under an explicit sufficient
endpoint-profile factorization condition. An unconstrained report can add
a new observation. Examples cover noncommuting updates and empty boundary
cases. Theorem WD2-T1 is elaborated in Lean 4. Finite instances of the
remaining statements are evaluated by `code/finite_distinction.py`; their
general forms are not Lean theorems in this package. The reproduction
entry checks file integrity, those tests, and the Lean build. The
refinement and minimization results are classical, not a quantum
reconstruction or a claim of new automata theory.
