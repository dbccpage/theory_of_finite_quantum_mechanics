# QM/math source and assessment recovery

This tooling replays bounded Rust implementations in majorana, mub, number_theory, operad_theory, sheaf_theory and qm. AuthorityEffect: None.

Historical input files, assessments and test evidence are retained under evidence/quality/l4a_qm_six, including recovery/original-inputs. Historical completed-grade labels are not current endorsements. Live gate decisions are unassessed until an independent source-bound review; passing baselines or a mutation ratio do not automatically award a grade. Capability defaults are provisional and limited to the actual delivered source.

Use replay.py --release --metrics --doctests for a fresh isolated offline snapshot, then records.py --receipt RECEIPT (and --check) to bind live sidecars. The source manifest includes copied fixture assets and local arithmetic dependencies. Candidate patches and interrupted runs remain historical and cannot certify current code. No full-workspace, continuum, global MUB6 solution, or Rust-to-Lean equivalence is implied.
