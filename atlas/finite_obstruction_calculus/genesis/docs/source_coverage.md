# Source coverage and correspondence

This companion refers to `dbccpage/19L57G1` at
`f1d56c010e6ba10a3b9418bd7cc5953c067250f2`. The source remains unchanged.
The first-publication audit checks **all 3,147 tracked files, 70,063,012 bytes,
23 top-level areas, and 121 research directories** against that commit.
The research declaration index contains 239 documents. These are population
and byte-identity counts, not counts of proved or independently reviewed results.

## What was checked

The [inventory manifest](../manifests/source_inventory.json) binds the
[complete pinned file inventory](../manifests/source_inventory_detail.json)
by SHA-256. The historical review is retained outside the release package. Its `full_pinned_source_file_inventory` retains every expected path,
Git blob hash, byte count, and file mode; that large inventory is stored once.
The new manifest adds a complete top-level and research crosswalk, current
source-declaration paths, and their SHA-256 hashes. Its proposition dispositions
come from that earlier review, checked against the same pinned source records.

The fresh executable audit compares the exact commit, complete Git tree, index,
and raw working-file bytes. It refuses extra files, including ignored files,
and refuses symlinks and submodules. It checks the complete branch population
and all 239 declaration-document hashes. The manifest, bound inventory, and
their parent directories are checked before resolving or reading them;
symlinks, non-regular control files, and unreadable traversal cause refusal.
It does not follow or execute source
instructions, run the source's gate suite, rebuild the source's proofs, or
validate mathematical claims merely because their names occur in a ledger.

The declaration review reads the source's status and claim boundaries, with
particular attention to its closeout, corrections, and statements used by this
companion. Coverage of all 121 directory declarations is distinct from a
line-by-line proof review of their implementations. The whole snapshot contains
1,240 Python files and 526 Lean files. Neither number is a fresh test or proof
verification result. Source labels such as `PROVED_THEOREM` and
`VERIFIED_FINITE` below remain source claims with their original scope.

## Current source record

