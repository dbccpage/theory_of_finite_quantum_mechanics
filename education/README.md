# Education reference import

AuthorityEffect: None.

This directory is a byte-preserved **reference import**, not a standalone
education application, a newly verified implementation, or an active QM build
target. The maintainer approved this reference-only disposition on 2026-10-26.
The source material's historical status labels and commands are retained as
source text, not adopted as claims about this checkout.

## Provenance and inventory

The six folders were copied from
a private upstream repository at commit 2ce57b4f06ff670e4b2bf673b6790effbd9575c8.
All 1,033 imported file paths and modes match that source. The Git blob identities match too,
except for one file whose links into the private upstream were replaced by plain citations on
2026-10-26 (listed under `post_import_edits`).
[IMPORT_PROVENANCE.json](IMPORT_PROVENANCE.json) records the exact source,
directory tree identities, counts and deterministic inventory digest.

| Reference folder | Imported files |
| --- | ---: |
| [000_oepregen](000_oepregen/README.md) | 26 |
| [001_oegen](001_oegen/README.md) | 158 |
| [002_oesn](002_oesn/README.md) | 97 |
| [003_oemssn](003_oemssn/README.md) | 346 |
| [005_oegenong](005_oegenong/README.md) | 77 |
| [006_oewdp](006_oewdp/README.md) | 329 |

This destination import does not establish that the upstream files were deleted,
that ownership transferred, or that all included mathematics or code is correct.
Only this wrapper and its provenance manifest are new editorial material.

## Dependencies and replay limits

The folders retain executable source as well as prose: Python, Lean, Rust, SQL
and notebooks. None was executed or built for this migration review. Old test
receipts remain historical evidence at their recorded source and environment;
they are not fresh QM test results. The five included Lean toolchain files all
declare Lean 4.35.0, which is not a claim that those packages were rebuilt here.

Upstream reproduction commands still use `omega_engine_education/documentation`.
Several checkers retain the old directory-depth assumptions and depend on the
shared PFP grammar owner,
which was not imported. For example,
[check_genesis.py](001_oegen/code/check_genesis.py) still searches the old grammar
locations. The
[Genesis Ongoing pin checker](005_oegenong/code/check_h3_pin.py) still targets the
old `omega_engine_atlas` layout. Running these files from QM is not supported by
this reference import.

For historical replay, use a separate, complete upstream checkout at the exact
source commit above, follow its
upstream documentation,
and supply each documented external source/environment dependency there.
Changing only the working directory in QM does not restore the old context.
No dependency installation, successful replay or upstream deletion is asserted.

Links were intentionally preserved. A simple inline-link existence scan found
235 source-resolvable relative-link occurrences that no longer resolve here;
722 other misses were already unresolved at the source pin. These are a
heuristic migration census, not a complete Markdown or semantic-link audit.
Use the pinned upstream context when a retained link leaves these six folders.

## Authority and integration boundary

The existing QM source populations, tests and CI configuration were not changed
to register this reference corpus. A passing QM check does not imply these
educational examples were checked. No new gate or global axiom restriction is
introduced: any Genesis-local `Classical.choice` restriction remains local to
its original audit and does not become QM policy.

Making this corpus standalone would be a separate, explicitly scoped migration:
resolve dependency ownership and paths, update live instructions, and obtain
source-bound replay evidence without rewriting historical receipts. This import
does not claim that work is complete.
