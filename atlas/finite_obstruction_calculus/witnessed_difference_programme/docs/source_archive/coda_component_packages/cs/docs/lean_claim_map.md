# CODA-CS Lean Claim Map (v1.1)

Mapping of active manuscript claims to Lean 4 declarations in `lean4/`. The declarations are self-contained; current compilation and axiom results are recorded separately.

| Manuscript ID | Claim Name | Formal Declaration | Lean Module | Axiom Dependencies | Status |
|---|---|---|---|---|---|
| **CS-D1** | Fibre constancy | `Coda.FiberConstant` | `Algebra.lean` | none | Mechanized |
| **CS-D2** | Factorization | `Coda.Factors` | `Algebra.lean` | none | Mechanized |
| **CS-D3** | Refinement | (composite $p = \mathrm{forget} \circ \mathrm{fine}$) | `Algebra.lean` | none | Mechanized |
| **CS-L1** | Factorization implies fibre constancy | `Coda.factor_implies_constant` | `Algebra.lean` | none | Mechanized (0 axioms) |
| **CS-T1** | Refinement preserves descent | `Coda.CS.refinement_preserves_descent` | `Algebra.lean` | none | Mechanized (0 axioms) |
| **CS-T2** | Family observation equality | `Coda.CS.family_observation` | `Algebra.lean` | `Quot.sound` | Mechanized |
| **CS-T3** | Collision obstructs factor | `Coda.CS.finite_shadow_collision` | `Algebra.lean` | none | Mechanized (0 axioms) |
| **CS-T4** | Strict refinement countermodel | `Coda.CS.refinement_strict_countermodel` | `Algebra.lean` | none | Mechanized (0 axioms) |
| **CS-T5** | Missing terminalizer blocks authority | `CodaCs.terminalizer_absence_blocks_query_authority` | `L01ContinuumNonCreation.lean` | none | Mechanized (0 axioms) |
| **CS-T5 (Witness)** | Non-creation existence witness | `CodaCs.continuum_limit_does_not_create_authority` | `L01ContinuumNonCreation.lean` | none | Mechanized (0 axioms) |

### Directional Scoping Note
- `Coda.factor_implies_constant` formalizes $\mathsf{Factors}(p,q) \implies \mathsf{FiberConstant}(p,q)$.
- `Coda.collision_obstructs_factor` formalizes the contrapositive obstruction:
  $$\neg\mathsf{FiberConstant}(p, q) \implies \neg\mathsf{Factors}(p, q)$$
  It does **not** assert that fibre constancy is equivalent to total factorization on non-surjective observations without choice.

### Standalone Verification
Run `lake build` from `lean4/` so Elan selects the pinned toolchain. `CodaCs.empty_shadow_tower_not_authorized`, `CodaCs.authorized_singleton_shadow_tower`, and `CodaCs.unauthorized_singleton_shadow_tower` in `D01D02Records.lean` record the operational empty/nonempty parity cases.
