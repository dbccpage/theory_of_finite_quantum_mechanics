# [TFQ-0490] k-item-delta-grammar

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `c06b7aeb-a75f-538e-ad42-b19e32eb4eee`  
> **Parent Derivation**: [TFQ-0488](tfq_0488_declared_challenge_import_per_level.md)

---

## 1. Abstract & Formal Statement

The sealed candidate space is enumerated to cost two (at most two items, arity at most two), with pruning lemmas certified against the unpruned space: unreferenced fresh data and forms never matter, an instance-only delta changes the target pair's profiles only if an instance mentions a target datum, and a delta holding a uniform-rule item is never a minimum valid response (rule_item_never_minimal). The second derivation's rung one enumerated three-item deltas (min_responses_three) under a node guard, but no k-item delta grammar with pruning lemmas proved beyond cost two exists, and the distance bound of two is not known to be the grammar's (S-4). The education audit lists k-item delta grammars with pruning lemmas as a missing prerequisite of the S(n) bridge. Narrowed in Lean 4 to one empty base with two data and arity one. Over a 10-atom universe, the well-formed admissions of one item are a fresh datum and one unary form, and the well-formed admissions of two items are datum-then-datum, datum-then-form, form-then-datum, form-then-form, form-then-rule, form-then-instance of argument 0, and form-then-instance of argument 1. That census has 9 well-formed deltas, and 7 of them leave the two target profile bits equal. The two form-then-instance deltas leave those bits unequal. The form-then-rule delta sets both bits true. Extending the argument-0 instance by the uniform rule makes a 3-item delta whose bits are equal, while the 2-item prefix has unequal bits. A fresh datum, then a form, then an instance of argument 2, keeps both target bits false and records that fresh argument. Arity two, a grammar for 3 or more items, and the sealed cost-two minimum on the full unpruned space stay open. The mention file and the rule-bridge file are not rechecked. AuthorityEffect is None.

### Governing Obligation
Define the k-item delta grammar for k ≥ 3, state and prove the pruning lemmas it relies on, and certify the pruned enumeration against the unpruned space at each declared k before using any k-item minimum. This file checks one empty base with two data and arity one: 9 well-formed deltas of at most two items, 2 of them with unequal target bits. The 3-item rule extension equalizes those bits, and an instance of argument 2 keeps them false. Arity two, a grammar for 3 or more items, and the sealed cost-two minimum stay open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Open: the cost-two minimum (CL-3-MIN-TWO) is relative to the sealed grammar and bounds, and nothing here establishes a k-item minimum or a bound on response size. This file checks one empty base with two data and arity one: 9 well-formed deltas of at most two items, 2 of them with unequal target bits. The 3-item rule extension equalizes those bits, and an instance of argument 2 keeps them false. Arity two, a grammar for 3 or more items, and the sealed cost-two minimum stay open.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::form_rule_both_true`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::fresh_datum_pairs_do_not_separate`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::nine_well_formed`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::no_single_item_separates`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::off_target_instance_keeps_bits`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::one_hundred_pairs`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::rule_extension_equalizes`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::rule_extension_is_longer`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::separating_pairs_are_two`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::seven_leave_bits_equal`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::ten_atoms`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::well_formed_pairs_are`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/CampaignPgwKItemDeltaGrammar.lean::well_formed_singles_are`](../../../lean4/CampaignPgwKItemDeltaGrammar.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/Mention.lean::collapsed_fresh_datum`](../../../lean4/Imported/Genesis19l57g1/Derivation/Mention.lean)
- [`lean4/Imported/Genesis19l57g1/Derivation/RuleBridge.lean::rule_item_never_minimal`](../../../lean4/Imported/Genesis19l57g1/Derivation/RuleBridge.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/enumeration.rs::iter_cost2_deltas`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/enumeration.rs)

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-k-item-delta-grammar.py`](../../../checks/independent/pgw-k-item-delta-grammar.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_stream/stream.py::iter_k_item_deltas`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stream/stream.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::iter_cost2_deltas`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:1081-1084`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:414-433`
  - `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md:1101`
