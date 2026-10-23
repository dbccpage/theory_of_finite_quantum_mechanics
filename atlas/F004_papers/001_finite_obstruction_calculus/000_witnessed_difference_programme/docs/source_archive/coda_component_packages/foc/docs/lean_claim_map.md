# Proof-Assistant Claim Map (Lean 4)

**Toolchain:** `leanprover/lean4:v4.34.0-rc1` via Lake (`package «coda_foc»`).
Reconstruction algebra is provided by the local modules `Foundations.lean` and `FOC.lean`.

| Claim | Module | Formal names | Axioms |
|---|---|---|---|
| **FOC-01** | `Algebra.lean` | `Coda.FOC.repair_refl`, `repair_symm`, `repair_trans` | `{propext, Quot.sound}` |
| **FOC-02** | `Algebra.lean` | `Coda.FOC.separator_obstructs`, `separator_exists` | `{propext, Quot.sound}`; `separator_exists` also `Classical.choice` |
| **FOC-03** | `Algebra.lean` | `Coda.FOC.exact_closed` | `{propext, Quot.sound}` |
| **FOC-04** | `Algebra.lean` | `Coda.FOC.weighted_diagonal_lower`, `diagonal_minimum`, `diagonal_zero_iff` | `{propext, Classical.choice, Quot.sound}` |
| **FOC-05** | `Algebra.lean` | `Coda.FOC.transport_bound`, `repair_distance_transport` | `{propext, Classical.choice, Quot.sound}` |
| **FOC-C1** | `Algebra.lean` (`FOC.lean`) | `Coda.FOC.separator_exists` (dual functional annihilating repair subspace with nontrivial pairing on nonzero quotient class) | `{propext, Classical.choice, Quot.sound}` |
| **FOC-T3** | `TerminalCompleteness.lean` | `FOC.TerminalCompleteness.native_trichotomy_total_decidable`, `exact_excludes_coherent_residual`, `coherent_residual_excludes_nonclosed_defect`, `exact_excludes_nonclosed_defect`, `exact_implies_closed`; cochain closure is `Coda.FOC.exact_closed` | no axioms for native decidable trichotomy case split; `exact_closed` uses `{propext, Quot.sound}` |
| (kernel $\Phi$–$\Gamma$) | `L20AKernel.lean` | `FOC.L20A.FOCSep.phi_zero_imp_gamma_zero`, `coherent_residual_iff`, `nonclosed_of_gamma_pos`, `gamma_cannot_separate_exact_coherent_residual`, `phi_cannot_separate_coherent_residual_nonclosed` | no axioms (pure propositional deduction from declared primitives P1–P4) |
| (kernel) | `PrimitiveDifference.lean` | Primitive difference quotient; setoid equivalence and delta factorization | `{propext, Quot.sound}` |
| (kernel) | `EpkPrimitiveDifference.lean` | Local family factor exists iff invariant; local green does not force global green | `{Quot.sound}` |
| (binding) | `Core.lean` | Imports the kernel modules and reconstruction algebra | within `{propext, Classical.choice, Quot.sound}` |

All proofs elaborate under `lake build` with zero `sorry` stubs. No custom axioms are added. Reconstruction theorems that use mathlib dual or metric lemmas depend on `Classical.choice` in addition to `{propext, Quot.sound}`. The discrete $\Phi$–$\Gamma$ kernel and terminal trichotomy case split require 0 axioms from declared primitives.

