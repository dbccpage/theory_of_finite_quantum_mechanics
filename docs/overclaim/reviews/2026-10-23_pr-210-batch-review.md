# Independent review and importer repair: PR #210

AuthorityEffect: None. AI-assisted review, with no human attestation.

The importer trusted an earlier plan's `verified` label but reread the source without comparing it with the plan's SHA-256 or length. If a source changed between planning and import, `import_sources.py` copied new bytes while PROVENANCE.json continued to identify the old bytes. Existing twins were also accepted without checking for drift.

The repair validates all rows before writing, copies the captured validated bytes, rechecks existing twins under the declared equality relation, and records the actual twin digest separately when line endings differ. It refuses stale sources, malformed hashes/sizes, duplicate identities, escaping paths and copy/twin destination collisions. Copy verification remains active under optimized Python. Bulk filesystem writes are still not transactional under an operating-system error; that limitation is recorded in the score.

Validation: 26 isolated CLI regressions pass, including both ordinary and optimized Python. All 129 committed provenance entries were independently compared with their individually named original source files: 107 copies and 22 resolved twins. The repaired importer also passes a dry run of the reconstructed full plan. No source archive was modified. Raw commands and digest comparisons are in `dag/research/atlas_sources_import/review_validation.json`.

**Not ready to merge.** The change includes 79 code artifacts after adding the regression suite, of which 77 lack companions. The bounded procedural importer is assessed L3D, below the required substantive L4 floor; the regression suite is L2D under the approved support-file exception. No artificial capability promotion or archive-wide grade is supplied.

The overclaim scan reports HIGH=4, MEDIUM=0, LOW=117, with no new HIGH finding beyond the existing baseline. The four HIGH R1 entries refer to the pre-existing external omega_engine_education dependencies, outside the seven imported F004 families. This is not a clean whole-PR mathematical review: the newly local source editions have not all been replayed and compared with every cited declaration. A copied source, even with verified provenance, does not itself establish the full statement of a PROVED_LEAN node. The full declaration/edition audit and its required companions remain outstanding. The 117 LOW numerical candidates are not claimed to have been recomputed by this importer review.
