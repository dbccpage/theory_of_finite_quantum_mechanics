# FSP-KITAEV-HONEYCOMB-SOLUTION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Kitaev (2006): in the four-Majorana representation of the honeycomb model, the plaquette fluxes W_p commute with H and with each other, and in each flux sector H is quadratic in the c Majoranas with a static Z2 gauge field (after projection to the physical subspace).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Kitaev honeycomb spin model and its Majorana representation (Kitaev 2006)

## Bottleneck

A sign-free sampling claim for this representation is not made or checked here; the gauge projection and flux-sector sum must be kept explicit.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-043 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/fsp/kitaev_honeycomb_bisimulation_bridge.py`

- file: [code/python/src/fsp/kitaev_honeycomb_bisimulation_bridge.py](../../../code/python/src/fsp/kitaev_honeycomb_bisimulation_bridge.py)
- sha256 (`bytes`): `83c7a6bc2b6e24b75bbcd469a3d1c0fcd9ce88ea8fa6ee820a9bc2a554603eeb`
- cited in: record TFQ-1207
- counts toward the grade: yes

### Python: `code/python/tests/fsp/test_kitaev_honeycomb_bisimulation.py`

- file: [code/python/tests/fsp/test_kitaev_honeycomb_bisimulation.py](../../../code/python/tests/fsp/test_kitaev_honeycomb_bisimulation.py)
- sha256 (`bytes`): `26a6d1c85e7e8e1170c0e563369604cd0fdc10d44a203d847d33cbedc9b91571`
- cited in: record TFQ-1207
- check: `python -m pytest code/python/tests/fsp/test_kitaev_honeycomb_bisimulation.py::test_vortex_free_ground_state`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_vortex_free_ground_state` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/fsp/test_kitaev_honeycomb_bisimulation.py::test_vortex_free_ground_state` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1207_fsp_kitaev_honeycomb_solution.md`

- file: [dag/derivations/26_fsp/tfq_1207_fsp_kitaev_honeycomb_solution.md](../../../dag/derivations/26_fsp/tfq_1207_fsp_kitaev_honeycomb_solution.md)
- sha256 (`lf-normalised`): `0ebd0dfc15b2b70e488dcdd6d206bc1ad34155458ba75abdfb68022cc9ea9fc4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1207
- counts toward the grade: no

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-KITAEV-HONEYCOMB-SOLUTION` `CONDITIONAL_ON_IMPORT`: [FSP-MAJORANA-CLIFFORD-PARITY](FSP-MAJORANA-CLIFFORD-PARITY.md) (IMPORTED_ASSUMPTION), [FSP-WITTEN-INDEX-INVARIANCE](FSP-WITTEN-INDEX-INVARIANCE.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `APP-R-FSP-LAUGHLIN-EXCHANGE-PHASE` `CONDITIONAL_ON_IMPORT`: [FSP-LAUGHLIN-EXCHANGE-PHASE](FSP-LAUGHLIN-EXCHANGE-PHASE.md) (IMPORTED_ASSUMPTION)
