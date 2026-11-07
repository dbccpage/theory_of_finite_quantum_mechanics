# Education reference import

AuthorityEffect: None.

This directory is a **reference import**, not a standalone
education application, a newly verified implementation, or an active QM build
target. The maintainer approved this reference-only disposition on 2026-10-26.
The source material's historical status labels and commands are retained as
source text, not adopted as claims about this checkout.

## Provenance and inventory

The six imported folders were copied from
a private upstream repository at commit 2ce57b4f06ff670e4b2bf673b6790effbd9575c8.
At import (commit `92a639ddc`) all 1,033 file paths, Git blob identities and modes matched
that source. On 2026-10-26 the folders were renamed to descriptive names, links into the
private upstream were removed, and references were updated to the renamed folders and to the
in-repo copies under `atlas/`. That edit changed 379 files.
[IMPORT_PROVENANCE.json](IMPORT_PROVENANCE.json) records the exact source, the directory tree
identities, counts and inventory digest at import, and under `post_import_edits` the folder
renames and each edited file with its original and current sha256.

Since 2026-11-06 the folders carry numbered prefixes in reading order: Pre-Genesis, S(n),
MSS-N, Genesis, then the Witnessed Difference Programme. The two Genesis folders that were under
`research/` (6 and 7) moved here at the same time; they were written in this repository and are
not part of the import.

| Folder | Stage | Tracked files |
| --- | --- | ---: |
| [1_pregenesis_empty_mark](1_pregenesis_empty_mark/README.md) | Pre-Genesis | 22 imported |
| [2_symmetric_group_presentations](2_symmetric_group_presentations/README.md) | S(n) | 96 imported |
| [3_minimal_symbol_systems](3_minimal_symbol_systems/README.md) | MSS-N | 333 imported |
| [4_genesis_primitives](4_genesis_primitives/README.md) | Genesis | 156 imported |
| [5_genesis_reading_notes](5_genesis_reading_notes/README.md) | Genesis | 65 imported |
| [6_genesis_foundations](6_genesis_foundations/this_repo.md) | Genesis | 3, written here |
| [7_genesis_language](7_genesis_language/SPEC.md) | Genesis | 1, written here |
| [8_witnessed_difference_programme](8_witnessed_difference_programme/README.md) | WDP | 306 imported |
| [999_external_publications_general_media](999_external_publications_general_media/) | outside publications | 21 imported |
| [problem_sets](problem_sets/problems/undergraduate_qm_25.yaml) | undergraduate problem set | 46, written here |
| [hamilton_noether_sources](hamilton_noether_sources/start_here.md) | Hamilton-Noether teaching pack | 43, written here |

The imported counts are the files tracked today; the import manifest records what was copied and
`post_import_edits` records every later edit or removal. The problem set and the teaching pack were
written in this repository and moved here from the root and from `dag/derivations`.

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
[check_genesis.py](4_genesis_primitives/code/check_genesis.py) still searches the old grammar
locations. The
[Genesis Ongoing pin checker](5_genesis_reading_notes/code/check_h3_pin.py) still targets the
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
