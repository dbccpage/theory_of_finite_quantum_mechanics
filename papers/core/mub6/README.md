# MUB(6): exact reductions, conditional interfaces and open gaps

**AuthorityEffect:** None.

> **Status:** incomplete. Whether seven mutually unbiased bases exist in
> dimension six is open. This deposit does not settle it. Gap G1 is OPEN in
> [the gap registry](research/mub6_gap_registry.json). The current scope is in
> [the paper](mub6.md) and [the claim ledger](mub6_claim_ledger.md).
> Some historical research files state stronger results; those statements are
> withdrawn in [the superseded notice](research/superseded_notice.md).

---

## 1. Summary

This deposit holds the manuscript, exact-arithmetic verifiers, receipts and
historical research records for a study of mutually unbiased bases (MUBs) in
dimension $d=6$. The Lean 4 sources it cites live in the source monorepo at
`lean4/research_programs/mub6/`. At the pinned source snapshot that directory holds
185 `.lean` files; the root module `Mub6.lean` imports 180 of them. Only three Lean export and audit
files are copied into this deposit under `lean4/`.

The checked results are exact reductions, finite computations and conditional
Lean theorems. Section 8 of the paper lists each claim with its evidence and
status.

## 2. Claim discipline

1. Every claim is scoped to the stated region, orbit, chart or premise.
2. Computational certifiers use exact rational ($\mathbb{Q}$) or cyclotomic
   ($\mathbb{Q}(\zeta_{24})$) arithmetic. Floating-point values are not
   accepted as certificates.
3. Conditional Lean theorems (for example `no_complete_mub6_via_route_c`) take
   their premises as hypotheses. They do not discharge those premises.
4. Files produced with LLM proposers (`code/mub_verify/openrouter_proposer.py`,
   `code/mub_verify/a2_llm_proposer.py`, the `*superbunny*` scripts and
   receipts) are exploratory records, not evidence. See
   [the provenance note](documentation/mub6_provenance_and_bridge_coverage.md).

## 3. Historical campaigns

Campaigns 1 to 8 are historical records. Their milestone names do not state
current results. The paper and the gap registry replace them.

## 4. Repository structure

```
010_mub6/
├── README.md                    # This document
├── agents.md                    # Agent rules for this deposit
├── LICENSE                      # CC-BY-4.0 (manuscript and documentation)
├── LICENSE-CODE                 # Apache License 2.0 (software)
├── mub6_global_proof_atlas.md   # Evidence index with status per surface
├── completion_supplement.md     # Historical replay notes (2026-09-25)
├── verify_deposit.py            # Deposit integrity verifier
├── mub6.md / mub6.tex / mub6.pdf # Canonical manuscript and synchronized renders
├── mub6_change_log.md            # Version history
├── mub6_claim_ledger.*           # Retained research indexes; excluded from preprint
├── research/                    # Gap registry, roadmap, historical records,
│                                # superseded_notice.md
├── artifacts/                   # Receipts and receipt manifest
├── code/mub_verify/             # Python research verifiers
├── scripts/                     # Receipt generators, release builder
├── lean4/                       # Three Lean export/audit files
├── rust/                        # Two Rust source files
├── tests/                       # Deposit pytest suite
└── zenodo/                      # Historical archive v1.0 and its manifests
```

## 5. Verification

From this directory:

```pwsh
py -3.12 verify_deposit.py --integrity-only
py -3.12 -m pytest tests -q -p no:cacheprovider
```

`verify_deposit.py` exits 0 on pass and 1 on any failure. It checks the paper
header with a schema kit from the source monorepo. Outside the monorepo, add
`--skip-header-schema`; the skip is printed as `SKIPPED`.

The Lean build and the Rust `omega_mub` tests need the source monorepo:

```pwsh
py -3.12 verify_deposit.py --integrity-only --lean --lean-root <monorepo>/lean4
cargo test -j 1 -p omega_mub --manifest-path <monorepo>/omega_engine/crates_rs/Cargo.toml
```

## 6. License

| Material | License |
| --- | --- |
| Manuscript text (`mub6.md` and its renders) | CC-BY-4.0 |
| Code, scripts and tests | Apache-2.0 (see `LICENSE-CODE`) |

## Publication candidate 1.1.1

