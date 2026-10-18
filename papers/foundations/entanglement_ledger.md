Claim Ledger — Paper QM_071: Entanglement as a Separability Obstruction (OMEGA-QM-SEP-OBS-036)
==============================================================================================

**Paper Key:** `003_quantum_foundations/071_entanglement_as_a_separability_obstruction`  

Date: 2026-06-17
Version: v0.1.0 Pre-Print
Series: qm / QM ingredient ladder (rung 8B)
Companions: QM_070 (rung 8A, product non-factorization), pub-001 (factorized states), pub-010 (voice)

Firewall note: QM is a realization spine. This paper mints no authority; the green/red firewall
is a finite structural fact about the declared product family. `StructureDerived(F,c) ⇏ IsAuth(t)`.

Paper character: a finite obstruction-calculus derivation with one mechanized theorem (ENC-1124,
entanglement-witness soundness). Honestly scoped: **soundness only** (a witness ⟹ entangled),
**relative to a declared finite product family** — NOT general separability, NOT completeness.

Claim index
-----------

| ID | Claim (abbreviated) | Status | Location |
|---|---|---|---|
| QM-071-C1 | Carrier = finite rational state vector incl. off-diagonal/coherence coordinates | [DEFINITION] | §1 |
| QM-071-C2 | Descent: bipartite QM state → finite coordinate vector | [DEFINITION / SCOPE FENCE] | §1 |
| QM-071-C3 | Separability defect $\delta_{\mathrm{sep}}=w-\sum_k\lambda_k P_k$ ($\lambda\ge0$, $\sum=1$) | [DEFINITION] | §2 |
| QM-071-C4 | ZeroRel: a finite separable-decomposition witness exists ($w\in\operatorname{conv}(P)$) | [DEFINITION] | §3 |
| QM-071-C5 | **Theorem (witness soundness):** separating $\varphi$ ($\varphi(P_k)\ge t$, $\varphi(w)<t$) ⟹ $w$ not $P$-separable | [PROVEN] — mechanized `witness_certifies_not_separable`, ENC-1124 | §5, §8 |
| QM-071-C6 | Witnesses: `uniform_separable` (convex mix separable); `zero_not_separable` (all-ones $\varphi$ separates zero vector) | [PROVEN] — mechanized | §8, worked example |
| QM-071-C7 | P-nonseparability = no separable decomposition in the declared convex product hull | [DEFINITION] | §3, §11 |
| QM-071-C8 | Local product-respecting maps don't create entanglement (product-preservation); general monotonicity NOT claimed | [PROVEN — elementary] + [SCOPE FENCE] | §9 |
| QM-071-C9 | Soundness only; completeness (every entangled state has a witness) NOT claimed | [SCOPE FENCE] | §5, §12, non-claims |
| QM-071-C10 | Relative to a DECLARED finite family; not general separability (hard) | [SCOPE FENCE] | §1, §12, non-claims |
| QM-071-C11 | Green/red firewall; mints no authority | [SCOPE FENCE] | §11 |
| QM-071-C12 | Comparison: entanglement-witness theorem (Horodecki; Gühne–Tóth); CHSH one instance | [INTERPRETIVE] — citations | §12 |
| QM-071-C13 | Falsifiability: a separable state with a valid separating witness; or "entangled" from an incomplete search | [SCOPE FENCE / FALSIFIABILITY] | Falsifiability |

Definition-as-theorem audit
---------------------------

PASSED. The single Theorem (C5) is genuinely a theorem (a soundness implication), mechanized;
its proof is one-line (convex-combination linearity + nonneg weights). C7 (entanglement =
non-membership) is explicitly typed `[DEFINITION]`, not dressed as a theorem. No inflation.

Support ledger (Part C — upgrade paths)
---------------------------------------

| ID | What would upgrade / extend it | Difficulty | Lean/numerical? | Obligation? |
|---|---|---|---|---|
| QM-071-C9 | **Completeness converse**: every non-separable state (rel. declared hull) admits a separating witness — the Hahn–Banach / finite-LP-duality direction. | Medium (finite LP duality) to Hard (general) | Prose + Lean | Research-level upgrade; **NOT honesty-gating** (soundness stands; completeness explicitly not claimed) |
| QM-071-C7 | Density-matrix instantiation: a richer declared product family + a Bell-state-vs-product witness with the off-diagonal carrier (the case QM_070's diagonal table could not see) | Medium — engineering | Numerical / Lean | Reproducibility target, not honesty-gating |
| QM-071-C12 | Resolved entanglement-witness citations (Horodecki separability criteria; Gühne–Tóth detection review) | Low | Misc (citation) | Resolved |

**No honesty-gating open obligations.** C5/C6 are mechanized (ENC-1124); C7/C9/C10/C11 are scope
fences; C8 is the proved product-preservation + a fence; C12 is interpretive. The completeness
converse and the density-matrix instantiation are deliberately out of scope here (claiming them
would misstate the paper).
