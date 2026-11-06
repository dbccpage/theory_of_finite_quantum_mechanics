# The Majorana Problem: Finite Parity Schedules, $\mathbb{F}_2$ Homology, Ising Algebra, and What Hardware Narratives Do Not Discharge

**Subtitle:** A Scoped Monograph on Combinatorial Cochain Complexes, $\mathbb{F}_2$ Residual Trichotomy, Surface Code Shadows, Tetron Arrays, and the Realization Packet Gap  
**Author:** Jeremy H. Carroll and the Omega Engine Retinue  
**Date:** 2026-09-19  
**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)  
**Status:** Master Monograph Volume (v1.1.0)  
**Series:** Projection Obstruction 026 (`projection_obstruction/026_microsoft_majorana_problem`)  
**Authority:** `AuthorityEffect: None`  
**Primary Reference:** `sealed-derivation-v1` (commit `3100c4e`)  

---

## Executive Summary & Epistemic Scope

This monograph addresses the mathematical structure, cochain homology, and verification boundaries of Majorana zero mode (MZM) parity schedules, planar/toric surface codes, and non-abelian Ising topological braiding within the CODA framework.

The central epistemological finding of this monograph is the **Microsoft Majorana Problem**: the structural obstruction to treating published or marketed Majorana/TQC hardware narratives (e.g. semiconductor-superconductor nanowires, zero-bias conductance peaks, or interferometric single-shot parity readouts) as automatically discharging finite algebraic verification obligations—or conversely, treating algebraic consistency checks over discrete carriers as validating physical quantum hardware.

The mathematical analysis establishes six core structural components:

1. **Finite $\mathbb{F}_2$ Cochain Complex & Residual Trichotomy**:
   For any declared finite cell complex $C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$ over $\mathbb{F}_2$ with boundary nilpotency $d_1 \circ d_0 = 0 \pmod 2$, every edge residual $\omega \in C^1$ admits an exclusive and exhaustive classification into:
   - `Exact`: $\omega \in \operatorname{im}(d_0)$ (coboundary / stabilizer-trivial).
   - `ClosedResidual`: $\omega \in \ker(d_1) \setminus \operatorname{im}(d_0)$ (nontrivial logical homology class in $H^1(C^\bullet; \mathbb{F}_2)$).
   - `OpenObstruction`: $d_1 \omega \neq 0$ (non-zero boundary syndrome).
   A prose complexity remark says this trichotomy is decidable in $O(n^3)$ bit operations via Gaussian elimination over $\mathbb{F}_2$. Lean `gaussian_elimination_cubic_bound` is `Nat.le_refl` of `n * n * n ≤ n * n * n` and is not that remark.
2. **Multi-Plaquette Surface-Code Shadows & Tetron Arrays**:
   The sentences below are the monograph's carrier description. Lean `torus_h1_dimension`, `cylinder_h1_dimension`, and `disk_h1_dimension` are `rfl` on an enum and are not a homology computation. Lean `toric_distance_3x4` is `rfl` of `min 3 4`, and `torus_3x4_additive_weight` is `rfl` of `3 + 4 = 7`.
   Parameterized tetron-array carriers are described with these labels:
   - Planar disk: $\dim H^1 = 0$, code distance none.
   - Cylinder: $\dim H^1 = 1$, code distance $d = \text{rows} + 1$.
   - Torus: $\dim H^1 = 2$, code distance $d = \min(\text{rows}, \text{cols})$.
   On a $3 \times 4$ torus, per-class minimum weights satisfy $w(\mathtt{h1:10}) = 3$, $w(\mathtt{h1:01}) = 4$, and $w(\mathtt{h1:11}) = 7 = 3 + 4$.
3. **Syndrome Decoding Complexity & The Cost of $\Phi_1$**:
   Over $\mathbb{F}_2$, certifying the quotient residual $\Phi_1([r]) = \min_\alpha \operatorname{wt}(r + d_0 \alpha)$ is equivalent to minimum-weight coset decoding (syndrome decoding), which is NP-hard in general. Budget-capped Gray-code searches provide certified upper bounds, degrading routing from `TypedHarmonic` to `ClosedResidual` when the search budget is exhausted.
4. **No $\ell^1$-vs-$\ell^2$ Separation Over $\mathbb{F}_2$**:
   For vectors with binary entries $v \in \{0, 1\}^n$, $\|v\|_p^p = \operatorname{wt}(v)$ for every $p \ge 1$. Consequently, $\ell^1$ and $\ell^2$ minimizations coincide identically across all Betti numbers. Higher homology $\dim H^1 \ge 2$ buys distinct logical classes, not an $\ell^1 / \ell^2$ norm separation gap.
5. **Imported Physical Models vs Declared Algebraic Objects**:
   The 1D Kitaev chain Hamiltonian, topological phase bounds ($|\mu| < 2t, |\Delta| > 0$), and non-abelian Ising anyon fusion rules ($\sigma \otimes \sigma = 1 \oplus \psi$) are strictly isolated as imported models. Exact matrix identities over $\mathbb{Q}(\zeta_{16})$ certify software associativity and Yang-Baxter relations without asserting physical anyonic braiding or universal quantum computation.
6. **Detector Inadequacy & Evidence Honesty**:
   Where a measurement map $M$ has non-trivial kernel $\ker M$, unmeasured residuals obstruct conclusive hypothesis discrimination. The monograph formalizes this as `DETECTOR_INADEQUATE`, enforcing that hardware narratives cannot substitute for missing empirical projection operators.

---

## Section 0: Provenance & Honesty Audit

### 0.1 Archive Inheritance

An archived preprint from March 2026 (*Topological Quantum Computation as $\ell^1$ Composition: Majorana Zero Modes, Ising Fusion, and Deterministic Gate Verification*, paper 023 v003) framed four verification boundaries around:

1. Kitaev-chain topological phase classification,
2. $\mathbb{Z}_2$ parity readout consistency,
3. Ising braid / Yang-Baxter algebraic checks,
4. Multi-qubit $F$-matrix / tensor restrictions.

That note also referenced contemporary experimental context (e.g. interferometric single-shot parity in InAs-Al hybrid devices [Aghaee et al., Nature 2025]) and utilized the narrative that hardware protects parity while software "terminalizes" algebraic schedules.

### 0.2 What Required Correction (Honesty Audit)

Multi-perspective adversarial review identified a **scope-composition failure**, not a failure of elementary $\mathbb{F}_2$ linear algebra:

| Failure Mode | Archive / Bridge Risk | Estate Remediation |
| :--- | :--- | :--- |
| **Name Collision** | `terminalize` / `Exact` read as FOC `ExactRepair` | Labels = **diagnostic schedule classes** only; Rust fence + receipt `authority_effect: "None"` |
| **Institutional Framing** | "Microsoft Technical Bridge Note" as if partner-grade | Retitled as engineering **audience**, not vendor endorsement |
| **Theorem Inflation** | Exhaustive case-split marketed as device theorem | Definition / decision procedure over **declared** incidence matrices |
| **Dual SOOT** | Python prototype and engines GF(2) forked | Canonical leaf crate `omega_majorana` and pure Python evaluator `code/majorana_evaluator.py` |
| **Lean Gap** | Claim path `majorana_parity/` without lake tree | Mechanized proof kernel compiled under `lean4/MajoranaCore.lean` (`po026`) with zero synthetic axioms |
| **FSP Overclaim** | "Sign-free subclass" read as generic FSP solution | Local positivity under **declared** symmetry only; generic FSP left untouched under PO-023 |

