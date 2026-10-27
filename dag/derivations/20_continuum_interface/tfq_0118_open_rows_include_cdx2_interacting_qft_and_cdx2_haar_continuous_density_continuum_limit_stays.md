# [TFQ-0118] Open rows include cdx2.interacting_qft and cdx2.haar_continuous_density. Continuum limit stays

> **Stage**: `CONTINUUM_INTERFACE` | **Status**: `OPEN_OBLIGATIONS`  
> **UUID**: `218733cd-63ff-5d1e-874e-ad74e72079c6`  
> **Parent Derivation**: [TFQ-0111](../19_finite_qg/tfq_0111_the_interface_stays_open_gap_f000_f002_001_and_gap_f002_s001_001_are_not_discharged.md)

---

## 1. Abstract & Formal Statement

Package 007 separates finite evidence from open continuum obligations. Its README says a pillar counts as a checked row only when the claim ledger marks it finite_checked or mechanized and axiom-audited. Five obligations stay open: polynomial density, metric completion, semantic normal forms, general chain maps, and a specific interacting theory. What is finite is cyclic inclusion and separating character sums inside a declared budget. What is not discharged is that interacting theory and the continuum limit, which remains GAP. A fixed-size enclosure is not smooth spacetime.

Narrowed in Lean 4 (`lean4/CyclicInclusionCharacterSums.lean`) and an independent Python verifier (`checks/independent/tfq-0118.py`) to three exact finite/algebraic components and scope fences:
1. **Injective Dyadic Cyclic Inclusion (`dyadicInclude : Fin N → Fin (2 * N)`)**: proves strict injectivity (`dyadicInclude_injective`), modular-addition homomorphism (`dyadicInclude_add_mod_hom`), and non-surjectivity onto `Fin (2 * N)` (`dyadicInclude_misses_odd_residue`).
2. **Point-Separating Character Sums Inside a Declared Finite Budget ($\mathbb{Z}/4\mathbb{Z}$)**: proves that the dual character sum over `Fin 4` equals $(4,0)$ on the diagonal and $(0,0)$ off the diagonal (`z4_character_point_projector_exact`), separating all distinct points $x \neq y$ (`z4_characters_separate_distinct_points`).
3. **Open Continuum Obligations Fences (`cdx2.haar_continuous_density` & `cdx2.interacting_qft`)**: proves that the quadratic Riemann-sum discretization defect $\frac{1}{3} - S_N(t^2) = \frac{3N-1}{6N^2}$ is strictly positive for every finite budget $N \ge 1$ (`discretization_defect_closed_form`, `discretization_defect_strictly_positive_for_all_finite_N`, `discretization_defect_dyadic_budget_table`), and that the quartic interacting EOM superposition defect $3gab(a+b)$ vanishes at $a=b=1$ if and only if $g=0$ (`quartic_superposition_defect_identity`, `quartic_superposition_at_unit_iff_free`).

### Governing Obligation
Open rows include cdx2.interacting_qft and cdx2.haar_continuous_density. Continuum limit stays GAP.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CyclicInclusionCharacterSums.lean`](../../../lean4/CyclicInclusionCharacterSums.lean):
  - `CyclicInclusionCharacterSums.dyadicInclude_injective`
  - `CyclicInclusionCharacterSums.dyadicInclude_add_mod_hom`
  - `CyclicInclusionCharacterSums.dyadicInclude_misses_odd_residue`
  - `CyclicInclusionCharacterSums.z4_character_point_projector_exact`
  - `CyclicInclusionCharacterSums.z4_characters_separate_distinct_points`
  - `CyclicInclusionCharacterSums.discretization_defect_closed_form`
  - `CyclicInclusionCharacterSums.discretization_defect_strictly_positive_for_all_finite_N`
  - `CyclicInclusionCharacterSums.discretization_defect_dyadic_budget_table`
  - `CyclicInclusionCharacterSums.quartic_superposition_defect_identity`
  - `CyclicInclusionCharacterSums.quartic_superposition_at_unit_iff_free`

### Sovereign Rust Certifiers
*Computational witness tracked under `theory_of_finite_qm` crate.*

### Python Oracles & Numerical Evaluators
- [`checks/independent/tfq-0118.py`](../../../checks/independent/tfq-0118.py)
- [`dag/derivations/independent/tfq-0118.md`](../independent/tfq-0118.md)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F002.S000`, `F002.S001`
- **Primary Source Paths**:
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
  - `external:git-tree:197a57e06c54cd85be796698967601ae741995cb`
