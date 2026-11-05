# Source archive

These 44 files reproduce the original input snapshot in `source_provenance.json`,
byte for byte. They were recovered on 2026-10-01 from Jeremy H. Carroll's
[CODA repository](https://github.com/dbccpage/CODA) at commit
`adce498821aae1d5168bf40d8ec9c97c02401840`. The recorded snapshot contains
1,967,435 bytes; its aggregate SHA-256 is
`ef19a585f6bb5c95794e3edfc7348e3ae1535bf613b9a0aa8f9f6e54a7f9d383`.

`coda_original_source_snapshot/<sha256>.txt` retains each source's exact UTF-8 bytes, including
its existing attribution and notices. The corresponding original path, byte
count and SHA-256 remain in `source_provenance.json`; recovery URLs and Git blob
identifiers appear in `docs/legacy_observer_inventory.json`. These files are
historical inputs, not additional editions of the canonical WDP monograph.
Their original claim statuses remain part of that historical evidence.

Run `python scripts/verify_observer_source_archive.py` to check all original
bytes without network access. To replay the separately recorded 529 absorbed
source blobs, run `python scripts/verify_source_provenance.py --absorbed-repo
/path/to/the_symbol_game`. Source custody establishes which text was reviewed;
the adapter proofs and executable countermodels establish its mathematical
interpretation.

## Retired WDP research inputs

`toric_code_chapter_23_import.md` is the standalone imported Chapter 23 draft.
Its mathematical content was integrated into canonical Chapter 23 with a
correction fence; this retained copy is provenance, not an additional theorem
source. `meron_model_generation_history/` retains the raw prompts, provider
responses and provider runner used during Meron research. They preserve
generation provenance and do not inherit theorem status from model output.

The other dated subdirectories retain source bytes behind their named review
or correction records. Active Meron derivations live separately in
`docs/meron_field_limit_derivations/`.
