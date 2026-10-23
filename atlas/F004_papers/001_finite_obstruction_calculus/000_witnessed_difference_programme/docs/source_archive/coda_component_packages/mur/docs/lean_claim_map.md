# Lean 4 Claim Map — CODA-MUR

**Paper:** CODA-MUR: Certified Representation Transport, Composition, and Irreversible Forgetting  
**Version:** `v3.1.1` (2026-09-28)  
**Status Ceiling:** `MECHANIZED`  

---

## Claim Matrix

| Claim ID | Paper Section | Exact Paper Statement | Status | Lean Module & Symbol |
|:---|:---|:---|:---|:---|
| **MUR-D1** | §1 | Transport record: states, observations, and commutes equality | `MECHANIZED` | `Coda.MUR.Transport` in `lean4/Algebra.lean` |
| **MUR-D2** | §1 | DescentSquareCertificate: $D_B F = \bar{F} D_A$ with morphism kinds | `MECHANIZED` | `CODA_MUR.DescentSquareCertificate` in `lean4/D01D02D03Records.lean` |
| **MUR-D3** | §6 | LossLedger: 4-bit loss record $(e, i, a, u)$ only | `MECHANIZED` | `CODA_MUR.LossLedger` in `lean4/D01D02D03Records.lean` |
| **MUR-T1** | §2 | Composite commutes: $r(g.\mathrm{states}(f.\mathrm{states}(x))) = g.\mathrm{observations}(f.\mathrm{observations}(p(x)))$ | `MECHANIZED` | `Coda.MUR.composite_commutes` in `lean4/Algebra.lean` |
| **MUR-T2** | §2 | Descent squares paste: $D_C \circ (G \circ F) = (\bar{G} \circ \bar{F}) \circ D_A$ | `MECHANIZED` | `CODA_MUR.descentSquareCertificate_paste` in `lean4/T01CertificatePasting.lean` |
| **MUR-T3** | §3 | Collisions transport: $p(x) = p(y) \implies q(f.\mathrm{states}(x)) = q(f.\mathrm{states}(y))$ | `MECHANIZED` | `Coda.MUR.collision_transports` in `lean4/Algebra.lean` |
| **MUR-T4** | §3 | Post-processing preserves collisions: $p(x) = p(y) \implies f(p(x)) = f(p(y))$ | `MECHANIZED` | `Coda.MUR.postprocess_preserves_collision` in `lean4/Algebra.lean` |
| **MUR-T5** | §4 | Non-recoverability after non-injective collapse: no left inverse recovering every source value exists | `MECHANIZED` | `Coda.MUR.loss_is_not_recoverable` in `lean4/Algebra.lean` |
| **MUR-T6** | §5 | $\chi$ alone does not imply target standing: concrete countermodel with uninhabited terminal | `MECHANIZED` | `CODA_MUR.concrete_commuting_square_uninhabited_standing` in `lean4/L02TerminalNonBypass.lean` |
| **MUR-T7** | §6 | Loss ledger necessity: lossy move without ledger is not loss-accounting admissible | `MECHANIZED` | `CODA_MUR.loss_accounting_admissible_necessity` in `lean4/T03T04T05LossNoCreation.lean` |
| **MUR-T8** | §6 | Boolean ledger OR associates with empty four-bit ledger as unit | `MECHANIZED` | `CODA_MUR.loss_sum_assoc` in `lean4/T03T04T05LossNoCreation.lean` |

---

## Axiom Audit

All Lean 4 targets in `coda_atlas/F005_coda/mur/lean4` build cleanly under `lake build` (12 jobs) with zero `sorry` stubs, all axioms within standard kernel whitelist `{propext, Quot.sound, Classical.choice}`.

The rational mass field and its additive extension are not present in Lean. `LossAlgebra` takes laws as fields and supplies no rational-mass instance. Python tests and the manuscript's elementary proof are the evidence for that extension. MUR-T7 uses an abstract `lossDefined` proposition, not the Python validation algorithm.
