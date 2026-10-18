# Claim Ledger — Paper QM-212 — The Microsoft Majorana Problem

**Paper Key:** `003_quantum_foundations/212_microsoft_majorana_problem`  

**Paper:** `qm_212_microsoft_majorana_problem.md`  
**Publication folder:** `omega_engine/research/published/003_quantum_foundations/qm_212_microsoft_majorana_problem/`  
**Series degree:** δ212  
**Ledger date:** 2026-08-01  
**Canonicality:** mirrors the paper's claim-id body index.  
**Authority:** none.

---

## 1. Claim registry

| ID | Claim | Type | Basis / notes |
|---|---|---|---|
| QM_212-C1 | Microsoft Majorana Problem = packet gap between hardware narratives and declared finite algebra | [DEFINITION / CONSTRUCTION] | §0.2 Def 0.1 |
| QM_212-C2 | GF(2) residual trichotomy (Exact / ClosedResidual / OpenObstruction) under $d_1 d_0=0$ | [DERIVED] elementary homology | §1 Thm 1; CODE_DEMO `omega_majorana` |
| QM_212-C3 | Classification decidable by GF(2) Gaussian elimination on finite dims | [CODE_DEMO + PROSE] | §1 Thm 2; Lean polytime residual |
| QM_212-C4 | Refuse classification when $d_1 d_0\neq 0$ | [DERIVED] | §1 Prop 3 |
| QM_212-C5 | Multi-plaquette surface toys are CODE_DEMO only; not thresholds/device packets | [SCOPE FENCE] | §2; links QM_101 THR-001 open |
| QM_212-C6 | Kitaev $H$ / phase table are imported condensed-matter context | [SCOPE FENCE] | §3.1; archive §2 |
| QM_212-C7 | Ising fusion + specialized $\mathbb{Q}(\zeta_{16})$ identities are declared algebra checks, not full MTC/physics | [CODE_DEMO + SCOPE FENCE] | §3.2; archive §5–5A |
| QM_212-C8 | $\mathbb{Z}_2$ parity bookkeeping ≠ experimental capacitance validation | [SCOPE FENCE] | §3.3 |
| QM_212-C9 | Local Majorana/Pfaffian positivity ≠ generic FSP solved | [SCOPE FENCE] | §3.4; programme 013 |
| QM_212-C10 | Hardware narratives quarantined as observer projections | [Q-HELD / SCOPE FENCE] | §5 Stm 5 |
| QM_212-C11 | LGGR on torus residual: local closed ≠ global trivial $H^1$ | [DERIVED toy] | §5 Stm 6; `surface_grid_2x2_torus` |
| QM_212-C12 | Tetron-array carriers realise $\dim H^1=0,1,2$ for disk / cylinder / torus, measured as $(E-\operatorname{rank} d_1)-\operatorname{rank} d_0$ and cross-checked against $(2\ \text{if closed else}\ 1)-\chi$ | [CODE_DEMO + DERIVED] | §2.3; `surface_carrier.py`, `tetron.rs`; mutation-killed |
| QM_212-C13 | **Self-correction.** The previous `tetron_carrier.py` has $\dim H^1=0$ at every size $T=1..4$ despite graph cycle rank $T-1$; every closed residual on it is `Exact` by construction, so it cannot exhibit a logical class | [CODE_DEMO / RETRACTION OF CARRIER] | §2.3; supersedes the earlier carrier |
| QM_212-C14 | Code distance: torus $=\min(\text{rows},\text{cols})$, cylinder $=\text{rows}+1$, disk none. Per-class minimum weights on $3\times4$ torus are $3$, $4$, $7=3+4$ | [CODE_DEMO] | §2.3; mutation-killed (min→max) |
| QM_212-C15 | $\Phi_1$ over GF(2) is the minimum-weight coset representative, i.e. syndrome decoding: NP-hard in general, MAX-CUT on the signed channel graph. The implementation is $2^{\operatorname{rank} d_0}$ and budget-capped; a capped search is an **upper bound**, and the terminal degrades `TypedHarmonic`→`ClosedResidual` rather than claiming exactness | [DERIVED + COMPLEXITY FENCE] | §2.3 |
| QM_212-C16 | The split (`Exact`/`ClosedResidual`/`OpenObstruction`) is polynomial — GF(2) Gaussian elimination, 17 ms/residual at torus $6\times6$ | [CODE_DEMO] | §2.3 |
| QM_212-C17 | **No $\ell^1$-vs-$\ell^2$ separation on any GF(2) parity carrier.** $\lVert v\rVert_p^p=\operatorname{wt}(v)$ for every $p$ on $\{0,1\}$ entries, so the two minimisations are identical at every Betti number; $\dim H^1\ge2$ buys **class typing**, not a norm gap | [DERIVED / NON-CLAIM] | §2.3; Non-claim N7 |

---

## 2. Ledger controls

* Source-qualified claim count: **17**.  
* No claim upgrades FOC ExactRepair, AuthorityEffect, PROVED, or vendor endorsement.  
* Provenance: rewrite of archive `023 - Majorana Topological QC/v003/majorana_topological_qc_v003.md` under estate fences.  
* Mechanization: Rust CODE_DEMO green (`cargo test -j 1 -p omega_majorana`); Lean `majorana_parity/` **OPEN**.  
* Any mismatch between this ledger and the paper terminalizes as a documentation obstruction until reconciled.