The [closeout, sections 9.4–10](sources/closeout.txt#L479-L587)
records three independent judgments:

| Question | Recorded judgment |
|---|---|
| Research stage | `CLOSED_WITH_OPEN_OBSTRUCTIONS` |
| Alpha reference implementation | `READY_WITHIN_DECLARED_SCOPE` |
| Original seed completion gate | `UNSATISFIED` |

The freeze was approved on 2026-09-28 for snapshot
`90ab34a056d80bb1048d926abcfdfef81e578fe1`, after both authorized continuations
had ended. The retained second-paper headers still say “FREEZE CANDIDATE”
because those bytes were frozen. The later closeout records the approval;
the old headers do not reopen the run. Outstanding source obligations include
gate injection coverage, the comparison requested within the source run,
and the unestablished input-count floor. Companion work does not retrospectively
change those source verdicts.

The root [README](sources/genesis_readme.txt) reports a dated local root-package run:
60 Python source files, 75 Lean modules, and 787 collected Python tests
(786 passed, one skipped). Its 1,530 axiom reports concern the enumerated
theorems, not every declaration in the entire repository. Definitions and
top-level audit apparatus have separate scope; the README explicitly records
`Classical.choice` in four audit-apparatus definitions. These are historical
source receipts, not measurements repeated by this companion audit.

## Top-level crosswalk

Every top-level area containing a tracked file has a row. Counts include
all files under each directory, including historical artifacts.

| Area | Files | Role |
|---|---:|---|
| `.claude` | 11 | Local gate instructions and verification skills. |
| `.gitattributes` | 1 | Tracked-byte and line-ending policy. |
| `.github` | 1 | Written local verification workflow; hosted CI is disabled. |
| `.gitignore` | 1 | Ignored-file policy. |
| `.python-version` | 1 | Python runtime declaration. |
| `AGENTS.md` | 1 | Source operating instructions. |
| `CLAUDE.md` | 1 | Source scope, exposure, vocabulary, and verification policies. |
| `LICENSE` | 1 | Source software license. |
| `README.md` | 1 | Entry point; includes explicitly dated root-only counts. |
| `artifacts` | 48 | Stored deterministic results and compressed finite trees. |
| `ci` | 22 | Gate, inventory, custody, and claim-resolution tools. |
| `code` | 61 | Sealed Python model, observer, candidate search, and finite studies. |
| `contact` | 6 | Contact and exposure record. |
| `docs` | 12 | Closeout, freeze approval, handoff, corrections, and research indexes. |
| `lean4` | 81 | Root formal development and its audit apparatus. |
| `ob1_e2_restatement` | 3 | Separate analysis of the endogenous-demand obligation. |
| `paper` | 30 | Preserved source paper, ledger, and change history. |
| `prompt` | 2 | Read-only input protocol and seed. |
| `pyproject.toml` | 1 | Python package and tool configuration. |
| `requirements.txt` | 1 | Python dependency versions. |
| `research` | 2797 | Post-seal branches, with their own inputs and claim ledgers. |
| `tests` | 63 | Root Python checks; separate from research tests. |
| `verification_20260817.md` | 1 | Historical verification record, not a current run. |

## Corrections that govern the companion's claims

The source's [dated correction record](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/docs/section3_claim_corrections.md)
withdraws several broader readings. These corrections apply when the companion
uses the corresponding results.

| Source area | Correspondence and claim boundary |
|---|---|
| Original minimum-response result | The minimum cost, surviving readings, declared bounds, equivalence relation, and supplied measure travel with the result. Ties do not authorize selection. |
| `alpha_engine` | The final handoff records repaired admission checks and nine passing local steps. Lean refinement, endogenous demand generation, and consumer bridges remain separate obligations. |
| `second_engine`, `second_run` | The first continuation examines the declared 144-engine class; the second records the 288-run census. Bounds and the missing Python-driver refinement remain explicit. |
| `g012_typed_translation` | Local codecs on typed tokens and Python strings are distinct implementations. The native cycle obstruction prevents an injective, transition-commuting encoding of a nontrivial replacement cycle into finite monotone admission histories. |
| `g013_trace_calculus` | Trace identities and composition have proved laws. Declared higher-cell constructors and reflexive boundary equalities do not supply a strict 2-category theorem. |
| `native_structure` | The later `CellD`/`FarRel` development has its own interchange result; it must not be attributed to G013. Its cost obstruction needs the stated path and square relations. |
| `g018_self_hosting` | Boolean self-negation lemmas require a representation/evaluation fixed-point bridge before they become a general self-predictor theorem. |
| `iso_sound`, `iso_sound_lean` | Bounded canonicalizer agreement and conditional abstract orbit lemmas do not settle general Python canonicalizer soundness. |
| `ignition`, `unboundedness` | A supplied schedule can produce arbitrary finite prefixes. An auxiliary Lean relation and actual Python-driver trajectories are separate evidence. |
| `conservation_ladder` | Constancy on states reachable from Genesis under every event is the stated result. Separate integer and dual-number examples do not prove a smooth physical conservation theory. |
| `domain_adapters`, `native_bridge` | A commuting map can collapse source observations. Required observation, equality, and continuation preservation must be named and proved separately. |
| `admission_sign_shadow` | The terminal remains `BRIDGE_PRODUCERS_PROVED_END_TO_END_OPEN`; producer proofs leave source authorization, nontriviality, calibration, and connector fields open. |
| `described_replay` | Its recorded failing custody check remains part of the record; a complete source inventory does not make every branch's historical verifier pass. |
| `p208c_commutator_tomography` | Dimension-general Lean results concern integer matrices. Exact Python tomography is separate from an arbitrary-field formal reconstruction theorem. |
| `p209a_wigner_phase_space` | Negativity of defined rational values does not prove their identity with a state-to-Wigner transform. |
| `p209b_clifford_symplectic` | Lean checks six explicit matrices modulo 2; Python separately enumerates matrices modulo 3. No general Clifford quotient follows. |
| `p209c_stabilizer_codes` | Explicit Lean commutation and syndrome facts remain distinct from Python distance, recovery, and projector calculations. |
| `p209d_nonclassical_horizons` | Finite maps, defined tables, and a doubling recurrence do not establish general state classification or simulator complexity. |
| `x303_bounded_agency`, `x310_vertical_integration` | The host harness needs its own refinement; a square comparing four counts is weaker than equality of complete relational states. |
| `boundary_seed`, `oriented_boundary` | Exposure and intervention records remain visible. Source isolation is not a proof of independent discovery or historical blindness. |

## All research directories

The [source registration table](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/README.md) has **118 rows**:
31 in the written gate-11 research job and 87 local-receipt rows. Three of the
latter are marked parked: `admit_leftover`, `dynamics_step`, and
`g1_local_class`. The three remaining directories—`_scaffold`, `e2e_tests`,
and `notes`—are infrastructure or notes outside that table.

“Gate 11” denotes inclusion in the written local research-job contract.
Hosted CI is disabled, and a Lean verifier can be listed in the written Lean
job while its research row says “local receipt.” Registration is neither a
fresh passing receipt nor a theorem about a branch's contents.

Each row below links the source's primary declaration. The manifest also lists
the branch's README, status, findings, and claim-ledger files where present,
with exact byte identities and the earlier review's proposition disposition.
The grouping is for navigation; it does not assert a derivation from one group
to another, or a completed encoding into an Omega Engine mathematics crate.

### Verification and research infrastructure

| Research directory | Primary declaration | Registration |
|---|---|---|
| `_scaffold` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/_scaffold/README.md) | Outside table |
| `e2e_tests` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/e2e_tests/README.md) | Outside table |
| `estate_honesty` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/estate_honesty/STATUS.md) | Gate 11 |
| `evidence_graph` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/evidence_graph/README.md) | Local receipt |
| `full_accounting` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/full_accounting/README.md) | Local receipt |

