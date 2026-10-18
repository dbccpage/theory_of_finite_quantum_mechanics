# Majorana GF(2) play ↔ Quantum Computing papers (item 6)

**Date:** 2026-08-01  
**AuthorityEffect:** None  
**Status:** Diagnostic playbook only — not PROVED, not GlobalGreen, not hardware.

## What landed

| Surface | Location | Gate |
|---|---|---|
| Canonical Rust kernel | `omega_engine/crates/omega_majorana` | `cargo test -j 1 -p omega_majorana` → **5/5 pass** |
| Engines compat re-export | `omega_engines::quantum::majorana_gf2_terminalizer` | `pub use omega_majorana::{…}` |
| Python dual-face | `omega_engine_py/omega_majorana` | relocated from root package |
| Root stub | `omega_engine_majorana` | deprecation redirect only |

## Multi-agent swarm verdicts (2026-08-01)

| Agent | Verdict | One-line |
|---|---|---|
| **Red** | ACCEPT_WITH_PATCHES | Thin leaf only; no wholesale demo dump; Auth=None; no dual SOOT |
| **Green** | GO_WITH_GATES | Play API + triangle/plaquette/prism; Artin braid remains Hold |
| **Blue** | Thin leaf owner | `omega_majorana` canonical; engines shim temporary; ODP packet later |
| **math-prof** | CONDITIONAL | GF(2) trichotomy = \(H^1(\mathbb{F}_2)\); Ising = specialized matrices only |
| **physics-prof** | CONDITIONAL_PASS | Discrete FOC fit; no MZM/hardware; cyclotomic = algebraic lift |
| **proofs (DERIV)** | Shared F₂ spine | Nilpotency + trichotomy + Mermin-as-instance; Born is **non-bridge** |
| **refutation** | REJECT_UNTIL_PATCHED (prose) | FOC-identity / Microsoft “Theorem” / audit ACCEPT must not smuggle |

**Narrow conditional core that survives all seven:**

> Declared finite \((C^\bullet,d)\) over \(\mathbb{F}_2\) with \(d_1 d_0=0\), residual \(r\in C^1\):  
> Exact / ClosedResidual / OpenObstruction are **diagnostic schedule labels**, receipt tag `omega.majorana-gf2-receipt.v1`, `authority_effect: "None"`.

## Bridge to `003_quantum_foundations` QC papers

Trend focus and programme README list fault-tolerance + qubit foundations. Map **honestly**:

| Paper | Core thesis (corpus) | Majorana play role |
|---|---|---|
| **qm_102** fault_tolerance_repair_capacity | Error syndromes are \(1\)-cochain coboundary defects on finite graphs over \(\mathbb{F}_2\); repair capacity \(\sim \lfloor(d-1)/2\rfloor\); Local Green ≠ Global Red | **Direct executable shadow:** triangle/plaquette/prism + `terminalize` classify whether a syndrome is coboundary / closed / open — same cochain shape as QM_102 §1, **without** distance-\(d\) threshold claims |
| **qm_101** threshold_theorems_as_repair_capacity | Threshold theorems = conditional repair-capacity certificates (packet THR-001); surface-code packet still open | Play **does not** populate THR-001. It only exercises the residual membership step that a full packet would use for \(s=\delta e\) bookkeeping |
| **qm_072** bit_shadow_and_qubit | Classical 2-state bit → \(\mathcal{H}_2\) under phase fiber; stabilizer/coboundary alone is classically simulable (Gottesman–Knill / QM_061) | GF(2) play is **exactly** the coboundary/stabilizer residual layer. It is **not** the Q2 interference / non-\(\ell^1\) resource. Fence: parity schedule ≠ qubit |
| **qm_091** Deutsch/Everett/Wolfram promotion error | Universal QC claims audited against carrier boundaries | Play must never be read as universal QC or TQ demonstration |

### Homology dictionary (diagnostic only)

| QM_102 / surface-code language | `omega_majorana` label | Not to be read as |
|---|---|---|
| Error \(e\in C^1\), syndrome \(s=\delta^1 e\) | residual / syndrome vector | physical noise process |
| Correctable / coboundary | `Exact` | FOC `ExactRepair` |
| Closed logical / nontrivial cycle | `ClosedResidual` | FOC `StabilizedSurvivor` / logical failure proof |
| Incoherent / not a cocycle | `OpenObstruction` | device “failed” |
| Threshold \(p_{\mathrm{th}}\), distance \(d\) | **absent** | any threshold theorem |

## Play sessions (executable)

```text
cargo test -j 1 -p omega_majorana play_ -- --nocapture
cargo test -j 1 -p omega_majorana play_surface_ -- --nocapture
```

| Session | Complex | Syndrome | Expected class |
|---|---|---|---|
| A | triangle | `[1,1,0]` | Exact |
| B | triangle | `[1,0,0]` | OpenObstruction |
| C | plaquette full cycle | `[1,1,1,1]` | ClosedResidual **or** Exact (rank-dependent; assert fence Auth=None) |
| D | prism | any with \(d_1 d_0=0\) | boundary gate green |
| E | `surface_grid_2x2_planar` | vertex-0 coboundary / single edge | Exact / OpenObstruction (\(H^1=0\) disk) |
| F | `surface_grid_2x2_torus` | `torus_logical_x/z_example` | **ClosedResidual** (nontrivial cocycles) |

## Paper anchor

- **QM_212** — `003_quantum_foundations/qm_212_microsoft_majorana_problem/`  
  Estate rewrite of archive Majorana TQC note; defines the **Microsoft Majorana Problem** as the packet gap between hardware narratives and declared GF(2)/Ising algebra.

## Next play (optional, Auth=None)

1. ~~Surface-code toy plaquette grid~~ — **done** (planar + torus CODE_DEMO).  
2. **DERIV P1–P3** — Lean `majorana_parity/` nilpotency + trichotomy + Mermin instance (proofs agent).  
3. **Vocabulary firewall** — rename public `Exact` → `GF2DiagnosticExact` or mandatory footnote vs FOC (refutation P1).  
4. **qm_102 / qm_212 worked example** — one receipt JSON as CODE_DEMO under paper support, not as threshold certificate.  
5. **Do not** promote Microsoft bridge note or FOC-identity prose without patches.

## Non-claims (binding)

- No physical Majorana zero modes, no Azure/Microsoft endorsement.  
- No surface-code threshold, no scalable FTQC proof.  
- No Born uniqueness, no continuum \(U(1)\), no thimble FSP solution.  
- No AuthorityEffect other than None.
