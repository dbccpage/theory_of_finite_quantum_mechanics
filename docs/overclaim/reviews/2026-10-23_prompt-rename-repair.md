# Review of prompt custody and Rename compatibility repair

AuthorityEffect: None. AI-drafted review, awaiting independent maintainer review.

Scope: tooling repair from `ff59f8fe712f4c8035069dca1b97521fb711d9ed`.
No node statement, status, bottleneck, derivation note or sealed artifact changes.
Integration base: `051091f7b6be583969482d323d4fac3e36b6ea8c`. The incoming
source-import and observer-stage changes are retained; protected paths are
compared with that base, not attributed to this repair.

Method: read the generator's planning/write boundaries, the structural validator,
the retained P0 histories and their delta artifacts, and the maintained Rename
port's provenance and theorem headers. Ran the changed-scope overclaim scanner,
campaign checks, custody tests, designated executable mutants and the existing
Lean replay driver. The source/port header comparison is textual after removing
comments and normalising whitespace; it is not a compiler-equivalence theorem.

Result: 0 nodes FULL, 0 NARROWED, 0 OVERCLAIM in this repair's node-change scope.
There is no node-change scope to adjudicate and no promotion. This review does
not re-certify all unchanged mathematical nodes.

## Statement versus evidence

| Claim | Evidence and boundary | Verdict |
|---|---|---|
| The curated P0 records can be retained without accepting their contents | `dag/pfp/generate_prompts.py:480` binds the generated audit, prompt, identity, input pins, retained bytes and delta evidence. The eight negative GTH records remain negative; TFQ-0084 remains pending host review. | Operational repair; no theorem claimed |
| An omitted index update cannot cause recorded P0 work to be overwritten | `dag/pfp/generate_prompts.py:208` also inspects stage history; the stale branch at `:520` remains protected. The contract tests exercise this case. | Operational repair; no theorem claimed |
| Quoted mathematical prose is distinct from a forced answer instruction | `dag/pfp/validate_prompts.py:22` excludes one exact source quote; `:122` checks the remaining instructions. Extra occurrences still trigger rejection. The validator remains structural and does not accept the source claim. | Operational repair; no theorem claimed |
| The maintained Rename port type-checks with the permitted axioms | `dag/research/genesis_rename_compatibility_lean_replay.json` records all 37 theorem audits and their unchanged headers. No Lean source is edited. | Compatibility evidence; unchanged theorem scopes |
| The complete Genesis runtime, necessary demand policy or global initiality follows | Not proved here. Existing node statements, scope fences and scoring exceptions are unchanged. | NOT PROVED |

## Corrections and custody

The archived direct-build failure is not converted into a passing receipt. The
maintained entry point is `Imported.GenesisOngoing.Second.Rename` in the existing
non-default `ImportedAtlas` library. Its reproducible plan and audit receipt are
added separately. The campaign compatibility port and historical failed-source
receipt remain intact. The remaining review obligations about complete Genesis
runtime refinement and whole-process comparison remain exactly as recorded.

The new Python companions are self-assessed L4D, awaiting maintainer review.
They do not alter or expand any existing support exception and do not claim an
independent score certification. Higher grades, global type coverage and complete
semantic mutation coverage are not claimed.

## Numbers recomputed

| Number | Recomputed evidence |
|---|---|
| 9 retained collections | Extension rows carrying explicit `retained_collection` bindings; their original files are preserved |
| 37 Rename theorem headers and audits | Signature comparison and complete cited-declaration audit in the compatibility replay receipt |
| 83 broader passing tests | Output in `prompt_retention_targeted_validation.json`; includes the original 23 retention cases |
| 30 final targeted passing cases | Same receipt; includes those 23 cases and the seven subsequent source-quote cases, so the counts overlap |
| 54 passing cases after integration | Final campaign receipt: prescribed campaign tests plus the final custody/classification suite |
| 8 designated mutants killed | `prompt_retention_challenges.json`, with all outcomes recorded; no survivor, invalid, equivalent, inconclusive or unrun candidate in that declared set |

## What the scanner cannot decide

The mechanical scan does not certify P0 semantics, human review, full node
statements or equivalence between source code and compiled programs. The maintained
port's existing quantifiers and hypotheses still govern its conclusions: the
attaining writing is existential, the lower bound quantifies over every writing,
and tracked-obstruction results retain their stated conditions. No broader claim
is inferred from a successful compile or repeated-run agreement.
