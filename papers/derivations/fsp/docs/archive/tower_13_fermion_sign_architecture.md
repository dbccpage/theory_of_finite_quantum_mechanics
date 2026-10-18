# The Problem of the Fermion Sign: Derivation Walk, Hamiltonian, Lean 4, Python & Normal Forms

**Directory:** `coda_all_universe/1_the_tower/13_the_problem_of_the_fermion_sign/`  
**Status:** MIGRATED / RETIRED IN PLACE  
**Canonical Implementation Home:** `coda_atlas/F004_papers/002_projection_obstruction/023_fermion_sign_and_computational_hardness`  
**AuthorityEffect:** None  
**Primary Formal Reference:** `sealed-derivation-v1` (`3100c4e`)  

> **MIGRATION NOTICE (2026-09-19):**  
> Pursuant to the FSP Review and Implementation Roadmap, this Tower directory has been consolidated into its single canonical home under `coda_atlas/F004_papers/002_projection_obstruction/023_fermion_sign_and_computational_hardness/`. All active development, proof mechanizations, and test suites are maintained exclusively in the Atlas repository.

---

## 1. Scope & Architecture

This directory provides the complete discrete architecture for the **Fermion Sign Problem**, tracing its algebraic emergence from the primitive difference germ `<>` through the pointed directed cut `<arb>` ($D_2$) and symmetric link `<ara>` / $S_2$, formalizing its mathematical obstruction in Lean 4, simulating path sign decay under discrete Hamiltonians, and classifying cochain defects via Boundary-Quotient Normal Form (BQNF):

``` text
13_the_problem_of_the_fermion_sign/
├── code/
│   ├── __init__.py
│   ├── fermion_boson_germ.py        # Genesis walk <> to <arb>, D2 vs S2, swap involution, invariant blindness
│   ├── fermionic_hamiltonian.py     # Fermi-Hubbard lattice Hamiltonian, Trotter path signs, Wheeler-DeWitt constraint
│   ├── bqnf_sign_evaluator.py       # Cochain complex, Banach quotient Q^1 = C^1 / im(d0), Meron involution witness
│   ├── fermion_gin_index.py         # Generalized Inverted Index (GIN) cochain engine & posting list queries
│   ├── hamiltonian_gin_bridge.py    # Bridges Hamiltonian Trotter paths to relational GIN posting lists & involution audits
│   ├── cdt_fermion_sign_evaluator.py    # Grassmann path integral Berezin scaling & bipartite reflection involution
│   ├── cdt_kd_doubling_evaluator.py     # Kähler-Dirac fermion doubling resolution & 16->4 spinor projection
│   ├── cdt_overlap_evaluator.py         # Ginsparg-Wilson / Neuberger overlap Dirac operator & Lüscher symmetry
│   ├── cdt_zolotarev_evaluator.py       # Rational Zolotarev minimax overlap operator & multi-shift CG
│   ├── cdt_topological_charge_evaluator.py # Atiyah-Singer lattice index Q = n_+ - n_- & instanton susceptibility
│   └── tests/
│       ├── test_fermion_sign_engine.py  # Comprehensive unit tests (pytest)
│       ├── test_fermion_gin_index.py    # GIN index & Majorana zero mode audits
│       ├── test_hamiltonian_gin_bridge.py # Hamiltonian path indexing & exact sign cancellation audits
│       ├── test_kitaev_honeycomb_bisimulation.py # Kitaev honeycomb model & GIN index bisimulation
│       └── test_chiral_superconductor_bisimulation.py # 3D chiral superconductor & Fermi arc audits
├── lean4/
│   ├── FermionSignCore.lean         # Lean 4 formalization of D2, S2, swap involution, invariant blindness, setoid quotient
│   ├── MajoranaGinCore.lean         # Lean 4 formalization of GIN involution cancellation & Kitaev MZM boundary decoupling
│   └── regge_wdw_core.lean          # Lean 4 formalization of Regge simplicial geometry & WDW constraints
├── normal_forms/
│   ├── normal_form_contract_schema.yaml
│   ├── nf.change.bqnf.fermion_sign.yaml # Specialized BQNF contract for fermion sign problem
│   ├── nf.change.bqnf.yaml
│   ├── nf.physics.wdwnf.yaml        # Wheeler-DeWitt Normal Form
│   ├── nf.physics.cdt_fermion_sign.yaml    # CDT Grassmann path integral Berezin scaling contract
│   ├── nf.physics.cdt_kd_doubling.yaml     # CDT Kähler-Dirac fermion doubling contract
│   ├── nf.physics.cdt_overlap_fermions.yaml # CDT Ginsparg-Wilson overlap Dirac operator contract
│   ├── nf.physics.cdt_zolotarev_overlap.yaml # CDT Zolotarev rational minimax overlap contract
│   ├── nf.physics.cdt_topological_charge.yaml # CDT Atiyah-Singer lattice index & instanton contract
│   ├── nf.derivation.pdnf.yaml      # Primitive Difference Normal Form
│   ├── nf.bridge.wir_relvar.yaml    # WIR-Relvar Bridge
│   ├── nf.classical.*.yaml          # Classical relational normal forms (0NF - 6NF, BCNF, DKNF, EKNF, ETNF, NF2)
│   ├── nf.derivation.*.yaml         # Derivation normal forms (AONF, OBNF, RPNF, SCNF)
│   ├── nf.experimental.gauge.yaml
│   ├── fermion_sign_nf_evaluator.py # Structural contract linter and BQNF evaluator
│   ├── test_fermion_sign_normal_forms.py # Pytest suite for normal form contracts (all 28 contracts)
│   ├── test_fsp_cdt_fermion_sign.py      # Pytest suite for CDT fermion sign Berezin scaling
│   ├── test_fsp_cdt_kd_doubling.py       # Pytest suite for CDT Kähler-Dirac doubling
│   ├── test_fsp_cdt_overlap_fermions.py  # Pytest suite for CDT Ginsparg-Wilson overlap fermions
│   ├── test_fsp_cdt_zolotarev_overlap.py # Pytest suite for CDT Zolotarev overlap solver
│   └── test_fsp_cdt_topological_charge.py # Pytest suite for CDT topological charge & Atiyah-Singer index
├── databases/
│   ├── fermion_gin_index_schema.sql # Inverted posting lists, involution pairs, and MZM audit views
│   ├── fermion_sign_problem.sql     # SQLite CTEs and PostgreSQL partitioned DDL
│   ├── regge_wdw_schema.sql         # 4D simplicial Regge triangulation & WDW constraint relational schema
│   └── schema.sql                   # Relational witness and stage schema
├── docs/
│   ├── 0_fermion_info.md            # Directed relation, swap, sign, and witness bookkeeping
│   ├── 1_boson_info.md              # Reflexive and symmetric finite relations
│   └── 2_u1_su3_gauge_and_sign_problem.md # Finite permutation and simplicial gauge data
└── fermion_sign_problem.md          # Relational CTEs, window quotients & Troyer-Wiese discussion
```

