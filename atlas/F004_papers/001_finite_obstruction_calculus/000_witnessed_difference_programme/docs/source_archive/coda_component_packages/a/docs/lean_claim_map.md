# CODA-A Lean claim map

Source paths below are relative to `lean4/`. Standard kernel axiom dependencies must be read from fresh `#print axioms` output; the historical transcript does not attest to every declaration.

| Claim | Declaration | File | Scope |
|---|---|---|---|
| A-D1 | `Coda.A.residual` | `A.lean` | Definition / additive identity |
| A-D2 | None | — | An explicit hypothesis of the projection theorems; no named IsProjection declaration |
| A-T1 | `Coda.A.residual_zero_iff` | `A.lean` | Additive group theorem |
| A-T2 | `Coda.A.residual_in_kernel` | `A.lean` | Requires C squared equals C |
| A-T3 | `Coda.A.residual_idempotent` | `A.lean` | Requires C squared equals C |
| A-T4a | `Coda.A.range_fixed_iff` | `A.lean` | Requires C squared equals C |
| A-T4b | `Coda.A.direct_sum_unique` | `A.lean` | Companion declaration direct_sum_decomposition proves existence |
| A-T5 | `Coda.A.residual_transport` | `A.lean` | Requires TC=DT |
| A-T6 | `Coda.A.quotient_residual_iff` | `A.lean` | Companion declaration quotient_section proves a function-level section |
| A-T7 | `Coda.A.quotient_universal` | `A.lean` | Lean proves underlying function and uniqueness on a set quotient; scalar linearity is prose and rational matrix evidence |
| A-S1 | `CodaA.residual_not_auth` | `D01D02Records.lean` | Formal constructor separation; provenance wording is an interpretive scope fence |
| COMP-01 | None | — | Finite execution contract |
| COMP-02 | `CodaA.ResidualTerminal` | `D01D02Records.lean` | Lean defines the label type, not the Python quotient-distance algorithm |
| A-T8 | None | — | No theorem and no implementation evidence |
| A-T9 | None | — | Prose proof and finite rational regressions; no single Lean theorem |

Additional declared proofs: `Coda.A.decomposition`, `Coda.A.direct_sum_decomposition`, and `Coda.A.quotient_section` in `A.lean`; `CodaA.toy_anomalon_exists` in `T03ToyAnomalonWitness.lean`. The toy theorem is an explicit constructor witness in the finite taxonomy.

`Coda.A.LinearMap` is an additive homomorphism record; its name does not supply a field-scalar structure. A-T7 scalar linearity is proved in the manuscript, not by the unique-function declaration.
