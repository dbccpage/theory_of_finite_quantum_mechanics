# PGW-ALPHA-LICENSE-BINDING-M1-M8

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The Alpha reference slice is READY_WITHIN_DECLARED_SCOPE: after one repair pass (commit b698cf7f) the eight mandatory conditions hold within the §7 trust boundary. M1 authorized admission executes only a member freshly recomputed from the sealed kernel; M2 a parent Node whose history does not replay to its regime is refused; M3 a License is bound to the source history digest, the target, the measure and the bounds, and reuse with any field changed is refused; M4 uniqueness is not authorization; M5 every retained class receives one disposition (explored, pruned or open); M6 proposal and evaluation are inert and OPEN, bound or guard outcomes are typed stops, never admitted successes; M7 the slice replays offline with no model provider; M8 one local command (python verify.py) passed nine of nine steps with 0 skipped checks, including 169 tests and the sealed kernel's 66. The audit reproduced B1, B2 and B3 through the real path, and each repair fired and recovered under live injection.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- Trust boundary of closeout §7: trusted sealed runtime modules, harness code and host; excluded process compromise, kernel or harness tampering, SHA-256 collisions, concurrent use and any authentication (assumption)
- The one-command receipt is a local receipt in dbccpage/19L57G1, not hosted CI and not re-run in this checkout (assumption)

## Bottleneck

Within the declared scope only: a License is checked for consistency with the call, not for provenance, so the host's call is the authorization; the refinement to Lean is NOT_PROVED, demand generation is OPEN and consumer bridges are OPEN.

## Source status

closeout.txt §3 M1-M8, §7 audit and §10 alpha_reference; ALPHA_HANDOFF §7; local receipt verify.py nine of nine

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/04_authorization/tfq_0505_alpha_license_binding_m1_m8.md`

- file: [dag/derivations/04_authorization/tfq_0505_alpha_license_binding_m1_m8.md](../../../dag/derivations/04_authorization/tfq_0505_alpha_license_binding_m1_m8.md)
- sha256 (`lf-normalised`): `5dec3cd308ec162211242cc0b954d1cb3c3cb328e661394901505d2489f2cbaf`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0505
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/docs/ALPHA_HANDOFF.md:130-133`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/driver_a.py::apply_licensed`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/harness.py::check_license_binding`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/tests/test_admission_boundary.py::B3LicenseBinding`

## Absences recorded by the TFQ records

- TFQ-0505 lean4: research/alpha_engine/lean/Harness.lean (dbccpage/19L57G1 only) is about harness datatypes and does not model the License binding; python_driver_refinement NOT_PROVED
- TFQ-0505 rust: no Rust port of the Alpha harness

## Routes

Incoming (1):

- `PGW-R-ALPHA-LICENSE-BINDING-M1-M8` `COMPUTED`: [TFQ-0331](TFQ-0331.md) (SOURCE_RECORD), [PGW-CANDIDATE-EXTENSION-GENERATOR](PGW-CANDIDATE-EXTENSION-GENERATOR.md) (DEFINITION)

Outgoing (1):

- `UDG-R-TFQ-0506` `DERIVED_PROSE`: [TFQ-0506](TFQ-0506.md) (DEFINITION)
