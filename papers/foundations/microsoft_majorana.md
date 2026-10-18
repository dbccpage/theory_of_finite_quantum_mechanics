# The Microsoft Majorana Problem: Finite Parity Schedules, Ising Algebra, and What Hardware Claims Do Not Discharge

## GTOC Foundations — Quantum Contact Series (qm_212_microsoft_majorana_problem)

**Date:** 2026-08-05 · **Version:** v0.2.0  
**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)  
**Status:** DRAFT (internal)  
**Authority:** `AuthorityEffect::None`  

## Mechanism inventory

| Slot | Value / Description |
| --- | --- |
| **Primitive Differences** | $\delta\omega$ = GF(2) residual / schedule mismatch on declared cochains |
| **Carriers / Structure** | Finite cell complex $C^0\to C^1\to C^2$ over $\mathbb{F}_2$; optional $\mathbb{Q}(\zeta_{16})$ Ising seed |
| **Cochain complex** | $C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$ with $d_1 d_0=0$ |
| **Coboundary maps** | $d_0$ (vertex→edge), $d_1$ (edge→face) |
| **ZeroRel** | Preserved under finite declared carriers |
| **Licensed repairs** | None |
| **Quotient / Q1** | $H^1=\ker d_1/\operatorname{im} d_0$ (diagnostic dimension only) |
| **Residuals** | Edge residual $\omega\in C^1$; face syndrome $s=d_1\omega$ |
| **Witnesses** | `omega_majorana` receipts (`omega.majorana-gf2-receipt.v1`); CODE_DEMO surface grids |
| **Observers / profiles** | Operational / engineering audience (not vendor endorsement) |
| **Anomalons** | None |
| **CompletionLaw** | Finite cochain completion only |
| **Terminal / route** | Route to 003 Quantum Foundations + `omega_majorana` play crate |
| **AuthorityEffect** | None |

document_id: "QM_212"
version: "v0.2.0"
status: "DRAFT"
authority_effect: "None"
mechanization: "CODE_DEMO (omega_majorana surface_grid_2x2_* + GF2 classifier); Lean majorana_parity/ OPEN"
claim_ledger: "qm_212_microsoft_majorana_problem_claim_ledger.md"
change_log: "qm_212_microsoft_majorana_problem_change_log.md"
provenance: "Archive rewrite of research_notes_000/.archive/023 - Majorana Topological QC/v003/majorana_topological_qc_v003.md under 003 honesty fences"

---

QM_212 — The Microsoft Majorana Problem
========================================

**Author:** Jeremy H. Carroll  
**Date:** August 2026  
**Canonical Version:** `v0.2.0`  
**Paper Identity:** `QM_212`  
**Authority:** None. Diagnostic algebra and claim-boundary audit only.

> **Status box (binding)**
>
> **Status:** First estate-native draft. Supersedes the archive note *Topological Quantum Computation as $\ell^1$ Composition* (paper 023 v003) for live navigation under `003_quantum_foundations`.  
> **Core (narrow algebra):** The verifiable *software* side of Majorana / Ising topological-QC talk reduces to (i) finite GF(2) cochain residual classification on a **declared** complex and (ii) exact specialized matrix identities in $\mathbb{Q}(\zeta_{16})$.  
> **The “Microsoft problem”:** Public hardware narratives (Kitaev-wire fabrication, interferometric parity, Azure-facing bridge language) create a **compositional claim gap**: device reports and algebraic diagnostics live on different carriers; neither side automatically discharges the other.  
> **AuthorityEffect:** `None`.

---

## Non-claim Box

