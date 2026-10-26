# Genesis Rename compatibility replay

AuthorityEffect: None.

The maintained Lean 4.35.0 target is `Imported.GenesisOngoing.Second.Rename`,
already registered in the non-default `ImportedAtlas` library. Its provenance
header records the inverse rewrite and indexed induction proof repairs. Reproduce
the build with the shared Mathlib cache junction in place:

```powershell
cd lean4
lake +leanprover/lean4:v4.35.0 build Imported.GenesisOngoing.Second.Rename
```

For the axiom audit, from the repository root, use absolute repository and work
paths with the existing replay driver:

```powershell
$replayRoot = (Get-Location).Path
$replayWork = Join-Path $replayRoot '.lake/rename-replay'
python -I -X utf8 dag/research/lean_replay_campaign/replay_campaign.py run --repo $replayRoot --plan dag/research/genesis_rename_compatibility_plan.json --work $replayWork --only Imported.GenesisOngoing.Second.Rename --workers 1
```

The plan names every theorem declared in that port. The associated receipt is
`genesis_rename_compatibility_lean_replay.json`; it binds committed LF bytes,
records the signature comparison with the archived source, and includes an
explicit axiom audit. The comparison checks theorem headers after removing
comments and normalising whitespace; it does not prove compiler equivalence.

The archived file under
`atlas/papers/finite_obstruction_calculus/genesis_ongoing/lean4/Second/Rename.lean`
remains immutable. Its recorded direct-build failure remains historical evidence;
that file is not the maintained compatibility entry point. The campaign's separate
`CampaignGenesisOngoingRename` port and its existing receipts are also retained.
The two ports use distinct dependency module paths and must be audited in separate
Lean environments rather than imported together.

No theorem statement, DAG status, derivation note, source archive or scope fence
changes in this repair. In particular, a writing attaining the upper bound remains
existential, the lower bound still quantifies over every writing, and the tracked
obstruction lemmas retain their stated hypotheses. This replay adds no claim about
the complete Genesis runtime, demand-policy necessity or global process initiality.