All former `papers/` files are at this package root. The canonical manuscript
is [mub6.md](mub6.md), dated 2026-10-16, version 1.1.1. The public preprint is
`mub6_publication.zip` with `mub6_publication.zip.sha256`. Its staged contents
are under `zenodo/preprint/`; research ledgers, prompts, historical archives,
receipts and incomplete Lean export files are excluded from this preprint.

Run `python scripts/build_pdf.py`, then
`python scripts/build_publication_release.py` from this directory.
Use `python scripts/verify_publication.py --root zenodo/preprint --archive mub6_publication.zip`
for read-only verification. The whole research-tree check remains
`python verify_deposit.py --integrity-only` and is a different check.

The candidate metadata is [zenodo_metadata.json](zenodo_metadata.json).
Read [the description](docs/descriptions.md), [quick start](docs/quick_start.md)
and [release identity](release_identity.json). This is a prepared candidate:
complete formal replay and author review remain outstanding. No external
deposit, reserved DOI or published record is claimed.

Manuscript and documentation are CC-BY-4.0 (`LICENSE`); software and historical
data/receipt assets retain Apache-2.0 (`LICENSE-CODE`). Original third-party
attribution and licensing remain applicable to historical source materials.

<!-- BEGIN UNIFIED-DAG-BACKLINKS -->
<!-- Generated by papers/core/tools/build_corpus_dag_backlinks.py; edit the tool, not this region. -->

## Unified DAG

Audit of 2026-10-21. The unified derivation DAG (`dag/fragments/unified_dag.json`) folds the records of this corpus into one graph: a record with no trunk counterpart is a NEW application-branch node with its own TFQ record; a restatement of a trunk step is an ALIAS row that points to the trunk node. *Source claimed* is the status the source asserted; *Audited* is the status the audit assigned against what is actually in this checkout (Lean declarations resolved, replays rerun, statements compared). The original claims, labels and text of this document are kept unchanged. A status below the source claim means the claim is not established as stated; it does not mean the underlying mathematics is false (only REFUTED means that). For an ALIAS row the audited column is the status of the trunk node, which is the authority for the restated step. Regenerate with `python -I -X utf8 papers/core/tools/build_corpus_dag_backlinks.py`. The MUB6 register has no status field; the claimed status of its records is PROVED_LEAN because each cites a Lean name. Rows whose id is not a `MUB6-DERIV-*` id come from the claim ledger, the paper or the atlas.

63 NEW records and 51 ALIAS rows; 35 same, 26 lowered, 1 raised, 1 reclassified. REFUTED: `MUB6-DERIV-062`.

