# Recovered evidence: Authorization as an Incompleteness Theory (formal and code half)

**AuthorityEffect:** None.

**Recovered:** 2026-10-21, from
`C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory` (42 files; the source
folder was read-only and none of its PowerShell was executed).

This directory holds the verbatim evidence files of the FORMAL and CODE half of that folder. The prose half
(papers, claim ledger, change log, goals, `_support/`) is recovered separately.

## Layout

| Path | What it is |
| --- | --- |
| `original/` | Byte-for-byte copies of the formal and code files, in the source's relative layout. Every SHA-256 matches `original/formal_binding_manifest.md`. |
| `original/formal/*.lean` | The eleven UNPORTED Lean sources (they use the old flat module names). The ported, built copies are `lean4/AuthIncompleteness/*.lean`. |
| `original/code/replay_packet/` | `packet_manifest.json`, proposal, contract, terminal policy, and the PowerShell evaluator and verifier (read, not run). |
| `original/code/tests/`, `original/code/integration_tests/` | The PowerShell test corpora (read, not run). |
| `original/computability_carrier_candidates.json` | The candidate inventory (globally `open`, nothing selected). |
| `original/formal_binding_manifest.md`, `original/evidence/source_map.md` | Producer-side binding manifest and source map. |
| `reconstructed/lean-toolchain` | NOT a recovered file. The packet manifest binds `lean4/genx/lean-toolchain` by hash; its content `leanprover/lean4:v4.32.2\n` was reconstructed and its SHA-256 equals the recorded `2bdc48ad...37273`. |
| `axiom_reports/` | `#print axioms` output for every ported theorem (58) and for the unported originals compiled with Lean v4.35.0 (identical). |
| `replay_results/recompute_report.json` | Output of `tools/recompute.py`. |
| `tools/` | `recompute.py` (re-runs every re-runnable computation) and `companions.py` (writes code-companion records). |

`.gitattributes` in this directory pins `* -text` so the hashed bytes survive any checkout.

## What was re-run, and whether it still matches

| Recorded evidence | Re-run | Result |
| --- | --- | --- |
| 18 SHA-256 bindings of recovered files in `formal_binding_manifest.md` | `tools/recompute.py` | all 18 match |
| 3 further packet artifacts (proposal, contract, terminal policy) | Python packet replay | all match their `packet_manifest.json` digests |
| `lean-toolchain` digest | reconstruction | matches (reconstructed, not recovered) |
| 3 digests of `lean4/genx/lakefile.lean`, `lake-manifest.json` and the PO-000 / J011 sources | none possible | not recovered |
| "23 unit cases, 21 rejected mutations" (PowerShell) | `code/python/tests/test_auth_incompleteness_replay_packet.py` | 23 cases reproduced, 21 mutations refused |
| "six cases, five rejected mutations" (carrier candidates) | `code/python/tests/test_auth_incompleteness_candidates.py` | reproduced; 7 evidence paths cannot be resolved here (see below) |
| Packet result: verified, terminal `open`, control-only report inadequate | Python port `qm.auth_incompleteness.replay_packet` | matches the contract's `expected` block |
| Integration replay: the bound transition model plus its dependency compile | Python `run_formal_replay` with `leanprover/lean4:v4.35.0` (the recorded v4.32.2 is not installed) | passes |
| "Build succeeded 2026-08-21, 40 jobs" and the printed axioms | `lake build AuthIncompleteness` (Lean 4.35.0, Mathlib v4.35.0 pin; the modules import no Mathlib) | builds; 58 `#print axioms` lines reproduce every recorded ceiling exactly (`none` or `propext`) |

Refinements the replay found, none of them contradicting a recorded claim:

* The marked-cell contract has TWO countertraces in the packet evaluator, `runningMarked` and `haltedMarked`
  (both step to `haltedBlank`). The contract only requires `runningMarked`; the Lean file names only that one.
* The evaluator hard-codes `full_report_adequate = true`; it is true by identity, but it is not computed.
* `replay_packet.psm1` pins PowerShell 7.6.3 at run time. The Python port cannot and does not check that.

Not re-runnable: the `lean4/genx` Lake target (the lakefile and manifest are absent); `PO-000` and `J011` sources;
the PO-022 and PO-023 scaffold greps (`theorem PO22_C1 : True`); the seven candidate evidence paths that name
PO-022 / PO-023 files, the GenX lakefile, and the two prose files `proof_program.md` and
`computability_lift_admission.md` (the last two resolve once the prose half sits beside this directory).

## Port notes

* Lean: `lean4/AuthIncompleteness/{Core,DirectTM,TokenCode,GlobalLift,Terminal,PDModels,Externality,Replay,TapeControl,TapeTransition}.lean`,
  root `lean4/AuthIncompleteness.lean`, `lean_lib AuthIncompleteness` in `lean4/lakefile.lean` (not a default
  target). `PDBridge.lean` is kept but excluded from the roots because it imports J011.
* No proof was changed: statements and proofs are byte-identical to the originals apart from module names and a
  provenance header. One deprecation warning appears under v4.35.0 (`if_neg` in `Replay.lean`); it is not
  an error and the proof was left unchanged.
* Python: `code/python/src/qm/auth_incompleteness/` (`replay_packet.py` = port of `replay_packet.psm1` plus
  `verify_transition_packet.ps1`; `carrier_candidates.py` = port of the candidate validator; `finite_models.py` = new
  executable twins of the Lean DTM0 / DTM1 / transition-table fixtures). PowerShell that computes something was
  ported to Python; the PowerShell itself is retained only here.

* NEW, not recovered: `lean4/AuthIncompleteness/MathlibBridge.lean` instantiates the recovered `GlobalLift` transport with
  Mathlib's `Computable` and `ComputablePred.halting_problem`. It was compiled with `lean` v4.35.0 against the Mathlib build
  (exit 0, no warning; output in `axiom_reports/mathlib_bridge_axioms.txt`) and is not a lakefile root.

See `../FORMAL_RECOVERY_NOTES.md` for the inventory, audit and the C1 to C8 reuse analysis.