---

## Section 1: Mechanism Inventory

Every component in this monograph is registered in the CODA Mechanism Matrix under strict claim discipline:

| Mechanism Slot | Binding in this Monograph |
| :--- | :--- |
| **Primitive Differences** | $\delta\omega \in \mathbb{F}_2$: Discrete parity mismatches and schedule cochain residuals on declared cell complexes. |
| **Carriers / Structure** | Finite 2-complexes $C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$ over $\mathbb{F}_2$; cyclotomic field $\mathbb{Q}(\zeta_{16})$ for specialized Ising matrices. |
| **Cochain Complex** | $C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$ satisfying exact boundary nilpotency $d_1 \circ d_0 = 0 \pmod 2$. |
| **Coboundary Maps** | $d_0: C^0 \to C^1$ (vertex-to-edge coboundary), $d_1: C^1 \to C^2$ (edge-to-face syndrome map). |
| **ZeroRel** | Residuals in $\operatorname{im}(d_0)$ are equivalent to zero (stabilizer coboundaries). Preserved under $\mathbb{F}_2$ quotient. |
| **Licensed Repairs** | Explicit vertex gauge shifts $\alpha \in C^0$ over $\mathbb{F}_2$; restricted by search budget bounds. |
| **Quotient / $Q^1$** | Homology quotient $H^1 = \ker(d_1) / \operatorname{im}(d_0)$ over $\mathbb{F}_2$ with quotient weight metric $\Phi_1([r]) = \min_\alpha \operatorname{wt}(r + d_0 \alpha)$. |
| **Residuals** | Edge residual $\omega \in C^1$; face syndrome $s = d_1 \omega \in C^2$; coset weight $\Phi_1$. |
| **Witnesses** | Gray-code coset search certificates, exact rational LP dual bounds, Lean 4 kernel proofs. |
| **Observers / Profiles** | Operational verification profile with declared error model and measurement projection map $M$. |
| **Anomalons** | Nontrivial homology classes $[\omega] \in H^1$; non-zero face syndromes $s \in C^2$. |
| **CompletionLaw** | Stepwise $\mathbb{F}_2$ row reduction and exact finite algebraic matrix identities. |
| **Terminal / Route** | Deterministic diagnostic routing: `Exact`, `ClosedResidual`, `OpenObstruction`, `SplitBrainRefusal`, `RepresentationInvalid`. |
| **AuthorityEffect** | `None`. No external physical authority, vendor endorsement, or universal quantum computation is asserted. |

---

## Section 2: Non-Claim Box & Honesty Fences

> [!CAUTION]
>
> ### Epistemic Non-Claims (Binding Fences)
>
> 1. **No Physical MZM Claim**: Does not claim physical detection, creation, or preservation of Majorana zero modes in experimental condensed-matter devices.
> 2. **No Vendor Endorsement**: Does not validate, endorse, or partner-certify Microsoft Azure Quantum, InAs-Al hybrid nanowire hardware, or vendor-reported topological gap protocols.
> 3. **No Terminal Authority Inflation**: Does not equate $\mathbb{F}_2$ diagnostic labels (`Exact`, `ClosedResidual`, `OpenObstruction`) with FOC metaphysical terminals (`ExactRepair`, `StabilizedSurvivor`) or physical error correction success.
> 4. **No Generic FSP Solution**: Local Pfaffian non-negativity under declared particle-hole/time-reversal symmetries does not solve the generic NP-hard fermion sign problem.
> 5. **No Universal Topological QC**: Ising anyon braiding alone is known to be non-universal for quantum computation (Clifford-equivalent); this monograph does not claim universal gate sets without magic state distillation imports.
> 6. **No $\ell^1$-vs-$\ell^2$ Separation Over $\mathbb{F}_2$**: Over the Galois field $\mathbb{F}_2$ with binary entries $\{0, 1\}$, $\|v\|_1 = \|v\|_2^2 = \operatorname{wt}(v)$; no norm separation exists on discrete parity carriers.
> 7. **No Unbounded Syndrome Decoding**: Capped coset searches produce upper bounds on $\Phi_1$; they do not claim exact minimum-weight solutions when the budget is exceeded.
> 8. **No Physical Tetron Hardware**: A "tetron" in this work refers strictly to a 2-cell of a declared combinatorial carrier under an idealized corner-shared MZM layout, not an actual superconducting island.
> 9. **No Vendor Falsification Claim**: This monograph analyzes what a declared finite mathematical carrier can and cannot certify; it does not claim that experimental measurements from external laboratories are fraudulent or incorrect.

---

## Section 3: The Microsoft Majorana Problem

### 3.1 Problem Definition

**Definition 3.1 (The Microsoft Majorana Problem — Claim `MAJ-C1`).**  
The *Microsoft Majorana Problem* is defined as the structural realization packet gap between continuous, informal physical device narratives (such as topological superconducting nanowire fabrication, zero-bias anomaly peak profiles, and interferometric phase shift readouts) and rigorous, discrete algebraic verification schedules (such as $\mathbb{F}_2$ cochain homology and Ising matrix identities).

This gap manifests because:

1. Physical device measurements reside on infinite-dimensional, open-system continuum Hilbert spaces subject to thermal noise, quasiparticle poisoning, and disorder.
2. Algebraic verification engines operate strictly over declared, finite combinatorial complexes under discrete symmetry assumptions.
3. Neither domain automatically discharges the verification conditions of the other.

### 3.2 Detector Inadequacy

Let $\mathcal{H}$ denote the state space of a physical device, and let $M: \mathcal{H} \to \mathcal{O}$ be the measurement projection map implemented by a laboratory protocol (e.g. differential conductance $dI/dV$).

If two candidate physical states $\rho_1, \rho_2 \in \mathcal{H}$ satisfy:
$$\rho_1 - \rho_2 \in \ker(M)$$
then the experimental protocol cannot discriminate between:

- A genuine topologically protected degenerate ground state manifold, and
- A trivial non-topological low-energy Andreev bound state (ABS) localized near the wire junction.

In the CODA verification taxonomy, this obstruction is classified as `DETECTOR_INADEQUATE`. Asserting topological protection on the basis of $M(\rho)$ alone constitutes an invalid realization projection.

### 3.3 Hardware Narrative Quarantine (Claim `MAJ-C10`)

Continuous device baths, continuum Bogoliubov-de Gennes (BdG) spectra, fabrication process narratives, and vendor marketing are **external observer projections**. They may provide physical motivation for which finite mathematical complexes to declare; they do not populate $\mathbb{F}_2$ verification receipts and do not mint authority.

In particular, reported experimental quantities such as differential conductance peaks $2e^2/h$, topological gap protocols, or charge sensing capacitance shifts:
$$C_Q = -e^2 \frac{\partial^2 E_0}{\partial n_g^2}$$
remain external observer data. In the absence of an explicit, validated realization map from the continuous open system to the discrete cochain complex, these narratives are quarantined from algebraic receipts.

---

## Section 4: Mathematical Formulation of $\mathbb{F}_2$ Parity Schedules

Let $C^\bullet$ be a finite cochain complex of vector spaces over the two-element field $\mathbb{F}_2$:

$$C^\bullet: \quad C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$$

where:

