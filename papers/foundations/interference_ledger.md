Claim Ledger — Paper QM_061: Interference as the Non-L1 Resource and the Buildability Set S (OMEGA-QM-INTERFERE-044)
====================================================================================================================

**Paper Key:** `003_quantum_foundations/061_interference_as_the_non_l1_resource`  

Date: 2026-06-18
Version: v1.0 (authored with the paper at v0.1.0)
Series: qm / QM ingredient ladder (rung 7 — interference) + buildability criterion

Companions: pub-010 (interference cross term), QM_060 (the phase fiber), QM_007 (L1/diagonal layer),
QM_101 (threshold theorems credited), QM_061 (Track-C stub, completed), QM_091 (firewall).

Firewall note: QM is a realization spine. No authority minted. `StructureDerived(F,c) ⇏ IsAuth(t)`.

Encyclopedia: secured as **ENC-1135** (`paper:qm061:INTERFERE-001`, MECHANIZED, 2026-06-19) — A1
(reuse of pub-010 Thm 7 / ENC-0318), A2 (coboundary holonomy), and the Part-B buildability criterion
$S$ (B1 `useful_qc_iff_setS`, B2 `S*_necessary`, B3 `setS_satisfiable`). The C8 holonomy *reading* stays
INTERPRETIVE (PL-QM044-1 TARGETED).

Paper character: **mixed — Part A interference is REUSE; Part B set-S is new.** Part A's
interference-not-L1 (C4) is **pub-010 Theorem 7** re-packaged (same `(1,1)`/`(1,−1)`
witness; pub-010 mechanizes it far more in `PaperQF002.L010_01_BornRedundancy`) — NOT a
novel result. The genuinely new content is C8 (the *holonomy* reading, INTERPRETIVE) and
Part B (the set-`S` iff). [index:index:interferencebuildability.lean](omega_engine/research/_indexes/_master_index.yaml) re-mechanizes the
load-bearing claims as a self-contained zero-import kernel for the buildability bundle
(lean 4.31.0-rc1, RC 0, axioms ⊆ {propext, Quot.sound}; 5 theorems axiom-free). Two
imported inputs stay cited hypotheses (phase carrier; λ_gen / LR cone). (2026-06-18:
credited pub-010 Thm 7 as A1's source after a cold re-read of the original — was
overstated as "new, not a reuse".)

Claim index
-----------

