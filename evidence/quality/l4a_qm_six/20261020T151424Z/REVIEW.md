# Six-directory QM/math review checkpoint

AuthorityEffect: None.

538 subjects have 1076 source-bound scoring/contract sidecars.
1548 scoped test cases passed. 26 five-gate assessments are complete.
The L4A goal remains in progress for unreviewed subjects. Null gates are unassessed; 3 source functions exceed Grade A structural ceilings (CCN <= 10, cognitive <= 15, nesting <= 3) across 538 subjects (7485 explicit source functions), all in unassessed Null-gate QM modules (`qm/bridge.rs`, `qm/report_fiber.rs`, `qm/simplicial_grav.rs`).

| Directory | Subjects | Completed assessments | Known E | Source functions above A ceilings |
|---|---:|---:|---:|---:|
| majorana | 21 | 5 | 0 | 0 |
| mub | 284 | 5 | 0 | 0 |
| number_theory | 39 | 4 | 0 | 0 |
| operad_theory | 36 | 4 | 0 | 0 |
| sheaf_theory | 24 | 4 | 0 | 0 |
| qm | 134 | 4 | 0 | 3 |

Structural counts include explicit source in test/support files and compatibility mirror entries (`mub/src/`);
they are not a measurement of compiler-expanded production execution or a semantic defect count.

Structural and mutation remediations completed in this checkpoint:
- Decomposed Band B, C, and D functions across `majorana`, `mub` (including `mub/src/` mirrors), `number_theory`, `operad_theory`, `sheaf_theory`, and `qm` below `CCN <= 10`, `cognitive_upper_bound <= 15`, and `control_nesting <= 3` (`0` functions exceeding Grade A across `majorana`, `mub`, `number_theory`, `operad_theory`, and `sheaf_theory`, and `3` functions remaining in unassessed `qm` modules out of `7485` explicit source functions).
- Added fallible constructor `BinaryField::try_new` with `BinaryFieldError` (`DegreeOutOfRange`, `DegreeMismatch`, `ReducibleModulus`, `OrderOverflow`) and unit test `try_new_refuses_invalid_degrees_and_reducible_moduli` in `number_theory/binary_field.rs`, promoting its `G3` gate from `B` to `A` (`L4A`).
- Expanded designated semantic mutations in `mutations.py` to 30 recipes (`MAJ01`–`MAJ05`, `MUB01`–`MUB05`, `NT01`–`NT05`, `OP01`–`OP05`, `SH01`–`SH05`, `QM01`–`QM05`) across 26 core modules (`30/30` killed, `0` survived, `conservative_ratio = 1.0`) and completed 26 five-gate `L4A` reviews in `specs.json`.

No commit, push, PR or merge is asserted by this checkpoint.
