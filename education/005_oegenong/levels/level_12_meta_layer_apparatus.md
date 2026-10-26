---
documentation_contract: symbol-game-documentation/v1
title: "Level 12: the OEWAS gates in `ci/`"
kind: grammar-reference
audience:
  - researchers
  - engineers
  - coding-agents
status: active
maturity: draft
claim_status: verified
authority_effect: "None"
source_pin: "dbccpage/H3V7N5QF@5d9488324ce976817987bd83a28d901371cfc073"
source_paths:
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/ci/OEWAS_GATES.md
  - ../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/tests/test_oewas_gates.py
last_verified: 2026-10-08
---

# Level 12: the OEWAS gates in `ci/`

**AuthorityEffect:** None.

**Pin:** `dbccpage/H3V7N5QF` at `5d9488324ce976817987bd83a28d901371cfc073`.

**Package:** [`001_genesis_ongoing_h3v7n5qf`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf).

![Level 12: the OEWAS gates in `ci/`](../_images/genesis_ongoing_12_meta_layer_apparatus.svg)

The drawing `genesis_ongoing_12_meta_layer_apparatus.svg` is an education schematic in this documentation tree. The sentences below are taken from the pinned package.

`ci/OEWAS_GATES.md` names four gates: vacuous self-comparison (`check_vacuous_checks.py`), definitional citation (`check_definitional_citations.py`), mutation must bite (`check_mutation_bite.py`), and cited Lean name in the derivation's own report (`check_axiom_citations.py`).

The vacuous-comparison gate flags an equality whose two operands canonicalize to the same expression. The definitional-citation gate flags a ledger row marked derived that rests on a Lean theorem that does not prove the row.

The file says each gate is shown by a bite: it fails on the defect, names it, and passes again when the defect is removed. The tests are `tests/test_oewas_gates.py`.

## Files

- [`ci/OEWAS_GATES.md`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/ci/OEWAS_GATES.md)
- [`tests/test_oewas_gates.py`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/tests/test_oewas_gates.py)
