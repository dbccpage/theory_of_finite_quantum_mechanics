Claim Ledger — Paper QM_062: The U(1)-Selector (OMEGA-QM-U1SELECTOR-046)
========================================================================

**Paper Key:** `003_quantum_foundations/062_the_u1_selector`  

Date: 2026-06-19
Version: v0.1.0 (Pre-Print)
Series: qm / QM ingredient ladder — the imported-ceiling selector (sharpens OB-U1)
Companions: QM_121 (OB-U1, the open selector), QM_061/QM_110 (only signedness forced), QM_101
(pairing-relativity), pub-010 (the Born-uniqueness firewall this mirrors); Lean `ForceComplexCarrier.lean`,
`U1Selector.lean`.

Firewall note: QM is a realization spine. No authority minted. `StructureDerived(F,c) ⇏ IsAuth(t)`.

Paper character: a **synthesis + honest conditional-forcing** paper over two mechanized Lean files. It
introduces ONE new mechanized layer (`U1Selector` — the two-level complex structure) on top of the
existing `ForceComplexCarrier`, and states the conditional forcing of ℂ/U(1) with the residual import
named. It is **NOT** a derivation of ℂ from nothing; it sharpens OB-U1 from open to conditional.
Secured as **ENC-1136**.

Claim index
-----------

| ID | Claim (abbreviated) | Status | Location |
|---|---|---|---|
| QM-062-C1 | The ladder forces signedness only ($\mathbb{Z}/2$), not ℂ — OB-U1 is genuinely open at the interference layer | [SCOPE FENCE] | §1 |
| QM-062-C2 | **Layer 1 (T-FORCE-★):** a nontrivial invariant phase forces a conjugation $\ast$ (the ℂ-shape); a symmetric/bilinear modulus admits only the trivial signs $\pm1$ | [PROVEN, MECHANIZED — `ForceComplexCarrier`: `conjugation_forced`, `realSigned_phaseInvariant_only_signs`] | §2 |
| QM-062-C3 | **Layer 2 (T-FORCE-ℂ):** within the declared Frobenius comparison class ℝ/ℂ/ℍ, ℝ-signed excluded (discrete, exponent 2), ℍ excluded (non-abelian $Q_8$), ℂ admits the abelian order-unbounded fiber | [PROVEN, MECHANIZED — `Z2_not_FCAI`, `Qua_not_FCAI`, `ProdCyc_FCAI`] | §3 |
| QM-062-C4 | **Honest gap:** the abstract phase-group shadow does NOT separate $U(1)$ from the torsion shadow $\mathbb{Q}/\mathbb{Z}$ (uniqueness-among-FCAI not established by Layer 2) | [SCOPE FENCE] | §3 |
| QM-062-C5 | **Layer 3 (new): complex structure.** $J^2=-I$ (rotation generator), $S^2=+I$ (sign), $J^2\neq S^2$ (continuous vs discrete) | [PROVEN, MECHANIZED — `U1Selector`: `J_sq`, `S_sq`, `continuous_vs_discrete` (axiom-free)] | §4 |
| QM-062-C6 | **Layer 3: ℂ appears.** $\{aI+bJ\}$ multiplies as the complex product; `cx` is an injective unital ring embedding $\mathbb{Z}[i]\hookrightarrow M_2(\mathbb{Z})$ | [PROVEN, MECHANIZED — `cx_mul`, `cx_add`, `cx_one`, `cx_realizes_gaussian`, `cx_injective`] | §4 |
| QM-062-C7 | $SO(2)\cong U(1)$ is the unit circle of the J-algebra; separated from $\mathbb{Q}/\mathbb{Z}$ by a connected one-parameter generator $J$ (continuous over ℝ; discrete $\mathbb{Z}/n$ shadow = `ForceComplexCarrier.Cyc n`) | [INTERPRETIVE — standard $SO(2)=U(1)$; discrete shadow mechanized] | §4 |
| QM-062-C8 | **The conditional forcing:** conjugation (L1) ∧ abelian (L2, ⇒ no ℍ) ∧ continuous reversible pairing-preserving transport (L3) ⇒ ℂ/U(1) at the two-level core | [INTERPRETIVE — synthesis over MECHANIZED L1–L3] | §5 |
| QM-062-C9 | **Imported residue 1:** continuity of reversible dynamics (a connected one-parameter flow exists) | [IMPORTED] | §5 |
| QM-062-C10 | **Imported residue 2:** global field-uniqueness across $n$ (ℝ excluded for $n>2$) — local tomography (Hardy/Masanes–Müller) + Renou et al. 2021 empirical falsification | [IMPORTED] | §5 |
| QM-062-C11 | OB-U1 is **sharpened, not discharged**: complex structure forced+mechanized at the 2-level core; residual import named; NOT "ℂ from nothing"; mints no authority | [SCOPE FENCE] | §5, non-claims |