> **What this paper does NOT claim:**
>
> 1. Does **not** claim physical Majorana zero modes, topological qubits, or room-temperature topological operation.  
> 2. Does **not** endorse, validate, or partner-certify Microsoft Azure Quantum, InAs–Al devices, or any vendor readout.  
> 3. Does **not** identify GF(2) labels `Exact` / `ClosedResidual` / `OpenObstruction` with FOC `ExactRepair` / `StabilizedSurvivor` / authority terminals.  
> 4. Does **not** solve the generic fermion sign problem (Troyer–Wiese NP-hard regime remains out of scope).  
> 5. Does **not** prove Ising modular tensor category completeness, universal topological QC from Ising alone, or scalable FTQC thresholds.  
> 6. Does **not** mint AuthorityEffect, PROVED, or GlobalGreen by relocation of code or by naming.
>
> Added in `v0.2.0`:
>
> 7. Does **not** exhibit an $\ell^1$-versus-$\ell^2$ separation. Over GF(2) the two norms coincide identically (§2.3); no Betti number changes this.
> 8. Does **not** perform syndrome decoding. $\Phi_1$ on an `OpenObstruction` is the gauge-minimal residual weight, not the minimum-weight error consistent with an observed syndrome.
> 9. Does **not** claim a capability comparison against a dense eigensolve. A parity class and a spectrum are different questions; the timing bounds the cost of the question actually answered, at matched MZM count.
> 10. Does **not** contain a physical tetron. A "tetron" here is a 2-cell of a declared finite carrier under an explicit corner-shared-MZM idealization — an interpretation of the algebra, not evidence about a device.
> 11. Does **not** assert that any Microsoft result is wrong. This paper analyses what a *declared finite carrier* can and cannot certify; it takes no position on the physics of any device, and holds no experimental data.

---

## 0. Why this paper exists (the problem statement)

### 0.1 Archive inheritance

An archived preprint (March 2026), *Topological Quantum Computation as $\ell^1$ Composition: Majorana Zero Modes, Ising Fusion, and Deterministic Gate Verification* (`majorana_topological_qc_v003.md`), framed four verification boundaries around:

1. Kitaev-chain topological phase classification,  
2. $\mathbb{Z}_2$ parity readout consistency,  
3. Ising braid / Yang–Baxter algebraic checks,  
4. multi-qubit $F$-matrix / tensor restrictions.

That note also referenced contemporary experimental context (e.g. interferometric single-shot parity in InAs–Al hybrid devices [Aghaee et al., Nature 2025]) and used the slogan that hardware protects parity while software “terminalizes” algebraic schedules.

### 0.2 What went wrong (honesty audit)

Multi-agent review (2026-08-01: Red / Green / Blue / math-prof / physics-prof / proofs / refutation) found a **scope-composition failure**, not a failure of elementary GF(2) linear algebra:

| Failure mode | Archive / bridge risk | Estate fix |
|---|---|---|
| Name collision | `terminalize` / `Exact` read as FOC ExactRepair | Labels = **diagnostic schedule classes** only; Rust fence + receipt `authority_effect: "None"` |
| Institutional framing | “Microsoft Technical Bridge Note” as if partner-grade | Retitle as engineering **audience**, not endorsement |
| Theorem inflation | Exhaustive case-split marketed as device theorem | Definition / decision procedure over **declared** matrices |
| Dual SOOT | Python prototype + engines GF(2) forked | Canonical leaf crate `omega_majorana` |
| Lean fiction | Claim path `majorana_parity/` without lake tree | Obligation OPEN (DERIV P1–P3) |
| FSP overclaim | “sign-free subclass” read as FSP solved | Local positivity under **declared** symmetry only; generic FSP untouched |

**Definition 0.1 (Microsoft Majorana Problem — Claim `QM_212-C1`).**  
The *Microsoft Majorana Problem* is the obstruction to treating published or marketed Majorana/TQC hardware narratives as automatically discharging finite algebraic verification obligations (or the converse): a **packet gap** between experimental carriers and declared GF(2)/Ising carriers under AuthorityEffect None.

This is a **foundations / packaging problem** for the Omega estate, not a refutation of any particular laboratory result.

---

## 1. Mathematical Formulation (finite GF(2) schedule core)

Let

$$
C^\bullet:\quad C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2
$$

be a **declared** finite cochain complex over $\mathbb{F}_2$ with $d_1\circ d_0 = 0$. A residual (edge error / parity mismatch schedule) is $\omega\in C^1$. Face syndrome is $s = d_1\omega\in C^2$.

