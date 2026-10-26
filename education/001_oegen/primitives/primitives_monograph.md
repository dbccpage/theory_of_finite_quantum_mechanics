---
documentation_contract: symbol-game-documentation/v1
title: "Genesis Primitives Monograph: Foundational Structures, Composed Types & Formal Carrier Specifications"
kind: grammar-reference
audience:
  - researchers
  - formal-verification-engineers
  - coding-agents
status: active
maturity: research
claim_status: review_required
authority_effect: "None"
source_paths:
  - dbccpage/19L57G1
  - omega_engine_education/documentation/001_genesis/primitives/code/
  - omega_engine_education/documentation/001_genesis/primitives/lean4/
related:
  - ../genesis.md
  - ../levels/README.md
  - ../normal_forms/README.md
  - ../../7_witnessed_difference_programme_wdp/README.md
last_verified: 2026-09-30
---

# Genesis Primitives Monograph: Foundational Structures, Composed Types & Formal Carrier Specifications

**AuthorityEffect:** None.\
**Provenance:** Selected educational models citing historical and later Genesis sources; full extraction fidelity is refuted by the 2026-10-01 audit.
**Epistemic Goal:** Investigate declared finite relational models and explicitly supplied domain realizations.

---

> **Dated correction, 2026-10-01.** The descriptions and evidential labels below
> are the historical pre-audit specification. Blanket full-fidelity, physical
> emergence and advanced-target verification claims are withdrawn as evidence.
> The [complete export inventory](../adversarial_verification/docs/primitive_inventory.md)
> records fourteen defect families and historical-pin drift. Nine local Lean
> theorems do not verify all these categories; a Python identity record is not
> a HoTT proof, the old equivalence flag omits surjectivity/pointing, and the
> general sheafification/quantum-Regge/curvature-contextuality bridges remain
> unpaid. Use the [checked replacements](../adversarial_verification/README.md)
> and their exact assumptions. Original source files remain unchanged.

## Executive Summary & Nineteen-Category Taxonomy

The historical taxonomy organizes separately admitted structures and supplied interpretations. Its displayed arrows are proposed dependencies, not a proof that physics is forced by the opaque seed:

$$
\boxed{\text{Uninterpreted Seed} \xrightarrow{\text{admission}} \text{Finite Regime} \xrightarrow{\text{requirement}} \text{Obstruction} \xrightarrow{\text{two-rule forcing}} \text{Structure}}
$$

The foundational types are organized into nineteen rigorous, dual-implemented categories spanning executable Python modules located under [`code/`](code/) and Lean 4 formal proof kernels located under [`lean4/`](lean4/):

| Category | Domain | Primary Carriers | Load-Bearing Invariants | Evidential Grade | WDP Level |
|---|---|---|---|---|:---:|
| **1. Seed & Regime** | Admission Core | `Supply`, `AdmitDatum`, `AdmitForm`, `AdmitInst`, `Regime` | Step determinism; discrete cost functionals $\mu_1, \mu_2$; token deduplication. | `NATIVE SEALED` | **WDP-00 / 01** |
| **2. Primitive Difference** | Distinction Germ | $W, A, B_s, B_c, B_l, C, D, E, F$, Minimal carriers $D_2, D_2^{\mathrm{rev}}, S_2$ | Irreducible asymmetric difference witness; $\mathbf{PtdRel}$ category morphisms. | `NATIVE SEALED` | **WDP-00 / 01** |
| **3. Primitive Passage** | Active Obstruction | `PS` (9-store passage state), `PEvent`, `DiffObs`, `Col`, `Cols` | Four-gate active obstruction: $\text{obst}_p = \text{ret} \land \text{prot} \land \text{dec} \land \text{zero}$. | `NATIVE SEALED` | **WDP-02 / 03** |
| **4. Refusal & Boundary** | Epistemic Frontiers | `Sup`, `Adm`, `Form`, `Inst`, 5 Disciplines, 6 Toggles | 64-toggle constitution space; typed refusal without exception panics. | `SEALED SUPPLEMENTARY` | **WDP-13 / 14** |
| **5. Simplicial Complex** | Homological Structure | `Cell`, `Edge`, `Tri`, `Tet`, `Complex` $(C_0..C_3)$, `Chain` | Nilpotency of discrete boundary operator: $\partial^2 \equiv 0$ on all finite chains. | `SEALED SUPPLEMENTARY` | **WDP-03 / 15** |
| **6. Transition & Trace** | Monoid Calculus | DDC 8-letter Alphabet $\mathcal{A}_{\mathrm{DDC}}$, 9 field deltas, 11 guards | `Profile` (7 components), `TRecord`, budget and license accounting. | `NATIVE SEALED` | **WDP-05 / 06** |
| **7. Derivation Engine** | Branch Exploration | Reading L, Reading F, Challenges 0–3, `Tree`, `Node`, `Edge` | Canonical branching quotient exploration; isomorphic deduplication of state trees. | `FINITE COMPUTATION` | **WDP-10 / 19** |
| **8. Constructive Apartness** | Positive Distinction | Relational carrier $n$, Apartness $\#$, Indistinguishability $\sim$ | Positive apartness forces $\sim$ to be an equivalence relation; 3 countermodels. | `NATIVE SEALED` | **WDP-00 / 01** |
| **9. Primitive Contact** | Pre-Topology | `WitnessedDiff` kernel, `ContactKernel`, separation | Contact pre-topology without metrics; diagonal-zero law $\delta(x,x)=0$. | `NATIVE SEALED` | **WDP-00 / 15** |
| **10. Attachment Ladder** | Skeletal Filtration | `Policy`, `lawful_to`, `up_block`, `up_family`, `shell_guard` | Lawful attachment without clamping; ascent over strictly ascending boundary. | `NATIVE SEALED` | **WDP-11 / 15** |
| **11. Renaming Structure** | Permutation Gauge | `Perm`, $S_n$ action, `automorphism_group`, `iso_canon_key` | Gauge transport along symmetric group; canonical orbit representative modulo $S_n$. | `NATIVE SEALED` | **WDP-02 / 04** |
| **12. Observer Inventory** | Probing Contexts & Presheaf | 9 observer slots, `Context`, `ObserverPresheaf`, `LocalSection`, `MeasurementContext` | Observational profile separation; Čech 0-cycle No-Signaling; Čech gluing obstruction $\gamma = \max(0, S_{\mathrm{CHSH}} - 2)$. | `NATIVE SEALED` | **WDP-09 / 11** |
| **13. Presentation Relativity** | Frame Relativity | `PresentationFrame`, `FrameTransformation`, gauge observables | Relational observable invariance under coordinate transforms across local patches. | `NATIVE SEALED` | **WDP-10** |
| **14. Controller Category** | Grammar Control | $2^{10} = 1024$ `KindDesc` family, `interp_k`, `response_live` | Controlled interpreter liveness; isolation of response executors and funding. | `NATIVE SEALED` | **WDP-09 / 14** |
| **15. Trace Algebra** | Causal Concurrency | `TRecord`, `are_independent_events`, `trace_commutes` | Causal partial order of discrete transitions via Mazurkiewicz trace monoids. | `NATIVE SEALED` | **WDP-05 / 16** |
| **16. Stable Content** | Relational Inertia | `prot_sep`, `quiescent_p`, `has_relational_inertia` | Persistence of protected separations across perturbation families (discrete inertia). | `NATIVE SEALED` | **WDP-02 / 06** |
| **17. Weight Profile** | Projective Pre-Measure | `Weights` over integer carriers, `same_profile`, `same_ray` | Exact rational ray equivalence via cross-multiplication: $w(p) v_{\text{tot}} = v(p) w_{\text{tot}}$. | `NATIVE SEALED` | **WDP-07 / 08** |
| **18. Represented Progress** | Down-Map Retractions | `World`, `sat`, `viol`, `quiescent`, `ProposalRecord.down_map` | Strict retraction down-map $r: \text{Ext} \to \text{Base}$ with $r|_{B} = \text{id}_B$. | `NATIVE SEALED` | **WDP-10 / 12** |
| **19. Endogenous Fidelity** | No-Outside Invariant | `RepresentedSupport`, `extract_support`, `SymmetryBreakingWitness` | Effectual-Outside Dichotomy: differences affecting outcomes must be in support. | `NATIVE SEALED` | **WDP-13 / 20 / 21** |