| ID | Claim (abbreviated) | Status | Location |
|---|---|---|---|
| QM-061-C1 | Carrier = sector amplitudes; L1 = diagonal Born weights $|c_s|^2$ (QM_007) | [DEFINITION] | §1 |
| QM-061-C2 | Primitive difference phase-blind on diagonal weights (pub-010); ZeroRel = L1-equivalence | [DEFINITION] | §2, §3 |
| QM-061-C3 | Interfered weight $\mathcal I(c)=|\sum c_s|^2$; deviation = cross term $\sum_{i\neq j}c_i^*c_j$ (pub-010 T7) | [DEFINITION] | §4 |
| QM-061-C4 | **Theorem A1:** no L1 functional computes $\mathcal I$; L1-equivalent configs can differ in interference | **[PROVEN, MECHANIZED — REUSE of pub-010 Thm 7]**; re-packaged zero-import as `L1_cannot_compute_interference` (same `(1,1)`/`(1,−1)` witness; pub-010's `twoRowMix*` is the fuller mechanization) — not novel | §5 |
| QM-061-C5 | Worked example $(1,1)$ vs $(1,-1)$: same L1, interfered 4 vs 0; cross $+2$ vs $-2$ | [WORKED EXAMPLE — `cPlus_cMinus_*`, decided] | §5 |
| QM-061-C6 | A1 is the finite form of RDB-03 (diagonal layer cannot carry interference) and is *compatible with* the Holevo lesson — but is **not** a derivation/finite-version of Holevo's theorem (A1 = non-identifiability; Holevo bounds accessible information) | [STANDARD — RDB-03; Holevo-*compatible*, not Holevo] | §5 |
| QM-061-C7 | **Theorem A2:** a coboundary (gauge) phase has zero holonomy around any closed walk | [PROVEN, MECHANIZED — `coboundary_loop_zero_holonomy` (LT-P)] | §6 |
| QM-061-C8 | Reading: interference resource = non-coboundary $H^1$ holonomy (argued from A1+A2, not one theorem) | [INTERPRETIVE] | §6 |
| QM-061-C9 | The $\mathbb C$/$U(1)$ phase carrier is imported (open $U(1)$-selector), not derived | [IMPORTED] | §6 |
| QM-061-C10 | Useful = working AND advantageous (carries the Part-A resource); else classically simulable | [SCOPE FENCE / DEFINITION] | §7 |
| QM-061-C11 | Set $S$ = $S_1$ race ∧ $S_2$ floor ∧ $S_3$ reachability ∧ $S_4$ advantage($H^1$ resource) | [DEFINITION] | §8 |
| QM-061-C12 | **Theorem B1 (finite buildability-predicate equivalence):** *inside the declared finite model*, the `UsefulQC` predicate ⟺ $S$; content = the biconditional Bounded ⟺ step ≤ 0. A packet criterion over declared predicates, NOT a physical existence theorem. | [PROVEN, MECHANIZED — `useful_qc_iff_setS`, `bounded_iff_step_nonpos`] | §9 |
| QM-061-C13 | **Theorem B2:** each $S_i$ independently necessary (drop-one witnesses) | [PROVEN, MECHANIZED — `S1_necessary`…`S4_necessary`] | §9 |
| QM-061-C14 | **Theorem B3:** $S$ satisfiable — criterion, not a no-go | [PROVEN, MECHANIZED — `setS_satisfiable`] | §9 |
| QM-061-C15 | $S$ members are declared conditions; B1 is a finite criterion, not a proof any device satisfies $S$; race uses imported λ_gen (PAPER001) + LR cone | [CONDITIONAL / SCOPE FENCE] | §9 |
| QM-061-C16 | Threshold theorems can be *read as* architecture-specific $S$-witnesses under their own hypotheses (NOT "=" the $S$-regime; $S$ is a unifying audit schema); $S$ is a two-sided finite criterion *corresponding to* the QM_061 Track-C stub (not a completion of the threshold literature); make-or-break read as $S_1\cap S_4$ | [INTERPRETIVE] | §10 |
| QM-061-C17 | NOT BQP⊆P, NOT efficient classical sim, NOT QC-impossible, NOT interpretation-deciding; mints no authority | [SCOPE FENCE] | §"What this does not claim" |

Definition-as-theorem audit
---------------------------

PASSED. The four theorems (A1, A2, B1, B2/B3) are genuine and **mechanized**, not relabeled
definitions: A1/A2 are `¬∃`/telescoping facts with explicit witnesses; B1's content is the real
biconditional `bounded_iff_step_nonpos` (not the shared declared flags); B2 is non-vacuous (drop-one
counter-witnesses). The interference=$H^1$-holonomy *reading* (C8) is correctly typed `[INTERPRETIVE]`,
not `[PROVEN]` — it is argued from A1+A2, not a single closed-form theorem. No inflation.

Support ledger (Part C — upgrade paths)
---------------------------------------

| ID | What would upgrade it | Difficulty | Lean/numerical? | Obligation |
|---|---|---|---|---|
| QM-061-C8 | A closed-form theorem `cross = g(holonomy)` linking the numerical cross term to the holonomy value | Medium (needs the continuum cosine / a discrete surrogate) | LEAN4 | PL-QM044-1 (TARGETED; not honesty-gating — A1+A2 already mechanized) |
| QM-061-C15 | A specific architecture packet discharging $S_1$–$S_4$ with replayable evidence (would instantiate B1, not strengthen it) | Architecture-scale | Numerical/packet | PL-QM044-2 (not honesty-gating; an instantiation, not a gap) |

**No honesty-gating open obligations.** The load-bearing claims (A1, A2, B1, B2, B3) are MECHANIZED
and axiom-clean. C8 is correctly INTERPRETIVE; C9/C15 are IMPORTED/CONDITIONAL fences; C16/C17 are
interpretive/scope fences. The two support entries are upgrades/instantiations, not open gaps.
