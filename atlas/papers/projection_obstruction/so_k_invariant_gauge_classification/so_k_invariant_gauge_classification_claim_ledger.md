Claim Ledger — GS-002: SO(k)-Invariant Gauge Rigidity for Declared Euclidean Stalks
===================================================================================

**Paper Key:** `000_coda/foc/so_k_invariant_gauge_classification`  
**Paper Identity:** `GS-002` (`so_k_invariant_gauge_classification.md`, canonical version: `v2.0.0`)  
**Legacy Paper Identity:** `Paper 002` / `Paper 006`  

This ledger catalogs every claim in `GS-002` with its type, governing hypotheses, proof location, mechanization status, and open obligations.

---

1. Claim-by-Claim Matrix

---

| ID | Claim | Type | Hypotheses | Proof / support | Mechanization | Open obligation |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | Local SO(k) rigidity; outer sum conditional on strong aggregation | PROVEN (local); CONDITIONAL (outer) | Euclidean stalks, full rotations, faithful homogeneous gauge; separately declared edge sum | §§3.2–3.3 | Partial Lean kernels; finite Python examples | General-k group-to-Euclidean Lean bridge |
| C2 | M-compatible gauge and M-contractive unit-body correspondence | IMPORTED; NOT LOCALLY PROVED | Finite-dimensional V; closed convex balanced absorbing bounded body | Companion [2] §2.2; reproduced in §2.1 | Not locally mechanized | Source status inherited; boundedness restored |
| C3 | Order reversal of admissible gauge classes | IMPORTED FROM [2] | Inclusion of transformation monoids | §2.2, Corollary 1 | No local code or Lean proof | Source status inherited |
| C4 | Maximal-symmetry native-norm endpoint | IMPORTED; CONDITIONAL | All bounded endomorphisms; native norm; Hahn–Banach | §2.2, Corollary 2; companion [2] | No local code or Lean proof | Source status inherited |
| C5 | Sphere-transitive isometric action forces the native norm up to scale | PROVEN; CONDITIONAL | Transitive action, invariance, faithfulness, homogeneity | §2.2, Corollary 3; §3.2 | Generic radial Lean kernel; finite numerical probes | Group-action and Euclidean instantiation remain explicit |
| C6 | Compact-group Haar-average norm construction | IMPORTED STANDARD RESULT | Continuous linear compact-group action; normalized Haar measure | §2.2, Corollary 4 | Not locally mechanized | Continuum and action hypotheses imported |
| C7 | Invariant orbit convex-hull construction | STANDARD SUPPORT | Continuous linear compact action; bounded spanning seed; balanced convex hull | §2.2, S8 | No local code or Lean proof | Standard convex-body argument |
| C8 | Indexed directed-edge cochains and target-stalk comparison defect | DEFINITION | Finite indexed edges; target-directed transports; real vector stalks | §3.1 | Flat identity-transport carrier implemented in Python | General transports are prose setup, not executable carrier |
| C9 | Theorem 3.1: local Euclidean gauge rigidity | PROVEN; CONDITIONAL | k >= 2; Euclidean structure; full SO(k) invariance; faithful homogeneous gauge | §3.2 | Generic radial and separate planar transitivity Lean kernels; finite audits | General-k transitivity and full Euclidean bridge not mechanized |
| C10 | Theorem 3.2: substitution into the strong edgewise sum | CONDITIONAL / DEFINITIONAL | Local rigidity and explicit edgewise aggregation | §3.3 | Python cost definition; separate Lean disjoint-support splitting lemma | Outer sum does not follow from local rotations |
| C11 | Flat primal quotient obstruction | DEFINITION | Finite identity-transport graph; positive weights | §4, Definition 4.1 | Floating-point primal candidates | No exact-arithmetic optimizer certificate |
| C12 | Theorem 4.2: mixed vector quotient duality and attainment | STANDARD FINITE APPLICATION | Finite-dimensional flat repairs; positive weights; continuity qualification | §4; imported convex duality [6] | Lean weak-duality kernels; tolerance-qualified Python witnesses | Full strong duality/attainment not mechanized |
| C13 | Equal single-cycle circulation iff exact repair difference | PROVEN FINITE GRAPH FACT | Single cycle; identity transports; signed traversal when needed | §5 explicit vertex partial sums | Anchored finite Lean kernel; floating-point examples | Graph-incidence instantiation remains prose |
| C14 | Lemma 5.1: normalized cycle quotient formula | PROVEN; CONDITIONAL | Single cycle; local norm; unit weights | §5 lower bound and concentrated achiever | Lean native-norm cost kernel; floating-point formula evaluation | General gauge/native-norm and graph identification in prose |
| C15 | Weighted cycle bottleneck formula | PROVEN; CONDITIONAL | Single cycle; local norm; positive weights | §5 weighted refinement | Lean native-norm weighted cost kernel; floating-point witnesses | General gauge/native-norm and graph identification in prose |
| C16 | Theorem 5.2: normalized triangle 2 versus sqrt(2) | PROVEN; CONDITIONAL | Common unit normalization; declared Euclidean structure | §5 | Lean rational squared-cost separation; Python examples | Geometric cost interpretation in prose |
| C17 | Observer-class separation and dimension scaling | PROVEN CONSEQUENCE | Specified gauges and common normalization | §5; finite diagonal examples | Floating-point examples and notebook assertions | No global or physical measurement claim |
| C18 | Theorem 6.1: mixed closure bound | PROVEN; CONDITIONAL | Finite complex; d1 d0 = 0; declared mixed norms | §6; scalar-incidence column proof for implementation | Abstract Lean invariance/infimum kernel; numerical operator calculation | Concrete norm instantiation not mechanized |
| C19 | Observer passivity and network/sheaf connections | IMPORTED / INTERPRETIVE | Compatible quotient maps and declared observer hypotheses | §7.1; companion framework [1] | Not locally mechanized | General transported adjoint replaces ordinary divergence |
| C20 | Legacy reflective-completion dependency | CONJECTURE; HISTORICAL REGISTER | Companion initiality-to-reflection lemma | Companion framework; no current local §7.1 claim | Open; not established by this review | PL-003-B remains open |
| C21 | Euclidean stalk inner product declared with SO(k) | IMPORTED INPUT | Declared Euclidean representation | §3.2 import note | Input, not a construction | No discharge of continuum/representation import |
| C22 | Real scalars, continuous group and convex-analysis imports | IMPORTED INPUT | Declared scalar, group, and standard analysis structures | §§2–4 | Input, not a construction | Finite carrier does not make these finite scalar objects |
| C23 | Applied and physical vocabulary | SCOPE LIMIT | Interpretation candidates only | §§1, 5 | No empirical realization supplied | No physical detector or dynamics result |
| C24 | No authority effect | PACKAGE POLICY | Evidence does not mint semantic or publication authority | Companion ledger and release documentation | Not a mathematical theorem | No proof promotion from packaging |
| C25 | Non-Abelian holonomy obstruction inequality | WITHDRAWN | Excised from v2.0.0 after counterexample | Historical §5.3; not in current manuscript | No current support claimed | Remains withdrawn |
| C26 | Unqualified extreme-weight numerical stability | WITHDRAWN | Excised from v2.0.0 | Historical §5.3; not in current manuscript | No current support claimed | Scale regressions do not restore a general stability theorem |
| C27 | McLachlan trace-norm projection extension | WITHDRAWN | Excised from v2.0.0 | Historical §5.3; not in current manuscript | No current support claimed | Remains withdrawn |

