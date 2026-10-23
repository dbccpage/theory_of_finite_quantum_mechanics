# Formal evidence scope

Lean is pinned to 4.34.1. The seven declarations in the stored axiom report
are conditional abstract additive projector identities. The structure
`SimplexOperatorSpace` supplies additivity, normalization, and same-site /
different-site trace-embedding laws as explicit hypotheses.

Theorem 4.1's formal declarations establish marginal preservation,
idempotence, and Q(PZ)=0 under those hypotheses. Theorem 4.2's declarations
establish one-site isolation and isolation of a vector already assumed to
lie in im(P). They do not show that every proper-support Hamiltonian
commutator is tangent. No density-matrix, SVD, Hamiltonian Taylor bound,
Hodge complex, or DDC model is instantiated in Lean.

The stored report says these declarations use no global logical axioms.
That does not mean there are no mathematical assumptions. Comments were
corrected during review; proof terms and the report were preserved.
No fresh pinned build was available in the review environment.

From this directory, on a machine with the pinned toolchain:

```bash
lake build
lake env lean Census.lean
```

From the package root:

```bash
python tools/replay_lean_axiom_census.py --check
python tools/replay_lean_axiom_census.py --replay
```

The first command checks generated text and the report inventory.
Only the second attempts compilation and a fresh axiom replay.
