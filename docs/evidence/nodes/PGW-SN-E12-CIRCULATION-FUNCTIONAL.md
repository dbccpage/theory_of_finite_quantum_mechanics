# PGW-SN-E12-CIRCULATION-FUNCTIONAL

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Example E12 takes the oriented triangle a→b→c→a with C₀ = C₁ = ℤ³, coboundary d₀ and supplied edge record x = (1,0,0). On the open path a→b→c the potential g = (0,1,1) realizes the first two records but predicts −1 on ca. The circulation I(x) = x_ab + x_bc + x_ca vanishes on every d₀g and I(x) = 1, so no integer or rational potential realizes all three records; conversely I(x) = 0 gives the potential (0, x_ab, x_ab + x_bc), so im d₀ = ker I and C¹/im d₀ ≅ ℤ. The combined paper states the same criterion over ℤ, and Cochain.lean establishes it as triangle_repair_invariant and triangle_repair_exact_iff.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared oriented incidence of the triangle graph adapter, not the intrinsic meaning of \<ab\> (assumption)

## Bottleneck

Lean covers the criterion over ℤ; the rational case is the same written argument. With edge evidence fixed the result is a certificate, not a repair, changing one entry is a separately priced response, and the example is not a Genesis stage.

## Source status

pregenesis_to_minimal_symbol_systems paper.md section 17.2 and lean4/Cochain.lean; 002_oesn levels/level_12 (E12)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/PreGenesisToMssn/Cochain.lean`

- file: [lean4/Imported/PreGenesisToMssn/Cochain.lean](../../../lean4/Imported/PreGenesisToMssn/Cochain.lean)
- sha256 (`bytes`): `cf023d13e4f326637fdf44fcde7c8a76d47d4db40d969301885673b4b1573f9c`
- cited in: node.lean, record TFQ-0523
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mssn_sn.json](../../../dag/research/lean_replay_campaign_mssn_sn.json) (module `Imported.PreGenesisToMssn.Cochain`): recorded sha256 `cf023d13e4f326637fdf44fcde7c8a76d47d4db40d969301885673b4b1573f9c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/PreGenesisToMssn/Cochain.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `triangle_repair_exact_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms triangle_repair_exact_iff` |
| `triangle_repair_invariant` | yes | yes | yes | Quot.sound, propext | `#print axioms triangle_repair_invariant` |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md](../../../atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md)
- sha256 (`lf-normalised`): `a4a7d840b11e912896032aebc9ead95f7978c0e6f60656f44645c6d8fadf593b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0523_sn_e12_circulation_functional.md`

- file: [dag/derivations/05_mssn_sn/tfq_0523_sn_e12_circulation_functional.md](../../../dag/derivations/05_mssn_sn/tfq_0523_sn_e12_circulation_functional.md)
- sha256 (`lf-normalised`): `e1eaae2200e83de9ce712d953408c602a8eae6399007684bda34e5b807d40747`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0523
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:7756423a02888ae5532df2549868d088c1e68fb2bffc6a5de003d1c89fd93802:48-51`
- `external:sha256:7756423a02888ae5532df2549868d088c1e68fb2bffc6a5de003d1c89fd93802:52-54`

## Absences recorded by the TFQ records

- TFQ-0523 python: no Python check of E12 in the S(n) strand
- TFQ-0523 rust: no Rust check of the converse potential (0, x_ab, x_ab + x_bc); the MSS-N circulation audit is recorded under TFQ-0534

## Routes

Incoming (1):

- `PGW-R-SN-E12-CIRCULATION-FUNCTIONAL` `DERIVED_LEAN`: [PGW-SN-E08-WEIGHTED-L1-DUALITY](PGW-SN-E08-WEIGHTED-L1-DUALITY.md) (PROVED_LEAN)

Outgoing (4):

- `PGW-R-MSSN-CIRCULATION-OBSTRUCTION` `DERIVED_LEAN`: [PGW-MSSN-CIRCULATION-OBSTRUCTION](PGW-MSSN-CIRCULATION-OBSTRUCTION.md) (PROVED_LEAN)
- `PGW-R-SN-E19-TORSION-ERASED-OVER-Q` `DERIVED_PROSE`: [PGW-SN-E19-TORSION-ERASED-OVER-Q](PGW-SN-E19-TORSION-ERASED-OVER-Q.md) (PROVED_PROSE)
- `PGW-R-SN-E20-OBSERVER-COMPLETION` `DERIVED_PROSE`: [PGW-SN-E20-OBSERVER-COMPLETION](PGW-SN-E20-OBSERVER-COMPLETION.md) (PROVED_PROSE)
- `PGW-R-SN-E21-REPAIR-RANK` `DERIVED_PROSE`: [PGW-SN-E21-REPAIR-RANK](PGW-SN-E21-REPAIR-RANK.md) (PROVED_PROSE)