---

2. Proof Packet Ledger & Lean Mechanization Scope

| ID | Result | Proof location | Dependency status |
| --- | --- | --- | --- |
| P003-G1 | $\mathrm{SO}(k)$ invariance forces the local Euclidean gauge | Theorem 3.1 | Requires $k\ge2$, faithful homogeneous convex gauge/norm, and full $\mathrm{SO}(k)$ invariance |
| P003-N1 | Exact edge-normalization dependence | Theorem 3.2 | Conditional on the declared strong edgewise sum; without normalization, the diagnostic is weighted or orbit-weighted $\ell^1(E;\ell^2)$ |
| P003-D1 | Mixed $\ell^1(E;\ell^2)$ quotient duality | Theorem 4.2 | Requires finite-dimensional cochains and positive edge weights |
| P003-T1 | Finite triangle-anomaly separation | Theorem 5.2 | Requires normalized equal edge weights for the clean $2$ versus $\sqrt2$ comparison |
| P003-C1 | Mixed closure bound | Theorem 6.1 | Requires a finite complex $C^0\xrightarrow{d_0}C^1\xrightarrow{d_1}C^2$ with $d_1d_0=0$ and declared mixed norms |

**Lean Mechanization Roots (`gs002` / `GS002`):**

* `lean4/gs002_l003_01_triangle_separation.lean`: exact rational identities for normalized triangle separation.
* `lean4/gs002_l003_02_s_ok_local_gauge.lean`: abstract unit-transitivity-to-sphere-constancy, radial collapse, and SO(2) circle transitivity.
* `lean4/gs002_l003_03_weighted_cycle_quotient.lean`: circulation-class algebra, normalized and weighted single-cycle quotient lower bounds.
* `lean4/gs002_l003_04_edge_decomposition.lean`: finite edge-decomposition under strong disjoint-support splitting (PL-003-A).
* `lean4/gs002_l003_05_mixed_closure_bound.lean`: abstract closure-repair invariance and order-theoretic quotient/infimum step.
* `lean4/gs002_l003_06_mixed_duality_weak.lean`: abstract weak-duality/certificate kernel for divergence-free witnesses.
* `lean4/gs002_l003_07_cycle_exactness.lean`: anchored finite-cycle exactness and cycle repair equivalence.
* `lean4/gs002_core.lean`: central library imports and exported definitions.

