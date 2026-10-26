---
documentation_contract: symbol-game-documentation/v1
title: "003_oemssn: Minimal Symbol System specification atlas"
kind: grammar-reference
status: active
maturity: research
atlas_status: specified
successor_status: declared
lift_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
aliases:
  - 003_minimal_symbol_system_n_mssn
---

# 003_oemssn: Minimal Symbol System specification atlas

MSS-N is an externally designed atlas of 101 capability specifications. It supplies
grammars, proposed interfaces, finite examples and verification obligations for
constructing mathematical representations. Its row number does not identify a
stage in the frozen Genesis derivation.

The active combined manuscript is [From Pre-Genesis to MSS-N](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md).
The former paper packages have been consolidated and removed. The retained
[papers directory](papers/README.md) points to the replacement manuscript.
The first-publication [Genesis paper](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md)
addresses the source derivation itself.

## Where to start

| Path | Purpose |
| --- | --- |
| [Reading guide](reading_guide.md) | Worked questions about grammar, evaluation, preservation and permission. |
| [Levels index](levels/README.md) | All 101 proposed capability rows. |
| [Alphabet and encoding note](levels/level_insert_38_symbol_ladder_and_transfinite_forms.md) | Exact alphabet inclusions, free-monoid non-isomorphism and a decodable countable code. |
| [Grammar](grammar/README.md) | The 22 named public starts and their lexical conventions. |
| [Code](code/README.md) | Grammar checker, codecs and targeted test commands. |
| [Lean inventory](lean4/README.md) | Actual algebraic theorems, syntax sketches and fixture checks, distinguished by scope. |
| [Domain packages](domains/README.md) | Finite examples and model-specific obligations. |
| [Publication review](publication_review.md) | Corrections, validation scope and remaining obligations. |

## Three different indices

| Object | What its index records | Evidence needed to advance |
| --- | --- | --- |
| Genesis source | A provenance-bearing construction or source step | The declared admission regime and its actual transition evidence. |
| S(n) core presentation | A documented stage of the retained Genesis interpretation | A stated correspondence with the source and its unresolved demand. |
| MSS atlas | An external capability specification | An implemented checker and a separately established lift preserving the stated questions. |

For example, MSS-2 proposes directed relations, while the S(2) core records
observational collapse. Matching the number 2 does not identify these objects.
There is no demonstrated sequence of licensed lifts from MSS-0 to MSS-100.

Supplying the literal `<>` in the canonical primitive regime does not admit a
carrier datum. The [WDP construction supplement](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/derivations/genesis_construction.md)
records an executable continuation with separate admissions and an explicit
simplicial interpretation. That construction does not reopen the frozen source
experiment or turn atlas headings into source discoveries.

## What the interfaces establish

A successful parse establishes membership in the selected grammar. An evaluator
must calculate its declared result from the submitted carrier. A lift must
preserve the specified equality, operations or questions; an authorization must
be checked under its own policy. These are separate obligations.

Three syntaxes occur in this estate: the unwrapped glyph families of
`mssn.ebnf`, the proposed `mss-boundary-v1` presentation, and the executable tower
wire with binary opcodes. They are not interchangeable. In particular, a level's
illustrative packet is not necessarily accepted by either executable parser.
Most `Evaluator::*` and `ERR_*` labels in the atlas are interface proposals;
use a concrete code path and validation receipt before treating one as implemented.
The historical per-row evidence flags are catalog metadata, not execution results.

## Reproduction

From the repository root, use a Python environment with pytest:

```sh
python omega_engine_education/documentation/003_oemssn/code/check_mssn.py
python -m pytest omega_engine_education/documentation/003_oemssn/code/tests/test_mssn_codec.py omega_engine_education/documentation/003_oemssn/code/tests/test_retraction_codec.py -q
```

The grammar checker replays 39 cases across 22 starts. The codec test suite
includes non-ASCII digit refusals, the finite Unicode token inventory, raw glyphs,
malformed directly constructed ASTs, retained postfix structure and rejection of
layout that the extended tokenizer previously discarded. These checks do not
prove semantic equivalence between Python and Lean.

The [physics cleanup](physics_claim_cleanup.md) is a dated historical review.
Its removals remain in effect; its former test failures and tool availability are
not a current build report. Retained finite algebra, graph and boundary examples
do not establish a derived physical theory.
