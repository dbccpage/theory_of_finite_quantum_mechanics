# Finite to Continuum Bridging Framework

Track 2 native verification, continuous Haar character proofs, and schema
contracts are described in [_docs/track2.md](_docs/track2.md). Its replayable
claim dossier separates finite evidence from open continuum obligations.

**AuthorityEffect:** None.  
**Domain:** CODA Layer 4 (CS: Continuum Shadow) to Layer 5 (Q: The Continuum).  
**Arithmetic Standard:** Exact Rational Arithmetic (`fractions.Fraction`) with zero floating-point leakage.

---

## 1. Overview

Binding scope. The checked core is the finite cyclic inclusions, the separating character sum, and the mechanized integer-character Haar limit named in `_docs/track2.md` and `claim_ledger.json`. Five obligations in that ledger stay `open`: Fourier-polynomial density, metric completion as a mechanized theorem, semantic fourth through sixth normal forms, general invertible rational chain maps, and any specific interacting quantum field theory. Wilsonian extrapolation below is `UNCERTIFIED_EXTRACTION_PROXY`. The dyadic direct limit is countable. Its metric completion is the circle. Those are different objects. The pillars below are programme descriptions. A pillar is a proved row only when `claim_ledger.json` marks that row `finite_checked` or `mechanized_and_axiom_audited`.

This package describes a bridge across these modular pillars:

1. **CODA-Q Interval Calculus (Step 1):** Implements certified rational interval arithmetic for real-valued physical observables. Instead of returning IEEE-754 floats with round-off drift, every observable is enclosed in a verified rational interval $[lo, hi] \in \mathbb{Q} \times \mathbb{Q}$ with width $< \varepsilon$.
2. **CS-Q Discretization Defect Operators (Step 2 - 1D & 2D):** Equips discrete lattice, quadrature, and cubature solvers with explicit discretization error operators:
   $$\text{Result}(\mathbf{a}) = \text{ContinuousValue} + \mathcal{E}(\mathbf{a}), \quad \text{where } |\mathcal{E}(\mathbf{a})| \le \sum_i C_i a_i^{p_i}$$
   yielding certified continuum enclosures and contractive multi-mesh refinement verification in both 1D and 2D.
3. **Wilsonian Finite-Size Extrapolation (Step 3):** Implements an exact rational Neville-Aitken extrapolation adapter taking discrete results from $L \in \{4, 6, 8, 12, \dots\}$ finite chains, fitting the finite-size scaling form:
   $$g(L) = f_\infty + \frac{c_1}{L^2} + \frac{c_2}{L^4} + \dots$$
   and computing an exact rational polynomial extrapolation proxy and pairwise spread indicator for the infinite-volume limit $f_\infty$ (flagged `UNCERTIFIED_EXTRACTION_PROXY` unless an external monotone remainder certificate is supplied).
4. **Pontryagin Duality Bridge (1D & 2D):** Connects finite cyclic translation character groups $\widehat{\mathbb{Z}_L} \cong \mathbb{Z}_L$ and 2D discrete tori $\widehat{\mathbb{Z}_{L_x} \times \mathbb{Z}_{L_y}} \cong \mathbb{Z}_{L_x} \times \mathbb{Z}_{L_y}$ to the circle group $S^1$, the 2-torus $T^2$ (2D Brillouin zone), and continuous translation $\mathbb{R}^d$, governed by honest staged programmes and strict anti-hype kill fences.
5. **Meron-Cluster Fermion Chain Bridge:** Bridges the exact finite transfer traces of the half-filled Meron cluster fermion chain ($L=4, 6, 8$) to exact finite-size free energy densities inside certified rational log intervals, together with an exact rational three-size Neville extrapolation proxy (`UNCERTIFIED_EXTRACTION_PROXY`).
6. **Symbol Game CODA-Meron 4D Continuum Ladder:** Extends the symbolic framework from 1D/2D up to 4D spacetime through 5 prioritized candidate targets ($T_1 \dots T_5$). Integrates Regge calculus (simplicity constraints $\Sigma \wedge \Sigma = 0$, contracted Bianchi identities, and certified rational deficit angle enclosures $[lo, hi] \in \mathbb{Q} \times \mathbb{Q}$) and non-Abelian topological cluster mechanisms ($T^2, T^3$ loop linking, and 4D half-instantons with second Chern class $c_2 \in \frac{1}{2}\mathbb{Z}$) into pure $\Gamma_{38}$ wire strings and exact rational receipts.