| Source id | Kind | TFQ record | DAG node | Source claimed | Audited | Reconciliation |
|---|---|---|---|---|---|---|
| `MUB6-ATLAS-CORNER-ROUTING` | NEW | [TFQ-1266](../../../dag/derivations/25_mub/tfq_1266_mub6_corner_routing_dephasing.md) | `MUB6-CORNER-ROUTING-DEPHASING` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C01` | NEW | [TFQ-1256](../../../dag/derivations/25_mub/tfq_1256_mub6_route_c_label_arithmetic.md) | `MUB6-ROUTE-C-LABEL-ARITHMETIC` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C05` | NEW | [TFQ-1257](../../../dag/derivations/25_mub/tfq_1257_mub6_route_c_conditional.md) | `MUB6-ROUTE-C-CONDITIONAL` | CONDITIONAL | **CONDITIONAL** | same |
| `MUB6-C10` | NEW | [TFQ-1259](../../../dag/derivations/25_mub/tfq_1259_mub6_cauchy_binet_minor_bound.md) | `MUB6-CAUCHY-BINET-MINOR-BOUND` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C12` | NEW | [TFQ-1260](../../../dag/derivations/25_mub/tfq_1260_mub6_bounded_block_quartet_equations.md) | `MUB6-BOUNDED-BLOCK-QUARTET-EQUATIONS` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C15` | NEW | [TFQ-1264](../../../dag/derivations/25_mub/tfq_1264_mub6_balanced_648_quadratic.md) | `MUB6-BALANCED-648-QUADRATIC` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C19` | NEW | [TFQ-1267](../../../dag/derivations/25_mub/tfq_1267_mub6_deltoid_cover_box_defect.md) | `MUB6-DELTOID-COVER-BOX-DEFECT` | COMPUTATIONALLY_CHECKED | **PROVED_PROSE** | raised |
| `MUB6-C20` | NEW | [TFQ-1269](../../../dag/derivations/25_mub/tfq_1269_mub6_szollosi_gauged_666.md) | `MUB6-SZOLLOSI-GAUGED-666` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C24` | NEW | [TFQ-1268](../../../dag/derivations/25_mub/tfq_1268_mub6_szollosi_618_system.md) | `MUB6-SZOLLOSI-618-SYSTEM` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C25` | NEW | [TFQ-1271](../../../dag/derivations/25_mub/tfq_1271_mub6_rectangular_krawczyk_soundness.md) | `MUB6-RECTANGULAR-KRAWCZYK-SOUNDNESS` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C27` | NEW | [TFQ-1272](../../../dag/derivations/25_mub/tfq_1272_mub6_szollosi_fullbox_unresolved.md) | `MUB6-SZOLLOSI-FULLBOX-UNRESOLVED` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | lowered |
| `MUB6-C28` | NEW | [TFQ-1270](../../../dag/derivations/25_mub/tfq_1270_mub6_szollosi_box_368_exclusion.md) | `MUB6-SZOLLOSI-BOX-368-EXCLUSION` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C29` | NEW | [TFQ-1276](../../../dag/derivations/25_mub/tfq_1276_mub6_concrete_projectors.md) | `MUB6-CONCRETE-PROJECTORS` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C30` | NEW | [TFQ-1277](../../../dag/derivations/25_mub/tfq_1277_mub6_concrete_moment_flatness.md) | `MUB6-CONCRETE-MOMENT-FLATNESS` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C32` | NEW | [TFQ-1278](../../../dag/derivations/25_mub/tfq_1278_mub6_word_projector_extraction.md) | `MUB6-WORD-PROJECTOR-EXTRACTION` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C34` | NEW | [TFQ-1279](../../../dag/derivations/25_mub/tfq_1279_mub6_interface_countermodel.md) | `MUB6-INTERFACE-COUNTERMODEL` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C35` | NEW | [TFQ-1280](../../../dag/derivations/25_mub/tfq_1280_mub6_commutative_flat_real_point.md) | `MUB6-COMMUTATIVE-FLAT-REAL-POINT` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C36` | NEW | [TFQ-1281](../../../dag/derivations/25_mub/tfq_1281_mub6_fourth_basis_flat_moments.md) | `MUB6-FOURTH-BASIS-FLAT-MOMENTS` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C37` | NEW | [TFQ-1282](../../../dag/derivations/25_mub/tfq_1282_mub6_empty_variety_moment_nonpsd.md) | `MUB6-EMPTY-VARIETY-MOMENT-NONPSD` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C40` | NEW | [TFQ-1274](../../../dag/derivations/25_mub/tfq_1274_mub6_szollosi_common_rays.md) | `MUB6-SZOLLOSI-COMMON-RAYS` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-C41` | NEW | [TFQ-1275](../../../dag/derivations/25_mub/tfq_1275_mub6_szollosi_special_point_pairs.md) | `MUB6-SZOLLOSI-SPECIAL-POINT-PAIRS` | COMPUTATIONALLY_CHECKED | **COMPUTATIONALLY_CHECKED** | same |
| `MUB6-DERIV-001` | ALIAS | - | `PG-INERT-DIAMOND` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-002` | ALIAS | - | `PG-ADMISSION-FLOOR` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-003` | ALIAS | - | `L1-QM002-O022A-PHI1-QUOTIENT` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-004` | ALIAS | - | `PG-GEN-REWRITING-COMMUTATION` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-005` | ALIAS | [TFQ-0003](../../../dag/derivations/03_finite_obstruction/tfq_0003_finite_obstruction_calculus_on_a_declared_carrier.md) | `TFQ-0003` | PROVED_LEAN | **OPEN** | restated in trunk |
| `MUB6-DERIV-006` | ALIAS | [TFQ-0455](../../../dag/derivations/02_genesis/tfq_0455_d2_initial_pointed.md) | `PGW-D2-INITIAL-POINTED` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-007` | ALIAS | [TFQ-0499](../../../dag/derivations/02_genesis/tfq_0499_python_lean_carrier_bridge.md) | `PGW-PYTHON-LEAN-CARRIER-BRIDGE` | PROVED_LEAN | **OPEN** | restated in trunk |
| `MUB6-DERIV-008` | ALIAS | [TFQ-0459](../../../dag/derivations/02_genesis/tfq_0459_canonical_key_classification.md) | `PGW-CANONICAL-KEY-CLASSIFICATION` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-009` | ALIAS | [TFQ-0447](../../../dag/derivations/02_genesis/tfq_0447_count_invariance_transport.md) | `PGW-COUNT-INVARIANCE-TRANSPORT` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-010` | ALIAS | [TFQ-0549](../../../dag/derivations/06_wdp/tfq_0549_wdp_degree_k_torsion_balance.md) | `PGW-WDP-DEGREE-K-TORSION-BALANCE` | PROVED_LEAN | **PROVED_PROSE** | restated in trunk |
| `MUB6-DERIV-011` | ALIAS | [TFQ-0553](../../../dag/derivations/06_wdp/tfq_0553_wdp_observer_quotient_passivity.md) | `PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-012` | ALIAS | - | `PG-WDP-DIAGNOSTIC-NOT-ROUTING` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-013` | ALIAS | - | `DS-QM090-092-AUTHORITY-FIREWALL` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | restated in trunk |
| `MUB6-DERIV-014` | ALIAS | - | `DS-QM103-SHOW-THE-PACKET-PROTOCOL` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-015` | ALIAS | - | `PG-WDP-DIAGNOSTIC-NOT-ROUTING` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-016` | ALIAS | - | `L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-017` | ALIAS | - | `L1-WDP-WITNESS-MASS` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-018` | ALIAS | - | `DS-QM081-STOCHASTIC-L1-CONTRACTION` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-019` | ALIAS | - | `L1-QM121-LADDER-RUNGS-2-6` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-020` | ALIAS | [TFQ-0170](../../../dag/derivations/22_implementation_sibling/tfq_0170_keep_majorization_finite_markov_laws_and_row_stochastic_maps_on_exact_rational_kernels.md) | `TFQ-0170` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | restated in trunk |
| `MUB6-DERIV-021` | ALIAS | - | `L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-022` | ALIAS | - | `L1-IMP-U1-PHASES` | PROVED_LEAN | **IMPORTED_ASSUMPTION** | restated in trunk |
| `MUB6-DERIV-023` | ALIAS | - | `FQ-BORN-NORMALIZATION-REDUNDANCY` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-024` | ALIAS | - | `GP-IMPORT-GLEASON` | PROVED_LEAN | **IMPORTED_ASSUMPTION** | restated in trunk |
| `MUB6-DERIV-025` | ALIAS | - | `DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-026` | ALIAS | - | `L1-IMP-HILBERT-INNER-PRODUCT` | PROVED_LEAN | **CONDITIONAL** | restated in trunk |
| `MUB6-DERIV-027` | ALIAS | [TFQ-0315](../../../dag/derivations/09_finite_hilbert/tfq_0315_exact_density_ray_and_population_shadow.md) | `TFQ-0315` | PROVED_LEAN | **SOURCE_RECORD** | restated in trunk |
| `MUB6-DERIV-028` | ALIAS | - | `DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT` | PROVED_LEAN | **IMPORTED_ASSUMPTION** | restated in trunk |
| `MUB6-DERIV-029` | ALIAS | [TFQ-0416](../../../dag/derivations/27_tensor_composition/tfq_0416_tensor_finite_povm_availability.md) | `TENSOR-FINITE-POVM-AVAILABILITY` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-030` | ALIAS | - | `FQ-CPTP-CLASS-DEFINITION` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-031` | ALIAS | [TFQ-0138](../../../dag/derivations/21_implementation_core/tfq_0138_heisenberg_picture_and_cayley_jet.md) | `TFQ-0138` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | restated in trunk |
| `MUB6-DERIV-032` | ALIAS | - | `DS-QM030-GRADED-PATHSUM` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | restated in trunk |
| `MUB6-DERIV-033` | ALIAS | - | `FQ-DISCRETE-DYNAMICS-DICHOTOMY` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-034` | ALIAS | - | `DS-QM041-HEISENBERG-PICTURE-FINITE` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | restated in trunk |
| `MUB6-DERIV-035` | ALIAS | - | `DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT` | PROVED_LEAN | **IMPORTED_ASSUMPTION** | restated in trunk |
| `MUB6-DERIV-036` | ALIAS | - | `FQ-U1-TRANSPORT-N-TORSION` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-037` | ALIAS | - | `DS-QM064-074-083-ANNEX-REDIRECT-ROWS` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-038` | ALIAS | - | `DS-QM063-HOLONOMY-COHERENT-INTENSITY` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-039` | ALIAS | - | `FQ-QM207-231-FINITE-MAP-CONTROLS` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-040` | ALIAS | - | `FQ-U1-TRANSPORT-N-TORSION` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-041` | ALIAS | [TFQ-0018](../../../dag/derivations/17_finite_qcd/tfq_0018_treat_c_n_as_a_declared_label_space_before_any_graph_attachment.md) | `TFQ-0018` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | restated in trunk |
| `MUB6-DERIV-042` | ALIAS | [TFQ-0011](../../../dag/derivations/17_finite_qcd/tfq_0011_finite_qcd_shadow.md) | `TFQ-0011` | PROVED_LEAN | **OPEN** | restated in trunk |
| `MUB6-DERIV-043` | ALIAS | [TFQ-0033](../../../dag/derivations/17_finite_qcd/tfq_0033_construct_an_explicit_three_index_color_contraction_before_using_a_baryon_singlet_label.md) | `TFQ-0033` | PROVED_LEAN | **OPEN** | restated in trunk |
| `MUB6-DERIV-044` | ALIAS | - | `DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-045` | ALIAS | [TFQ-0021](../../../dag/derivations/17_finite_qcd/tfq_0021_record_channel_factors_as_casimir_arithmetic_not_as_composites.md) | `TFQ-0021` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | restated in trunk |
| `MUB6-DERIV-046` | ALIAS | [TFQ-0084](../../../dag/derivations/19_finite_qg/tfq_0084_finite_quantum_gravity_shadow.md) | `TFQ-0084` | PROVED_LEAN | **OPEN** | restated in trunk |
| `MUB6-DERIV-047` | ALIAS | [TFQ-0107](../../../dag/derivations/19_finite_qg/tfq_0107_gap_einstein_equation_and_physical_cosmological_constant_stay_unpaid_deficit_is_not.md) | `TFQ-0107` | PROVED_LEAN | **OPEN** | restated in trunk |
| `MUB6-DERIV-048` | ALIAS | - | `DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-049` | ALIAS | - | `DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-050` | ALIAS | - | `DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS` | PROVED_LEAN | **PROVED_LEAN** | restated in trunk |
| `MUB6-DERIV-051` | NEW | [TFQ-1221](../../../dag/derivations/25_mub/tfq_1221_mub6_quhex_tensor_carrier.md) | `MUB6-QUHEX-TENSOR-CARRIER` | PROVED_LEAN | **DEFINITION** | reclassified |
| `MUB6-DERIV-052` | NEW | [TFQ-1222](../../../dag/derivations/25_mub/tfq_1222_mub6_no_field_of_order_six.md) | `MUB6-NO-FIELD-OF-ORDER-SIX` | PROVED_LEAN | **IMPORTED_ASSUMPTION** | lowered |
| `MUB6-DERIV-053` | NEW | [TFQ-1223](../../../dag/derivations/25_mub/tfq_1223_mub6_weyl_heisenberg_d6.md) | `MUB6-WEYL-HEISENBERG-D6` | PROVED_LEAN | **IMPORTED_ASSUMPTION** | lowered |
| `MUB6-DERIV-054` | NEW | [TFQ-1224](../../../dag/derivations/25_mub/tfq_1224_mub6_weyl_stabilizer_bound.md) | `MUB6-WEYL-STABILIZER-BOUND` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-055` | ALIAS | [TFQ-0402](../../../dag/derivations/25_mub/tfq_0402_mub_exact_projectors.md) | `MUB-EXACT-PROJECTORS` | PROVED_LEAN | **DEFINITION** | restated in trunk |
| `MUB6-DERIV-056` | NEW | [TFQ-1225](../../../dag/derivations/25_mub/tfq_1225_mub6_quartet_raw_hadamard_transport.md) | `MUB6-QUARTET-RAW-HADAMARD-TRANSPORT` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-057` | NEW | [TFQ-1226](../../../dag/derivations/25_mub/tfq_1226_mub6_fourier_dita_family_chm.md) | `MUB6-FOURIER-DITA-FAMILY-CHM` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-058` | NEW | [TFQ-1227](../../../dag/derivations/25_mub/tfq_1227_mub6_haagerup_matrix_chm.md) | `MUB6-HAAGERUP-MATRIX-CHM` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-059` | NEW | [TFQ-1228](../../../dag/derivations/25_mub/tfq_1228_mub6_szollosi_two_circulant.md) | `MUB6-SZOLLOSI-TWO-CIRCULANT` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-060` | NEW | [TFQ-1229](../../../dag/derivations/25_mub/tfq_1229_mub6_karlsson_affine_ansatz.md) | `MUB6-KARLSSON-AFFINE-ANSATZ` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-061` | NEW | [TFQ-1230](../../../dag/derivations/25_mub/tfq_1230_mub6_tao_matrix_chm.md) | `MUB6-TAO-MATRIX-CHM` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-062` | NEW | [TFQ-1231](../../../dag/derivations/25_mub/tfq_1231_mub6_affine_fiber_third_basis.md) | `MUB6-AFFINE-FIBER-THIRD-BASIS` | PROVED_LEAN | **REFUTED** | lowered |
| `MUB6-DERIV-063` | NEW | [TFQ-1232](../../../dag/derivations/25_mub/tfq_1232_mub6_product_triple_lower_bound.md) | `MUB6-PRODUCT-TRIPLE-LOWER-BOUND` | PROVED_LEAN | **COMPUTATIONALLY_CHECKED** | lowered |
| `MUB6-DERIV-064` | NEW | [TFQ-1233](../../../dag/derivations/25_mub/tfq_1233_mub6_fixed_triple_variety.md) | `MUB6-FIXED-TRIPLE-VARIETY` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-065` | NEW | [TFQ-1234](../../../dag/derivations/25_mub/tfq_1234_mub6_180_residual_count.md) | `MUB6-180-RESIDUAL-COUNT` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-066` | NEW | [TFQ-1235](../../../dag/derivations/25_mub/tfq_1235_mub6_gram_nullstellensatz_claim.md) | `MUB6-GRAM-NULLSTELLENSATZ-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-067` | NEW | [TFQ-1236](../../../dag/derivations/25_mub/tfq_1236_mub6_groebner_elimination_claim.md) | `MUB6-GROEBNER-ELIMINATION-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-068` | NEW | [TFQ-1237](../../../dag/derivations/25_mub/tfq_1237_mub6_torus_cad_emptiness_claim.md) | `MUB6-TORUS-CAD-EMPTINESS-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-069` | NEW | [TFQ-1251](../../../dag/derivations/25_mub/tfq_1251_mub6_moment_evaluation_flat.md) | `MUB6-MOMENT-EVALUATION-FLAT` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-070` | NEW | [TFQ-1238](../../../dag/derivations/25_mub/tfq_1238_mub6_degree2_sdp_gap_claim.md) | `MUB6-DEGREE2-SDP-GAP-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-071` | NEW | [TFQ-1239](../../../dag/derivations/25_mub/tfq_1239_mub6_flat_extension_failure_claim.md) | `MUB6-FLAT-EXTENSION-FAILURE-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-072` | NEW | [TFQ-1240](../../../dag/derivations/25_mub/tfq_1240_mub6_commutativity_defect_claim.md) | `MUB6-COMMUTATIVITY-DEFECT-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-073` | NEW | [TFQ-1241](../../../dag/derivations/25_mub/tfq_1241_mub6_positivstellensatz_claim.md) | `MUB6-POSITIVSTELLENSATZ-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-074` | NEW | [TFQ-1242](../../../dag/derivations/25_mub/tfq_1242_mub6_rational_ldl_claim.md) | `MUB6-RATIONAL-LDL-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-075` | NEW | [TFQ-1252](../../../dag/derivations/25_mub/tfq_1252_mub6_conjecture2_premise.md) | `MUB6-CONJECTURE2-PREMISE` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-076` | NEW | [TFQ-1253](../../../dag/derivations/25_mub/tfq_1253_mub6_tao_laurent_norm_nine.md) | `MUB6-TAO-LAURENT-NORM-NINE` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-DERIV-077` | NEW | [TFQ-1243](../../../dag/derivations/25_mub/tfq_1243_mub6_krawczyk_global_cover_claim.md) | `MUB6-KRAWCZYK-GLOBAL-COVER-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-078` | NEW | [TFQ-1244](../../../dag/derivations/25_mub/tfq_1244_mub6_smale_alpha_claim.md) | `MUB6-SMALE-ALPHA-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-079` | NEW | [TFQ-1245](../../../dag/derivations/25_mub/tfq_1245_mub6_residual_fence_claim.md) | `MUB6-RESIDUAL-FENCE-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-080` | NEW | [TFQ-1246](../../../dag/derivations/25_mub/tfq_1246_mub6_cusp_puiseux_claim.md) | `MUB6-CUSP-PUISEUX-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-081` | NEW | [TFQ-1247](../../../dag/derivations/25_mub/tfq_1247_mub6_psi_gluing_claim.md) | `MUB6-PSI-GLUING-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-082` | NEW | [TFQ-1248](../../../dag/derivations/25_mub/tfq_1248_mub6_phi1_circulation_claim.md) | `MUB6-PHI1-CIRCULATION-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-083` | NEW | [TFQ-1249](../../../dag/derivations/25_mub/tfq_1249_mub6_route_c_landing_claim.md) | `MUB6-ROUTE-C-LANDING-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-084` | NEW | [TFQ-1250](../../../dag/derivations/25_mub/tfq_1250_mub6_five_branch_routing_claim.md) | `MUB6-FIVE-BRANCH-ROUTING-CLAIM` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-085` | NEW | [TFQ-1254](../../../dag/derivations/25_mub/tfq_1254_mub6_no_quartet_d6.md) | `MUB6-NO-QUARTET-D6` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-DERIV-086` | NEW | [TFQ-1255](../../../dag/derivations/25_mub/tfq_1255_mub6_max_mub_six_equals_three.md) | `MUB6-MAX-MUB-SIX-EQUALS-THREE` | PROVED_LEAN | **OPEN** | lowered |
| `MUB6-IMPORT-OPENAI-LE5` | NEW | [TFQ-1365](../../../dag/derivations/25_mub/tfq_1365_mub6_openai_family_le_five.md) | `MUB6-OPENAI-FAMILY-LE-FIVE` | IMPORTED_ASSUMPTION | **IMPORTED_ASSUMPTION** | same |
| `MUB6-LEDGER-COVER56` | NEW | [TFQ-1273](../../../dag/derivations/25_mub/tfq_1273_mub6_cover56_curvature_premise.md) | `MUB6-COVER56-CURVATURE-PREMISE` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-LEDGER-G3-GLUING` | NEW | [TFQ-1258](../../../dag/derivations/25_mub/tfq_1258_mub6_gluing_g3_opaque.md) | `MUB6-GLUING-G3-OPAQUE` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-PAPER-BALANCE-SYZYGY` | NEW | [TFQ-1265](../../../dag/derivations/25_mub/tfq_1265_mub6_transition_balance_syzygy.md) | `MUB6-TRANSITION-BALANCE-SYZYGY` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-PAPER-CLOSE-COLUMNS` | NEW | [TFQ-1263](../../../dag/derivations/25_mub/tfq_1263_mub6_close_columns_exclusion.md) | `MUB6-CLOSE-COLUMNS-EXCLUSION` | PROVED_LEAN | **PROVED_LEAN** | same |
| `MUB6-PAPER-FINITE-CORNER` | NEW | [TFQ-1261](../../../dag/derivations/25_mub/tfq_1261_mub6_finite_corner_reduction.md) | `MUB6-FINITE-CORNER-REDUCTION` | PROVED_LEAN | **IMPORTED_ASSUMPTION** | lowered |
| `MUB6-PAPER-QUADRATIC-LIFT` | NEW | [TFQ-1262](../../../dag/derivations/25_mub/tfq_1262_mub6_quadratic_lift_386.md) | `MUB6-QUADRATIC-LIFT-386` | PROVED_LEAN | **PROVED_LEAN** | same |

<!-- END UNIFIED-DAG-BACKLINKS -->