### Theorem 1 (GF(2) residual trichotomy — Claim `QM_212-C2`)

For any such complex and any $\omega\in C^1$, **exactly one** of the following holds:

| Diagnostic label | Predicate | Homological reading |
|---|---|---|
| `Exact` | $\omega\in\operatorname{im}d_0$ | coboundary / stabilizer-trivial class |
| `ClosedResidual` | $\omega\in\ker d_1\setminus\operatorname{im}d_0$ | nontrivial class in $H^1=\ker d_1/\operatorname{im}d_0$ |
| `OpenObstruction` | $d_1\omega\neq 0$ | not a cocycle; detectable face syndrome |

*Proof (elementary).* Partition $C^1$ by membership in $\operatorname{im}d_0$ and $\ker d_1$. Under $d_1 d_0=0$, $\operatorname{im}d_0\subseteq\ker d_1$, so the three classes are exclusive and exhaustive. $\blacksquare$

**Naming fence.** These labels are **not** FOC terminals. Estate code emits receipt tag `omega.majorana-gf2-receipt.v1` with `authority_effect = "None"`.

### Theorem 2 (Polynomial classification — Claim `QM_212-C3`)

Given declared matrices $(d_0,d_1)$ and $\omega$, Gaussian elimination over $\mathbb{F}_2$ decides the trichotomy in $O(n^3)$ bit operations on the finite dimensions (prose / CODE_DEMO; Lean complexity residual).

*Implementation.* `omega_majorana::MajoranaGF2Terminalizer::terminalize` (Rust leaf crate; engines re-export is compatibility-only).

### Proposition 3 (Boundary refuse — Claim `QM_212-C4`)

If $d_1 d_0\neq 0$, classification is refused (`RepresentationInvalid` / `Err`). No homology label is emitted.

---

## 2. Worked multi-plaquette surface-code shadow (CODE_DEMO)

Surface-code literature (and QM_101 / QM_102 repair-capacity packaging) uses the same cochain shape: errors on edges, syndromes on faces, logicals as nontrivial $H^1$ classes.

### 2.1 Planar $2\times 2$ plaquette grid (disk)

- Carrier: `surface_grid_2x2_planar` — $3\times 3$ vertices, 12 edges, 4 faces.  
- With all faces filled, $\dim H^1=0$ (disk).  
- Play: vertex coboundary → `Exact`; single edge → `OpenObstruction`.

### 2.2 Torus $2\times 2$ (nontrivial logical-like classes)

- Carrier: `surface_grid_2x2_torus` — $2\times 2$ vertices, 8 edges, 4 faces (periodic).  
- Expect $\dim H^1=2$ over $\mathbb{F}_2$.  
- Cocycle representatives (not bare length-2 chain loops):

| Residual | Status (CODE_DEMO) | Reading |
|---|---|---|
| `torus_logical_x_example` = $e_1+e_3$ | `ClosedResidual` | nontrivial cocycle class |
| `torus_logical_z_example` = $e_4+e_5$ | `ClosedResidual` | independent class |
| single edge | `OpenObstruction` | detectable syndrome |
| column of $d_0$ (vertex 0) | `Exact` | coboundary |

**Fence (Claim `QM_212-C5`).** This is a **finite toy**, not a distance-$d$ threshold certificate, not Google Willow validation, and not a Microsoft device packet (cf. QM_101 THR-001 open surface-code packet obligation).

Executable gate:

```text
cargo test -j 1 -p omega_majorana play_surface_ -- --nocapture
```

### 2.3 Tetron-array carriers: $H^1$, code distance, and the cost of $\Phi_1$

Added in `v0.2.0`. The surface toys above are $2\times2$ fixtures; the tetron-array
carrier family (`omega_engine_majorana/carriers/surface_carrier.py`, Rust face
`crates/omega_majorana/src/tetron.rs`) is parameterised by topology and extent, and
its homology is *measured*, not asserted.

| Topology | $\dim H^1$ | Code distance |
|---|---|---|
| disk | $0$ | none |
| cylinder | $1$ | $\text{rows}+1$ |
| torus | $2$ | $\min(\text{rows},\text{cols})$ |