### Demand, admission, and authorization

| Research directory | Primary declaration | Registration |
|---|---|---|
| `alpha_engine` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/alpha_engine/STATUS.md) | Local receipt |
| `endogenous_demand` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/endogenous_demand/STATUS.md) | Local receipt |
| `ignition` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/ignition/README.md) | Local receipt |
| `instance_demand` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/instance_demand/STATUS.md) | Local receipt |
| `standing_commitment` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/standing_commitment/STATUS.md) | Local receipt |
| `symmetry_floor` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/symmetry_floor/STATUS.md) | Local receipt |
| `two_sided_commitment` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/two_sided_commitment/STATUS.md) | Local receipt |

### Second derivation and its continuations

| Research directory | Primary declaration | Registration |
|---|---|---|
| `second` | [paper.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/second/paper.md) | Local receipt |
| `second_class` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/second_class/STATUS.md) | Gate 11 |
| `second_duration` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/second_duration/STATUS.md) | Gate 11 |
| `second_engine` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/second_engine/STATUS.md) | Gate 11 |
| `second_index` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/second_index/STATUS.md) | Gate 11 |
| `second_inheritance` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/second_inheritance/STATUS.md) | Gate 11 |
| `second_iso` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/second_iso/STATUS.md) | Gate 11 |
| `second_nofirst` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/second_nofirst/STATUS.md) | Gate 11 |
| `second_profile` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/second_profile/STATUS.md) | Gate 11 |
| `second_response` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/second_response/STATUS.md) | Gate 11 |
| `second_run` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/second_run/STATUS.md) | Gate 11 |
| `second_stake` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/second_stake/STATUS.md) | Gate 11 |
| `second_stream` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/second_stream/STATUS.md) | Gate 11 |
| `second_succession` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/second_succession/STATUS.md) | Gate 11 |
| `second_symmetry` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/second_symmetry/STATUS.md) | Gate 11 |

### Representation and preservation

| Research directory | Primary declaration | Registration |
|---|---|---|
| `conservation_ladder` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/conservation_ladder/README.md) | Gate 11 |
| `domain_adapters` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/domain_adapters/README.md) | Gate 11 |
| `native_bridge` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/native_bridge/README.md) | Gate 11 |
| `native_structure` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/native_structure/README.md) | Gate 11 |

### Costs, measures, and signs

| Research directory | Primary declaration | Registration |
|---|---|---|
| `admission_sign_shadow` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/admission_sign_shadow/STATUS.md) | Local receipt |
| `cost_cohomology` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/cost_cohomology/STATUS.md) | Local receipt |
| `exchange_coefficients` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/exchange_coefficients/README.md) | Local receipt |
| `fresh_characters` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/fresh_characters/STATUS.md) | Local receipt |
| `path_dependent_cost` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/path_dependent_cost/STATUS.md) | Local receipt |
| `reach_additivity` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/reach_additivity/STATUS.md) | Local receipt |
| `reach_measure` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/reach_measure/STATUS.md) | Local receipt |
| `sign_slice` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/sign_slice/STATUS.md) | Local receipt |
| `sign_tower` | [FINDINGS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/sign_tower/FINDINGS.md) | Local receipt |
| `twin_pricing` | [FINDINGS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/twin_pricing/FINDINGS.md) | Local receipt |

