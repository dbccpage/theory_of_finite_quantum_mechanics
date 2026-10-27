# [TFQ-0199] Do not treat the GR holonomy scaffold or the 2D Regge sum

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `OPEN`  
> **UUID**: `79aef985-3be4-5e3d-b130-01dd91dd3230`  
> **Parent Derivation**: [TFQ-0197](tfq_0197_feed_finite_gravity_only_the_rational_regge_proxy_not_the_arccosine_deficit.md)

---

## 1. Abstract & Formal Statement

Other gravity files are scaffolds or a different 2D calculus and must not be folded into the rational 4D proxy. `src/holonomy.rs` is a best-effort scaffold (`code/rust/src/majorana/holonomy.rs` and `code/rust/src/general_relativity/holonomy.rs`). `src/regge_calculus.rs` is finite 2D Regge (`code/rust/src/general_relativity/regge_calculus.rs`), with action a sum of vertex deficits, and it says it is not continuum GR and not 3+1 dihedral Regge. `src/discrete_spacetime.rs` (`code/rust/src/general_relativity/discrete_spacetime.rs`) is the combinatorial carrier via `omega_homology::simplicial`. The obligation is to withhold those labels and the 2D deficit sum from the `exact_regge` proxy (`code/rust/src/general_relativity/exact_regge/action.rs`). `FiniteQFTAndGravity.lean` keeps $\pi$ and square roots out of its identities.

### Governing Obligation
Do not treat the GR holonomy scaffold or the 2D Regge sum as the exact rational 4D gravity shadow.

---

## 2. Derivation Context & Mathematical Grounding

1. **4D Exact Rational Regge Proxy (`code/rust/src/general_relativity/exact_regge/action.rs`)**:
   - On a 4D simplicial manifold (`SimplicialManifold4D`), `rational_regge_proxy` evaluates the exact rational Cayley-Menger squared area $A_h^2 \in \mathbb{Q}_{\ge 0}$ on each of the $\binom{5}{3} = 10$ triangular hinges $h$ of each pentatope (`area_squared_in_pentatope`) and sums
     $$S_{\text{proxy}} = \sum_{h} A_h^2 \, \kappa_h \in \mathbb{Q}, \qquad K_{\text{tot}} = \sum_{h} \kappa_h \in \mathbb{Q},$$
     where $\kappa_h \in \mathbb{Q}$ is the declared rational hinge defect.
   - On the orthogonal right pentatope (`orthogonal_pentatope`), the $6$ right-triangle hinges at vertex $0$ have $A_h^2 = 1/4$ and the $4$ equilateral base hinges have $A_h^2 = 3/4$ (total squared hinge area $6(1/4) + 4(3/4) = 9/2$).
   - Flat admission (`flat_chart_admitted`) requires exact rational equality $S_{\text{proxy}} = 0$ (`flat_einstein_hilbert()`), rejecting a sub-cutoff defect $\kappa_{h_0} = 1 / 10^9$ ($S_{\text{proxy}} = 1 / 4000000000 \ne 0$) even though $|S_{\text{proxy}}| < 10^{-6}$.
2. **Non-Conflation Fence Against 2D Regge and Carrier/Holonomy Scaffolds**:
   - `code/rust/src/general_relativity/regge_calculus.rs` (`ReggeCalculus::regge_action_2d`) and `code/rust/src/general_relativity/einstein_hilbert_action.rs` (`EinsteinHilbertAction::try_from_regge`) evaluate `f64` arccosine vertex deficits $\delta_v = 2\pi - \sum_{t \ni v} \theta_{t,v}$ on 2D triangulations (`AUTHORITY_FENCE`: `"not the exact proxy (the sum of area_squared times kappa)"`).
   - `code/rust/src/general_relativity/discrete_spacetime.rs` (`DiscreteSpacetime::euler_characteristic`) is a pure combinatorial carrier (`SimplicialComplex`) with $\chi(\Delta^2) = \chi(\Delta^4) = 1$ and no metric data.
   - `code/rust/src/majorana/holonomy.rs` (`holonomy_receipt_gf2`) evaluates $\mathbb{F}_2$ face residuals $d_1 A \pmod 2$ on 2-complexes, where a 4-edge plaquette with $A=(1,1,1,1)$ is flat ($1+1+1+1 \equiv 0 \pmod 2$), unlike a non-trivial unit rational quaternion holonomy $q_1 = (3/5, 4/5, 0, 0)$ whose fourth power is $q_1^4 = (-527/625, -336/625, 0, 0) \ne 1$.
   - `lean4/FiniteQFTAndGravity.lean` keeps $\pi$ and square roots out of its exact rational identities (`gr_deflection_twice_newton`, `mercury_per_orbit_arcsec`).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/GravityProxyVsReggeSum.lean`](../../../lean4/GravityProxyVsReggeSum.lean) (`GravityProxyVsReggeSum.tfq0199_gr_holonomy_regge_not_4d_gravity_shadow_scope_certificate`)
- [`lean4/FiniteQFTAndGravity.lean`](../../../lean4/FiniteQFTAndGravity.lean) (`FiniteQFTAndGravity.gr_deflection_twice_newton`)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/general_relativity/exact_regge/action.rs`](../../../code/rust/src/general_relativity/exact_regge/action.rs) (`rational_regge_proxy`, `flat_chart_admitted`, `defect_bound_holds`, `tests::einstein_hilbert_fence_decision_equals_proxy_action`)
- [`code/rust/src/general_relativity/discrete_spacetime.rs`](../../../code/rust/src/general_relativity/discrete_spacetime.rs) (`DiscreteSpacetime::euler_characteristic`, `tests::triangle_has_three_edges`)
- [`code/rust/src/general_relativity/regge_calculus.rs`](../../../code/rust/src/general_relativity/regge_calculus.rs) (`ReggeCalculus::regge_action_2d`, `tests::six_equilateral_flat_at_center`)
- [`code/rust/src/general_relativity/einstein_hilbert_action.rs`](../../../code/rust/src/general_relativity/einstein_hilbert_action.rs) (`EinsteinHilbertAction::try_from_regge`, `tests::action_matches_sum_of_deficits`)
- [`code/rust/src/majorana/holonomy.rs`](../../../code/rust/src/majorana/holonomy.rs) (`holonomy_receipt_gf2`, `tests::plaquette_full_cycle_flat_in_f2`)

### Python Oracles & Numerical Evaluators
- [`checks/independent/tfq-0199.py`](../../../checks/independent/tfq-0199.py) (`run_all_checks`)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
