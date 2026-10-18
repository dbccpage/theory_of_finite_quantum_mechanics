# MUB6 publication preparation review

Date: 2026-10-16. Candidate: 1.1.1.
Source baseline: `2d03b504106356593d76f5a6bafc259019d52247`.
Disposition: prepared preprint candidate; publication approval outstanding.
No external upload, DOI reservation or publication was performed.

## Delivered changes

All twelve files formerly in `papers/` now reside at the package root.
The canonical manuscript and renders are `mub6.md`, `mub6.tex` and `mub6.pdf`.
Maintained package references and the active paper-DAG locations were updated;
historical `source_reported` paths retain their original snapshot meaning.

The manuscript has the canonical four-line header, explicit limits on external
formal reports, a mechanism inventory instead of a raw claim-ledger table,
persistent bibliography links and corrected historical archive counts.
The public preprint contains 19 files. Its description, keywords, references,
reproduction guide, metadata, full licenses and source-bound renders are included.
Research ledgers, prompts, receipts, historical archives and incomplete Lean
exports remain outside this curated preprint. The research checkout retains them.

`mub6_publication.zip` SHA-256:
`0d88612c02e574c425bfa7c94fa366b3c105b4472e972764210042aa259ba338`.
The `.zip.sha256` sidecar binds the archive; the extracted root has both
`MANIFEST.sha256` and `SHA256SUMS` with exact membership and digest checks.

## Validation performed

| Check | Observed result and limit |
| --- | --- |
| Deposit tests | 119 passed, 0 failures, 0 errors, 0 skips; Python 3.12.14, pytest 9.1.1; final JUnit output in excluded scratch storage |
| Negative controls | Unmanifested file, mutated PDF, resealed stale render, metadata disagreement, malformed related identifier, false publication promotion and altered ZIP member, prepended/appended archive bytes, same-byte control symlinks and unreadable directory traversal all refused |
| Manuscript header | Strict repository schema accepted the current source; schema runtime Python 3.13.11, Pydantic 2.13.5 |
| Render | Pandoc 3.7.0.2, MiKTeX-XeTeX 4.16 / MiKTeX 25.12; three passes; 15 pages; 0 missing glyphs; 0 horizontal boxes exceeding 10 points |
| Visual review | Layout checked across a 15-page contact sheet, with full-size first/last page inspection; not a symbol-by-symbol proof audit |
| Archive | All 19 members match the staged tree and sidecar; current loose manuscript, TeX, PDF and metadata match their extracted members |
| Isolation | Extracted package verifier passed under Python isolated mode, with no ambient monorepo imports |
| Maintained research tree | Both outer manifests and the read-only integrity sweep pass; nested preprint manifests are themselves checksum-bound payload |
| Determinism | Repeated packaging of the frozen payload gives identical ZIP bytes; regenerating the PDF is a separate operation |
| Historical archive | Git baseline and current tarball are byte-identical; 493 historical files and 496 surrounding manifest entries |
| Exact minor constants | Rational averaging gives 216/20 = 54/5; cofactor bound gives 4/(54/5) = 10/27; this arithmetic is not a substitute for the matrix theorem |

The historical archive digest remains
`461da04389d2b28ab2a73419822211bc86e66cded046bd8a91a7f5d7c3f41d93`.
Its regression test now checks historical member bytes against the historical
manifest, while current-envelope files and the maintained tree have separate
checks. This repairs the former requirement that an archived gap registry equal
its newer working copy. No historical member or digest was rewritten.

The outer research-envelope walker and verifier now exclude only their own root
manifests from circular checks. Nested `MANIFEST.sha256` and `SHA256SUMS` files
are included as payload. A regression test changes a nested manifest and confirms
that the outer verification rejects the altered bytes.

The source count is 185 Lean files and 180 root imports at the baseline.
Neither a current complete Lean build/census nor the native Rust suite was run
as part of this publication preparation. The deposited PDF does not claim those
runs. Test dependencies were read from the existing environment; they are not
bundled in the manuscript-only archive. Lint/type gates were not certified.

## Literature and claim review

Bibliographic identities were checked against the cited arXiv pages and the
[published Matolcsi et al. article](https://link.springer.com/article/10.1007/s10801-026-01506-x).
Its Conjecture 3 concerns Szöllősi-family quartet nonextension; Proposition 4.2
depends on both conjectures. The manuscript preserves that distinction and the
separate concrete Fourier-landing obligation. The classification citation
concerns single Hadamard matrices, rather than exclusion of every quartet.

The [Zenodo metadata documentation](https://developers.zenodo.org/#depositions)
was used for the local preprint metadata. No remote metadata validation occurred.
No concept DOI was invented; an existing record must be identified before adding
an `isVersionOf` relation. A search also surfaced a recent claimed Szöllősi result
at [Zenodo record 23051062](https://zenodo.org/records/23051062), but its primary
record could not be retrieved. Its authorship and argument remain unverified;
it was not used to close an obligation or added to the scholarly bibliography.

## Outstanding publication requirements

The repository's 52-check republication gate on the final preprint snapshot
reports BLOCKED: 12 PASS, 6 NOT_APPLICABLE, 9 FAIL and 25 NOT_VERIFIED.
The byte manifests pass that gate. Its remaining requirements include semantic
review evidence, current theorem replay and axiom census, test/coverage evidence,
DOI lineage where applicable, and author authorization.

Several failures also reflect the template's expectation of a bundled Lean
project, tests under `code/tests/`, and claim ledgers. This preprint is explicitly
a manuscript package referencing external research. The governance skill retires
claim ledgers, while the current 52-check implementation still requests one.
No ledger or placeholder proof project was added to manufacture a passing gate.

Before release, the author must approve this limited checkpoint scope and resolve
the formal-evidence requirements or choose an explicitly accepted manuscript-only
review profile. The Route C landing, full analytic family/cusp exclusion and
moment/empty-variety obligations remain open research, not packaging fixes.
This review does not establish a dimension-wide MUB bound.