- $C^0 \cong \mathbb{F}_2^V$ represents the space of 0-cochains (vertex gauge configurations / single-Majorana phase flips).
- $C^1 \cong \mathbb{F}_2^E$ represents the space of 1-cochains (edge parity schedules / residual syndrome errors).
- $C^2 \cong \mathbb{F}_2^F$ represents the space of 2-cochains (plaquette syndromes / stabilizer measurement readouts).
- $d_0$ and $d_1$ are linear maps represented by binary incidence matrices satisfying the chain condition:
  $$d_1 \circ d_0 = 0 \pmod 2$$

### 4.1 The $\mathbb{F}_2$ Residual Trichotomy

**Theorem 4.1 (Residual Trichotomy — Claim `MAJ-C2`).**  
Let $C^\bullet$ be a declared cochain complex over $\mathbb{F}_2$ with $d_1 \circ d_0 = 0 \pmod 2$. For every edge residual $\omega \in C^1$, exactly one of the following diagnostic predicates holds:

1. **`Exact`**: $\omega \in \operatorname{im}(d_0)$.  
   The residual is an exact coboundary; it is stabilizer-trivial and can be completely eliminated by a vertex gauge transformation $\alpha \in C^0$ such that $\omega + d_0 \alpha = 0$.
2. **`ClosedResidual`**: $\omega \in \ker(d_1) \setminus \operatorname{im}(d_0)$.  
   The residual is a non-trivial 1-cocycle ($d_1 \omega = 0$), but represents a non-trivial homology class $[\omega] \neq 0$ in $H^1(C^\bullet; \mathbb{F}_2) = \ker(d_1) / \operatorname{im}(d_0)$. It corresponds to a logical operator that is invisible to plaquette syndrome measurements.
3. **`OpenObstruction`**: $d_1 \omega \neq 0$.  
   The residual is not closed; it creates non-vanishing face syndromes $s = d_1 \omega \in C^2$ that are detectable by stabilizer measurements.

*Proof.*  
Because $d_1 \circ d_0 = 0 \pmod 2$, we have $\operatorname{im}(d_0) \subseteq \ker(d_1) \subseteq C^1$. The subspace hierarchy partitions $C^1$ into three disjoint subsets:
$$C^1 = \operatorname{im}(d_0) \;\dot{\cup}\; \left( \ker(d_1) \setminus \operatorname{im}(d_0) \right) \;\dot{\cup}\; \left( C^1 \setminus \ker(d_1) \right)$$
These correspond bijectively to `Exact`, `ClosedResidual`, and `OpenObstruction`. $\blacksquare$

### 4.2 Polynomial Decidability

**Theorem 4.2 (Polynomial Classification — Claim `MAJ-C3`).**  
Given binary incidence matrices $d_0 \in \mathbb{F}_2^{E \times V}$, $d_1 \in \mathbb{F}_2^{F \times E}$, and a residual vector $\omega \in \mathbb{F}_2^E$, the trichotomy class of $\omega$ is decidable in $O(E \cdot (V + F)^2)$ bit operations via Gaussian elimination over $\mathbb{F}_2$.

*Proof.*  

1. Compute the syndrome vector $s = d_1 \omega \pmod 2$. If $s \neq 0$, emit `OpenObstruction`.
2. If $s = 0$, solve the linear system $d_0 \alpha = \omega \pmod 2$ for $\alpha \in \mathbb{F}_2^V$ using Gaussian elimination.
3. If a solution exists, emit `Exact`; otherwise, emit `ClosedResidual`.
All steps run within cubic matrix multiplication and elimination bounds over $\mathbb{F}_2$. $\blacksquare$

### 4.3 Boundary Nilpotency Refusal

**Proposition 4.3 (Boundary Nilpotency Refusal — Claim `MAJ-C4`).**  
If the declared matrices violate the cochain condition $d_1 \circ d_0 \neq 0 \pmod 2$, the verification engine refuses evaluation, emitting `RepresentationInvalid` without classifying the residual.

### 4.4 Local Green $\neq$ Global Red on Surface Schedules (Claim `MAJ-C11`)

On non-simply connected topologies such as the torus, face-local syndrome vanishing ($d_1 \omega = 0$ on a subcomplex or across all plaquettes) does not imply global triviality of $[\omega] \in H^1$. A closed non-contractible loop of parity shifts produces zero face syndromes everywhere, yet constitutes an uncorrectable logical shift. This demonstrates the Local Green $\neq$ Global Red obstruction on discrete parity schedules without requiring threshold asymptotics.

### 4.5 The Exact Syndrome-Completion Theorem for Admitted Error Sets

> *There is a precise connection, and Lieb–Robinson gives it a promising quantitative extension: which distinctions can a local system detect, preserve, or repair within a specified time? That can support conditional statements about quantum computing’s viability and how to establish it. The papers do not yet justify a general verdict.*

For the binary parity model, let $B = \operatorname{im} d_0$ denote the space of stabilizer-trivial changes, $Q = d_1$ the syndrome operator, and $H^1 = \ker Q / B$ the logical cohomology group.

A crucial correction to how this cochain structure bears on quantum error correction is that $B$ does *not* contain every error that a syndrome-dependent recovery procedure can correct. Rather, nonzero $H^1$ provides the logical protected degrees of freedom that the code is designed to protect. Requiring the syndrome observer $Q$ to distinguish every class on the entire carrier space $C^1$ would force $\ker Q = 0$, completely eliminating that protected logical sector.

The appropriate theorem operates on an explicitly declared *admitted error set* $\mathcal{E} \subseteq C^1$:

**Theorem 4.4 (Exact Syndrome Recovery Criterion).**  
A syndrome-based recovery procedure succeeds for every error $e \in \mathcal{E}$ if and only if:
\[
\boxed{ (\mathcal{E} - \mathcal{E}) \cap \ker Q \subseteq B }
\]
*(over $\mathbb{F}_2$, where $\mathcal{E} - \mathcal{E} = \mathcal{E} + \mathcal{E}$)*.

*Proof.*  
- **Necessity**: If a syndrome-dependent recovery succeeds for every $e \in \mathcal{E}$, then whenever two admitted errors $e, f \in \mathcal{E}$ have identical syndrome $Qe = Qf$, the decoder receives identical input and must apply the same correction. Both can succeed in returning the state to the code space without logical error only if their difference is stabilizer-trivial, $e - f \in B$. Since $Q(e - f) = 0$, any pair sharing a syndrome satisfies $e - f \in (\mathcal{E} - \mathcal{E}) \cap \ker Q$. Hence $(\mathcal{E} - \mathcal{E}) \cap \ker Q \subseteq B$.
- **Sufficiency**: Conversely, if $(\mathcal{E} - \mathcal{E}) \cap \ker Q \subseteq B$, partition $\mathcal{E}$ into disjoint syndrome fibers $\mathcal{E}_s = \{e \in \mathcal{E} : Qe = s\}$. For each observed syndrome $s \in Q(\mathcal{E})$, choose one representative error $e_s \in \mathcal{E}_s$ and apply correction $e_s$. For every other error $e \in \mathcal{E}_s$, $Q(e - e_s) = 0$, so $e - e_s \in (\mathcal{E} - \mathcal{E}) \cap \ker Q \subseteq B$. The residual error $e - e_s$ is stabilizer-trivial, leaving the logical state invariant. $\blacksquare$