---

3. Support Ledger

* **S1 — Absolute homogeneity clarification lemma (easy).** If $j:\mathbb R^k\to\mathbb R_{\ge0}$ is faithful, subadditive, and absolutely homogeneous ($j(\lambda x)=|\lambda|j(x)$), then $j$ is a norm. If $j$ is only positively homogeneous on $\lambda\ge0$, then symmetry ($j(-x)=j(x)$) must be added separately.
* **S2 — SO(k) transitivity lemma (standard/easy).** For $k\ge2$, $\mathrm{SO}(k)$ acts transitively on every Euclidean sphere $S_r^{k-1}\subset\mathbb R^k$. Therefore any $\mathrm{SO}(k)$-invariant absolutely homogeneous faithful gauge is $c\|\cdot\|_2$.
* **S3 — Edge aggregation decomposition lemma (easy/moderate; Lean-mechanized in strong finite form).** If a finite edge diagnostic satisfies strong disjoint-support splitting over edge restrictions, then $J(\omega)=\sum_{e\in E}j_e(\omega_e)$. If decomposability is weaker than explicit local summability or strong partition additivity, additional hypotheses are required.
* **S4 — Weighted mixed quotient duality lemma (standard; weak-duality kernel Lean-mechanized).** For finite-dimensional $C^0\xrightarrow{d_0}C^1$ with $C^1=\oplus_e\mathbb R^k$ and positive weights $c_e$, $\inf_{\alpha}\sum_e c_e\|\omega_e-(d_0\alpha)_e\|_2 = \max_{d_0^*\varphi=0, \|\varphi_e\|_2\le c_e} \sum_e\langle\varphi_e,\omega_e\rangle$. The Lean kernel formalizes the certificate side: divergence-free witnesses are invariant under exact repairs, and representative-wise witness bounds descend to the quotient infimum. The full Fenchel--Rockafellar equality/attainment theorem remains the cited finite-dimensional convex-duality bridge.
* **S5 — Single-cycle quotient norm lemma (easy).** For a finite directed cycle with normalized equal edge weights and local norm $j$, the quotient norm modulo exact repairs equals the local norm of the total circulation: $\Phi_j([\omega])=j\left(\sum_{e\in C}\omega_e\right)$.
* **S6 — Weighted single-cycle refinement lemma (easy).** For a finite directed cycle with positive weights $w_e$, $\Phi_{j,w}([\omega])=(\min_e w_e) j\left(\sum_{e\in C}\omega_e\right)$.
* **S7 — Mixed closure bound lemma (easy; abstract kernel Lean-mechanized).** For a finite complex $C^0\xrightarrow{d_0}C^1\xrightarrow{d_1}C^2$ with $d_1d_0=0$ and declared norms on $C^1,C^2$, $\|d_1h\|_{C^2}\le \|d_1\|_{C^1\to C^2}\inf_\alpha\|h+d_0\alpha\|_{C^1}$. The Lean kernel formalizes repair invariance and the infimum/cofinality step; concrete weighted mixed-norm operator constants remain part of the prose setup.
* **S8 — Orbit-convex-hull gauge construction lemma (moderate).** For compact $G$ acting continuously and linearly on finite-dimensional $V$, the closed balanced convex hull of a bounded seed set whose span is $V$ defines a faithful $G$-invariant gauge by its Minkowski functional.
* **S9 — Cross-paper dependency-status lemma (easy).** Any claim imported from the general finite obstruction framework or M-compatible gauge-classification paper inherits its source-paper claim status unless this paper independently establishes it.

---

4. Import / Oracle Boundary Register

