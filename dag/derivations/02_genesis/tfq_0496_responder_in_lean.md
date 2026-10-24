# [TFQ-0496] responder-in-lean

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `bb19a38b-1b3e-5ad3-af65-21e0237ad470`  
> **Parent Derivation**: [TFQ-0486](tfq_0486_genesis_freeze_endpoint_ledger.md)

---

## 1. Abstract & Formal Statement

Narrowed boundary, status left OPEN: in one declared shadow, a demand is read only for the collapsed kind with the uniform-rule flag false. Of the four flag pairs, the read count is 1. The copied mark, a form of arity 1 followed by argument list [0], and the copied link, a form of arity 2 followed by [0, 1], each have length 2. Item-count cost mu1 is 2 for both, so the two lists tie at cost 2. The pair cost mu2 is (2, 1) for the mark and (2, 2) for the link, and (2, 1) precedes (2, 2) because the item counts are equal and 1 < 2. Both lists lie inside the shadow bound of length at most 2 and new-form arity sum at most 2 with no rule item. A two-item list that contains a rule item lies outside that bound. One three-item list has length 3 and lies outside the length bound 2. This shadow does not state the sealed responder, and the node status stays OPEN.

### Governing Obligation
Keep this shadow separate from the sealed responder. Stating that responder's minimum, cost and tie over the sealed candidate space, its domain on ruled regimes, and both demand kinds stays open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0490](tfq_0490_k_item_delta_grammar.md) k-item-delta-grammar

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The shadow reads one declared flag table and compares two copied lists. It does not state a minimum, a cost, or a tie of the sealed responder in the second derivation's packages (S-3). It does not refuse a regime that holds a uniform rule (S-1), and it does not read or refuse a same pair that is separable (S-2). The length bound 2 is not identified with the grammar (S-4). Attempt one's G-4 and attempt two's H-1 stay open. Status stays OPEN.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwResponderInLean.lean::pgwBound_inside`](../../../lean4/CampaignPgwResponderInLean.lean)
- [`lean4/CampaignPgwResponderInLean.lean::pgwMark_link_shape`](../../../lean4/CampaignPgwResponderInLean.lean)
- [`lean4/CampaignPgwResponderInLean.lean::pgwMu1_tie`](../../../lean4/CampaignPgwResponderInLean.lean)
- [`lean4/CampaignPgwResponderInLean.lean::pgwMu2_mark_before_link`](../../../lean4/CampaignPgwResponderInLean.lean)
- [`lean4/CampaignPgwResponderInLean.lean::pgwMu2_pairs`](../../../lean4/CampaignPgwResponderInLean.lean)
- [`lean4/CampaignPgwResponderInLean.lean::pgwRead_count`](../../../lean4/CampaignPgwResponderInLean.lean)
- [`lean4/CampaignPgwResponderInLean.lean::pgwRead_table`](../../../lean4/CampaignPgwResponderInLean.lean)
- [`lean4/CampaignPgwResponderInLean.lean::pgwRuled_outside`](../../../lean4/CampaignPgwResponderInLean.lean)
- [`lean4/CampaignPgwResponderInLean.lean::pgwThree_outside`](../../../lean4/CampaignPgwResponderInLean.lean)
- `missing obligation: sealed responder minimum, cost and tie in the second derivation's packages (S-3)`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs::min_responses`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs)

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-responder-in-lean.py`](../../../checks/independent/pgw-responder-in-lean.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::min_responses`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:1081-1084`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:217-223`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:1054-1059`