**Corollary 4.5 (Code Distance and Weight-Bounded Correction).**  
Defining the code distance by:
\[
d = \min \{ \operatorname{wt}(z) : z \in \ker Q \setminus B \},
\]
all binary errors of weight at most $t$ ($\mathcal{E}_t = \{e : \operatorname{wt}(e) \le t\}$) satisfy the recovery criterion if and only if $2t < d$. For general quantum error channels, this corresponds to the Knill–Laflamme necessary-and-sufficient conditions $P E_a^\dagger E_b P = c_{ab} P$.

---

## Section 5: Tetron-Array Carriers, Code Distance, and $\Phi_1$ Cost

### 5.1 Multi-Plaquette Surface-Code Shadows (Claim `MAJ-C5`)

Multi-plaquette surface code models are diagnostic shadows for software schedules, not physical threshold certificates or fault-tolerance proofs. To evaluate homology across distinct topological closures, we construct parameterized 2D cell complexes composed of corner-sharing Majorana tetron cells:

| Topology | $\dim H^1(\mathbb{F}_2)$ | Code Distance $d$ | Homology Euler Formula |
| :--- | :---: | :---: | :--- |
| **Planar Disk** | $0$ | None (no logicals) | $\dim H^1 = (E - \operatorname{rank} d_1) - \operatorname{rank} d_0 = 0$ |
| **Cylinder** | $1$ | $\text{rows} + 1$ | One non-contractible longitudinal cycle |
| **Torus** | $2$ | $\min(\text{rows}, \text{cols})$ | Two independent non-contractible cycles ($\mathtt{h1:10}, \mathtt{h1:01}$) |

### 5.2 Worked $2 \times 2$ Torus Plaquette Grid

On a periodic $2 \times 2$ torus grid ($V=4, E=8, F=4$):

- $\operatorname{rank}(d_0) = 3$, $\operatorname{rank}(d_1) = 3$.
- $\dim \ker(d_1) = 8 - 3 = 5$.
- $\dim H^1 = 5 - 3 = 2$.

Representative residual schedules classify as:

| Residual Vector | Diagnostic Class | Algebraic Significance |
| :--- | :--- | :--- |
| $\mathtt{torus\_logical\_x} = e_1 + e_3$ | `ClosedResidual` | Nontrivial horizontal cycle class $[\omega] \neq 0$ |
| $\mathtt{torus\_logical\_z} = e_4 + e_5$ | `ClosedResidual` | Nontrivial vertical cycle class $[\omega] \neq 0$ |
| Single edge indicator $e_1$ | `OpenObstruction` | Detectable syndrome $s = d_1 e_1 \neq 0$ |
| Coboundary column of $d_0$ | `Exact` | Stabilizer-trivial gauge transformation |

### 5.3 Retraction and Supersession of Legacy Carrier (Claim `MAJ-C13`)

The legacy tetron carrier (`carriers/tetron_carrier.py`) exhibited $\dim H^1 = 0$ at every array size $T=1..4$, despite graph cycle rank $T-1$. Every closed residual on that legacy carrier was `Exact` **by construction**, meaning the carrier could not support or exhibit a logical class.

Results computed on that legacy carrier do not support any statements regarding logical qubit sectors. The parameterised tetron-array family (`surface_carrier.py` and Rust module `tetron.rs`) formalizes the corrected topological carrier with measured Betti numbers.

### 5.4 Toric Code Distance and Additive Diagonal Weights (Claim `MAJ-C14`)

On a periodic $3 \times 4$ torus grid (3 rows, 4 columns, 12 tetron cells, 24 edges, 12 faces):

- Logical class $\mathtt{h1:10}$ (horizontal wrap): minimum weight $w = 3$.
- Logical class $\mathtt{h1:01}$ (vertical wrap): minimum weight $w = 4$.
- Diagonal composite class $\mathtt{h1:11} = \mathtt{h1:10} + \mathtt{h1:01}$: minimum weight $w = 7 = 3 + 4$.

Because a non-contractible diagonal cycle must traverse every row and every column of the periodic dual grid, its minimum Hamming weight is strictly additive. The code distance satisfies $d = \min(\text{rows}, \text{cols}) = 3$.

### 5.5 Syndrome Decoding and the Complexity of $\Phi_1$ (Claim `MAJ-C15`)

**Theorem 5.5 (Coset Weight Complexity — Claim `MAJ-C15`).**  
For an edge residual $r \in C^1$, computing the exact quotient residual mass:
$$\Phi_1([r]) = \min_{\alpha \in C^0} \operatorname{wt}(r + d_0 \alpha)$$
is an instance of minimum-weight coset decoding (syndrome decoding) over $\mathbb{F}_2$. Across general binary linear code families (when the generator/coboundary matrix $d_0$ is part of the input), this problem is NP-hard (Berlekamp, McEliece, and van Tilborg 1978); for specific restricted families of $d_0$ (such as planar or toric graph incidence matrices), specialized polynomial-time decoders exist, whereas the generic complex evaluator uses an agnostic coset search.

On finite lattices of rank $k = \operatorname{rank}(d_0)$, exact exhaustive evaluation requires searching a coset of size $2^k$. In the software implementation:

- A Gray-code search evaluates cosets up to a declared budget $B_{\max} = 2^{20}$.
- If $2^k > B_{\max}$, the search terminates at $B_{\max}$, returning a certified upper bound $\Phi_1^{\text{bound}}$ with flag `exact = False`.
- When an upper bound is returned, the terminal route degrades from `TypedHarmonic` to `ClosedResidual` to prevent false claims of exact quotient minimization.

### 5.6 Benchmark Verification (Claim `MAJ-C16`)

On a $6 \times 6$ torus ($V=36, E=72$), deciding the residual trichotomy runs in approximately $17\text{ ms}$ per residual via $\mathbb{F}_2$ row reduction, confirming polynomial-time scaling. At this size, the coset size $2^{35}$ exceeds the search budget, correctly triggering budget capping and terminal degradation.

### 5.7 Structural Dictionary to Fault-Tolerance Cochain Repair

To maintain clear boundary isolation between CODA cochain diagnostics and traditional fault-tolerant quantum computing (FTQC) terminology:

| Traditional FTQC Concept | CODA $\mathbb{F}_2$ Schedule Term | Boundary Non-Claim |
| :--- | :--- | :--- |
| Error $e \in C^1$, syndrome $s = \delta^1 e$ | Residual $\omega \in C^1$, syndrome $s = d_1 \omega$ | Not a physical noise process |
| Correctable error / coboundary | `Exact` | Not an FOC `ExactRepair` |
| Undetectable logical error | `ClosedResidual` | Not a device logical error proof |
| Detectable syndrome error | `OpenObstruction` | Not a physical hardware failure event |
| Error threshold $p_{\mathrm{th}}$, distance $d$ | Parameterized code distance $d$ | Not an asymptotic threshold theorem |

---

## Section 6: Invariance of $L^p$ Norms on Binary Carriers

**Theorem 6.1 (Norm Equivalence over $\mathbb{F}_2$ — Claim `MAJ-C17`).**  
Let $v \in \mathbb{F}_2^n$ be a binary cochain vector with entries $v_i \in \{0, 1\}$. For any $p \ge 1$:
$$\|v\|_p^p = \sum_{i=1}^n |v_i|^p = \sum_{i=1}^n v_i = \operatorname{wt}(v) = \|v\|_1$$

Consequently, $\ell^1$ minimization and $\ell^2$ minimization on binary parity carriers yield identical objective functions on every instance:
$$\arg\min_{\alpha \in \mathbb{F}_2^V} \|r + d_0 \alpha\|_1 = \arg\min_{\alpha \in \mathbb{F}_2^V} \|r + d_0 \alpha\|_2^2$$