### Declared formal foundations

| Research directory | Primary declaration | Registration |
|---|---|---|
| `g001_target_charter` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/g001_target_charter/README.md) | Local receipt |
| `g010_primitive_removal` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/g010_primitive_removal/README.md) | Local receipt |
| `g011_finitary_substrate` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/g011_finitary_substrate/README.md) | Local receipt |
| `g012_typed_translation` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/g012_typed_translation/README.md) | Local receipt |
| `g013_trace_calculus` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/g013_trace_calculus/README.md) | Local receipt |
| `g014_observer_descent` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/g014_observer_descent/README.md) | Local receipt |
| `g015_autonomous_stepping` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/g015_autonomous_stepping/README.md) | Local receipt |
| `g018_self_hosting` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/g018_self_hosting/README.md) | Local receipt |
| `g1_local_class` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/g1_local_class/STATUS.md) | Local receipt; parked |

### Mathematical constructions

| Research directory | Primary declaration | Registration |
|---|---|---|
| `m104_equality_order` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/m104_equality_order/README.md) | Local receipt |
| `m105_number_tower` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/m105_number_tower/README.md) | Local receipt |
| `m108_internal_algebra` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/m108_internal_algebra/README.md) | Local receipt |
| `m109_obstruction_homology` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/m109_obstruction_homology/README.md) | Local receipt |
| `m114_solver_adapter` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/m114_solver_adapter/README.md) | Local receipt |

### Supplied physical models

| Research directory | Primary declaration | Registration |
|---|---|---|
| `p200_operational_protocols` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/p200_operational_protocols/README.md) | Local receipt |
| `p201_relational_spacetime` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/p201_relational_spacetime/README.md) | Local receipt |
| `p203_composite_systems` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/p203_composite_systems/README.md) | Local receipt |
| `p204_operational_valuations` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/p204_operational_valuations/README.md) | Local receipt |
| `p208a_path_interference` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/p208a_path_interference/README.md) | Gate 11 |
| `p208b_contextuality_nonlocality` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/p208b_contextuality_nonlocality/README.md) | Gate 11 |
| `p208c_commutator_tomography` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/p208c_commutator_tomography/README.md) | Gate 11 |
| `p209a_wigner_phase_space` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/p209a_wigner_phase_space/README.md) | Local receipt |
| `p209b_clifford_symplectic` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/p209b_clifford_symplectic/README.md) | Local receipt |
| `p209c_stabilizer_codes` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/p209c_stabilizer_codes/README.md) | Gate 11 |
| `p209d_nonclassical_horizons` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/p209d_nonclassical_horizons/README.md) | Local receipt |

### Operational integration

| Research directory | Primary declaration | Registration |
|---|---|---|
| `x300_observer_information` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/x300_observer_information/README.md) | Local receipt |
| `x301_formal_semantics` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/x301_formal_semantics/README.md) | Local receipt |
| `x302_operational_reasoning` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/x302_operational_reasoning/README.md) | Local receipt |
| `x303_bounded_agency` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/x303_bounded_agency/README.md) | Local receipt |
| `x310_vertical_integration` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/x310_vertical_integration/README.md) | Local receipt |

### Finite structures and source boundaries

