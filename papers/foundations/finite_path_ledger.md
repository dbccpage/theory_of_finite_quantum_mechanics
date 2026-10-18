Claim Ledger — Paper QM_031: Finite Path-Sum as Graded Transport (OMEGA-QM-PATHSUM-042)
=======================================================================================

**Paper Key:** `003_quantum_foundations/031_finite_path_sum_as_graded_transport`  

Date: 2026-06-19
Version: v0.1.0 Pre-Print
Series: qm / QM ingredient ladder — **synthesis rung** (was "rung 9 — path-sum/unitary dynamics"; unitary dynamics is NOT derived here)
Companions: pub-010 (the probability stand), pub-005 (CPTP/trace-norm boundary), QM_082 (channels), QM_060 (superposition fiber), QM_061 (interference), QM_090 (continuum lift), QM_010 (mechanized finite-shadow, ENC-1072)

Firewall note: QM is a realization spine. No authority minted. `StructureDerived(F,c) ⇏ IsAuth(t)`.

Paper character: a **synthesis + position paper over already-proven components.** It (i) keeps the
elementary graded-transport skeleton (the path-sum identity, **MECHANIZED** as ENC-1128; graded
finite-shadow realization MECHANIZED as ENC-1072), (ii) decomposes the Feynman path integral into three separable layers
(skeleton / phase lift / imported continuum), and (iii) takes a **fenced stand on what probability is
in QM** whose load-bearing clauses are all reuse of pub-010's proven theorems, with Born-quadratic
uniqueness explicitly imported (the firewall against an origin overclaim). No new theorem machinery.

Claim index
-----------

| ID | Claim (abbreviated) | Status | Location |
|---|---|---|---|
| QM-031-C1 | Carrier = finite weighted transition matrix $M$ over a commutative semiring (commutativity a simplifying convenience) | [DEFINITION] | §1 |
| QM-031-C2 | Primitive difference = direct vs composite multi-step weight; resolved by Chapman–Kolmogorov | [DEFINITION] | §2 |
| QM-031-C3 | ZeroRel: equal path-sums identify accounts (Omega bookkeeping, NOT theorem payload) | [DEFINITION / OMEGA BOOKKEEPING] | §3 |
| QM-031-C4 | $n$-step propagator = $M^n$; path-sum = its length-$n$ path expansion | [DEFINITION] | §4 |
| QM-031-C5 | **Theorem (§5):** (i) $(M^n)(b\mid a)=\sum_{\text{len-}n}\prod M$; (ii) $M^{m+n}=M^m M^n$ | [index:PROVEN, MECHANIZED — ENC-1128, [index:FinitePathSum.lean](omega_engine/research/_indexes/_master_index.yaml): `pathSum_eq_matpow` + `matpow_compose`, axiom-clean on the standard Mathlib set]; graded finite-shadow realization also MECHANIZED (ENC-1072, `Classical.choice`-free) | §5 |
| QM-031-C6 | Worked example: swap $M$, $M^2=I$, $M^3=M$ (weighted-walk counts) | [WORKED EXAMPLE] | §5 |
| QM-031-C7 | §5 is the finite **shadow** of "sum over histories," NOT the Feynman integral (which needs layers 2–3) | [SCOPE FENCE] | §5 |
| QM-031-C8 | **Three-layer decomposition thesis:** Feynman path integral = graded skeleton + phase lift + imported continuum | [INTERPRETIVE] | Abstract, §1–§8 |
| QM-031-C9 | **Phase lift = the only non-classical step:** superposed phase is the quotient fiber (QM_060); interference (cross term) is the non-L1 resource | [reuse — QM_060; pub-010 Thm 7 / QM_061, MECHANIZED] | §6 |
| QM-031-C10 | $\mathbb C$/$U(1)$ phase carrier is imported (open $U(1)$-selector), not derived | [IMPORTED] | §6 |
| QM-031-C11 | **STAND clause 1:** probability = L1 normalization $P=w/\sum w$ (no Hilbert needed) | [STANDARD / reuse — pub-010 Thm 1, PROVEN+MECHANIZED] | §7.1 |
| QM-031-C12 | **STAND clause 2:** Born square is redundant re-encoding ($|c|^2/\sum|c|^2 = w/\sum w$) | [PROVEN, MECHANIZED — reuse pub-010 Thm 4] | §7.2 |
| QM-031-C13 | **STAND clause 3:** quantum surplus = phase/interference (dynamics), not the probability rule | [PROVEN, MECHANIZED — reuse pub-010 Thm 7 / QM_061] | §7.3 |
| QM-031-C14 | **STAND clause 4 (the firewall):** Born-*quadratic* uniqueness is IMPORTED (Gleason), not derived | [IMPORTED — pub-010 Thm 6; Gleason 1957] | §7.4 |
| QM-031-C15 | **The stand (framing):** QM probability is classical L1 normalization; Born square redundant; quantum surplus is phase, not probability — a *position* over C11–C14, NOT an origin/derivation claim | [INTERPRETIVE] | §7 |
| QM-031-C16 | Continuum path integral is the imported analytic lift (measure + convergence, `OracleNeeded`) | [SCOPE FENCE / IMPORTED] | §8 |
| QM-031-C17 | Readout: CPTP induces a column-stochastic **population shadow** after basis choice + diagonal read (does NOT determine the full channel) | [reuse — QM_082] | §9 |
| QM-031-C18 | NOT the continuum integral; complex/unitary amplitudes not forced; Born not derived & its uniqueness imported; stand is NOT "probability explained away / non-fundamental"; mints no authority | [SCOPE FENCE] | §0, §11, non-claims |

