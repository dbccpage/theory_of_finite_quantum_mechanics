---
documentation_contract: symbol-game-documentation/v1
title: "MSS-N Level 63: Discrete gravity"
kind: grammar-reference
level: 63
status: active
maturity: research
atlas_status: specified
evidence_grades:
  named: true
  syntax: true
  computed: true
  Lean: false
  gated: true
successor_status: declared
successor:
  row: MSS-64
  relation: declared_research_successor
  lift_status: unlicensed
lift_status: unlicensed
lift_proof_status: absent
lift_license_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md
---

# MSS-N Level 63: Discrete gravity

**AuthorityEffect:** None.\
**Level:** Level 63 (Epoch V: Gauge Theory & Discrete Spacetime)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(63) = 128 + 8 \times (63 - 22) = 456$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*\
**Runtime Pipeline:** `Evaluator::targets.stage_063` | Primary Error: `ERR_SIMPLICIAL_METRIC_DEFECT`\
**Atlas Capabilities:** `simplicial_metric`, `metric_action`

---

## Part I: Row Contract

### 1. Architectural Overview & Context

Level 63 resides within **Epoch V: Gauge Theory & Discrete Spacetime** in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=63$.

- **Stage Classification:** Finite typed representation of discrete Regge calculus, piecewise-flat simplicial metrics, Cayley-Menger nondegeneracy, hinge deficit angles, and discrete gravitational actions without self-granting authority.
- **Mathematical Substrate:** A discrete $D$-dimensional simplicial complex $M = (\Delta_0, \Delta_1, \dots, \Delta_D)$ equipped with piecewise-flat Regge geometry:
  1. **Declared Dimension:** Discrete spacetime dimension $D \in \{2, 3, 4\}$.
  2. **Simplex Metric Representation:** For each 1-simplex (edge) $e = (v_i, v_j) \in \Delta_1$, an exact squared edge length $\ell_e^2 \in \mathbb{Q}_{>0}$.
  3. **Geometric Nondegeneracy & Cayley-Menger Determinant:**
     For every $D$-simplex $\sigma = (v_0, \dots, v_D) \in \Delta_D$, the Cayley-Menger matrix $C(\sigma)$ is defined by:
     $$C(\sigma) = \begin{pmatrix} 0 & 1 & 1 & \dots & 1 \\ 1 & 0 & \ell_{01}^2 & \dots & \ell_{0D}^2 \\ 1 & \ell_{10}^2 & 0 & \dots & \ell_{1D}^2 \\ \vdots & \vdots & \vdots & \ddots & \vdots \\ 1 & \ell_{D0}^2 & \ell_{D1}^2 & \dots & 0 \end{pmatrix}$$
     The metric must satisfy the strict geometric nondegeneracy test:
     $$\det(C(\sigma)) \cdot (-1)^{D+1} > 0$$
     guaranteeing positive squared $D$-volume $V_\sigma^2 = \frac{(-1)^{D+1}}{2^D (D!)^2} \det(C(\sigma)) > 0$ and strict satisfaction of all generalized triangle inequalities.
  4. **Hinge Incidence & Codimension-2 Bones:**
     A hinge $h \in \Delta_{D-2}$ is a codimension-2 simplex (vertices in 2D, edges in 3D, triangles in 4D). For each hinge $h$, its incidence star is $\operatorname{Star}(h) = \{\sigma \in \Delta_D \mid h \subset \sigma\}$.
  5. **Dihedral Angles & Deficit Curvature:**
     For each incident simplex $\sigma \in \operatorname{Star}(h)$, the interior dihedral angle $\theta_h(\sigma)$ at hinge $h$ is determined from the Cayley-Menger cofactor subdeterminants. The discrete deficit angle representing localized scalar curvature is:
     $$\epsilon_h = 2\pi - \sum_{\sigma \in \operatorname{Star}(h)} \theta_h(\sigma)$$
  6. **Discrete Regge Gravitational Action:**
     $$S_R = \sum_{h \in \Delta_{D-2}} V_h \cdot \epsilon_h - \Lambda \sum_{\sigma \in \Delta_D} V_\sigma$$
     where $V_h$ is the volume of hinge $h$, $V_\sigma$ is the volume of $D$-simplex $\sigma$, and $\Lambda \in \mathbb{Q}$ is the declared cosmological constant.

### 2. Wire Packet Grammar & Mathematical Carrier

The wire packet explicitly declares the dimension, simplicial mesh topology, squared edge lengths, Cayley-Menger determinants, hinge incidence catalog, and evaluated Regge action:

```text
<spacetime_dimension simplicial_mesh squared_edge_lengths cayley_menger_witness hinge_incidence regge_action_receipt>
```

- `spacetime_dimension`: Dimension integer $D \in \{2, 3, 4\}$.
- `simplicial_mesh`: Triangulation topology catalog $\Delta_0, \dots, \Delta_D$.
- `squared_edge_lengths`: Dictionary mapping edges $e \in \Delta_1$ to rational squared lengths $\ell_e^2 \in \mathbb{Q}_{>0}$.
- `cayley_menger_witness`: Dictionary mapping each $D$-simplex $\sigma \in \Delta_D$ to its evaluated determinant $\det(C(\sigma))$.
- `hinge_incidence`: Dictionary mapping each hinge $h \in \Delta_{D-2}$ to incident simplices $\operatorname{Star}(h)$ and dihedral angles $\theta_h(\sigma)$.
- `regge_action_receipt`: Recomputed discrete Regge action value $S_R \in \mathbb{Q}$ with cosmological constant $\Lambda \in \mathbb{Q}$.

### 3. Runtime Pipeline Evaluator & Verification Obligation

- **Runtime Pipeline:** `Evaluator::targets.stage_063`
- **Primary Error Code:** `ERR_SIMPLICIAL_METRIC_DEFECT`
- **Atlas Capabilities:** `simplicial_metric`, `metric_action`
- **Locally Checkable Verification Obligation:**
  1. **Strict Length Positivity:** Check that $\ell_e^2 > 0$ in $\mathbb{Q}$ for all edges $e \in \Delta_1$.
  2. **Cayley-Menger Nondegeneracy:** Recompute $\det(C(\sigma))$ for every $D$-simplex and verify that $\det(C(\sigma)) \cdot (-1)^{D+1} > 0$.
  3. **Hinge Incidence Closure:** Verify that every hinge $h \in \Delta_{D-2}$ is properly indexed and that all incident simplices in $\operatorname{Star}(h)$ share $h$ as a sub-simplex.
  4. **Action Recomputation:** Recompute the discrete Regge action $S_R = \sum_h V_h \epsilon_h - \Lambda \sum_\sigma V_\sigma$ and assert agreement with `regge_action_receipt`.
- **Falsifier Boundary / Negative Counterexample:**
  - A triangulation containing a degenerate or inverted simplex ($\det(C(\sigma)) \cdot (-1)^{D+1} \le 0$) is rejected with `ERR_SIMPLICIAL_METRIC_DEFECT`.
  - An evaluated Regge action computed without hinge incidence or using inconsistent edge lengths across shared faces is rejected with `ERR_SIMPLICIAL_METRIC_DEFECT`.
- **Boundary Warning:** Level 63 records computed/gated verification receipts; it does not confer ambient authority or self-grant execution privileges.

### 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-63 within Epoch V: Gauge Theory & Discrete Spacetime.
   - Computed/gated verification receipts enforcing Cayley-Menger metric nondegeneracy, hinge deficit angle calculation, and exact discrete Regge action evaluation.
2. **What this does not support:**
   - Does not establish an automatic retraction from MSS-62 or claim continuum smooth Einstein-Hilbert limit without explicit refinement sequences.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-63 accepts valid discrete Regge geometry packets satisfying Cayley-Menger nondegeneracy and rejects degenerate or metric-inconsistent simplicial complexes with `ERR_SIMPLICIAL_METRIC_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=64$ discrete Bianchi identity fixtures using the local CI test harness.

---

## Part II: Lift Record from Predecessor (MSS-62 $\to$ MSS-63)

- **Lift Status:** `unlicensed` (lift_license_status: unlicensed, lift_proof_status: absent; design-stage specification row; no conservative embedding or retraction proof $r_{63}(u_{63}(x))=x$ has been licensed from MSS-62).
- **Predecessor Stage:** MSS-62 (`level_62_discrete_lattice_gauge.md`).
- **Successor Rationale:** When 2-cell lattice gauge theories (MSS-62) lack dynamical metric degrees of freedom, edge length assignments, and simplicial curvature deficits, MSS-63 is declared as the specification row providing discrete Regge gravity within the external research atlas.
- **Conditional Lift Obligation:** Any future accepted lift into MSS-63 must exhibit $(u_{63}, r_{63})$ satisfying $r_{63}(u_{63}(x)) = x$. No predecessor lift is currently claimed (`lift_status: unlicensed`, `lift_proof_status: absent`).