| Research directory | Primary declaration | Registration |
|---|---|---|
| `admit_leftover` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/admit_leftover/STATUS.md) | Local receipt; parked |
| `balance_carrier` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/balance_carrier/STATUS.md) | Local receipt |
| `blind_restart` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/blind_restart/STATUS.md) | Gate 11 |
| `boundary_seed` | [paper.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/boundary_seed/paper.md) | Gate 11 |
| `closed_family` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/closed_family/STATUS.md) | Local receipt |
| `coherent_process_limits` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/coherent_process_limits/README.md) | Local receipt |
| `concurrency` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/concurrency/README.md) | Local receipt |
| `convention_price` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/convention_price/STATUS.md) | Local receipt |
| `described_replay` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/described_replay/STATUS.md) | Local receipt |
| `diagonal_identity` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/diagonal_identity/STATUS.md) | Local receipt |
| `dynamics_step` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/dynamics_step/STATUS.md) | Local receipt; parked |
| `endogenous_continuum` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/endogenous_continuum/README.md) | Local receipt |
| `f_class_distinctness` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/f_class_distinctness/STATUS.md) | Local receipt |
| `family_embedding` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/family_embedding/STATUS.md) | Local receipt |
| `genesis_continuation` | [claims.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/genesis_continuation/claims.md) | Local receipt |
| `grammar_fit` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/grammar_fit/STATUS.md) | Local receipt |
| `higher_order_diagonalization` | [FINDINGS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/higher_order_diagonalization/FINDINGS.md) | Local receipt |
| `identification_dual` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/identification_dual/STATUS.md) | Local receipt |
| `internal_syntax_logic` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/internal_syntax_logic/README.md) | Local receipt |
| `iso_sound` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/iso_sound/STATUS.md) | Local receipt |
| `iso_sound_lean` | [FINDINGS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/iso_sound_lean/FINDINGS.md) | Local receipt |
| `limit_and_observer` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/limit_and_observer/STATUS.md) | Gate 11 |
| `local_reuse` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/local_reuse/README.md) | Local receipt |
| `magnification` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/magnification/README.md) | Local receipt |
| `multi_depth` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/multi_depth/STATUS.md) | Local receipt |
| `multi_magnitude` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/multi_magnitude/STATUS.md) | Local receipt |
| `natural_sections` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/natural_sections/STATUS.md) | Local receipt |
| `notes` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/notes/README.md) | Outside table |
| `observer_visibility` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/observer_visibility/STATUS.md) | Local receipt |
| `oriented_boundary` | [CLOSURE.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/oriented_boundary/CLOSURE.md) | Local receipt |
| `partial_decide` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/partial_decide/STATUS.md) | Gate 11 |
| `portable_interface` | [INTERFACE.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/portable_interface/INTERFACE.md) | Gate 11 |
| `post_seal_walk` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/post_seal_walk/README.md) | Local receipt |
| `priced_admissions` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/priced_admissions/STATUS.md) | Local receipt |
| `primitive_difference_tower` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/primitive_difference_tower/STATUS.md) | Gate 11 |
| `reachable` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/reachable/README.md) | Local receipt |
| `reading_f_iso` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/reading_f_iso/STATUS.md) | Local receipt |
| `record_reading` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/record_reading/README.md) | Local receipt |
| `redheffer` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/redheffer/STATUS.md) | Local receipt |
| `represented_execution` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/represented_execution/README.md) | Local receipt |
| `s9_obligations` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/s9_obligations/STATUS.md) | Local receipt |
| `self_interpreter` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/self_interpreter/STATUS.md) | Local receipt |
| `setting_translation` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/setting_translation/README.md) | Local receipt |
| `seventh_constructor` | [FINDINGS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/seventh_constructor/FINDINGS.md) | Local receipt |
| `side_free` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/side_free/STATUS.md) | Gate 11 |
| `target_a_execution` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/target_a_execution/README.md) | Local receipt |
| `target_b_dynamics` | [README.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/target_b_dynamics/README.md) | Local receipt |
| `thinghood` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/thinghood/STATUS.md) | Local receipt |
| `typed_translation` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/typed_translation/STATUS.md) | Gate 11 |
| `unboundedness` | [STATUS.md](https://github.com/dbccpage/19L57G1/blob/f1d56c010e6ba10a3b9418bd7cc5953c067250f2/research/unboundedness/STATUS.md) | Local receipt |

## Reproduce the byte audit

Use a pristine checkout at the full source commit, with Git line-ending
conversion disabled. The audit reads the supplied checkout and writes only
its JSON result to standard output. Run from this paper directory:

```sh
python code/audit_source.py \
  --source-root /path/to/pristine/19L57G1 \
  --manifest manifests/source_inventory.json
```

The successful receipt names its exact command, Python and Git versions,
exit status, manifest digest, and checked population. A missing or altered
file produces a nonzero exit status. This strict audit intentionally refuses
build products and ignored caches in the source checkout; use a separate
pristine checkout instead of deleting working research outputs.

The isolated controls are in
[`code/tests/test_source_audit.py`](../code/tests/test_source_audit.py). They
exercise altered bytes, missing files, a wrong commit, staged deletion,
untracked and ignored files, symlink substitution, a tampered inventory,
inconsistent tree metadata, omitted branches, and false declaration hashes.
Control-file symlinks, symlinked control directories, non-regular control files,
and injected traversal permission failures also produce failure receipts.
They do not execute the 19L57G1 research suite.

The Rust correspondence and educational interpretations have additional
contracts and checks. File fidelity establishes which source they compare
against; it does not substitute for those semantic checks.