| # | Imported structure | Where used | Price / status |
|---|---|---|---|
| **I1** | The completed continuum $\mathbb R$ — limits, suprema, square roots | $\mathbb R^k$ stalks (§3.1); $\mathbb R$-valued gauges throughout; every infimum/maximum (§4, §6) | **IMPORTED — R2b; Q-gated (G7).** Not constructed here. "Finite" in this paper means *finite carrier* and *finite-dimensional stalks*; the scalars, the fibre, and the symmetry group are continuum objects. |
| **I2** | Inner product on $\mathbb R^k$; the $\ell^2$ stalk norm — **the $L^2$ fibre** | The entire $\ell^2$ factor: Thms 3.1, 3.2, 4.2, 6.1; Lem 5.1; Thm 5.2; the paper's title | **IMPORTED + OBSTRUCTION.** Admitted *together with* $\mathrm{SO}(k)$ (§3.2 import note); never constructed at this degree. Charter §6.2 registers the $L^2$/phase fibre and the $\ell^2$-norm inner-product space as `OBSTRUCTION` (R1 — an added fibre over the exhibited $L^1$ data) **+** `IMPORTED` (R2/R3). **This paper declares and prices that import; it does not discharge R1.** |
| **I3** | $\mathrm{SO}(k)$ as a continuous (Lie) group, and its transitivity on the Euclidean sphere | Thm 3.1 hypothesis and proof; §3.3; §5; §7.1 | **IMPORTED — R2b; Q-gated (G7); `OracleNeeded`.** General-k transitivity is not mechanized; planar circle transitivity has a separate Lean kernel (PL-003-C). Definitionally carries I2, since $R^\top R=I$ presupposes the inner product. A **declared gauge**, not a physical rotation group (I8). |
| **I4** | Fenchel–Rockafellar strong duality and attainment; conjugacy of $c_e\|\cdot\|_2$ with the Euclidean ball | Thm 4.2 proof (§4) | **IMPORTED — `[STANDARD + Rockafellar 1970]`; `OracleNeeded` at this degree.** Only the certificate side is mechanized; the equality/attainment step is not. |
| **I5** | Haar measure on a compact group; $j_G(x)=\int_G q(gx)\,dg$ | Cor 4 (§2.2) | **IMPORTED — R2b.** Inherited from [2]; not constructed here. |
| **I6** | Closed convex hull $\overline{\operatorname{conv}}$; Minkowski functional over $\mathbb R$; Hahn–Banach | Thm 2.1; Cor 2; Lemma S8 | **IMPORTED — inherited from [2] with source-paper status (S9).** |
| **I7** | $\sqrt2\notin\mathbb Q$ — an extension of the derived scalars | Thm 5.2; §5 Predictions A/B; abstract; Zenodo description | **IMPORTED — minimally R2a** (finite, non-continuum, cheap, *not* Q-gated); **as actually obtained here, via I1 (R2b).** See the §5 import note. |
| **I8** | Physical / applied realization vocabulary — "strain", "sensor", "displacement field", "force", and "rotation" as a spatial act | §1 motivation; §1.2 item 5; §5 finite numerical consequence | **INTERPRETIVE / SCOPE FENCE.** Names interpretation candidates only. No physical realization, dynamics, spacetime, locality, or measurement claim is made or earned here. |

---

5. Formalization-Status Firewall & GTOC/GTLA Compliance

* **Historical build (2026-09-28 receipt):** `lake build GS002` green — Lean v4.34.0-rc1, mathlib pinned (`de5ce8a9a66a4aa68a9bdbb35b63a06d34d9ca11`). **`sorry`: 0, `admit`: 0, custom axioms: 0** across all eight sources.
* **Axiom surface:** Every theorem and lemma declaration in the seven theorem modules is an explicit `#print axioms` target and appears in the retained dated receipt; the release gate requires fresh dependency-set agreement. The results depend solely on standard Lean 4 foundational axioms: `[propext, Classical.choice, Quot.sound]` (or a subset). No native-decision or synthetic axioms are generated.
* **Scope:** Stated over arbitrary `NormedAddCommGroup` / `AddCommMonoid`.
* **GTOC/GTLA boundary:** Mints no authority, no terminalizer, no semantic authority.

<!-- claim-id-body-only-sync:begin -->

Body-only ID sync (packaging)
---

Packaging hygiene; no OPEN→PROVED.

| ID | Claim | Type | Status |
|---|---|---|---|
| GS-002 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| P003-C1 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |
| UTF-8-clean | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |

<!-- claim-id-body-only-sync:end -->

## Publication review evidence (2026-10-02)

No theorem has been promoted by test coverage or packaging. The source-level Lean census and retained provenance hashes are checked separately from the fresh build, which is unavailable on this host. Numerical audits and optimizer flags remain finite-sample or tolerance-qualified evidence. See `docs/publication_review.md`.