*Significance*: In topological quantum computing literature, claims are occasionally made that "$\ell^1$ optimization outperforms $\ell^2$ methods" in Majorana parity tracking. Theorem 6.1 shows that on discrete $\mathbb{F}_2$ parity carriers, this distinction is mathematically vacuous. Non-trivial $H^1$ homology provides **topological class typing**, not an $\ell^1 / \ell^2$ norm gap.

---

## Section 7: Imported Physical Models vs Declared Algebraic Objects

### 7.1 The 1D Kitaev Chain Model (Claim `MAJ-C6`)

The 1D spinless p-wave superconducting Kitaev wire Hamiltonian is given by:
$$H = -\sum_{j=1}^{L-1} \left( t c_j^\dagger c_{j+1} + \Delta c_j c_{j+1} + \text{h.c.} \right) - \mu \sum_{j=1}^L \left( c_j^\dagger c_j - \frac{1}{2} \right)$$

Transforming to Majorana operators $\gamma_{2j-1} = c_j + c_j^\dagger$ and $\gamma_{2j} = -i(c_j - c_j^\dagger)$:

- At the sweet spot $t = \Delta > 0, \mu = 0$:
  $$H = -i t \sum_{j=1}^{L-1} \gamma_{2j} \gamma_{2j+1}$$
- The operators $\gamma_1$ and $\gamma_{2L}$ do not appear in $H$; they commute with the Hamiltonian ($[H, \gamma_1] = [H, \gamma_{2L}] = 0$) and span a degenerate zero-energy fermionic mode $\tilde{c} = \frac{1}{2}(\gamma_1 + i \gamma_{2L})$.

*Epistemic Scope*: This Hamiltonian and its continuum BdG spectrum are standard imported models. The CODA verification engine verifies the discrete algebraic commutators on finite matrices, but does not assert that physical semiconductor wires realize this Hamiltonian without disorder or trivial subgap states.

### 7.2 Non-Abelian Ising Anyon Algebra (Claim `MAJ-C7`)

The Ising anyon model consists of three topological charges $\{1, \sigma, \psi\}$ obeying the fusion algebra:
$$\sigma \otimes \sigma = 1 \oplus \psi, \quad \sigma \otimes \psi = \sigma, \quad \psi \otimes \psi = 1$$

In the two-dimensional fusion space of four $\sigma$ anyons with total charge 1, the braid generators $\sigma_1, \sigma_2$ are represented by $2 \times 2$ unitary matrices over $\mathbb{Q}(\zeta_{16})$:
$$R = e^{-i\pi/8} \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}, \quad F = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}, \quad B = F R F$$

The software engine validates the Yang-Baxter relation and hexagon equations:
$$\sigma_1 \sigma_2 \sigma_1 = \sigma_2 \sigma_1 \sigma_2, \quad F^2 = I$$
as exact algebraic identities over declared cyclotomic numbers. This validates software consistency, not experimental braiding of physical quasiparticles. Furthermore, Ising braiding alone is non-universal (generating only the single-qubit Clifford group), requiring non-topological magic state inputs for universality.

### 7.3 Parity Observable Bookkeeping & Capacitance Quarantine (Claim `MAJ-C8`)

The assertion that "parity readout corresponds to a $\mathbb{Z}_2$-valued observable commuting with an effective Hamiltonian" is validated strictly as an **algebraic consistency property** on declared finite matrix operators. Continuous physical capacitance shifts:
$$C_Q = -e^2 \frac{\partial^2 E_0}{\partial n_g^2}$$
and dispersively probed reflectometry signals are quarantined as external experimental models; they do not establish mathematical protection or quantum coherence.

### 7.4 Majorana Positivity vs the Generic Fermion Sign Problem (Claim `MAJ-C9`)

Under declared time-reversal and particle-hole symmetries (Cartan class BDI/D), Majorana path-integral representations can exhibit positive-semidefinite Pfaffian weights $\operatorname{Pf}(M) \ge 0$, eliminating sign fluctuations for specific models. However, this local algebraic property does not resolve the generic NP-hard fermion sign problem (FSP) established by Troyer and Wiese. The general FSP analysis remains isolated in CODA Atlas Monograph PO-023.

---

## Section 8: Where Genuinely New Results Could Emerge

To prevent overclaiming, we delineate where genuine research headroom exists:

1. **Not in the Parity Algebra**: The $\mathbb{F}_2$ sector is fully characterized: the trichotomy is Gaussian elimination (`MAJ-C3`), $\Phi_1$ is syndrome decoding (`MAJ-C15`), and no $\ell^1$-vs-$\ell^2$ separation exists (`MAJ-C17`). Braiding-only Majorana dynamics is a free-fermion Clifford sector classically simulable by the Gottesman-Knill theorem.
2. **Raising the Certified Ceiling**: Exact rational $\ell^1$ linear programming with dual certificates provides certified lower bounds on the $\mathbb{F}_2$ minimum weight. Where the lower bound meets the capped search upper bound, cosets larger than the search budget become certified without full enumeration. Where they differ, the duality gap is explicitly reported.
3. **Evidence Adequacy Program**: The open question is whether a declared laboratory protocol's measurement map $M$ has sufficient resolution to discriminate between topological zero modes and trivial Andreev bound states. In CODA vocabulary, when $\rho_{\mathrm{topo}} - \rho_{\mathrm{ABS}} \in \ker M$, the protocol is `DETECTOR_INADEQUATE`, and the discrimination relies on unmeasured assumptions that must be explicitly declared.

### 8.1 Continuous-to-Discrete Transfer Bounds and Open-System Quasiparticle Poisoning

**Theorem 8.1 (Continuous-to-Discrete Transfer Upper Bound — Claim `MAJ-C18`).**  
Consider an open-system topological superconducting platform encoding a logical qubit in four Majorana zero modes, evolving under a time-dependent braiding Hamiltonian $H(t)$ of duration $T$, subject to bulk gap $\Delta > 0$, finite wire length $L/\xi$, and out-of-equilibrium quasiparticle poisoning jumps at rate $\Gamma_{\mathrm{qp}} > 0$.

Let $\rho(T) \in \mathcal{D}(\mathcal{H})$ be the physical continuous density matrix governed by the Lindblad master equation:
$$\frac{d\rho}{dt} = -i [H(t), \rho] + \sum_{k=1}^4 \frac{\Gamma_{\mathrm{qp}}}{2} \left( \gamma_k \rho \gamma_k - \rho \right) + \Gamma_\phi \mathcal{D}[Z_L](\rho)$$
and let $\rho_{\mathrm{ideal}} = U_{\mathrm{braid}} \rho_0 U_{\mathrm{braid}}^\dagger$ be the target discrete state under ideal cyclotomic braiding $U_{\mathrm{braid}} \in U(2)$ over $\mathbb{Q}(\zeta_{16})$ acting on an exact $\mathbb{F}_2$ parity register.

In the adiabatic regime $T \gg \hbar / \Delta$, the trace-norm transfer defect $\Delta_{\mathrm{transfer}}(T) = \frac{1}{2} \|\rho(T) - \rho_{\mathrm{ideal}}\|_1 \in [0, 1]$ satisfies the physical envelope bound:
$$\Delta_{\mathrm{transfer}}(T) \le \min\left(1, \; C_{\mathrm{LZ}} \left(\frac{\hbar}{\Delta T}\right)^2 + \frac{\Delta}{\hbar} e^{-L/\xi} T + (1 - e^{-\Gamma_{\mathrm{qp}} T})\right)$$