Definition-as-theorem audit
---------------------------

PASSED. The mechanized claims (C2, C3, C5, C6) are genuine theorems in two Lean files (each
`#print axioms`-audited; several axiom-free, the rest ⊆ `{propext, Quot.sound}`), not relabeled
definitions: T-FORCE-★ is a both-directions dichotomy with witnesses; the exclusions are real
non-vacuous facts on inhabited fibers; `J^2=-I` and `cx_mul` are computed/proved identities;
`cx_injective` reads coordinates. The synthesis (C8) and the $U(1)$ reading (C7) are correctly typed
`[INTERPRETIVE]`; the imports (C9/C10) are correctly `[IMPORTED]`; C4 honestly fences the residual
non-uniqueness Layer 2 cannot close. No inflation — explicitly NOT "ℂ derived."

Support ledger (Part C — upgrade paths)
---------------------------------------

| ID | What would upgrade it | Difficulty | Lean/numerical? | Obligation |
|---|---|---|---|---|
| QM-062-C7 | Remaining half: the ℂ (not just ℤ[i]) ring iso (+ the `rot_mul` matrix form, if wanted). The continuous $SO(2)=U(1)$ angle-addition half was **discharged 2026-06-22** — recursion cycle 005 mechanized `QM.U1Transport` (`phase_add`, `phase_zero`, `norm_phase`, `u1_one_parameter`; [index:index:U1AngleAddition.lean](omega_engine/research/_indexes/_master_index.yaml), realized via `Circle`/`Complex.exp` rather than `rot_mul`), hardened by cycle 006's torsion exclusion (`QM.U1Torsion.kernel_infinite`/`nonconstant`; [index:index:U1TorsionExclusion.lean](omega_engine/research/_indexes/_master_index.yaml)). Continuity itself stays IMPORTED (C9) | Low–Medium (needs Mathlib Complex) | LEAN4 | PL-QM046-1 (angle-addition half discharged, cycles 005/006; remainder hardening, NOT honesty-gating — the algebra is mechanized over ℤ[i]) |
| QM-062-C9/C10 | Discharge an import: derive continuity of reversible dynamics, or derive global field-uniqueness without local tomography | Hard / research | Prose then LEAN4 | research horizon; deliberately OUT OF SCOPE (the named residue / the firewall) |

**No honesty-gating open obligations.** The load-bearing forced claims (C2, C3, C5, C6) are MECHANIZED;
the synthesis (C8) is correctly INTERPRETIVE and explicitly conditional; the residue (C9/C10) is
correctly IMPORTED and named. PL-QM046-1's angle-addition half was discharged 2026-06-22 (recursion
cycles 005/006: [index:index:U1AngleAddition.lean](omega_engine/research/_indexes/_master_index.yaml) + [index:index:U1TorsionExclusion.lean](omega_engine/research/_indexes/_master_index.yaml)); the remaining ℂ-ring-iso half is a
green-upgrade whose algebraic content is already mechanized over ℤ[i]. Neither cycle changes the C8/C9/C10
typing. The selector is **sharpened, not claimed discharged.**

<!-- claim-id-body-only-sync:begin -->

Body-only ID sync (packaging)
-----------------------------

**AuthorityEffect:** None. Packaging hygiene; no OPEN→PROVED.

| ID | Claim | Type | Status |
|---|---|---|---|
| QM-U1SELECTOR-046 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |

<!-- claim-id-body-only-sync:end -->