---

## 1. Seed, Admission Events & Regimes (Category 1)

### 1.1 Mathematical Definitions
- **Presentation Token ($T$):** An uninterpreted glyph (e.g. `<>`, `<a>`, `<ab>`). Token identity is visible only to the metatheory; the object language has no internal access to presentation identity unless an admitted judgment supplies an internal distinction.
- **Supply Event ($\mathrm{Supply}(t)$):** External presentation of token $t$. Provably does not mutate admitted regime state:
  $$\operatorname{step}(R, \mathrm{Supply}(t)) = R$$
- **AdmitDatum ($\mathrm{AdmitDatum}(t)$):** Internalizes presentation token $t$ as datum $d \in \mathbb{N}$. Deduplicates on presentation identity ($t \in R.\text{data} \implies R' = R$).
- **AdmitForm ($\mathrm{AdmitForm}(a)$):** Declares a judgment form with arity $a \ge 1$.
- **AdmitInst ($\mathrm{AdmitInst}(f, \vec{x})$):** Asserts an instance of form $f$ on argument tuple $\vec{x}$.
- **AdmitRuleAll ($\mathrm{AdmitRuleAll}(f)$):** Declares the uniform all-tuples rule on form $f$.
- **Impose ($\mathrm{Impose}(i, j)$):** Externally imposed persistent separation requirement $i < j$.

### 1.2 Composed Type: `Regime`
$$R = (\text{data}, \text{forms}, \text{insts}, \text{rules}, \text{reqs})$$
- `data`: $\text{tuple}[str, \dots]$
- `forms`: $\text{tuple}[\text{int}, \dots]$ (each entry $\ge 1$)
- `insts`: $\text{frozenset}[(f, \vec{x})]$
- `rules`: $\text{frozenset}[f]$
- `reqs`: $\text{frozenset}[(i, j)]$ ($i < j$)

### 1.3 Candidate Responses and Cost Measures
A response delta $\Delta$ is a canonically sorted tuple of items:
$$\Delta = (it_1, it_2, \dots, it_k), \quad it \in \{\text{NewDatum}, \text{NewForm}(a), \text{NewInst}(f, \vec{x}), \text{NewRuleAll}(f)\}$$
- **Cost Measure $\mu_1$:** Raw item count $\mu_1(\Delta) = |\Delta|$.
- **Cost Measure $\mu_2$:** Lexicographic pair $\mu_2(\Delta) = (|\Delta|, \sum_{it \in \Delta, it = \text{NewForm}(a)} a)$.

---

## 2. Primitive Difference Germ & Pointed Carrier Universe (Category 2)

### 2.1 The Nine Candidate Readings
All candidates are predicates over the common signature:
$$\text{Setting} = (X, r, a, b, \text{ret}, \text{prot}, \mathrm{Ops})$$

| Candidate | Name | Formal Predicate | Theorem / Status |
|---|---|---|---|
| **W** | Bare witnessed pair | $r(a, b)$ | Initial object in $\mathbf{PtdRel}$ |
| **A** | Pointed irreflexive witness (PD-A) | $r(a, b) \land \operatorname{Irrefl}(r)$ | Weakest candidate forcing distinct endpoints |
| **Bs** | Symmetric axis (PD-B) | $A(S) \land \operatorname{Symm}(r)$ | Retained branch |
| **Bc** | Cotransitive axis (PD-B) | $A(S) \land \operatorname{Cotrans}(r)$ | Fails at carrier 3 minimally |
| **Bl** | Located axis (PD-B) | $A(S) \land \operatorname{Located}(r)$ | Decidable boolean indicator |
| **C** | Witnessed non-identification (PD-C) | $r(a, b) \land \operatorname{prot}(a, b)$ | Fact + demand without irreflexivity |
| **D** | Non-factorization through point (PD-D) | $\neg \exists p : 1 \to X, p(*) = a \land p(*) = b$ | Metatheoretically $a \ne b$ |
| **E** | Irreducibility under operations (PD-E) | $\forall f \in \operatorname{Clos}(\mathrm{Ops}), f(a) \ne f(b)$ | Controller-relative |
| **F** | Protected retained PD (PD-F) | $A(S) \land \operatorname{ret}(a, b) \land \operatorname{prot}(a, b)$ | Necessary for active obstruction |

### 2.2 Concrete Minimal Carrier Primitives
- **$D_2$ (Oriented 2-Element Carrier):** $(\{0, 1\}, \{(0, 1)\}, 0, 1)$. Initial among all pointed witnessed relations:
  $$\forall (X, r, a, b) \text{ with } r(a, b), \exists! f : D_2 \to X \text{ preserving endpoints and edge}$$
- **$D_2^{\mathrm{rev}}$ (Reversed Carrier):** $(\{0, 1\}, \{(1, 0)\}, 0, 1)$.
- **$S_2$ (Symmetric Carrier):** $(\{0, 1\}, \{(0, 1), (1, 0)\}, 0, 1)$.

---

## 3. Primitive Passage Dynamics & Active Obstruction (Category 3)

### 3.1 Composed State: `PS` (`PState`)
$$\text{PState} = (\text{occ}, \text{asserted}, \text{wit}, \text{prot}, \text{obs}, \text{budget}, \text{licensed}, \text{refusals}, \text{halted})$$
where $\text{obs} = \operatorname{None}$ indicates a pre-observational state.

### 3.2 Four Total Gates of Active Obstruction
Active obstruction is the normative conflict wherein a protected, retained difference is unperceived by the declared observation:

$$\boxed{\operatorname{obstP}(s, i, j) \iff \operatorname{retainedP}(s, i, j) \land \operatorname{protectedP}(s, i, j) \land \operatorname{declaredP}(s) \land \operatorname{zeroP}(s.\text{obs}, i, j)}$$

1. **Gate 1 (`retainedP`):** $(i, j) \in s.\text{wit}$
2. **Gate 2 (`protectedP`):** $(i, j) \in s.\text{prot}$
3. **Gate 3 (`declaredP`):** $s.\text{obs} \ne \operatorname{None}$
4. **Gate 4 (`zeroP`):** $\forall c \in s.\text{obs}, (i \in c \iff j \in c)$

**Independence Theorem:** Each gate is strictly independent; dropping any single gate allows spurious unobstructed collapse or false alarms.

---

## 4. Refusal Disciplines, World Models & Constitution Toggles (Category 4)

### 4.1 Re-admission Disciplines
When an already-admitted token is re-presented:
1. `silent`: No state change.
2. `meta`: Re-admission recorded in history log only.
3. `fact`: Internal refusal counter incremented (`refusals += 1`).
4. `reify_untagged`: Appends fresh datum index without tag.
5. `reify_tagged`: Appends fresh datum index with tag in `tags` store.

### 4.2 Constitution Description (`Desc`): 6-Toggle Family
The kernel constitution carries 6 independent boolean toggles ($2^6 = 64$ distinct evaluators):
- `dedup_admit`: deduplicate tokens on admission
- `guard_require`: validate requirement indices
- `guard_accept`: require positive structural progress
- `gate_budget`: decrement budget on structure creation
- `gate_license`: require external license for extensions
- `cert_refusal`: require exhaustion certificate before refusal

---

## 5. Simplicial Complexes, Higher Structures & Regge Calculus (Category 5)

### 5.1 Graded Complex
$$K = (C_0, C_1, C_2, C_3)$$
- Vertices: $C_0 \subseteq \mathbb{N}$ (0-simplices)
- Edges: $C_1 \subseteq \{(u, v) \mid u < v\}$ (1-simplices)
- Triangles: $C_2 \subseteq \{(u, v, w) \mid u < v < w\}$ (2-simplices)
- Tetrahedra: $C_3 \subseteq \{(u, v, w, x) \mid u < v < w < x\}$ (3-simplices)

### 5.2 Boundary Cancellation Theorem
For any simplex $\sigma = [v_0, v_1, \dots, v_k]$:
$$\partial \sigma = \sum_{i=0}^k (-1)^i [v_0, \dots, \hat{v}_i, \dots, v_k] \implies \partial^2 \sigma \equiv 0$$
Strict vertex ascent ($\operatorname{asc}(\sigma)$) is required for facet distinctness.

### 5.3 Higher-Dimensional Regge Calculus Metric Structures (`ReggeComplex`)
A combinatorial complex $K$ is elevated to a Regge calculus manifold by assigning positive metric lengths $\ell(e) > 0$ to every 1-simplex $e \in C_1$:
1. **2D Triangle Angles:** Evaluated via the exact law of cosines:
   $$\cos \theta_t(v) = \frac{b^2 + c^2 - a^2}{2bc}, \quad \theta_t(v) \in (0, \pi)$$
2. **3D Tetrahedron Dihedral Angles:** Evaluated without coordinate embeddings via the 5x5 Cayley-Menger matrix $M$ and its algebraic cofactors:
   $$\cos \theta_\sigma(e) = \frac{\mathrm{Cofactor}(M)_{3,4}}{\sqrt{\mathrm{Cofactor}(M)_{3,3} \cdot \mathrm{Cofactor}(M)_{4,4}}}, \quad \theta_\sigma(e) \in (0, \pi)$$
3. **Discrete Deficit Angles at Hinges:**
   For a hinge $h$ (codimension-2 simplex: vertex in 2D, edge in 3D):
   $$\epsilon(h) = 2\pi - \sum_{\sigma \supset h} \theta_\sigma(h)$$
   - **Flat 2D Hexagon:** 6 equilateral triangles meeting at vertex 0 $\implies \epsilon(0) = 0.0$.
   - **Elliptic 2D Cap:** 5 equilateral triangles $\implies \epsilon(0) = \pi/3 \approx 1.0472$ rad ($+60^\circ$ positive curvature).
   - **Hyperbolic 2D Saddle:** 7 equilateral triangles $\implies \epsilon(0) = -\pi/3 \approx -1.0472$ rad ($-60^\circ$ negative curvature).
   - **Flat 3D Cluster:** 4 tetrahedra with dihedral angle $\pi/2$ around edge $(0, 1) \implies \epsilon(0, 1) = 0.0$.
   - **Curved 3D Star:** 5 regular tetrahedra around edge $(0, 1) \implies \epsilon(0, 1) = 2\pi - 5\arccos(1/3) \approx 0.1284$ rad ($+7.36^\circ$ positive curvature bone).

### 5.4 Discrete Gauss-Bonnet Index Theorem
For any closed 2D triangulated surface $K$, the sum of discrete deficit angles across all vertices is topologically invariant:
$$\sum_{v \in C_0} \epsilon(v) = 2\pi \chi(K)$$
On the boundary 2-sphere of a 3-simplex (tetrahedron): $\chi = 4 - 6 + 4 = 2$, each vertex has deficit $\pi$, and $\sum \epsilon = 4\pi = 2\pi \chi$ with exact zero discrepancy.

### 5.5 Discrete Deficit Angle Curvature Bounds & Čech Gluing Obstructions
In discrete differential geometry and sheaf theory, parallel transporting a local Euclidean frame around the link of hinge $h$ yields an $\mathrm{SO}(d)$ holonomy rotation $\Omega_h = \mathcal{R}(\epsilon(h))$.
1. Local charts admit a single global section if and only if $\epsilon(h) = 0$.
2. The **Čech gluing obstruction** is given identically by the deficit angle magnitude:
   $$\gamma_{\check{\mathrm{C}}\mathrm{ech}}(h) = |\epsilon(h)|$$
3. A discrete deficit angle curvature bound $\max_h |\epsilon(h)| \le \Delta$ strictly enforces an upper bound on the Čech gluing obstruction across the entire simplicial cover.
4. **Sheaf Projection to Category 12:** Projecting any Regge star to an `ObserverPresheaf` yields local sections that strictly satisfy Čech 0-cycle compatibility ($d_0 s = 0$, No-Signaling) across shared faces, with non-trivial contextuality iff the deficit angle is non-zero.

### 5.6 The Advanced Extension: 25 Sheaf, 5 HoTT, and 10 Quantum Regge Targets
Extending beyond the core 19 categories, Genesis and WDP reach 40 advanced foundational targets implemented in [`code/sheaf_theory.py`](code/sheaf_theory.py), [`code/hott_primitives.py`](code/hott_primitives.py), and [`code/quantum_regge.py`](code/quantum_regge.py), verified by [`test_sheaf_hott_quantum_regge.py`](code/tests/test_sheaf_hott_quantum_regge.py) (40/40 passed):

#### I. 25 Sheaf Theory Targets (SH-01 to SH-25)
1. **SH-01 Poset Open Set Category:** Alexandrov topology generated by simplicial face posets.
2. **SH-02 Presheaf Functor:** Contravariant assignment $U \mapsto \mathcal{F}(U)$ with associative restriction morphisms.
3. **SH-03 Stalk at a Simplex:** Canonical direct limit over stars $\mathcal{F}_\sigma \cong \mathcal{F}(U_\sigma)$.
4. **SH-04 Presheaf Morphisms:** Natural transformations commuting with restrictions.
5. **SH-05 Subpresheaves & Kernels:** Section-wise kernels $\ker(\alpha)(U) = \ker(\alpha_U)$.
6. **SH-06 Separated Presheaf (S1):** Local agreement on open covers forces global section identity.
7. **SH-07 Sheaf Condition (S2 Gluing):** Unique global section extending matching local families.
8. **SH-08 Equalizer Diagram:** Exact sequence $0 \to \mathcal{F}(U) \to \prod \mathcal{F}(U_i) \rightrightarrows \prod \mathcal{F}(U_i \cap U_j)$.
9. **SH-09 Grothendieck Plus Functor $\mathcal{F}^+$:** $\mathcal{F}^+(U) = \check{H}^0(U, \mathcal{F})$.
10. **SH-10 Sheafification $\mathcal{F}^\#$:** Left adjoint to inclusion $\mathbf{Sh}(X) \hookrightarrow \mathbf{PSh}(X)$.
11. **SH-11 Constant Sheaf vs Presheaf:** Local constancy on connected components $\underline{A}(U) = A^{\pi_0(U)}$.
12. **SH-12 Skyscraper Sheaf $i_{x*} A$:** Exact Dirac localization at vertex $x$.
13. **SH-13 Direct Image (Pushforward $f_*$):** $(f_* \mathcal{F})(V) = \mathcal{F}(f^{-1}(V))$.
14. **SH-14 Inverse Image (Pullback $f^*$):** Adjoint pair $f^* \dashv f_*$.
15. **SH-15 Structure Sheaf $\mathcal{O}_X$:** Sheaf of rational piecewise affine function rings.
16. **SH-16 Čech Cochain Complex:** Alternating cochains with nilpotent coboundary $\check{\delta}^2 \equiv 0$.
17. **SH-17 Čech Zeroth Cohomology $\check{H}^0$:** Space of globally compatible sections.
18. **SH-18 Čech First Cohomology $\check{H}^1$:** Gluing obstruction space measuring non-trivial cocycles.
19. **SH-19 Torsors & Principal $\mathbb{Z}_2$-Sheaves:** Holonomy around loops classifying flat gauge bundles.
20. **SH-20 Long Exact Sequence:** Connecting homomorphism $\delta^*: \check{H}^0(\mathcal{H}) \to \check{H}^1(\mathcal{F})$.
21. **SH-21 Flasque (Injective) Sheaves:** Surjective restriction maps guaranteeing vanishing higher cohomology.
22. **SH-22 Soft / Fine Sheaves:** Partitions of unity subordinate to finite covers.
23. **SH-23 Grothendieck Pretopology & Sites:** Covering sieves on simplicial face posets.
24. **SH-24 Leray Acyclic Cover Theorem:** Coincidence of Čech and derived functor sheaf cohomology.
25. **SH-25 Local-to-Global Spectral Sequence:** $E_2^{p,q} = \check{H}^p(\mathcal{U}, \mathcal{H}^q(\mathcal{F})) \implies H^{p+q}(X, \mathcal{F})$.

#### II. 5 Easiest HoTT Targets (HoTT-01 to HoTT-05)
1. **HoTT-01 Identity / Path Type:** Type of witnesses $\operatorname{Id}_A(x, y)$ inhabited iff $x \sim y$, with $\operatorname{refl}_x$.
2. **HoTT-02 Path Transport & J-Eliminator:** $\operatorname{transport}^P(p, u)$ with computational rule $\operatorname{transport}^P(\operatorname{refl}, u) \equiv u$.
3. **HoTT-03 Homotopy Groupoid:** Inverse $p^{-1}$, concatenation $p \cdot q$, and groupoid unit/invertibility laws.
4. **HoTT-04 Function Extensionality ($\operatorname{FunExt}$):** Pointwise homotopy $\prod_x (f(x) = g(x)) \implies (f = g)$.
5. **HoTT-05 Finite Univalence Axiom:** $\operatorname{Id}_{\mathcal{U}}(A, B) \simeq (A \simeq B)$ verified constructively on Genesis minimal carriers $D_2 \simeq D_2^{\mathrm{rev}}$.

#### III. 10 Quantum Regge Calculus & QM Targets (RQ-01 to RQ-10)
1. **RQ-01 Classical Regge Action with $\Lambda$:** $S_{\mathrm{Regge}} = \sum A_h \epsilon_h - \Lambda \sum V_\sigma$.
2. **RQ-02 Regge Field Equations & Schläfli Identity:** $\sum A_h d\theta_\sigma(h) = 0 \implies \partial S / \partial \ell_e = 0$.
3. **RQ-03 Metric Polytope & Triangle Inequalities:** Metric domain $\mathcal{M}_K$ where Cayley-Menger determinants remain positive.
4. **RQ-04 Tullio Regge Quantum Path Integral Propagator:** $\mathcal{Z}[K] = \int_{\mathcal{M}_K} \prod d\ell \, \mu(\ell) e^{i S_{\mathrm{Regge}}/\hbar}$.
5. **RQ-05 Discrete Wheeler-DeWitt Hamiltonian Constraint:** Simplicial constraint $\hat{\mathcal{H}}_v \Psi = 0$ at vertices.
6. **RQ-06 Ponzano-Regge Semiclassical Amplitude:** Asymptotic correspondence $\{6j\} \sim \frac{1}{\sqrt{12\pi V}} \cos(S + \pi/4)$.
7. **RQ-07 Quantum Tetrahedron Area & Volume Spectrum:** Spin network duals with discrete area and volume eigenvalues.
8. **RQ-08 Discrete Diffeomorphism Zero Modes:** Reparametrization gauge invariance in flat simplicial triangulations.
9. **RQ-09 Curvature-Bounded Quantum Phase Space:** Curvature cutoff $|\epsilon(h)| \le \Delta$ regularizing quantum singularity fluctuations.
10. **RQ-10 Regge-Čech Sheaf Quantum Contextuality Bridge:** Deficit angle $|\epsilon|$ directly bounding Čech contextuality and Bell-CHSH violation ($S_{\mathrm{CHSH}} \le 2 + |\epsilon|$).

---

## 6. Transition Alphabet & Trace Monoid (Category 6)

### 6.1 DDC 8-Letter Operational Alphabet $\mathcal{A}_{\mathrm{DDC}}$
$$\mathcal{A}_{\mathrm{DDC}} = \{E, R, C, I, \Lambda, D, M, T\}$$
- $E$ (External supply)
- $R$ (Retention / admission)
- $C$ (Collision / contact)
- $I$ (Internalization / instance assertion)
- $\Lambda$ (Structural lift)
- $D$ (Descent / retraction)
- $M$ (Measurement / observation)
- $T$ (Terminal / refusal)

### 6.2 Composed Type: `TRecord`
$$\operatorname{TRecord} = (\text{pre}, \text{ev}, \text{guard}, \text{post}, \text{cls}, \text{spend}, \text{profile})$$
Carries complete 7-component effect profile:
$$\operatorname{Profile} = (\text{field\_delta}, \text{guard}, \text{obst\_effect}, \text{budget\_delta}, \text{continuity}, \text{origin}, \text{accepted})$$

---

## 7. Derivation Engine & Branching Quotient Trees (Category 7)

### 7.1 Surviving Readings
- **Reading L (Strict Retention):** Bare supply creates no internal data; admission requires explicit retention. Genesis target $(0, 1)$.
- **Reading F (Possession Admission):** Initial inscription `<>` is admitted at genesis. Genesis target $(1, 2)$.

### 7.2 Tree, Node & Edge
- `Node`: Represents an isomorphism equivalence class of regimes ($R_1 \cong R_2$).
- `Edge`: Directed transition tagged by challenge, response delta, tie classes, and orbit size.
- **Equivariant Orbit Selection:** Challenge selection proceeds via automorphism orbits of collapsed pairs, ensuring branch well-definedness under isomorphism quotients.

---

## 8. Constructive Apartness & Indistinguishability (Category 8)

### 8.1 Axioms of Positive Constructive Apartness
A relation $\# \subseteq X \times X$ is a constructive positive apartness iff it satisfies:
1. **Irreflexivity:** $\forall x \in X, \neg (x \# x)$
2. **Symmetry:** $\forall x, y \in X, x \# y \implies y \# x$
3. **Cotransitivity:** $\forall x, y, z \in X, x \# y \implies (x \# z \lor z \# y)$

### 8.2 Indistinguishability as Negation
Two points are indistinguishable, written $x \sim y$, iff they are not apart:
$$x \sim y \iff \neg (x \# y)$$

### 8.3 The Equivalence Theorem
$$\boxed{\operatorname{isApart}(n, r) \implies \operatorname{isEquivalence}(n, \neg r)}$$
*Proof Sketch:* Reflexivity follows from irreflexivity of $\#$. Symmetry follows from symmetry of $\#$. Transitivity follows from cotransitivity: suppose $x \sim y$ ($\neg(x \# y)$) and $y \sim z$ ($\neg(y \# z)$). If $x \# z$, cotransitivity with intermediate point $y$ yields $x \# y \lor y \# z$, contradiction.

### 8.4 Minimal Insufficiency Countermodels
The three conditions are strictly minimal:
1. **Bare reflexivity break:** Relation with $(0, 0)$ breaks reflexivity of $\sim$.
2. **Irreflexivity alone:** Directed pair $(0, 1)$ without symmetry breaks symmetry of $\sim$.
3. **Symmetry without cotransitivity:** 3-point cycle $(0, 1), (1, 0)$ without cotransitivity breaks transitivity of $\sim$.

---

## 9. Pre-Topological Contact Spaces & Replacement Kernels (Category 9)

### 9.1 The Replacement Kernel: `WitnessedDiff`
The fundamental difference kernel $(X, R, \delta, \text{zero}, a, b)$ satisfies:
1. **Diagonal-Zero Law:** $\forall x \in X, \operatorname{zero}(\delta(x, x)) = \text{True}$.
2. **Designated Witness Non-Zero:** $\operatorname{zero}(\delta(a, b)) = \text{False}$.
3. **Induced Apartness:** $x \# y \iff \neg \operatorname{zero}(\delta(x, y))$.

### 9.2 Contact Pre-Topology: `ContactKernel`
A pre-topological proximity space is a finite carrier equipped with a contact relation $C(A, B)$ satisfying:
- $C(A, B) \implies A \ne \emptyset \land B \ne \emptyset$
- $A \cap B \ne \emptyset \implies C(A, B)$
- $C(A, B) \iff C(B, A)$
Proximity separation is defined without metrics: $\operatorname{Sep}(A, B) \iff \neg C(A, B)$.

---

## 10. Attachment Ladder & Lawful Skeletal Filtration (Category 10)

### 10.1 Lawful Attachment Policies
A policy $\pi : \mathbb{N} \to \mathbb{N}$ assigns each step $k+1$ a parent $\pi(k+1)$.
$$\operatorname{lawful\_to}(\pi, N) \iff \forall k \le N, \pi(k+1) \le k$$
Lawfulness ensures attachments connect exclusively to already-represented structure without retroactive clamping.

### 10.2 UpFamily One-Edge Grammar
For a passage state $s$ with carrier length $|s.\text{occ}|$, the legal extension family is generated by:
$$\operatorname{up\_family}(s) = \{\operatorname{up\_block}(s, p) \mid p \in [0, |s.\text{occ}| - 1]\}$$
where each block emits four atomic events:
$$\operatorname{up\_block}(s, p) = [\operatorname{admitOcc}(\text{tok}), \operatorname{assertWit}(p, c), \operatorname{admitWit}(p, c), \operatorname{protect}(p, c)]$$

### 10.3 Simplicial Shell Guard
A $(k+1)$-cell is admissible only over an unfilled boundary with strictly ascending vertex ordering:
$$\operatorname{shell\_guard}(k, [v_0, \dots, v_k]) \iff \forall i < k, v_i < v_{i+1}$$

---

## 11. Renaming Structures, Permutations & Gauge Transport (Category 11)

### 11.1 Symmetric Group Action on Relational Carriers
For permutation $p \in S_n$ and relation $r \subseteq n \times n$:
$$p \cdot r = \{(p(i), p(j)) \mid (i, j) \in r\}$$

### 11.2 Relational Isomorphism and Symmetries
- **Isomorphism:** $r_1 \cong r_2 \iff \exists p \in S_n, p \cdot r_1 = r_2$.
- **Automorphism Group:** $\operatorname{Aut}(r) = \{p \in S_n \mid p \cdot r = r\}$.
- **Canonical Orbit Representative (`iso_canon_key`):**
  $$\operatorname{iso\_canon\_key}(n, r) = \min_{p \in S_n} \operatorname{sort}(p \cdot r)$$
  Provides a strict gauge-invariant representation for relational states.

---

## 12. Observer Inventory, Contexts & Observation Profiles (Category 12)

### 12.1 The Nine-Slot Observer Decomposition
An observer is a 9-slot functional decomposition:
$$\operatorname{Observer} = (\text{carrier}, \text{local\_state}, \text{support}, \text{defect}, \text{reversal}, \text{closure}, \text{residual}, \text{maps}, \text{terminal})$$

### 12.2 Probing Contexts with Slot Holes
A probing context $c = (f, (s_0, s_1, \dots, s_{k-1}))$ for form $f$ of arity $k$ contains at least one hole ($\text{None}$). Plugging datum $d$ yields an instance:
$$\operatorname{plug}(c, d) = (f, (d \text{ if } s_i = \text{None else } s_i)_{i=0}^{k-1})$$

### 12.3 Observation Profiles and Behavioral Quotient
The profile of datum $d$ in regime $R$ is the set of all derivable contexts:
$$\operatorname{Prof}_R(d) = \{c \in \operatorname{Contexts}(R) \mid \operatorname{derivable}(R, \operatorname{plug}(c, d))\}$$
- **Separation:** $i$ and $j$ are separable iff $\operatorname{Prof}_R(i) \ne \operatorname{Prof}_R(j)$.
- **Collapsed Pairs:** $\operatorname{Collapsed}(R) = \{(i, j) \mid i < j \land \operatorname{Prof}_R(i) = \operatorname{Prof}_R(j)\}$.
Profile equality induces the exact observational quotient on relational carriers.

### 12.4 Presheaf Contextuality & Čech Gluing Obstruction (Abramsky-Brandenburger)
Following the sheaf-theoretic formulation of quantum contextuality (Abramsky & Brandenburger 2011), empirical observations across probing contexts form a presheaf of local sections:
- **Measurement Cover:** $\mathcal{M} = \{(A_1, B_1), (A_1, B_2), (A_2, B_1), (A_2, B_2)\}$ represents maximal compatible subsets of observables.
- **Local Section:** $s_C \in \mathcal{E}(C)$ is an empirical distribution over outcomes in $\{-1, +1\}^2$ with restriction morphism $\rho^C_U: \mathcal{E}(C) \to \mathcal{E}(U)$ given by marginalization.
- **Čech 0-Cycle Condition (No-Signaling):** Pairwise agreement on overlaps:
  $$\rho^C_{C \cap C'}(s_C) = \rho^{C'}_{C \cap C'}(s_{C'}) \iff d_0 s = 0$$
- **Čech Gluing Obstruction:** By Fine's Theorem (1982), local sections glue into a global joint distribution iff $|S_{\mathrm{CHSH}}| \le 2.0$. The Čech gluing obstruction is:
  $$\gamma = \max(0.0, |S_{\mathrm{CHSH}}| - 2.0)$$
  vanishing on classical LHV models ($\gamma = 0$) and strictly witnessing non-trivial cohomology on quantum/contextual models ($\gamma = 0.8 = 4/5$ for rational Pythagorean Bell; $\gamma = 2.0$ for PR boxes).

---

## 13. Presentation Relativity & Gauge Frame Transformations (Category 13)

### 13.1 Local Presentation Frames
A presentation frame is a localized basis:
$$\mathcal{F} = (\text{frame\_id}, n, r_{\text{local}})$$

### 13.2 Frame Transformations and Observables
A transition $\mathcal{T} : \mathcal{F}_1 \to \mathcal{F}_2$ maps node indices $\phi : n_1 \to n_2$. An observable $\mathcal{O} : \mathcal{R} \to V$ is **gauge-invariant** iff:
$$\mathcal{O}(r) = \mathcal{O}(\phi \cdot r) \quad \forall \mathcal{T}$$

---

## 14. Controller Category & Variable Event Grammars (Category 14)

### 14.1 The 1024-Member Grammar Family
Given 10 fundamental controllable passage event kinds:
$$\text{Kinds} = (\text{admitOcc}, \text{admitWit}, \text{protect}, \text{declareObs}, \text{refineCol}, \text{addCol}, \text{refuse}, \text{setBudget}, \text{setLicense}, \text{halt})$$
A controller descriptor $d \in \{0, 1\}^{10}$ determines step execution:
$$\operatorname{interp}_k(d, s, e) = \begin{cases} \operatorname{pstep}(s, e) & \text{if } d[\operatorname{kind}(e)] = 1 \\ s & \text{otherwise} \end{cases}$$

### 14.2 Syntactic Response-Liveness
$$\operatorname{response\_live}(d) \iff d[\text{refineCol}] \land d[\text{addCol}] \land d[\text{setBudget}]$$
Enforces that a live controller must possess both response operators and funding mechanisms.

---

## 15. Trace Algebra, Mazurkiewicz Monoids & Causal Concurrency (Category 15)

### 15.1 Relational Concurrency without External Clocks
Two events $e_1, e_2$ are causally independent ($e_1 \mathrel{I} e_2$) if they mutate disjoint state stores (e.g. `assertWit` and `setBudget`).

### 15.2 Mazurkiewicz Commutation Law
$$\boxed{e_1 \mathrel{I} e_2 \implies \operatorname{pstep}(\operatorname{pstep}(s, e_1), e_2) = \operatorname{pstep}(\operatorname{pstep}(s, e_2), e_1)}$$
The causal partial order of discrete physics is generated as the quotient monoid $\mathcal{A}^* / \equiv_I$ without invoking continuous time coordinates.

---

## 16. Stable Content, Relational Inertia & Quiescence (Category 16)

### 16.1 Protected Separation and Quiescence
- **Protected Separation:** $\operatorname{prot\_sep}(s, i, j) \iff (i, j) \in s.\text{prot} \land \operatorname{sep}(s.\text{obs}, i, j)$.
- **Quiescence:** $\operatorname{quiescent}(s, n) \iff \forall i, j < n, \neg \operatorname{obstP}(s, i, j)$.

### 16.2 Relational Inertia
A relational feature $(i, j)$ possesses **relational inertia** across perturbation set $\mathcal{P}$ iff:
$$\operatorname{prot\_sep}(s, i, j) \land \forall s' \in \mathcal{P}, \operatorname{prot\_sep}(s', i, j)$$
Relational inertia defines the discrete analogue of physical persistence and invariant mass.

---

## 17. Weight Profiles, Ray Equivalence & Pre-Measure (Category 17)

### 17.1 Integer Additive Valuations
Weights are integer mappings $w : X \to \mathbb{N}$ with total mass $w_{\text{tot}} = \sum_{x \in X} w(x)$.

### 17.2 Projective Ray Equivalence without Floats
Two profiles $w, v$ belong to the same projective ray ($w \sim_{\text{ray}} v$) iff they satisfy the cross-multiplication identity over $\mathbb{Z}$:
$$\boxed{\forall p \in X, \quad w(p) \cdot v_{\text{tot}} = v(p) \cdot w_{\text{tot}}}$$
Completely eliminates floating-point rounding errors and division from finite pre-measure theory.

---

## 18. Represented Progress, Retractions & Proposal Records (Category 18)

### 18.1 Represented World State
$$W = (\text{data}, \text{views}, \text{reqs}, \text{refusals}, \text{budget}, \text{aug\_licensed})$$
- $\operatorname{sat}(W, (i, j)) \iff \exists c \in W.\text{views}, (i \in c \ne j \in c)$.
- $\operatorname{viol}(W, (i, j)) \iff (i, j) \in W.\text{reqs} \land \neg \operatorname{sat}(W, (i, j))$.
- $\operatorname{quiescent}(W) \iff \forall r \in W.\text{reqs}, \operatorname{sat}(W, r)$.

### 18.2 Retraction Down-Maps
Every extension proposal $\operatorname{Prop} = (\text{name}, \text{target}, \rho, \text{cost})$ carries an explicit retraction map $\rho : X_{\text{ext}} \to X_{\text{base}}$ satisfying the identity on the base carrier:
$$\boxed{\forall x \in X_{\text{base}}, \quad \rho(x) = x}$$

---

## 19. Endogenous Fidelity, No-Outside Invariants & Gauge Breaking (Category 19)

### 19.1 The No-Outside Contract
Internal operations have no access to external annotations. The operational support is:
$$\operatorname{Support}(W) = (W.\text{data}, W.\text{views}, W.\text{reqs}, W.\text{refusals}, W.\text{budget}, W.\text{aug\_licensed})$$

### 19.2 The Effectual-Outside Dichotomy (Rule 1 & Rule 3)
$$\boxed{\operatorname{Support}(W_1) = \operatorname{Support}(W_2) \implies \mathcal{E}_{\text{op}}(W_1) = \mathcal{E}_{\text{op}}(W_2)}$$
*Contrapositive:* Any difference that alters an internal operational verdict MUST already reside inside the represented support. External, unrepresented variables have zero authority.

### 19.3 Symmetry Breaking Witness
$$\operatorname{BreakingWitness} = (\text{symmetry\_name}, (a, b), \text{distinguishing\_relation})$$
Provides an explicit certificate when an automorphism symmetry is broken by an admitted distinction.

---

## 20. Comprehensive Mapping to Witnessed Difference Programme (WDP Levels 0–21)

| Genesis Category | Primary Conceptual Construct | Primary WDP Level | WDP Chapter Focus |
|---|---|:---:|---|
| **Cat. 1: Seed & Regime** | Admission Core & Deltas | **Level 0 / Level 1** | The Admitted Cut $(X, E, \tau, \mathcal{K})$; Residuals before witnesses |
| **Cat. 2: Primitive Difference** | Pointed Difference Germs ($W..F$) | **Level 0 / Level 1** | Seven non-coercing witness roles; Minimal carriers $D_2, S_2$ |
| **Cat. 3: Primitive Passage** | 4-Gate Active Obstruction | **Level 2 / Level 3** | Symmetry, nonselection, price of retention; Finite cochains $(\Phi_1, \Gamma_2)$ |
| **Cat. 4: Refusal & Boundary** | 64-Toggle Constitution Space | **Level 13 / Level 14** | Awareness boundary & firewall; Authority as a separate layer |
| **Cat. 5: Simplicial Complex** | Cell Calculus & $\partial^2 \equiv 0$ | **Level 3 / Level 15** | Finite cochains & certificates; Spatial/history diagnostics |
| **Cat. 6: Transition & Trace** | DDC Alphabet $\mathcal{A}_{\mathrm{DDC}}$ & Profiles | **Level 5 / Level 6** | Recurrence, succession, constitutive order; Duration, exactness, clocks |
| **Cat. 7: Derivation Engine** | Reading L/F & Branching Trees | **Level 10 / Level 19** | Intersubjective presentation & descent; Relative completeness |
| **Cat. 8: Constructive Apartness** | Positive Apartness & Indistinguishability | **Level 0 / Level 1** | Constructive cut; Equivalence theorem without classical LEM |
| **Cat. 9: Primitive Contact** | `WitnessedDiff` & Contact Pre-Topology | **Level 0 / Level 15** | Relational pre-topology without background metric space |
| **Cat. 10: Attachment Ladder** | Lawful Skeletal Filtration | **Level 11 / Level 15** | Observation ladder; Unfilled boundary ascent |
| **Cat. 11: Renaming Structure** | $S_n$ Action, $\operatorname{Aut}(r)$, Gauge Key | **Level 2 / Level 4** | Automorphism quotient; Gauge symmetries without coordinates |
| **Cat. 12: Observer Inventory** | 9-Slot Observer & Probing Contexts | **Level 9 / Level 11** | Layered observer architecture; Observation profile ladder |
| **Cat. 13: Presentation Relativity** | Frame Transformations & Naturality | **Level 10** | Intersubjective presentation, descent, and redundancy |
| **Cat. 14: Controller Category** | 1024-Member Event Grammars | **Level 9 / Level 14** | Observer policy layer; Separation of funding and execution |
| **Cat. 15: Trace Algebra** | Mazurkiewicz Monoids & Commutation | **Level 5 / Level 16** | Causal order without external clocks; Weighted history paths |
| **Cat. 16: Stable Content** | Relational Inertia & Persistence | **Level 2 / Level 6** | Price of retention; Periodic stability and invariant mass |
| **Cat. 17: Weight Profile** | Projective Ray Equivalence over $\mathbb{Z}$ | **Level 7 / Level 8** | Multiplicity, additive weight; Probability scope fences |
| **Cat. 18: Represented Progress** | Down-Map Retractions & World | **Level 10 / Level 12** | Local vs global satisfiability; Measurement calibration & provenance |
| **Cat. 19: Endogenous Fidelity** | No-Outside Invariant & Breaking | **Level 13 / Level 20 / Level 21** | Awareness firewall; Falsifiers and nonclaims; Synthesis |

---

## 21. Claim Hygiene & Formal Fences

In strict compliance with repository claim hygiene standards:

1. **What this specification supports:**
   - 19 fully executable Python modules located under [`code/`](code/) and 19 formal Lean 4 modules located under [`lean4/`](lean4/) matching the sealed derivation `19L57G1`.
   - 28 passed unit tests executing all 19 primitive families without failures or warnings (`code/tests/test_genesis_primitives.py`).
   - 40 passed targeted tests executing all 25 Sheaf Theory, 5 HoTT, and 10 Quantum Regge targets without failures or warnings (`code/tests/test_sheaf_hott_quantum_regge.py`).
   - Exact constructive rational and integer cross-multiplication eliminating all floating-point roundoff.
   - Constructive proofs that positive apartness forces indistinguishability to be an equivalence relation, that boundary operators satisfy $\partial^2 \equiv 0$, and that independent events commute.
   - Discrete Gauss-Bonnet index invariance ($\sum_v \epsilon(v) = 2\pi\chi(K)$) and bounded Čech gluing obstructions on 2D and 3D Regge simplicial complexes.
   - Homotopy groupoid laws, Function Extensionality, and Voevodsky's Finite Univalence Axiom on Genesis minimal relational carriers ($D_2 \simeq D_2^{\mathrm{rev}}$).
   - Tullio Regge simplicial action, Schläfli identity cancellation, discrete Wheeler-DeWitt constraints, Ponzano-Regge $6j$ asymptotics, and the Regge-Čech quantum contextuality bridge.

2. **What it does not support:**
   - Does not prove physical continuum spacetime, string theory, or smooth Riemannian Einsteinian manifolds.
   - Does not assert physical ontology beyond verified finite relational structures.
   - Does not assert unstratified infinity-topos univalence over arbitrary infinite universes.
   - Does not claim that real-world quantum mechanics or gravity is fully settled by finite toy models.

3. **Narrowest defensible claim:**
   The 19 categories and their 40 advanced extensions provide an exact, sound, constructive mathematical substrate for relational distinction, pre-topological proximity, discrete causal order, permutation gauge invariance, simplicial Regge curvature, finite sheaf cohomology, minimal carrier univalence, and discrete path integral amplitudes, operating with zero background manifolds and zero external clocks.

4. **Next test needed:**
   Integration of the 40 targets into Lean 4 proof kernels under `omega_engine_education/documentation/001_genesis/primitives/lean4/` and cross-linking to WDP Level 0–21.

---

## 22. Related Authoritative Documentation

- [`meta_theory_deep_research_report.md`](meta_theory_deep_research_report.md): *Genesis / 19L57G1 as a Meta-Foundational Substrate for Formal World Models* (canonical 1,800-line research report on the sealed derivation and extended research estate).
- [`../demos/README.md`](../demos/README.md): Genesis evolutionary ascent demo suite ($\langle\rangle \to \langle a \rangle \dots \to \text{auth}$) and Category 12 Čech presheaf contextuality suite.
- [`../../006_oewdp/README.md`](../../006_oewdp/README.md): The Witnessed Difference Programme normative curriculum and measurement foundations.