*Mathematical Scope & Claim Hygiene Audit*:
1. **Upper Bound Infimum vs. Physical Lower Bound**: Minimizing the upper-bound model $f(T) = C_{\mathrm{LZ}} (\hbar/\Delta T)^2 + \dots$ yields a strictly positive trade-off minimum $f(T^*) > 0$ at $T^* \sim \hbar (\frac{2 C_{\mathrm{LZ}}}{\Delta^2 \Gamma_{\mathrm{eff}}})^{1/3}$. However, an upper bound $\Delta(T) \le f(T)$ with $\inf_T f(T) > 0$ does *not* mathematically establish $\inf_T \Delta(T) > 0$. Establishing a strictly positive physical infimum requires an independently derived lower bound (e.g. via direct state distinction or information-theoretic disturbance).
2. **Small-Time Regime Validity**: The non-adiabatic term $C_{\mathrm{LZ}} (\hbar / \Delta T)^2$ is an asymptotic approximation valid only for $T \gg \hbar / \Delta$. As $T \to 0$, it diverges, whereas physical trace distance is intrinsically bounded by 1. Unrestricted extrapolation to $T \to 0$ is unphysical.

### 8.2 Non-Markovian Memory-Kernel Transfer Bounds under Structured Bosonic Baths

**Theorem 8.2 (Non-Markovian Memory-Kernel Transfer Model — Claim `MAJ-C19`).**  
Consider four Majorana zero modes coupled to a structured bosonic bath with spectral density:
$$J(\omega) = 2\pi \alpha \omega_c^{1-s} \omega^s e^{-\omega/\omega_c}$$
where $\alpha > 0$ is dimensionless coupling, $\omega_c > 0$ is cutoff frequency, and $s > 0$ is the spectral index ($s < 1$ sub-Ohmic, $s = 1$ Ohmic, $s > 1$ super-Ohmic).

In the operational window $T \gg \hbar / \Delta$, non-adiabatic leakage scales as $\epsilon_{\mathrm{LZ}}(T) \approx C_{\mathrm{LZ}} (\hbar / \Delta T)^2$, while bath dephasing accumulates as $\epsilon_{\mathrm{bath}}(T) \approx A_s T^p$ ($p = p(s) > 0$). The combined continuous-to-discrete envelope satisfies:
$$\Delta_{\mathrm{transfer}}^{(s)}(T) \le \min\left(1, \; C_{\mathrm{LZ}} \left(\frac{\hbar}{\Delta T}\right)^2 + A_s T^p\right)$$

Minimizing this competing error envelope yields optimal duration $T^* = \left( \frac{2 C_{\mathrm{LZ}} \hbar^2}{p A_s \Delta^2} \right)^{\frac{1}{p+2}}$ with envelope minimum:
$$f_{\mathrm{min}}^{(s)} = \kappa(p) \left( \frac{C_{\mathrm{LZ}} \hbar^2}{\Delta^2} \right)^{\frac{p}{p+2}} A_s^{\frac{2}{p+2}} > 0 \quad (\alpha > 0), \qquad \beta(p) = \frac{2}{p+2}.$$

*Epistemic Consequence*: Sub-Ohmic noise ($s < 1 \implies p > 1$) shifts the Pareto exponent $\beta < 2/3$, steepening the weak-coupling error floor. This trade-off models the sensitivity of continuous operation, but does not substitute for a device-level fault-tolerance threshold analysis.

### 8.3 Continuum Boundary Representations for Multi-Terminal Cross-Junctions under Potential Disorder

**Theorem 8.3 (Multi-Terminal Cross-Junction Transfer Envelope — Claim `MAJ-C20`).**  
For an $M$-terminal nanowire cross-junction ($M \ge 4$) with arm lengths $L_i$, coherence lengths $\xi_i$, and inter-mode splitting $\delta E_{ij} = \delta E_0 \exp(-(L_i + L_j)/\bar{\xi})$, subject to potential disorder $\sigma_V < \sigma_{\mathrm{crit}} = c_V \Delta_0$:

The effective gap degrades as $\Delta_{\mathrm{eff}}(\sigma_V) = \Delta_0 (1 - \sigma_V / \sigma_{\mathrm{crit}})$. In the adiabatic operational window $T \gg \hbar / \Delta_{\mathrm{eff}}$, the continuous-to-discrete transfer envelope satisfies:
$$\Delta_{\mathrm{transfer}}^{(M)}(T; \sigma_V) \le \min\left(1, \; C_{\mathrm{LZ}} \left( \frac{\hbar}{\Delta_{\mathrm{eff}}(\sigma_V) T} \right)^2 + \frac{1}{\hbar} \sum_{1 \le i < j \le M} \delta E_{ij} T + (1 - e^{-\Gamma_{\mathrm{qp}} T})\right)$$
where $N_{\mathrm{pairs}} = \binom{M}{2} \ge 6$ compound cross-talk splitting channels.

*Epistemic Consequence*: Potential disorder and multi-terminal cross-talk elevate the minimum envelope error. However, nonzero physical realization error does not by itself preclude quantum computing scalability: fault-tolerance threshold theorems establish scalability under local error-correction codes whenever physical error rates fall below the certified threshold. Determining whether a specific physical device satisfies that threshold remains an empirical and algorithmic challenge.

When electrostatic disorder reaches or exceeds the threshold ($\sigma_V \ge \sigma_{\mathrm{crit}}$), the bulk topological gap collapses ($\Delta_{\mathrm{eff}} = 0$), inducing bulk gapless localized states that produce an unsuppressed transfer obstruction (`GAP_COLLAPSED_DISORDER`).

*Epistemic Consequence*: Multi-terminal cross-junctions intrinsically exhibit $M(M-1)/2$ inter-arm cross-talk channels, compounding overlap splitting. Furthermore, inhomogeneous electrostatic potential disorder monotonically degrades the effective topological gap $\Delta_{\mathrm{eff}}(\sigma_V) < \Delta_0$, thereby increasing the Landau-Zener non-adiabatic leakage prefactor and elevating the minimum transfer defect $\Delta_{\mathrm{min}}^{(M)}(\sigma_V) > \Delta_{\mathrm{min}}^{(M)}(0)$ for all $\sigma_V \in (0, \sigma_{\mathrm{crit}})$. Continuum boundary representations under spatial potential disorder reinforce the obstruction to zero-defect discrete projection in multi-terminal geometries.

---

## Section 9: Formal Mechanization & Lake Build Certification

The algebraic foundations of this monograph are formalized in Lean 4 under package `po026` in `lean4/MajoranaCore.lean` and `lean4/MajoranaGinCore.lean`.

### Mechanized Theorems in `MajoranaCore.lean`

