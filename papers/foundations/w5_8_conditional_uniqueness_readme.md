# W5.8 — Conditional uniqueness of complex Hilbert under named axioms

**Date:** 2026-07-31 (LT d=3 deepen: explicit product vs composite)
**AuthorityEffect: None**
**Programme:** DERIV-MASTER-20260730 Wave 5
**Path bind:** `docs/path_to_finite_regime_qm.md` §C.20 (item 20)
**Axiom bind:** `AX-LIFT-V0` (`proof_packets/w5_6_lift_classification_20260730/axiom_set_freeze.md`)

## Status this fire (LT d=3 residual deepen)

| Layer | Status | Path |
|---|---|---|
| Statement freeze | **DOC-FROZEN** | this packet + `fail_conditions.yaml` + `uniqueness_ledger.md` |
| Registry conditional uniqueness | **TOY-MECH** | Lean/Python dual |
| LT minimality for uniqueness | **TOY-MECH** | V0∖{LT} admits complex ≠ rebit |
| V0.1 purification vs uniqueness | **TOY-MECH** | purifies ℂ/ℝ but uniqueness still needs LT |
| Continuous V0.1 | **REFUSED on FinL1** | continuum pathway OPEN/import |
| Multipartite LT3 uniqueness | **TOY-MECH** | consistency with V0-unique slice |
| LT3 explicit counts | **TOY-MECH** | ℂ $64=64$, ℝ $27\neq 36$, ℍ $216\neq 120$ |
| Bipartite LT at d=3 | **TOY-MECH** | this residual deepen |
| d=3 explicit counts | **TOY-MECH** | ℂ $81=81$, ℝ $36\neq 45$, ℍ $225\neq 153$ |
| R_LIFT reconstruction pathway | **TOY-MECH / CONDITIONAL** | host-gated on AX-LIFT-V0 package |
| Absolute mathematical uniqueness | **OPEN / REFUSED outside registry** | W5.11 fence (not upgraded) |

**Not Wave-5 full exit.** Absolute uniqueness outside registry remains open/refused. Does not close W7.1 full recovery.

## Theorem (registry form)

**Hypothesis.** $L$ ranges over the declared finite registry
$\{\mathtt{complexHilbert},\mathtt{realHilbert},\mathtt{quaternionicHilbert}\}$.

**Claim.**
\[
\mathrm{satisfiesAxLiftV0}(L) \;\Longleftrightarrow\; L = \mathtt{complexHilbert}.
\]

## LT d=3 residual deepen (this fire)

Bipartite local tomography at factor dimension 3 — explicit density-param witnesses:

| Lift | $\mathrm{params}(3)^2$ | $\mathrm{params}(9)$ | LT? |
|---|---|---|---|
| complex | $81$ | $81$ | pass |
| rebit | $36$ | $45$ | fail |
| quat | $225$ | $153$ | fail |

Multipartite three-qubit LT3 counts (consistency residual, not forced into V0):

| Lift | localProd3 | compositeParams3 | LT3? |
|---|---|---|---|
| complex | $64$ | $64$ | pass |
| rebit | $27$ | $36$ | fail |
| quat | $216$ | $120$ | fail |

Complex LT identity holds algebraically for all $d_A,d_B$ (`complex_lt_identity`).
**OPEN fence retained:** absolute uniqueness outside registry; continuum pathway import.

## R_LIFT pathway

Reconstruction pathway for freeze T08 / W7.1 residual:

- Under `axLiftV0Package` host: pathway **recovered** (unique registry lift = complex).
- Under `finL1Alone` host: pathway **not** recovered (minus-LT non-uniqueness).
- Absolute outside-registry uniqueness still **refused**.

## Nonclaims

- Does not prove uniqueness among all Jordan / GPT / continuum models.
- Does not discharge Koecher–Vinberg.
- Does not promote R_LIFT on W7.1 package this fire (pathway only).
- Does not claim Wave-5 exit.
- AuthorityEffect: None.

## Next legal steps

1. W7.1 residual: promote R_LIFT under liftToy / V0 package flag (using this pathway).
2. Absolute outside-registry uniqueness remains OPEN/REFUSED.

*AuthorityEffect: None.*
