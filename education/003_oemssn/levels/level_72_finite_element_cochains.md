---
documentation_contract: symbol-game-documentation/v1
title: "MSS-N Level 72: Finite mesh cochains"
kind: grammar-reference
level: 72
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
  row: MSS-73
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

# MSS-N Level 72: Finite mesh cochains

**AuthorityEffect:** None.\
**Level:** Level 72 (Epoch VI: Hardness, Real Numbers & Continuum Fences)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(72) = 128 + 8 \times (72 - 22) = 528$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*\
**Runtime Pipeline:** `Evaluator::targets.stage_072` | Primary Error: `ERR_MESH_COMPLEX_DEFECT`\
**Atlas Capabilities:** `mesh_cochains`, `boundary_operator`

> [!NOTE]
> **Nomenclature Precision:** This stage is canonically titled **Finite Mesh Cochains** (formerly designated *Finite element cochains*). Incidence nilpotence and boundary conditions define a combinatorial mesh and cochain complex, but do not by themselves constitute a Finite Element Exterior Calculus (FEEC) method. Full FEEC requires polynomial basis spaces, degrees of freedom, mass/stiffness bilinear forms, and commuting canonical projections, which are not assumed at this row.

---

## Part I: Row Contract

### 1. Architectural Overview & Context

Level 72 resides within **Epoch VI: Hardness, Real Numbers & Continuum Fences** in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=72$.

- **Stage Classification:** Finite typed representation of cell mesh complexes, incidence boundary operators, and discrete cochain evaluation without self-granting authority.
- **Mathematical Carrier & Discrete Complex:**
  1. **Mesh Complex $K$:** A finite cell complex decomposed by dimension $K = \bigcup_{k=0}^D K_k$, where $K_k$ is the finite set of $k$-dimensional cells.
  2. **Signed Boundary Operators:** Rational matrices $[\partial_k] \in \{-1, 0, 1\}^{|K_{k-1}| \times |K_k|}$ encoding oriented geometric incidence.
  3. **Coboundary Operator (Discrete Exterior Derivative):**
     $$d^k = \partial_{k+1}^T: C^k(K; \mathbb{Q}) \to C^{k+1}(K; \mathbb{Q})$$
  4. **Algebraic Nilpotence:**
     Exact algebraic verification that every boundary of a boundary vanishes identically:
     $$\partial_{k-1} \circ \partial_k = 0 \quad \iff \quad [\partial_{k-1}][\partial_k] = 0_{|K_{k-2}| \times |K_k|}$$
     and dually $d^k \circ d^{k-1} = 0$.
  5. **Discrete Cochains & Boundary Conditions:**
     A discrete $k$-cochain $\omega^k \in C^k(K; \mathbb{Q})$ assigns exact rational values to $k$-cells. Essential boundary conditions are verified on the marked boundary subcomplex $\partial K \subset K$.

### 2. Wire Packet Grammar & Mathematical Carrier

The wire packet explicitly declares the graded cell complex dimensions, signed boundary incidence matrices, cochain evaluation vectors, and boundary constraint receipts:

```text
<mesh_complex boundary_matrices cochain_vector boundary_conditions>
```

- `mesh_complex`: Graded cell counts $(|K_0|, |K_1|, \dots, |K_D|)$ and declared dimension $D \in \mathbb{N}_{\ge 1}$.
- `boundary_matrices`: Array of signed incidence matrices $([\partial_1], \dots, [\partial_D])$ with entries in $\{-1, 0, 1\}$.
- `cochain_vector`: Rational cochain assignment $\omega^k \in \mathbb{Q}^{|K_k|}$ on a declared degree $k$.
- `boundary_conditions`: Set of constrained cell indices on marked subcomplex $\partial K$ and their assigned rational values.

### 3. Runtime Pipeline Evaluator & Verification Obligation

- **Runtime Pipeline:** `Evaluator::targets.stage_072`
- **Primary Error Code:** `ERR_MESH_COMPLEX_DEFECT`
- **Atlas Capabilities:** `mesh_cochains`, `boundary_operator`
- **Locally Checkable Verification Obligation:**
  1. **Dimension & Shape Purity:** Verify that $[\partial_k]$ has dimension $|K_{k-1}| \times |K_k|$ with entries restricted strictly to $\{-1, 0, 1\}$.
  2. **Exact Nilpotence Recomputation:** Compute matrix product $[\partial_{k-1}][\partial_k]$ over $\mathbb{Z}$ for all $2 \le k \le D$, and assert that the product is the zero matrix $0$.
  3. **Cochain Well-Definedness:** Verify that `cochain_vector` has length $|K_k|$ with rational entries.
  4. **Boundary Condition Compliance:** Check that $\omega^k$ matches all declared boundary constraints on $\partial K$.
- **Falsifier Boundary / Negative Counterexample:**
  - An incidence matrix sequence violating nilpotence ($[\partial_{k-1}][\partial_k] \ne 0$) is rejected with `ERR_MESH_COMPLEX_DEFECT`.
  - A cochain referencing nonexistent cells or failing declared boundary conditions on $\partial K$ is rejected with `ERR_MESH_COMPLEX_DEFECT`.
- **Boundary Warning:** Level 72 records computed/gated verification receipts; it does not confer ambient authority or self-grant execution privileges.

### 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-72 within Epoch VI: Hardness, Real Numbers & Continuum Fences.
   - Computed/gated verification receipts enforcing signed cell incidence, exact nilpotence $\partial^2 = 0$, and discrete cochain evaluation on finite meshes.
2. **What this does not support:**
   - Does not establish finite element function spaces, interpolation estimates, or smooth de Rham cohomology isomorphisms.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-72 accepts valid finite mesh cochain complexes satisfying algebraic nilpotence and boundary constraints, rejecting defective incidence matrices with `ERR_MESH_COMPLEX_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=73$ continuum approximation fixtures using the local CI test harness.

---

## Part II: Lift Record from Predecessor (MSS-71 $\to$ MSS-72)

- **Lift Status:** `unlicensed` (lift_license_status: unlicensed, lift_proof_status: absent; design-stage specification row; no conservative embedding or retraction proof $r_{72}(u_{72}(x))=x$ has been licensed from MSS-71).
- **Predecessor Stage:** MSS-71 (`level_71_analytic_limit_fences.md`).
- **Successor Rationale:** When analytic limit fences (MSS-71) lack discrete topological spaces and differential chain/cochain complexes, MSS-72 is declared as the specification row providing finite mesh cochains and nilpotent boundary operators within the external research atlas.
- **Conditional Lift Obligation:** Any future accepted lift into MSS-72 must exhibit $(u_{72}, r_{72})$ satisfying $r_{72}(u_{72}(x)) = x$. No predecessor lift is currently claimed (`lift_status: unlicensed`, `lift_proof_status: absent`).
