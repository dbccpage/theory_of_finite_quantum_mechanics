---
documentation_contract: symbol-game-documentation/v1
title: "002_oesn: S(n) presentations and finite mathematical examples"
kind: grammar-reference
status: active
maturity: research
authority_effect: "None"
aliases:
  - 002_s_n
related:
  - ../000_oepregen/README.md
  - ../001_oegen/README.md
  - ../003_oemssn/README.md
  - ../004_oepfp/README.md
---

# 002_oesn: S(n) presentations and finite mathematical examples

AuthorityEffect: None.

This strand continues Genesis using explicit stage labels, demand records,
representations and finite examples. Start with the [source correspondence](source_correspondence.md),
then [sn.md](sn.md), the [reading guide](reading_guide.md) and the
[curriculum](curriculum.md).

The source is [19L57G1 pinned at `f1d56c010e6ba10a3b9418bd7cc5953c067250f2`](https://github.com/dbccpage/19L57G1/tree/f1d56c010e6ba10a3b9418bd7cc5953c067250f2).
Its `<ab>` is one opaque datum; the pair syntax in this folder is a later
interpretation. The initial `<>` is one token, two ASCII bytes, and zero
admitted data. Supply and admission remain distinct operations.

## Directory catalogue

| Directory | Contents |
| --- | --- |
| [levels](levels/README.md) | Lessons 00–06 and finite mathematical examples 07–21 |
| [grammar](grammar/sn_guide.md) | Flat EBNF and explicit recursive audit profile |
| [code](code/README.md) | Small Python models, syntax checks and tests |
| [lean4](lean4/SnTheorems.lean) | Typed syntax, declared finite carriers and image-recovery proofs |
| [normal_forms](normal_forms/README.md) | Draft contract specifications and schema |
| [domains](domains/README.md) | Declared database, protocol and geometric applications |
| [papers](papers/README.md) | Navigation to the consolidated paper |
| [_images](_images) | Schematics retained with the corresponding lesson identifiers |

The active combined paper is [From Pre-Genesis to MSS-N](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md).
The Rust primitive owner is [omega_ooutwire_primitives](../../../omega_engine/crates_rs/omega_ooutwire_primitives/src/lib.rs);
its planned name is `omega_genesis`. The [WDP construction](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/derivations/genesis_construction.md)
is the executable continuation from literal `<>` through recorded admissions
to a chosen finite simplicial interpretation.

## Lesson files

| File | Status |
| --- | --- |
| [level_00_ground](levels/level_00_ground.md) | Source-oriented lesson / supplied ledger |
| [level_01_symbol_genesis](levels/level_01_symbol_genesis.md) | Source-oriented lesson / supplied ledger |
| [level_02_relational_pairings](levels/level_02_relational_pairings.md) | Source-oriented lesson / supplied ledger |
| [level_03_abstract_simplices](levels/level_03_abstract_simplices.md) | Source-oriented lesson / supplied ledger |
| [level_04_simplex_graph_expansions](levels/level_04_simplex_graph_expansions.md) | Source-oriented lesson / supplied ledger |
| [level_05_regge_metric_simplices](levels/level_05_regge_metric_simplices.md) | Source-oriented lesson / supplied ledger |
| [level_06_tower_extension_retraction](levels/level_06_tower_extension_retraction.md) | Source-oriented lesson / supplied ledger |
| [level_07_transfer_operators_orbits](levels/level_07_transfer_operators_orbits.md) | Declared mathematical example |
| [level_08_monadic_adjunction_cochains](levels/level_08_monadic_adjunction_cochains.md) | Declared mathematical example |
| [level_09_dagger_monads_reversal](levels/level_09_dagger_monads_reversal.md) | Declared mathematical example |
| [level_10_spectral_epistemic_quarantine](levels/level_10_spectral_epistemic_quarantine.md) | Declared mathematical example |
| [level_11_polygraph_confluence_peaks](levels/level_11_polygraph_confluence_peaks.md) | Declared mathematical example |
| [level_12_observer_stack_dda](levels/level_12_observer_stack_dda.md) | Declared mathematical example |
| [level_13_alternation_cycle_detection](levels/level_13_alternation_cycle_detection.md) | Declared mathematical example |
| [level_14_bounded_quantifier_grammar](levels/level_14_bounded_quantifier_grammar.md) | Declared mathematical example |
| [level_15_rbg_authority_separation](levels/level_15_rbg_authority_separation.md) | Declared mathematical example |
| [level_16_filtered_ind_objects](levels/level_16_filtered_ind_objects.md) | Declared mathematical example |
| [level_17_per_lift_dialects](levels/level_17_per_lift_dialects.md) | Declared mathematical example |
| [level_18_discrete_hodge_decomposition](levels/level_18_discrete_hodge_decomposition.md) | Declared mathematical example |
| [level_19_zeta_spectral_shadow](levels/level_19_zeta_spectral_shadow.md) | Declared mathematical example |
| [level_20_autopoietic_reflection](levels/level_20_autopoietic_reflection.md) | Declared mathematical example |
| [level_21_discrete_4d_regge_curvature](levels/level_21_discrete_4d_regge_curvature.md) | Declared mathematical example |

## Known divergences

The audit corrections distinguish actual source facts from later constructions:

- S(0)–S(6), W, H and `(0,1,1,1,0,1,1)` are local presentation and ledger
  choices. They are not field names or a forced stage sequence in 19L57G1.
- Source cost-two separation chooses a unary mark under the refined arity
  price. A binary edge is an additional interpretation, not that minimizer.
- Grammar cases SN_001–SN_085 check syntax. The earlier attribution of
  semantic E13–E21 checks to them, including nonexistent SN_086–089, is withdrawn.
- Local Python models and Lean tables have narrower scopes than source replay.
  The ground carrier and image-recovery defects were corrected; see
  [the exact scope](source_correspondence.md).
- Verification callbacks no longer automatically grant policy approval.
  Local callback records are unsigned and do not authenticate an authority.

The files in this strand do not depend on retired curriculum notebooks.
Run the maintained checks from [code/README.md](code/README.md).
