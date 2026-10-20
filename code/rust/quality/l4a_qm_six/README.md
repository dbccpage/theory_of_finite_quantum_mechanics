# QM/math source and assessment recovery

This tooling replays bounded Rust implementations in majorana, mub, number_theory, operad_theory, sheaf_theory and qm. AuthorityEffect: None.

Historical input files, assessments and test evidence are retained under evidence/quality/l4a_qm_six, including recovery/original-inputs. Historical completed-grade labels are not current endorsements. Live gate decisions are unassessed until an independent source-bound review; passing baselines or a mutation ratio do not automatically award a grade. Capability defaults are provisional and limited to the actual delivered source.

Use replay.py --release --metrics --doctests for a fresh isolated offline snapshot, then records.py --receipt RECEIPT (and --check) to bind live sidecars. The source manifest includes copied fixture assets and local arithmetic dependencies. Candidate patches and interrupted runs remain historical and cannot certify current code. No full-workspace, continuum, global MUB6 solution, or Rust-to-Lean equivalence is implied.

The 20261020T192034Z recovery run preserves deliberately interrupted doctest and extra-challenge work separately; see recovery/review.md and recovery/expedite-interruption.json. A failed or cancelled command is not a passing result, and the incomplete mutation build is not a certification input.

Companion storage now uses one `<source-stem>.contract.score.yaml`. Original receipt-addressed records and all scoring versions are retained inside that file; old physical companions are removed. See [the migration guide](../../../../docs/CONTRACT_SCORING_HISTORY.md). Legacy quality-tool path addresses resolve through the scoped reader/writer adapter.