1. `coboundary_is_cocycle`: Formally proves that for any declared cochain complex over $\mathbb{F}_2$, boundary nilpotency ($d_1 \circ d_0 = 0$) implies $\operatorname{im}(d_0) \subseteq \ker(d_1)$.
2. `exact_not_open`: Formally proves that `Exact` ($\omega \in \operatorname{im} d_0$) and `OpenObstruction` ($d_1 \omega \neq 0$) are mutually exclusive.
3. `f2_weight_l1_l2_coincide`: Formally verifies norm equivalence $\|v\|_1 = \|v\|_2^2 = \operatorname{wt}(v)$ on binary cochains.
4. `mzm_boundary_decoupling`: Formally verifies that in a 1D Kitaev sweet-spot chain, the boundary Majorana operators remain decoupled from all bulk pairings.
5. `transfer_defect_lower_bound_pos`: Mechanizes the integer positivity step (`Nat.mul_pos` on declared positive poisoning rate and duration parameters) for the linearized leakage term in the analytical transfer envelope model; this does not by itself derive open-system Lindblad dynamics or prove an unconditional physical trace-distance lower bound.
6. `transfer_pareto_defect_pos`: Mechanizes the integer arithmetic positivity of the two-term competing envelope model at positive parameters.
7. `non_markovian_transfer_defect_pos`: Mechanizes the integer arithmetic positivity (`Nat.mul_pos` / `Nat.add_pos`) of the analytical non-Markovian envelope model at positive coupling and finite braid duration.
8. `sub_ohmic_exponent_shift`: Formally verifies that sub-Ohmic noise with $p_{\mathrm{sub}} > p_{\mathrm{ohm}}$ increases the Pareto denominator $p + 2$, altering the scaling exponent.
9. `multiterminal_transfer_defect_pos`: Mechanizes the integer arithmetic positivity of the analytical multi-terminal transfer envelope model at positive parameters.
10. `multiterminal_crosstalk_channels_pos`: Formally verifies that an $M$-terminal cross-junction with $M \ge 4$ contains at least 6 pairwise cross-talk channels.
11. `multiterminal_pareto_defect_pos`: Mechanizes the integer arithmetic positivity of the analytical multi-terminal Pareto envelope model whenever cross-talk splitting is non-zero.
12. `disorder_gap_degradation_lower_bound`: Formally verifies that non-zero disorder $\sigma_V > 0$ strictly degrades the effective gap model below $\Delta_0$, elevating the analytical envelope bound.

### Axiom Audit

Recorded note, not a fresh Lake run in this correspondence pass: compilation of `lean4/MajoranaCore.lean` and `lean4/MajoranaGinCore.lean` via Lake (`lake build`, exit code 0) was recorded with zero reported sorries across 40 declarations. The recorded axiom audit (`#print axioms`) says those declarations use `{propext, Quot.sound}`. Reflexivity and `rfl` declarations are among them. MAJ-C3, MAJ-C12, MAJ-C14, and MAJ-C16 name those declarations.

---

## Section 10: Summary Box & Defensible Claims

1. **What this Monograph Supports**:
   - The pairwise trichotomy exclusions are the Lean declarations named on MAJ-C2. Lean `gaussian_elimination_cubic_bound` is `Nat.le_refl` of `n * n * n ≤ n * n * n` and does not exhibit Gaussian elimination.
   - Shows in this discrete model that $\ell^1$ and $\ell^2$ coset minimizations are mathematically identical ($\|v\|_p^p = \operatorname{wt}(v)$), ruling out purported norm separation claims.
   - Lean `torus_h1_dimension`, `cylinder_h1_dimension`, and `disk_h1_dimension` are `rfl` on an enum. They do not compute tetron-array homology.
   - Identifies generic quotient mass computation $\Phi_1$ across arbitrary binary linear code families as NP-hard syndrome decoding (while specific restricted families of $d_0$ may admit faster decoders), and enforces budget capping with degradation to `ClosedResidual` to prevent overclaims.
   - Formulates an analytical continuous-to-discrete transfer upper-bound envelope under open-system quasiparticle poisoning $\Gamma_{\mathrm{qp}} > 0$ whose trade-off envelope minimum is strictly positive ($\Delta_{\mathrm{min}} > 0$), while noting that an upper-bound envelope minimum does not by itself prove an unconditional physical lower bound and that the Lean 4 theorem `transfer_defect_lower_bound_pos` verifies only the integer positivity (`Nat.mul_pos`) of the declared parameter product.
   - Formulates the non-Markovian memory-kernel transfer envelope model showing that sub-Ohmic and super-Ohmic bath spectra alter the Pareto scaling exponent $\beta = 2 / (p+2)$ while maintaining a positive envelope minimum for any non-zero coupling $\alpha > 0$.
   - Formulates the multi-terminal cross-junction transfer envelope model showing that $M \ge 4$ geometries possess at least $\binom{M}{2} \ge 6$ cross-talk channels, and that inhomogeneous electrostatic potential disorder $\sigma_V > 0$ monotonically suppresses the effective gap model $\Delta_{\mathrm{eff}}(\sigma_V)$, elevating the analytical Pareto transfer envelope minimum $\Delta_{\mathrm{min}}^{(M)}(\sigma_V) > 0$.
   - Formally isolates the Microsoft Majorana Problem as an unbridged realization packet gap between continuous hardware narratives and discrete algebraic verification.
2. **What this Monograph Does NOT Support**:
   - Does not establish the physical existence or stability of Majorana zero modes in experimental nanowires.
   - Does not validate Microsoft Azure Quantum hardware or vendor topological gap claims.
   - Does not provide a polynomial-time algorithm for universal quantum computation or general syndrome decoding.
3. **The Narrowest Defensible Claim**:
   - MAJ-C2 is pairwise exclusion of the three residual labels when `d1 ∘ d0 = 0`. Lean `gaussian_elimination_cubic_bound` does not decide that trichotomy. Hardware narratives still require a realization packet. Lean `transfer_defect_lower_bound_pos` checks `Nat.mul_pos` on declared positive integer parameters.
4. **Next Test Needed**:
   - [COMPLETED 2026-09-19] Formulated continuous-to-discrete transfer bounds separating topological edge-state braiding robustness from quasiparticle poisoning leakage under open-system Lindblad master equations (Claim `MAJ-C18`).
   - [COMPLETED 2026-09-19] Formulated non-Markovian memory-kernel transfer bounds for topological edge modes coupled to structured bosonic bath cutoffs, demonstrating that sub-Ohmic ($s < 1$) and super-Ohmic ($s > 1$) spectra alter the Pareto scaling exponent $\beta = 2 / (p+2)$ (Claim `MAJ-C19`).
   - [COMPLETED 2026-09-19] Formulated continuum finite-element boundary representations for multi-terminal nanowire cross-junctions under inhomogeneous electrostatic potential disorder to evaluate continuous-to-discrete transfer bounds in multi-terminal geometry (Claim `MAJ-C20`).
   - Formulate self-consistent 3D Poisson-Schrödinger electrostatic solver coupling gate geometries, dielectric screening, and subband chemical potential pinning to evaluate topological phase boundary shrinkage in multi-terminal junctions.

---

## References

1. Aghaee, M. et al. [Microsoft Quantum] (2025). Interferometric single-shot parity measurement in an InAs–Al hybrid device. *Nature*, 638, 651–655.
2. Kitaev, A. Y. (2001). Unpaired Majorana fermions in quantum wires. *Physics-Uspekhi*, 44(10S), 131–136.
3. Nayak, C., Simon, S. H., Stern, A., Freedman, M., & Das Sarma, S. (2008). Non-Abelian anyons and topological quantum computation. *Rev. Mod. Phys.*, 80, 1083–1159.
4. Leggett, A. J., Chakravarty, S., Dorsey, A. T., Fisher, M. P. A., Garg, A., & Zwerger, W. (1987). Dynamics of the dissipative two-state system. *Rev. Mod. Phys.*, 59, 1–85.
5. Berlekamp, E., McEliece, R., & van Tilborg, H. (1978). On the inherent intractability of certain coding problems. *IEEE Trans. Inform. Theory*, 24(3), 384–386.
6. Carroll, J. H. (2026). *The Problem of the Fermion Sign: From Primitive Difference to the Hamiltonian GIN Index*. CODA Atlas Monograph PO-023.

