# [TFQ-0171] Do not collapse unnormalized finite valuations into the normalized rational probability simplex

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `ad624434-8292-540c-b408-bc43541823ec`  
> **Parent Derivation**: [TFQ-0167](tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md)

---

## 1. Abstract & Formal Statement

Unnormalized mass is a different carrier from the probability simplex. src/finite_valuation.rs states exact nonnegative Boolean valuations with no normalization requirement, and it admits an empty carrier that FinN refuses. src/lib.rs also declares signed_representation.rs, local_deterministic.rs, and marginal_compatibility.rs; those three bodies were not opened, so only the module declarations are in scope. The obligation is to keep an unnormalized valuation from standing in for a law that sums to one. H001ProbabilitySimplex.lean says its scaled integer grid is not the ordinary rational simplex.

### Governing Obligation
Do not collapse unnormalized finite valuations into the normalized rational probability simplex.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Unnormalized Boolean Valuation vs Normalized Probability Simplex (`finite_valuation.rs` vs `simplex.rs`)**: `BooleanValuation::try_new(size, entries)` verifies that `entries` form a finite Boolean subalgebra with $v(\emptyset) = 0$, $v(A) \ge 0$, and disjoint additivity $v(A \cup B) = v(A) + v(B)$, imposing no unit-sum constraint and admitting `size = 0`, whereas `ProbabilitySimplex::try_new` and `FinN::try_new` reject `size = 0` and require total mass $1$.
- **Scaled Integer Grid vs Rational Simplex (`lean4/H001ProbabilitySimplex.lean`, `lean4/H001Rats.lean`)**: `ScaledProb Q E M` represents integer weights summing to $M > 0$; `doubleW = (1, 1)` has non-negative weights with mass $2 \ne 1$ (`double_not_normalized`), `signedW = (2, -1)` has mass $1$ (`signed_mass_one`) but fails non-negativity (`signed_not_nonneg`), and rational laws such as $(1/3, 2/3)$ require scale divisibility $3 \mid M$.
- **Sibling Module Contracts**: `SignedValuation` (`signed_representation.rs`), `binary_local_vertices` (`local_deterministic.rs`), and `MarginalScenario` (`marginal_compatibility.rs`) enforce distinct carrier and normalization invariants replayed in `checks/independent/tfq-0171.py` and formalized in `lean4/CampaignTfq0171ImplementationSibling.lean`.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `lean4/CampaignTfq0171ImplementationSibling.lean`:
  - `CampaignTfq0171ImplementationSibling.boolean_valuation_empty_carrier_and_unnormalized_mass`
  - `CampaignTfq0171ImplementationSibling.boolean_valuation_disjoint_additivity_and_atom_reconstruction`
  - `CampaignTfq0171ImplementationSibling.scaled_integer_simplex_grid_vs_rational_simplex_separation`
  - `CampaignTfq0171ImplementationSibling.signed_valuation_negativity_and_expectation_bound`
  - `CampaignTfq0171ImplementationSibling.marginal_compatibility_and_local_deterministic_normalization`
  - `CampaignTfq0171ImplementationSibling.unnormalized_valuation_cannot_stand_in_for_probability_simplex_fence`
  - `CampaignTfq0171ImplementationSibling.empty_carrier_valuation_rejected_by_fin_n_and_simplex_fence`
  - `CampaignTfq0171ImplementationSibling.scaled_integer_grid_not_ordinary_rational_simplex_fence`
  - `CampaignTfq0171ImplementationSibling.sibling_modules_distinct_carrier_contracts_fence`
  - `CampaignTfq0171ImplementationSibling.tfq0171_unnormalized_valuation_and_simplex_scope_ledger_fence`
- `lean4/H001ProbabilitySimplex.lean`:
  - `FableHilbertWalk20260819.H001.probability_simplex`
  - `FableHilbertWalk20260819.H001.double_not_normalized`
  - `FableHilbertWalk20260819.H001.signed_not_nonneg`
- `lean4/H001Rats.lean`:
  - `FableHilbertWalk20260819.H001Rats.qrel_equivalence`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `code/rust/src/finite_probability/finite_valuation.rs`:
  - `BooleanValuation::try_new`
- `code/rust/src/finite_probability/signed_representation.rs`:
  - `SignedValuation::from_weights`
- `code/rust/src/finite_probability/local_deterministic.rs`:
  - `binary_local_vertices`
- `code/rust/src/finite_probability/marginal_compatibility.rs`:
  - `MarginalScenario::validate_probabilities`

### Independent Python Verification
- `checks/independent/tfq-0171.py`:
  - `run_all_checks`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000`
- **Primary Source Paths**:
  - `lean4/H001ProbabilitySimplex.lean`
  - `lean4/H001Rats.lean`
  - `lean4/CampaignTfq0171ImplementationSibling.lean`
  - `code/rust/src/finite_probability/finite_valuation.rs`
  - `checks/independent/tfq-0171.py`
