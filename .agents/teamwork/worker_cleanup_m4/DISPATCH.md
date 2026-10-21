## 2026-10-20T21:45:05Z
You are a Worker agent (worker_cleanup_m4).
Your working directory is: c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\worker_cleanup_m4

MANDATORY FIRST STEP:
Read c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\original_request.md

OBJECTIVES (Milestone 4 Disk Space Cleanup & Final Gate Verification):
1. Clean Cargo target directories:
   In code/rust/quality/category_homology/rust_metrics/, execute `cargo clean` (or remove target/) to ensure local disk space discipline (Requirement R4). Confirm no large temporary Cargo target/ directories or build caches remain across the workspace.
2. Final Verification Pass:
   Execute and confirm exit code 0 on:
   - python dag/validate_derivation_dag.py --no-files
   - python dag/pfp/validate_prompts.py
   - python -m pytest dag/test_validate_derivation_dag.py dag/pfp/test_custody.py dag/pfp/test_staged_prompts.py code/python/tests/test_qm_atlas_loc.py
   - python scripts/verify_qm_atlas_loc.py
3. Document disk space findings and verification results in handoff.md in your working directory. Notify parent orchestrator when complete.
