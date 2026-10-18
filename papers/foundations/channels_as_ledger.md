Claim Ledger — Paper QM_082: Channels as Stochastic Kernels and the CPTP Lift (OMEGA-QM-CHAN-STOCH-041)
=======================================================================================================

**Paper Key:** `003_quantum_foundations/082_channels_as_stochastic_kernels_and_the_cptp_lift`  

Date: 2026-06-17
Version: v0.1.0 Pre-Print
Series: qm / QM ingredient ladder (rung 4: channels / stochastic kernels / CPTP population shadows)
Companions: QM_007 (rung 3, diagonal density), pub-005 and QM_081 (CPTP/trace-norm), pub-010 (voice)

Firewall note: QM is a realization spine. No authority minted. `StructureDerived(F,c) ⇏ IsAuth(t)`.

Paper character: a finite obstruction-calculus derivation. One theorem (ENC-1127), **MECHANIZED**
(2026-06-19; [index:index:StochasticChannel.lean](omega_engine/research/_indexes/_master_index.yaml), PL-QM041-1 discharged).

Claim index
-----------

| ID | Claim (abbreviated) | Status | Location |
|---|---|---|---|
| QM-082-C1 | Carrier = finite outcome distributions (rung-3 diagonal densities) | [DEFINITION] | §1 |
| QM-082-C2 | Classical channel = stochastic kernel $K\ge0$, unit column sums | [DEFINITION] | §4, §5 |
| QM-082-C3 | ZeroRel: identity kernel fixes the simplex; kernels equal iff equal on simplex | [DEFINITION] | §3 |
| QM-082-C4 | **Theorem:** (i) $K$ preserves states; (ii) $K\circ L$ stochastic (channels compose, monoid); (iii) CPTP ($\sum A_k^\dagger A_k=I$) induces a column-stochastic **output-diagonal population shadow** $K$ — does NOT preserve diagonality (may create output coherences) and does NOT determine the channel | [PROVEN, MECHANIZED] — ENC-1127 (MECHANIZED); [index:index:StochasticChannel.lean](omega_engine/research/_indexes/_master_index.yaml) | §5, §8 |
| QM-082-C5 | Worked example: bit-flip kernel preserves $(3/4,1/4)\to(1/4,3/4)$, $K\circ K=I$; CPTP $X\rho X$ induces it | [WORKED EXAMPLE] | Worked example |
| QM-082-C6 | **CP / coherence transport is the non-forced lift** — not implied by the classical kernel | [SCOPE FENCE] | §6, §9 |
| QM-082-C7 | Induced stochastic kernel is basis-relative | [INTERPRETIVE] | §7 |
| QM-082-C8 | Kraus/Choi/Stinespring are certified-transport equivalents (CODA-MUR-Q pentagon) | [INTERPRETIVE] | §9, §12 |
| QM-082-C9 | NOT a CPTP-as-ontology derivation; CP not forced; **CPTP monotonicity alone does not uniquely select the trace-norm gauge** (pub-005) | [SCOPE FENCE] | §11, non-claims |
| QM-082-C10 | Green/red firewall; mints no authority | [SCOPE FENCE] | §11 |
| QM-082-C11 | Comparison: stochastic matrices, data-processing/CPTP monotonicity, pub-005 | [INTERPRETIVE] | §12 |

Definition-as-theorem audit
---------------------------

PASSED. Theorem (C4) is genuine (state-preservation + composition + CPTP-descent); proof one line
per part. C2/C3 `[DEFINITION]`. Status **MECHANIZED** ([index:index:StochasticChannel.lean](omega_engine/research/_indexes/_master_index.yaml), 2026-06-19). No inflation.

Support ledger (Part C — upgrade paths)
---------------------------------------

| ID | What would upgrade it | Difficulty | Lean/numerical? | Obligation |
|---|---|---|---|---|
| ~~QM-082-C4~~ | ~~Mechanize `stochastic_*`, `kraus_diagonal_stochastic`~~ → **DONE 2026-06-19** ([index:index:StochasticChannel.lean](omega_engine/research/_indexes/_master_index.yaml); ENC-1127 MECHANIZED; Kraus at population level) | — | LEAN4 | ~~**PL-QM041-1**~~ **DISCHARGED** |
| QM-082-C6 | The CP lift proper: when off-diagonal/coherence transport is admissible (the CPTP structure above the classical kernel) — the harder rung | Medium | Prose + Lean | research-level; out of scope here |

**No honesty-gating open obligations.** C4 **MECHANIZED** (`StochasticChannel.lean`; PL-QM041-1 discharged 2026-06-19); formerly a hardening
target. C6–C11 are fences/interpretive.
