Claim Ledger — Paper QM_060: Superposition as the Quotient Fiber (OMEGA-QM-SUPERPOS-043)
========================================================================================

**Paper Key:** `003_quantum_foundations/060_superposition_as_the_quotient_fiber`  

Date: 2026-06-17
Version: v0.1.0 Pre-Print
Series: qm / QM ingredient ladder (phase-fiber rung)
Companions: pub-010 (lift redundancy / row-sparsity / cross term), QM_070 (phase-blind quotient)

Firewall note: QM is a realization spine. No authority minted. `StructureDerived(F,c) ⇏ IsAuth(t)`.

Paper character: a **reuse / synthesis** of pub-010. One entry (ENC-1129), **PROVED-PROSE** by reuse;
the constituents are **MECHANIZED in pub-010** (`PaperQF002.L010_01_BornRedundancy`). A dedicated
superposition Lean is optional (PL-QM043-1, TARGETED, NON-BLOCKING).

Claim index
-----------

| ID | Claim (abbreviated) | Status | Location |
|---|---|---|---|
| QM-060-C1 | Carrier = residual weights $w$; superposition = lift $c_\gamma=\sqrt{w_\gamma}e^{i\theta_\gamma}$ | [DEFINITION] | §1 |
| QM-060-C2 | Phase-blind $\delta(c,c')_\gamma=|c_\gamma|^2-|c'_\gamma|^2$; ZeroRel identifies equal-modulus lifts (any phase) | [DEFINITION] | §2, §3 |
| QM-060-C3 | Quotient base = weights; fiber = phases over a weight point | [DEFINITION] | §4 |
| QM-060-C4 | **Theorem (reuse):** (i) $|c|^2=w$ redundant (pub-010 T4); (ii) phase $\in\ker\delta$ quotient-invisible (T3); (iii) phase reappears as mixing cross term (T7) ⟹ superposition = quotient fiber | [PROVEN — prose, reuse of pub-010] — ENC-1129; constituents MECHANIZED in pub-010 | §5, §8 |
| QM-060-C5 | Worked example: $(1,1)$ vs $(1,-1)$ — same law/quotient point, different fiber, distinguished only under mixing | [WORKED EXAMPLE] | Worked example |
| QM-060-C6 | Fiber carries no probability mass; its content is the interference cross term (rung 7) | [SCOPE FENCE] | §6 |
| QM-060-C7 | Superposition observer-relative (phase-blind base vs mixing observer) | [INTERPRETIVE] | §7 |
| QM-060-C8 | NOT a derivation of Hilbert/unitarity/Born-as-ontology (pub-010 T6 imports those); phase not "physical" beyond packet-distinguishable effects | [SCOPE FENCE] | §11, non-claims |
| QM-060-C9 | Green/red firewall; reuse not new machinery; mints no authority | [SCOPE FENCE] | §11 |

Definition-as-theorem audit
---------------------------

PASSED. The Theorem (C4) is genuine but explicitly a **reuse/synthesis** of pub-010's PROVEN +
MECHANIZED Thms 3/4/7; typed `[PROVEN — prose, reuse]`, not claimed as new. No inflation.

Support ledger (Part C — upgrade paths)
---------------------------------------

| ID | What would upgrade it | Difficulty | Lean/numerical? | Obligation |
|---|---|---|---|---|
| QM-060-C4 | Optional: a dedicated [index:index:SuperpositionFiber.lean](omega_engine/research/_indexes/_master_index.yaml) re-packaging pub-010's redundancy + cross term as the "fiber" statement | Low (re-packaging) | LEAN4 | PL-QM043-1 (TARGETED; **optional** — constituents already MECHANIZED in pub-010) |

**No honesty-gating open obligations.** The content is pub-010's (PROVEN + MECHANIZED); this paper
names it as the quotient fiber. C6–C9 are fences/interpretive.