---

## 2. Derivation Walk: From Void to the Sign Problem

1. **Stage 0 (`<>`) — The Void ($\emptyset$)**: Pure inertia; external supply changes nothing (`supply_no_op`).
2. **Stage 1 (`<a>`) — Lone Mark**: Single point locus; no boundary or distinction possible.
3. **Stage 2 (`<ab>`) — Unmarked Pair**: Observational collapse $[a] = [b]$ without an admitted relation.
4. **Stage 3 (`<arb>`) — Directed Cut ($D_2$) [Fermion Germ]**:
   - Directed irreflexive cut $a \to b \land \neg(b \to a)$ with non-zero boundary $\partial_1(a \to b) = b - a \neq 0$.
   - Rigid automorphism group $\mathrm{Aut}(D_2) = \{\mathrm{id}\}$.
   - Antisymmetric under swap $a \leftrightarrow b$.
5. **Stage 4 (`<ara>`) — Diagonal Excision**: Self-loop $a \to a$ has zero boundary $\partial_1 = 0$; refused under strict irreflexivity.
6. **Stage 5 (`<ara>` / $S_2$) — Symmetric Link [Boson Germ]**:
   - Symmetrized pair $S_2$ and closed 1-cycle $Z_1$.
   - Admits swap involution $\mathrm{Aut}(S_2) = \mathbb{Z}_2$, orientation-blind.
7. **Fermion Sign Problem Emergence**:
   - Proved in `lean4/FermionSignCore.lean` (`swap_invariant_blind`): swap-invariant observation packages cannot distinguish $D_2$ from $D_2^{\mathrm{rev}}$.
   - Under quotienting over permutation groups $S_n$ or gauge equivalence classes, signed parity $(-1)^{\pi(\gamma)}$ induces cancellation between positive and negative path amplitudes.
   - The gross sum ($Z_{\mathrm{bosonic}} = \sum |w|$) exponentially dwarfs the net sum ($Z_{\mathrm{fermionic}} = \sum w (-1)^\pi$), driving $\langle \mathrm{Sign} \rangle = e^{-\beta N \Delta f} \to 0$.

---

## 3. The Hamiltonian: Wheeler-DeWitt and Discrete Fermi-Hubbard

1. **Wheeler-DeWitt Constraint $\mathcal{H}_\perp$**:
   - Implemented in `code/fermionic_hamiltonian.py` and `normal_forms/nf.physics.wdwnf.yaml`.
   - Discrete scalar curvature violation: $\mathcal{H}_\perp(v) = \frac{1}{\sqrt{q_v}} \sum G_{ee'} \pi_e \pi_{e'} - \sqrt{q_v} R(v)$.
   - Direct-sum cochain embedding $C^1 \oplus C^0$ prevents scalar violations from being laundered into pure gauge.