---

## 2. Directory Layout

```
omega_engine_projects/finite_to_continuum/
├── code/
│   ├── __init__.py
│   ├── interval_calculus.py        # Step 1: RationalInterval, ln, exp, and pi enclosures
│   ├── discretization_defect.py    # Step 2: 1D Discretization error operator E(a) <= C a^p
│   ├── coda_2d_discretization_defect.py # Step 2: 2D Discretization error operator and 2D cubature
│   ├── wilsonian_extrapolator.py   # Step 3: Exact Neville finite-size scaling extrapolator
│   ├── pontryagin_duality.py       # 1D Pontryagin programme and character orthogonality
│   ├── coda_2d_pontryagin.py       # 2D Pontryagin programme, T^2 dual, and 2D characters
│   ├── meron_wilsonian_bridge.py   # Meron fermion chain thermodynamic limit bridge
│   └── symbol_game_coda_meron_ladder.py # Top 5 candidate targets walking CODA & Meron to 4D
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_interval_calculus.py   # 9 unit tests for interval arithmetic & bounds
│   ├── test_discretization_defect.py # 5 unit tests for 1D defect bounds & refinement
│   ├── test_coda_2d_discretization_defect.py # 3 unit tests for 2D defect bounds & cubature
│   ├── test_wilsonian_extrapolator.py # 4 unit tests for L=4, 6, 8, 12 scaling recovery
│   ├── test_pontryagin_duality.py  # 8 unit tests for 1D 7-stage receipt & orthogonality
│   ├── test_coda_2d_pontryagin.py  # 3 unit tests for 2D 6-stage receipt & 2D orthogonality
│   ├── test_meron_wilsonian_bridge.py # 3 unit tests for Meron fermion chain extrapolation
│   └── test_symbol_game_coda_meron_ladder.py # 11 unit tests for 4D ladder & Gamma38 wire
├── demos/
│   ├── code/
│   │   ├── __init__.py
│   │   └── demo_finite_to_continuum_pipeline.py # End-to-end executable 5-section demo
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_demo_pipeline.py   # Automated regression test for demo pipeline
│   └── results/
│       └── demo_pipeline_receipt.json # Stamped execution receipt
└── results/
    ├── continuum_recovery_receipt.json # Master certified execution receipt
    └── coda_meron_4d_ladder_receipt.json # Certified top-5 4D ladder receipt
```

---

## 3. Scope & Claim Discipline

### What This Artifact Supports
- Exact rational interval enclosure $[lo, hi] \in \mathbb{Q} \times \mathbb{Q}$ of real observables, transcendentals ($\sqrt{2}, \pi, e$), and natural logs $\ln(x)$ with super-exponential range reduction.
- Multi-mesh contractive defect verification for 1D quadrature and 2D cubature with proven asymptotic convergence order $p=2$.
- Exact polynomial elimination of finite-size scaling corrections $1/L^2, 1/L^4$ from chains $L \in \{4, 6, 8, 12\}$.
- Exact rational interval enclosure of the finite-size half-filled Meron cluster fermion chain free energy densities ($Z(4)=912, Z(6)=33012, Z(8)=973824$) to width $< 10^{-19}$, together with a three-size Neville polynomial extrapolation proxy (`f_inf_proxy` $\approx 1.69411$) and pairwise spread indicator (`UNCERTIFIED_EXTRACTION_PROXY`).
- Fail-closed refusal of overclaims regarding $\pi, \pi^2, U(1), T^2$, and continuous couplings via kill condition fences (`PI_FROM_EXACT_Q`, `U1_FROM_L1_MASS`, `ZN_SOLD_AS_U1`, `ALPHA_AS_EXACT`, `PI_FROM_EXACT_Q_2D`, `T2_FROM_L1_ALONE`, `Z2_SOLD_AS_T2`, `ALPHA_2D_AS_EXACT`).

### What This Artifact Does Not Support
- It does **not** claim to solve arbitrary unconstrained non-linear partial differential equations.
- It does **not** derive $\pi$ or $\pi^2$ from discrete cochain algebra alone without the Pontryagin dual Haar normalization.
- It does **not** claim thermodynamic limit convergence for systems undergoing first-order phase transitions without gapped/conformal scaling forms.