Definition-as-theorem audit
---------------------------

PASSED. The only native theorem (C5) is genuine (path-sum identity + Chapman–Kolmogorov; elementary
induction), now **MECHANIZED** (ENC-1128, [index:index:FinitePathSum.lean](omega_engine/research/_indexes/_master_index.yaml)) with an additional
`Classical.choice`-free graded finite-shadow realization (ENC-1072). C8/C15 (the
decomposition and the stand) are explicitly typed `[INTERPRETIVE]` — positions over proven
components, NOT theorems. The stand's load-bearing clauses C11–C13 are reuse of pub-010's
PROVEN+MECHANIZED Thms 1/4/7; the origin-overclaim is firewalled by C14 (Born uniqueness IMPORTED).
No inflation; no definition wearing theorem clothes.

Support ledger (Part C — upgrade paths)
---------------------------------------

| ID | What would upgrade it | Difficulty | Lean/numerical? | Obligation |
|---|---|---|---|---|
| ~~QM-031-C5~~ | ~~Mechanize `pathSum_eq_matpow`, `matpow_compose` (`FinitePathSum.lean`)~~ → **DONE 2026-06-19**: landed general over any finite index type + `CommSemiring` (`pathSum_eq_matpow`, `matpow_compose`, `matpow_compose_apply`, `pathSum_compose`, swap replay), axiom-clean; ENC-1128 now MECHANIZED | — | LEAN4 | ~~**PL-QM042-1**~~ **DISCHARGED** |
| QM-031-C14/C15 | Deriving Born-quadratic uniqueness from L1 additivity *without* the Gleason-type imports would upgrade the stand from "position" to "derivation" (and would change clause 4) | Hard / research-level | Prose then LEAN4 | research horizon; deliberately OUT OF SCOPE (the firewall) |

**No honesty-gating open obligations.** The stand's components (C11–C13) are MECHANIZED reuse; C5 is
now MECHANIZED (ENC-1128, [index:index:FinitePathSum.lean](omega_engine/research/_indexes/_master_index.yaml); **PL-QM042-1 DISCHARGED 2026-06-19**); the
stand (C15) is correctly INTERPRETIVE and explicitly fenced against the origin overclaim by C14.