measured as $(E-\operatorname{rank} d_1)-\operatorname{rank} d_0$ and independently
checked against $(2\ \text{if closed else}\ 1)-\chi$. The chain law $d_1d_0=0$ holds on
every instance built, and is mutation-killed (dropping one edge from an island 2-cell
fails 43 tests).

**Self-correction (binding).** The *previous* tetron carrier
(`carriers/tetron_carrier.py`) has $\dim H^1=0$ at every array size $T=1..4$, despite
graph cycle rank $T-1$. Every closed residual on it was `Exact` **by construction** —
the carrier could not exhibit a logical class at all. Results computed on that carrier
do not support any statement about logical sectors, and the homology-correct family
above supersedes it.

**Per-class minimum weights** on a $3\times4$ torus: $w(\texttt{h1:10})=3$,
$w(\texttt{h1:01})=4$, $w(\texttt{h1:11})=7=3+4$ — a logical string must cross every
lattice row *and* every column, so the diagonal class costs both.

**Cost, stated rather than hidden.** The three-way split is polynomial (GF(2) Gaussian
elimination; 17 ms/residual at torus $6\times6$, $V=36$, $E=72$). Certifying $\Phi_1$ is
**not**: over GF(2), $\Phi_1([r])=\min_\alpha \operatorname{wt}(r+d_0\alpha)$ is the
minimum-weight coset representative within a fixed class—distinct from syndrome decoding
(which searches across all classes for an error matching an observed face syndrome).
The implementation is $2^{\operatorname{rank} d_0}$ Gray-code steps with an explicit budget;
at torus $6\times6$ the coset has $2^{35}$ elements and the search is capped, so the certificate
reports `exact=False`. A capped search yields an **upper bound, never a minimum**, and
the terminal degrades from `TypedHarmonic` to `ClosedResidual` rather than claiming
exactness.

**No $\ell^1$-versus-$\ell^2$ separation here (new non-claim, N7 below).** Over GF(2)
with $\{0,1\}$ entries, $\lVert v\rVert_p^p=\operatorname{wt}(v)$ for *every* $p$, so
$\ell^1$ and $\ell^2$ minimisation coincide identically, at every Betti number. What
$\dim H^1\ge2$ buys is **class typing** — several distinct nonzero classes, whose
minimum weights differ — not a norm gap. Any "$\ell^1$ beats $\ell^2$" statement on a
GF(2) parity carrier is not weak evidence; it is not well-formed. The real-valued
$\ell^1$-vs-$\ell^2$ comparison is a different object on a different carrier.

### 2.4 Dictionary to QM_102

| QM_102 language | QM_212 / `omega_majorana` | Not claimed |
|---|---|---|
| Error $e\in C^1$, syndrome $s=\delta^1 e$ | residual $\omega$, $s=d_1\omega$ | physical noise process |
| Correctable / coboundary | `Exact` | FOC ExactRepair |
| Logical / nontrivial cycle | `ClosedResidual` | device logical failure proof |
| Detectable | `OpenObstruction` | hardware failure event |
| Threshold $p_{\mathrm{th}}$, distance $d$ | **absent** | FTQC threshold theorems |

---

## 3. Archive content retained under fences

### 3.1 Kitaev chain as **imported** physical model (Claim `QM_212-C6` — SCOPE FENCE)

The archive Hamiltonian

$$
H = \sum_i\bigl[-t(c_i^\dagger c_{i+1}+\mathrm{h.c.})+\Delta(c_i c_{i+1}+\mathrm{h.c.})\bigr]-\mu\sum_i\bigl(n_i-\tfrac12\bigr)
$$

and the phase table $|\mu|<2t$, $|\Delta|>0$ (topological) are **standard condensed-matter imports**. This paper does **not** re-derive BdG spectra, winding numbers, or experimental phase diagrams. They may appear only as **context labels** for which algebraic carriers one *might* declare — never as theorems proved by `omega_majorana`.

### 3.2 Ising fusion data as **declared** algebra (Claim `QM_212-C7`)

