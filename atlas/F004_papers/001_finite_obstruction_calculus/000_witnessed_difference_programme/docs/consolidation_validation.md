# Consolidation candidate: validation and remaining work

Date: 2026-10-05. AuthorityEffect: None.
Baseline: `1c522d55e2584fa964b8019f65a9590f90166ea7`.

The source map covers 774 original tracked assets. Its baseline replay passed;
694 assets retain their exact original bytes and one identical asset is
deduplicated. Amendments concern the relocated application and teaching links;
the CODA and Prime component archives preserve their original bytes.

Local checks run with Python 3.13.11:

- Eight focused custody tests passed, including wrong bytes, missing files,
  duplicate sources, path escape, same-byte symlink, nonregular entry, and
  an unexpectedly retained retired root.
- Seven relocated CODA pipeline/workspace tests passed, including a standalone
  copy's explicit Python-only result when no native workspace is present.
- Forty-seven CODA documentation/FOC adversarial tests passed.
- Five workbench catalog tests passed after the Prime source path change.
- Five new PFP drafts replayed 37 finite controls, with zero model calls.
- CODA, Prime, and pipeline-attestation governance scripts passed. Their path-only
  edits match across the four host copies.

Written proofs, abstract Lean models, and concrete replay remain separate.
Original Lean reports are retained; no fresh Lean or Rust compilation is claimed.

## Release boundary

The initial `scripts/verify_release.py --write` refused the imported historical
monograph, change-log and claim-ledger filenames because its canonical
publication surfaces must be singletons. The 23 original documents are now
explicit `.md.txt` source snapshots, with unchanged bytes and original names
bound in the custody map. Their original release ZIPs remain intact. The
unchanged verifier now accepts the source inventory. See the
[source index](coda_component_source_index.md).

An inventory/checksum match is not publication readiness. The rendered edition
and historical Lean reports retain their prior scopes; no fresh edition,
compiler run or publication is asserted by this consolidation.

## Active goal boundary

Source consolidation and §P.19 are reviewable. Papers 023–027 are unpublished
finite drafts with pinned context, two-level teaching packets and replay
receipts. Their model-internal experiments are unexecuted. The
[single seven-day campaign](../../plans/derivations_7day_plan.md)
now names the actual owners, priority targets, handoffs and acceptance criteria.
Completion of this consolidation request does not assert full finite WDP
completion, continuum reconstruction or publication readiness.

## Requested-deliverable audit

| Requirement | Delivered evidence |
| --- | --- |
| Remote-main baseline | `origin/main` is the pinned consolidation baseline and an ancestor of the feature branch. |
| Education 080 into 070 | CODA reading route, domains, levels and original 800/810 laboratory tracks live in course 070. The original root is a redirect. |
| F005 into WDP and retirement | The custody map covers all 596 tracked F005 assets. The source root is absent; Appendix P and the integration map identify the mathematical owners. |
| Education 130 into 070 | Prime reading route, domains, levels and original 1300/1310 laboratory tracks live in course 070. The original root is a redirect. |
| Prime atlas into WDP | Its 48 tracked assets are retained under the Prime source package; P.19 states the integrated finite obligations. The original root was a redirect; it was retired on 2026-10-06. |
| CODA application integration | Its 57 tracked assets are retained under `code/coda_application`, with repaired imports and explicit Python-only fallback. The original research root is absent. |
| Source review and five PFP papers | The paper-series source table records the requested findings, 021/022 and the four education strands. Drafts 023–027 contain proofs, five two-level teaching packets and 37 replay controls. |
| One seven-day plan | `plans/derivations_7day_plan.md` (formerly `ow/plans/codex_7day_plan.md`; the three supporting catalogs were merged into it on 2026-10-06) controls the five bounded derivation lanes. Three supporting catalogs retain all 52 fenced examples and link to existing current owners. |

The consolidation deliverables are complete for author review. Subsequent
execution of the seven-day campaign remains future work. Its planned native
builds and model episodes are not recorded here as completed evidence.