### Narrowest Defensible Claim
> For declared 1D and 2D discrete models, exact rational interval arithmetic encloses fixed-size finite-volume observables and discretization defect bounds without floating-point drift, while three-size Neville elimination computes an exact rational polynomial extrapolation proxy and pairwise spread indicator (`UNCERTIFIED_EXTRACTION_PROXY`), which is not a certified thermodynamic-limit bound without an independent monotone remainder certificate.

### Next Test Needed
> Extend the 2D lattice defect operator to the 2D Hubbard model at half-filling on $L \times L$ tori ($L \in \{4, 6\}$), verifying sign cancellation across 2D winding sectors in $\mathbb{Z} \times \mathbb{Z}$.

---

## 4. Execution & Verification

### Run Demo Pipeline:
```bash
py -3.12 omega_engine_projects/finite_to_continuum/demos/code/demo_finite_to_continuum_pipeline.py
```

### Run Unit Tests:
```bash
py -3.12 -m unittest omega_engine_projects/finite_to_continuum/tests/test_interval_calculus.py
py -3.12 -m unittest omega_engine_projects/finite_to_continuum/tests/test_discretization_defect.py
py -3.12 -m unittest omega_engine_projects/finite_to_continuum/tests/test_coda_2d_discretization_defect.py
py -3.12 -m unittest omega_engine_projects/finite_to_continuum/tests/test_wilsonian_extrapolator.py
py -3.12 -m unittest omega_engine_projects/finite_to_continuum/tests/test_pontryagin_duality.py
py -3.12 -m unittest omega_engine_projects/finite_to_continuum/tests/test_coda_2d_pontryagin.py
py -3.12 -m unittest omega_engine_projects/finite_to_continuum/tests/test_meron_wilsonian_bridge.py
py -3.12 -m unittest omega_engine_projects/finite_to_continuum/tests/test_symbol_game_coda_meron_ladder.py
py -3.12 -m unittest omega_engine_projects/finite_to_continuum/demos/tests/test_demo_pipeline.py
```

### Run 4D Symbol Game Ladder:
```bash
py -3.12 omega_engine_projects/finite_to_continuum/code/symbol_game_coda_meron_ladder.py
```

## Source-bound fixed-temperature and volume refinement

`code/meron_time_refinement.py` calls the existing full-Fock occupation-basis
transfer function at rational q=1+r/M. Its parameter interval, scalar
correction and explicit time/volume radius refer to one declared U=t chain
target. The [WDP derivation](../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/meron_time_and_volume_refinement.md)
proves the common target by matrix logarithms and bounded-bond near-additivity.
It does not treat the old Neville interval as a proved thermodynamic bound.

Replay `tests/time_refinement/test_meron_time_refinement.py` with the scoped
pytest recipe and a writable external basetemp. Resource refusals are explicit;
the mathematical all-level theorem and finite execution tests are separate.
This is not a spatial-mesh field theory or a general sign-problem solver.

## Actual observable and spin-sector transport

The [model/query derivation](../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/meron_spin_and_observable_transport.md)
binds the raw time-integrated SQL observable to actual insertion derivatives.
The Python companion uses an independent exact block-matrix transfer; thirteen
checks include four unchanged SQL fixture comparisons and explicit input/
normalization refusals. The native generic derivative product belongs to
linear algebra, the parity-dependent spin model and query to quantum physics,
and WDP retains its selected plan. The written fixed-volume Kubo limit does
not provide the growing-volume or spatial scaling theorem.

## Static spatial Gaussian source profile

The [spatial derivation](../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/meron_spatial_gaussian_source.md)
retains one continuous circle test profile across grids and the original
signed half-time Meron query. It derives locality and explicit quadratic and
higher-source errors in the declared theta<=1/192 region. Exact periodic
piecewise-linear profiles, derived norms/integrals and original weighted SQL
comparisons are in `code/circle_piecewise_linear.py`,
`code/meron_spatial_source.py` and `tests/spatial_source/`.
The constructed target is a static Gaussian random distribution; its
geometry and scaling are inputs. Finite signed source functions are not
assumed to be probability characteristic functions or a quantum field.