Fusion rules

$$
\sigma\otimes\sigma = 1\oplus\psi,\qquad \psi\otimes\psi=1,\qquad \psi\otimes\sigma=\sigma
$$

and specialized braid matrices over $\mathbb{Q}(\zeta_{16})$ may be checked as **exact finite identities** (Yang–Baxter for declared $R_1,R_2$; $F^2=I$; specialized hexagon).  

**Not proved:** full Ising MTC axioms, modularity, physical anyon braiding, universality (Ising alone is not universal TQC without magic/supplement — archive Thm 5A.1 retained as **restriction fence**).

### 3.3 Parity readout as $\mathbb{Z}_2$ observable bookkeeping (Claim `QM_212-C8`)

“Parity readout corresponds to a $\mathbb{Z}_2$-valued observable commuting with an effective Hamiltonian” is allowed only as an **algebraic consistency** statement on a **declared** operator package. Capacitance formulas $C_Q=-e^2\partial^2 E_0/\partial n_g^2$ remain experimental / continuum imports (Q-held).

### 3.4 Majorana positivity vs FSP (Claim `QM_212-C9` — SCOPE FENCE)

Archive Thm 3.1 (Pfaffian non-negativity under BDI/D-type symmetry) is retained only as:

> Under **declared** symmetry/Hamiltonian hypotheses, a Majorana representation can make a **specific** path-integral subclass sign-structured (Pfaffian).  
> This does **not** terminate the generic fermion sign problem.

Cross-programme: FSP estate remains `013_the_problem_of_the_fermion_sign/`.

---

## 4. Composition pipeline (diagnostic only)

```text
Declared finite complex (d0, d1) over F2
        |  verify d1 d0 = 0
        v
Residual ω on edges
        |  GF(2) Gaussian elimination
        v
Receipt: Exact | ClosedResidual | OpenObstruction
        |  authority_effect = None
        v
Optional: Q(ζ16) Ising matrix identity seeds
        |  not physical braiding
        v
Host ledger / demos (Python dual-face) — still Auth=None
```

Higher-order $F$-matrix $n$-ary checks from the archive remain a **software constraint** story (associativity of declared matrices), not homotopy-of-nature.

---

## 5. Observer projection quarantine

### Statement 5 (Hardware narrative quarantine — Claim `QM_212-C10`)

Continuous device baths, continuum BdG spectra, fabrication process narratives, and vendor marketing are **external observer projections**. They may motivate which finite packets to declare; they do not populate GF(2) receipts or mint authority.

### Statement 6 (LGGR on parity schedules — Claim `QM_212-C11`)

Local Green $\neq$ Global Red: face-local syndrome zeroing ($d_1\omega=0$ on a subcomplex) does not imply global triviality of $[\omega]\in H^1$ on the declared carrier (torus toy: `ClosedResidual`). Same LGGR spirit as QM_102, without thresholds.

---

## 6. Summary Box

1. **What it supports:** Finite GF(2) residual trichotomy on declared complexes; multi-plaquette CODE_DEMO; exact specialized Ising matrix checks; an explicit name for the **packet gap** between Majorana hardware narratives and algebraic diagnostics (“Microsoft Majorana Problem”).  
2. **What it does not support:** Device validation, FOC authority, universal TQC, generic FSP solution, threshold theorems.  
3. **Narrowest defensible claim:** Given declared $(d_0,d_1,\omega)$ over $\mathbb{F}_2$ with $d_1 d_0=0$, Omega can emit a replayable **diagnostic** schedule receipt; hardware claims require a separate, fully populated realization packet (QM_101/QM_103).  
4. **Next tests:** Lean `majorana_parity/` nilpotency + trichotomy (DERIV P1–P2); optional QM_102 worked-example attachment of a torus receipt as CODE_DEMO only; prose firewall on any remaining “Microsoft bridge theorem” language.

### 6.1 Where a genuinely new result could come from (`v0.2.0`)

Recorded so the paper does not imply more headroom than the algebra has. The
programme document is
`omega_engine/omega_engine_majorana/docs/discrimination_program_and_falsifiers_20260805.md`.

