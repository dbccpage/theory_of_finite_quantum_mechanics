# Education reference import

AuthorityEffect: None.

This directory is a **reference import**, not a standalone
education application, a newly verified implementation, or an active QM build
target. The maintainer approved this reference-only disposition on 2026-10-26.
The source material's historical status labels and commands are retained as
source text, not adopted as claims about this checkout.

## Provenance and inventory

The six folders were copied from
a private upstream repository at commit 2ce57b4f06ff670e4b2bf673b6790effbd9575c8.
At import (commit `92a639ddc`) all 1,033 file paths, Git blob identities and modes matched
that source. On 2026-10-26 the folders were renamed to descriptive names, links into the
private upstream were removed, and references were updated to the renamed folders and to the
in-repo copies under `atlas/`. That edit changed 379 files.
[IMPORT_PROVENANCE.json](IMPORT_PROVENANCE.json) records the exact source, the directory tree
identities, counts and inventory digest at import, and under `post_import_edits` the folder
renames and each edited file with its original and current sha256.

| Reference folder | Imported files |
| --- | ---: |
| [pregenesis_empty_mark](pregenesis_empty_mark/README.md) | 26 |
| [genesis_primitives](genesis_primitives/README.md) | 158 |
| [symmetric_group_presentations](symmetric_group_presentations/README.md) | 97 |
| [minimal_symbol_systems](minimal_symbol_systems/README.md) | 346 |
| [genesis_reading_notes](genesis_reading_notes/README.md) | 77 |
| [witnessed_difference_programme](witnessed_difference_programme/README.md) | 329 |

This destination import does not establish that the upstream files were deleted,
that ownership transferred, or that all included mathematics or code is correct.
Apart from the edits recorded under `post_import_edits`, only this wrapper and its provenance manifest are new editorial material.

## Dependencies and replay limits

The folders retain executable source as well as prose: Python, Lean, Rust, SQL
and notebooks. None was executed or built for this migration review. Old test
receipts remain historical evidence at their recorded source and environment;
they are not fresh QM test results. The five included Lean toolchain files all
declare Lean 4.35.0, which is not a claim that those packages were rebuilt here.

Upstream reproduction commands still use the upstream folder layout.
Several checkers retain the old directory-depth assumptions and depend on the
shared PFP grammar owner,
which was not imported. For example,
[check_genesis.py](genesis_primitives/code/check_genesis.py) still searches the old grammar
locations. The
[Genesis Ongoing pin checker](genesis_reading_notes/code/check_h3_pin.py) still targets the
old upstream atlas layout. Running these files from QM is not supported by
this reference import.

For historical replay, use a separate, complete upstream checkout at the exact
source commit above, follow its
upstream documentation,
and supply each documented external source/environment dependency there.
Changing only the working directory in QM does not restore the old context.
No dependency installation, successful replay or upstream deletion is asserted.

Relative links inside the folders were preserved, apart from the renames above. A simple inline-link existence scan found
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