2. **Discrete Fermionic Lattice Hamiltonian**:
   - Implemented in `code/fermionic_hamiltonian.py`.
   - Tight-binding hopping and on-site Hubbard $U$ on finite graphs.
   - Generates configuration paths with permutation phases and demonstrates exponential sign decay on frustrated geometries (triangle clusters).

---

## 4. Boundary-Quotient Normal Form (BQNF) Solver

Implemented in `code/bqnf_sign_evaluator.py`:

- Cochain complex $C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$.
- Banach quotient $Q^1 = C^1 / \mathrm{im}(d_0)$ with quotient norm $\Phi_1(q) = \inf_{\alpha} \|c - d_0 \alpha\|_1$.
- Search and certification of fixed-point-free, sign-reversing, weight-preserving involution witnesses $\Xi$ (meron clusters).
- Deterministic five-way routing:
  - `ExactRepair`: $\Phi_1 = 0$, pure gauge.
  - `ExactCancellation`: $\Xi$ certified, exact pairing of opposite sign paths.
  - `StabilizedSurvivor`: $d_1 c_1 = 0$ with persistent non-zero quotient defect mass.
  - `OpenSignObstruction`: Uncancelled defect with non-zero closure and no involution.
  - `Refused`: Dimension or nilpotency breach.

---

## 5. Verification Commands

Run unit tests and normal form validation:

```pwsh
# 1. Full tower 13 test suite (91 tests across code and normal forms)
python -m pytest coda_all_universe/1_the_tower/13_the_problem_of_the_fermion_sign/ -v

# 2. Code unit tests (germ, Hamiltonian, BQNF, GIN index, Kitaev honeycomb, 3D chiral superconductor)
python -m pytest coda_all_universe/1_the_tower/13_the_problem_of_the_fermion_sign/code/tests/ -v

# 3. Normal forms pytest suite (all 29 contracts + 6 CDT FSP suites including SUSY Witten)
python -m pytest coda_all_universe/1_the_tower/13_the_problem_of_the_fermion_sign/normal_forms/ -v

# 4. Lean 4 formalization checks
lean coda_all_universe/1_the_tower/13_the_problem_of_the_fermion_sign/lean4/FermionSignCore.lean
lean coda_all_universe/1_the_tower/13_the_problem_of_the_fermion_sign/lean4/MajoranaGinCore.lean
lean coda_all_universe/1_the_tower/13_the_problem_of_the_fermion_sign/lean4/regge_wdw_core.lean
```

---

## 6. Claim Hygiene Ledger

1. **What this supports:**  
   Discrete algebraic and relational models tracing the fermion/boson split from genesis stages, formal Lean 4 proofs of invariant blindness, exact computation of many-body Trotter paths with permutation phases, BQNF cochain quotient routing, Ginsparg-Wilson/Zolotarev overlap Dirac operators, Atiyah-Singer topological charge quantization, and exact cancellation of fermion determinant sign fluctuations via the Nicolai map and topological Witten index on supersymmetric CDT complexes.
2. **What this does not support:**  
   Continuous QFT path integrals, solving generic NP-hard sign problems in polynomial time on arbitrary non-supersymmetric or non-bipartite lattices, or ungrounded claims of a physical Theory of Everything.
3. **The narrowest defensible claim:**  
   Under exact unbroken supersymmetry, positive-energy states form exact boson-fermion doublets that cancel pairwise in the Witten index $\Delta_{\text{Witten}} = \operatorname{Tr}((-1)^F e^{-\beta H_{\text{SUSY}}}) = n_B^0 - n_F^0 \in \mathbb{Z}$, and the Nicolai map Jacobian identically equals the Berezin fermion determinant $\det(D_F) = |\det(\frac{\delta\mathcal{N}}{\delta\phi})| > 0$, eliminating sign fluctuations ($\langle\operatorname{Sign}\rangle = 1.0$) while preserving the super-Wheeler-DeWitt constraint ($\Phi_{\text{super}} \le 10^{-8}$); spontaneous or geometric supersymmetry breaking induces zero-mode lifting, sign resurgence ($\langle\operatorname{Sign}\rangle < 1.0$), and super-WDW constraint breach ($\Phi_{\text{super}} > 10^{-8}$).
4. **The next test needed:**  
   Formulate the 4D supersymmetric CDT graviton-gravitino supermultiplet coupling on curved simplicial geometries to evaluate whether local $N=1$ supergravity transformation invariance $\delta e^a_\mu = \frac{1}{2} \bar{\epsilon} \gamma^a \psi_\mu$ eliminates gauge-fixing ghost determinant sign fluctuations on dynamical causal triangulations.