- **Not from the parity algebra.** The GF(2) sector is well understood: the
  trichotomy is Gaussian elimination (C16), $\Phi_1$ is syndrome decoding
  (C15), and there is no $\ell^1$-vs-$\ell^2$ separation to be had (C17/N7).
  Braiding-only Majorana dynamics is a free-fermion/Clifford sector that the
  literature already treats as classically simulable — which is *why* Ising
  alone is not universal (§3.2 restriction fence). Any claim of novelty there
  is refuted on sight.
- **Raising the certified ceiling (tractable).** The exact rational
  $\ell^1$ projection with dual witness
  (`crates/omega_solvers/src/exact_weighted_l1_lp.rs`) supplies a *certified
  lower bound* on the GF(2) minimum weight. Where it meets the capped
  search's upper bound, a coset larger than the budget becomes certifiable
  without exhaustion; where it does not, the **gap** is reported. Expect
  looseness: the relaxation's optimum can be fractional.
- **Evidence adequacy (the real target).** The open question is not whether
  the algebra is right but whether a declared protocol's observables
  *discriminate* the hypotheses they are read as discriminating. In this
  estate's vocabulary that is `DETECTOR_INADEQUATE`: a difference lying in
  $\ker M$ for the protocol's measurement map $M$ is an **unmeasured
  residual**, and any discrimination then rests on an assumption not carried
  by $M$, which must be declared. This is a statement about evidence, never
  about a device — and it is gated on sourcing a protocol's declared
  observables precisely enough to build $M$ without guessing. If that cannot
  be done, the programme stops and says so.

---

## References

1. Archive source: `omega_engine/research/published/research_notes_000/.archive/023 - Majorana Topological QC/v003/majorana_topological_qc_v003.md` (v0.4 preprint, March 2026).  
2. Aghaee, M. et al. [Microsoft Quantum] (2025). Interferometric single-shot parity measurement in an InAs–Al hybrid device. *Nature*, 638, 651–655. **[STANDARD context only]**  
3. Nayak, C. et al. (2008). Non-Abelian anyons and topological quantum computation. *Rev. Mod. Phys.*, 80, 1083–1159. **[STANDARD]**  
4. QM_101 — Threshold theorems as repair-capacity certificates.  
5. QM_102 — Fault tolerance / cochain repair capacity.  
6. QM_072 — Bit shadow and qubit (stabilizer/coboundary vs non-$\ell^1$ interference).  
7. QM_091 — Deutsch / Everett / Wolfram promotion error.  
8. Code: `omega_engine/crates/omega_majorana` (GF(2) classifier + surface grid toys).  
9. Estate evidence: `omega_majorana/evidence/majorana_play_qc_bridge_20260801.md`.

---

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QM_212-C1` | [DEFINITION] Microsoft Majorana Problem = packet gap hardware narrative ↔ declared algebra |
| `QM_212-C2` | [DERIVED / ELEMENTARY] GF(2) residual trichotomy under $d_1 d_0=0$ |
| `QM_212-C3` | [CODE_DEMO + PROSE] Poly-time classification via Gaussian elimination |
| `QM_212-C4` | [DERIVED] Boundary refuse when $d_1 d_0\neq 0$ |
| `QM_212-C5` | [SCOPE FENCE] Surface grid toys ≠ threshold / device packets |
| `QM_212-C6` | [SCOPE FENCE] Kitaev Hamiltonian / phases imported, not discharged by this code |
| `QM_212-C7` | [CODE_DEMO + FENCE] Ising fusion / specialized braid identities; not full MTC |
| `QM_212-C8` | [SCOPE FENCE] Parity $\mathbb{Z}_2$ bookkeeping ≠ capacitance experiment proof |
| `QM_212-C9` | [SCOPE FENCE] Local Pfaffian positivity ≠ generic FSP solved |
| `QM_212-C10` | [Q-HELD] Hardware narratives quarantined as observer projections |
| `QM_212-C11` | [DERIVED toy] LGGR on declared torus residual classes |

<!-- claim-id-body-index:end -->
