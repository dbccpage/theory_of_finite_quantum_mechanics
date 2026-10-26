# [TFQ-0502] stream-at-four-items

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `4970530a-d2d8-54e0-b42a-b5d0b73dce71`  
> **Parent Derivation**: [TFQ-0486](tfq_0486_genesis_freeze_endpoint_ledger.md)

---

## 1. Abstract & Formal Statement

Challenge 1, the stream as a response, is OPEN with scoped finite results only: no retained V1 minimum of 1680 carries a datum, 32 of them were selected at three items, all fourteen recorded refusal situations are answered at exactly three items, and two new first refusals appear. 1039 nodes stopped at the guard, targets after a node's first refusal were not searched (the first-refusal short-circuit), and four items were not computed (R1-X PENDING); V2 beyond nineteen situations and the narrow-versus-wide comparison are also OPEN. Attempt two's runs add only that no response carries a datum at two items, and the continuation was not authorized to take Challenge 1 up.

### Governing Obligation
Compute the stream challenge at four items with targets searched after a first refusal and the guard-stopped frontier reported, or prove a bound that makes the four-item case unnecessary. The retained minima, the refusal census, the guard-stopped frontier, and the four-item stream computation stay open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Open; the three-item answers hold at the computed scope only, and a refusal at three items is not a refusal at four. Narrowed in Lean 4 to one reply at item count 3, two replies at item count 4, and one short-circuit flag. The retained minima, the refusal census, the guard-stopped frontier, and the four-item stream computation stay open.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwStreamAtFourItems.lean::pgwStreamAtThree`](../../../lean4/CampaignPgwStreamAtFourItems.lean)
- [`lean4/CampaignPgwStreamAtFourItems.lean::pgwStreamFourAccepts`](../../../lean4/CampaignPgwStreamAtFourItems.lean)
- [`lean4/CampaignPgwStreamAtFourItems.lean::pgwStreamFourRefuses`](../../../lean4/CampaignPgwStreamAtFourItems.lean)
- [`lean4/CampaignPgwStreamAtFourItems.lean::pgwStreamOpenSearchReachesFour`](../../../lean4/CampaignPgwStreamAtFourItems.lean)
- [`lean4/CampaignPgwStreamAtFourItems.lean::pgwStreamShortCircuitKeepsThree`](../../../lean4/CampaignPgwStreamAtFourItems.lean)
- [`lean4/CampaignPgwStreamAtFourItems.lean::pgwStreamShortCircuitSkipsFour`](../../../lean4/CampaignPgwStreamAtFourItems.lean)
- [`lean4/CampaignPgwStreamAtFourItems.lean::pgwStreamThreeNotFour`](../../../lean4/CampaignPgwStreamAtFourItems.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust port of the stream tree`

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-stream-at-four-items.py::main`](../../../checks/independent/pgw-stream-at-four-items.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_stream/stream.py::build_stream_tree`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stream/stream.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:259`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/continuation.txt:1067-1070`
  - `dag/derivations/independent/pgw-stream-at-four-items.md:5`
  - `dag/research/campaign_pgw-stream-at-four-items_lean_replay.json:6`
