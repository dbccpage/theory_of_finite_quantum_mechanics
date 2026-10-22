# Superseded research statements

**AuthorityEffect:** None.

The files listed below are kept unchanged. All but the synthesis note are
byte-pinned members of the historical archive
`zenodo/mub6_formal_archive_v1.0.tar.gz` (see `zenodo/release_manifest.sha256`),
so their digests still replay. Some of their status lines are withdrawn. Read [the paper](../mub6.md) and
[the gap registry](mub6_gap_registry.json) for the current scope.

## Withdrawn statements

| File | Lines | Withdrawn statement | Current scope |
| --- | --- | --- | --- |
| `research/mub6_frontier_synthesis.md` | 5, 7 | `NoCompleteMUB6` "unconditionally mechanized" or "unconditionally derived" via Route C. | `no_complete_mub6_via_route_c` takes the landing hypothesis `h_landing` as a premise (paper section 3, claim MUB6-C04). Gap G1 is OPEN. |
| `research/mub6.md` | 5, 91, 93, 97 | Complete MUB(6) "unconditionally resolved in the negative" via Route C. | The same Route C theorem is conditional (MUB6-C04, MUB6-C05). The existence of seven MUBs in dimension six is open. |
| `research/mub6_roadmap.md` | 4, 8, 214, 226 | `NoCompleteMUB6` "unconditionally established" or "unconditionally mechanized". | Same as above. The roadmap's Target C3 remains an open target, not a result. |
| `research/g1_foundation/g1_elimination_receipt.md` | 14 | Every 6×6 complex Hadamard matrix "routes to a certified moduli component with zero lost solutions". | `comprehensive_moduli_exhaustiveness` (`MasterClassification.lean:779`) concludes only that some component c in {szollosiDeltoid, karlssonVolume} exists; nothing links c to H. Gap G1 is OPEN. Added 2026-10-16. |
| `documentation/mub6_master_classification_and_openai_comparative_synthesis.md` | 132 | The Szöllősi branch is "Certified across 56 global cells". | Conjecture 3 is OPEN. The cell receipts do not exclude a quartet on the family (see [the 2026-10-16 review](mub6_review_and_next_derivation.md)). Added 2026-10-16. |

## What this notice does not do

- It does not change any archived byte or any digest.
- It does not re-seal the archive. A new archive version would have to drop or
  amend these files and be re-sealed with `scripts/build_zenodo_release.py`.

## Correction notes added in place (2026-10-21)

Each flagged line in `research/mub6.md` (5, 91, 93, 97 at the time), `research/mub6_roadmap.md` (4, 8, 214,
226) and `research/mub6_frontier_synthesis.md` (5, 7) is now followed by a dated correction note. The
original text was not changed or deleted. The digests of these three live files therefore differ from
their members in `zenodo/mub6_formal_archive_v1.0.tar.gz`; the archive members are unchanged and still
replay. The outer deposit manifests (`manifest.sha256`, `sha256sums`) were regenerated for the live files.
The comparison sections of `documentation/mub6_master_classification_and_openai_comparative_synthesis.md`
were rewritten on the same date because they misdescribed OpenAI's work.