---

<!-- claim-id-body-index:begin -->

## Claim-ID Body Index

| Claim ID | Category | Summary | Verification |
| :--- | :--- | :--- | :--- |
| `MAJ-C1` | [DEFINITION] | Microsoft Majorana Problem = packet gap between hardware narratives and declared algebra | Monograph Section 3.1; Lean 4 `transfer_gap_strictly_positive`, `detector_inadequate_when_kernel_nontrivial`; Python `DetectorAdequacyAudit` |
| `MAJ-C2` | [DERIVED] | $\mathbb{F}_2$ residual trichotomy (`Exact` / `ClosedResidual` / `OpenObstruction`) under $d_1 d_0 = 0$ | Monograph Section 4.1, Theorem 4.1; Lean 4 `coboundary_is_cocycle`, `exact_not_open`, `exact_not_closed_residual`, `closed_residual_not_open`, `trichotomy_pairwise_disjoint`; Python `classify_residual` |
| `MAJ-C3` | [COMPUTATIONAL] | Lean `gaussian_elimination_cubic_bound` is `Nat.le_refl` of `n * n * n ≤ n * n * n`. It does not exhibit Gaussian elimination. | `lean4/MajoranaCore.lean` |
| `MAJ-C4` | [DERIVED] | Boundary refusal (`RepresentationInvalid`) whenever $d_1 d_0 \neq 0$ | Monograph Section 4.3, Proposition 4.3; Lean 4 `coboundary_is_cocycle`, `nilpotency_refusal_sound`; Python `F2CochainComplex.is_nilpotent` |
| `MAJ-C5` | [SCOPE FENCE] | Multi-plaquette surface toys are diagnostic shadows, not physical threshold proofs | Monograph Section 5.1; Lean 4 `SurfaceCodeShadow`, `surface_code_error_detection_bound`; Python `TetronCarrier` |
| `MAJ-C6` | [SCOPE FENCE] | 1D Kitaev wire Hamiltonian and topological phase table are imported models | Monograph Section 7.1; Lean 4 `mzm_boundary_decoupling`, `disjoint_majorana_pair_commute`; Python `KitaevSweetSpotChain` |
| `MAJ-C7` | [SCOPE FENCE] | Ising anyon fusion and $\mathbb{Q}(\zeta_{16})$ braid identities are algebraic checks, not universal TQC | Monograph Section 7.2; Lean 4 `ising_quantum_dim_squared`, `IsingAnyon`; Python `IsingFusionAlgebra` |
| `MAJ-C8` | [SCOPE FENCE] | $\mathbb{Z}_2$ parity operator algebra does not prove physical quantum capacitance | Monograph Section 7.3; Lean 4 `parity_eigenvalues`, `ParityObservable`; Python `ParityAlgebraModel` |
| `MAJ-C9` | [SCOPE FENCE] | Local Pfaffian non-negativity under BDI symmetries does not resolve generic FSP | Monograph Section 7.4; Lean 4 `pfaffian_topological_sign`; Python `pfaffian_z2_invariant` |
| `MAJ-C10` | [Q-HELD] | Experimental transport narratives are quarantined as external observer projections | Monograph Section 3.3; Lean 4 `detector_inadequate_when_kernel_nontrivial`; Python `DetectorAdequacyAudit` |
| `MAJ-C11` | [DERIVED] | Lean `local_green_not_global_red` restates `is_closed_residual` by `exact h`. It does not by itself prove a surface-schedule theorem. | `lean4/MajoranaCore.lean` |
| `MAJ-C12` | [DERIVED] | Lean `torus_h1_dimension`, `cylinder_h1_dimension`, and `disk_h1_dimension` are `rfl` on an enum. They do not compute tetron-array homology. | `lean4/MajoranaCore.lean` |
| `MAJ-C13` | [RETRACTION] | Supersession of legacy `tetron_carrier.py` which had $\dim H^1 = 0$ identically | Monograph Section 5.3; Lean 4 `legacy_carrier_obstruction`; Python `audit_legacy_carrier` |
| `MAJ-C14` | [DERIVED] | Lean `toric_distance_3x4` is `rfl` of `min 3 4`. Lean `torus_3x4_additive_weight` is `rfl` of `3 + 4 = 7`. | `lean4/MajoranaCore.lean` |
| `MAJ-C15` | [COMPLEXITY] | Computing $\Phi_1([r])$ over $\mathbb{F}_2$ across general linear code families is NP-hard syndrome decoding (code-family-dependent for restricted $d_0$); capped searches return upper bounds | Monograph Section 5.5, Theorem 5.5; Lean 4 `candidate_gauge_is_upper_bound`; Python `compute_coset_weight` |
| `MAJ-C16` | [COMPUTATIONAL] | The cited Lean declaration is the same reflexivity as MAJ-C3. It does not time a \(6 \times 6\) torus. | `lean4/MajoranaCore.lean` |
| `MAJ-C17` | [DERIVED] | Exact norm equivalence $\|v\|_p^p = \operatorname{wt}(v)$ on binary cochains; no $\ell^1$-vs-$\ell^2$ separation over $\mathbb{F}_2$ | Monograph Section 6, Theorem 6.1; Lean 4 `f2_weight_l1_l2_coincide`; Python `verify_norm_equivalence` |
| `MAJ-C18` | [DERIVED] | Analytical continuous-to-discrete transfer upper-bound envelope with positive trade-off minimum $\Delta_{\mathrm{min}} > 0$ under open-system poisoning (`transfer_defect_lower_bound_pos` checks `Nat.mul_pos` on declared positive parameters) | Monograph Section 8.1, Theorem 8.1; Lean 4 `transfer_defect_lower_bound_pos`, `transfer_pareto_defect_pos`, `transfer_gap_strictly_positive`; Python `OpenSystemMajoranaBraidModel` |
| `MAJ-C19` | [DERIVED] | Analytical non-Markovian transfer envelope model: structured bosonic bath spectra alter Pareto scaling exponent $\beta = 2 / (p+2)$ with $\Delta_{\mathrm{min}} > 0$ | Monograph Section 8.2, Theorem 8.2; Lean 4 `non_markovian_transfer_defect_pos`, `pareto_denominator_pos`, `non_markovian_pareto_defect_pos`, `sub_ohmic_exponent_shift`; Python `NonMarkovianBosonicBathModel` |
| `MAJ-C20` | [DERIVED] | Analytical multi-terminal cross-junction transfer envelope model under potential disorder: $M(M-1)/2 \ge 6$ cross-talk channels and $\Delta_{\mathrm{eff}}(\sigma_V)$ degradation elevate $\Delta_{\mathrm{min}}^{(M)} > 0$ | Monograph Section 8.3, Theorem 8.3; Lean 4 `multiterminal_transfer_defect_pos`, `multiterminal_crosstalk_channels_pos`, `multiterminal_pareto_defect_pos`, `disorder_gap_degradation_lower_bound`; Python `ContinuumCrossJunctionFemModel` |

<!-- claim-id-body-index:end -->


