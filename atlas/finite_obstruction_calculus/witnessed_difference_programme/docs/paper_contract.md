# Literal research-paper contract

The contract preserves and inventories the current Witnessed Difference Programme;
it does not rewrite, summarize, or promote its mathematics. `ResearchPaper` is a
strict Pydantic v2 model with frozen objects, tuple collections, forbidden extra
fields, validated source spans, and exact source/hash bindings.

## What is modeled

| Surface | Model and information |
| --- | --- |
| Manuscript | `PaperDocument`: every character belongs to one ordered literal block; UTF-8 byte count and SHA-256 bind the whole document. |
| Sections and subsections | `Section` and `HeadingBlock`: literal heading, heading level, printed number where present, parent/children, ordered direct blocks, and full source span. |
| Prose and source syntax | `ProseBlock`, `MathBlock`, `CodeBlock`, `TableBlock`, `MarkupBlock`: exact raw source, SHA-256, and half-open Unicode character offsets with one-based lines. Markdown table rows also have literal cells. |
| Mathematics | `Equation`: exact delimited source and TeX payload, inline/display mode, source location, section, explicit `label`/`tag` values. Unnumbered expressions receive section-scoped occurrence IDs; these are index IDs, not invented equation numbers. |
| Metadata | `MetadataField`: literal bold metadata names/values and their locations, including author, date, version, and license. |
| Claim references | `ClaimOccurrence`: every recognized literal ID occurrence, including lookup IDs inside inline code. A reference or range endpoint is not a new claim declaration. |
| Authoritative claims | `ClaimLedger`/`ClaimRecord`: the 154 canonical rows and nine R12/R13 supplement rows, kept in separate registers, with exact status, statement, evidence, and canonical-location cells. |
| Implementation bindings | `ClaimCodeMap`/`ClaimCodeBinding`: the exact current JSON plus its 87 typed module/test bindings. Paths must exist and statuses must match the canonical ledger. |
| Links and anchors | `TextReference`: literal Markdown links, HTML anchors, and reference definitions with locations. Canonical ledger anchors are checked against manuscript anchors. |
| Folder/file inventory | Named folder components, every recursive directory, and every regular file's path, size, Git blob identity, and mode. Unknown top-level folders are retained explicitly as `additional_folders`. |
| Change review | `PaperBaseline`, `Fingerprint`, `AuditReport`, `Change`: file/directory, document, section, equation, claim status/statement/evidence, metadata, and link drift. The whole-document digest catches changes to any remaining syntax. |

`ResearchPaper` uses composition: a code folder is a component of a paper, not a
subclass of a paper. Folder subclasses constrain their literal paths:

| Property | Type | Required |
| --- | --- | --- |
| `code` | `CodeFolder` | yes |
| `code.tests` | `TestsFolder`, path `code/tests` | yes |
| `docs` | `DocsFolder` | yes |
| `lean4` | `Lean4Folder` | yes |
| `scripts` | `ScriptsFolder` | yes |
| `evidence` | `EvidenceFolder` | no |
| `jupyter_notebooks` | `JupyterNotebooksFolder` | no |
| `images` | `ImagesFolder` | no |
| `manifests` | `ManifestsFolder` | no |

The prose hierarchy follows the literal Markdown heading levels, including the
embedded supplements' top-level headings. It does not invent a logical hierarchy
that contradicts those printed headings. Other ledger tables, historical rows,
and GEN-WDP references remain fully preserved and indexed; they are not silently
promoted into the canonical 154-row register. Future authoritative registers need
their own explicit schema/parser before receiving typed status credit.

This is a conservative source index rather than a full CommonMark renderer or
TeX interpreter. Delimited `$…$`, `$$…$$`, `\(…\)`, and `\[…\]` mathematics is
indexed. Undelimited Unicode formulas, complex TeX table layout, and unsupported
syntax remain literal source blocks. An unclosed supported delimiter is retained
and reported; baseline creation/checking refuses parser diagnostics. Structural
validation and fingerprints do not establish mathematical correctness.

## Exact Python used for the results

- `code/paper_contract/models.py`: all Pydantic types and cross-field validation.
- `code/paper_contract/parser.py`: literal extraction and claim-register parsing.
- `code/paper_contract/inventory.py`: pinned-tree and live-worktree ingestion.
- `code/paper_contract/audit.py`: fingerprints, integrity checks, and change reports.
- `scripts/build_paper_contract_snapshot.py`: the exact result generator, including
  complete typed JSON round-trip verification.
- `scripts/check_paper_contract.py`: inspection, schema, snapshot, baseline, and check CLI.
- `code/tests/python/unit_tests/test_paper_contract.py`: actual-paper and adversarial tests.

Install from this paper directory with `python -m pip install -e '.[contract]'`,
or use the updated lock: `uv sync --locked --extra dev --extra contract`.
The contract dependency is optional for the existing finite witness package and
included in the dev extra so the new tests also work in the paper's usual suite.

```bash
python scripts/check_paper_contract.py inspect
python scripts/check_paper_contract.py schema --output /tmp/research_paper.schema.json
python scripts/check_paper_contract.py snapshot --output /tmp/research_paper.literal.json
python -m pytest code/tests/python/unit_tests/test_paper_contract.py -o addopts='' -p no:cacheprovider
```

The live scanner hashes working bytes of tracked files plus untracked nonignored
additions. Missing tracked files, unresolved
merges, symlinks, submodules, duplicate paths, and path escapes are refused.
Ignored build outputs are outside this intentional Git inventory.

For the pinned source inputs used to produce the initial results, place the raw
manuscript, raw claim ledger, `claim_code_map.json`, and `github_tree.json` in a
source directory. The tree object has `commit`, repository-relative paper `root`,
and complete paper-relative Git tree `entries` (`path`, `type`, `mode`, and blob
`sha`/`size`). Then run the exact supplied generator:

```bash
python scripts/build_paper_contract_snapshot.py --source SOURCE_DIR --output-directory RESULTS_DIR
```

The initial manuscript input is pinned to commit
`cd003a2fa195f399947de98940a678930559ed0d`, version 2.2.1. Its extraction has
409 headings, 4,747 delimited math expressions, 154 canonical rows, nine R12/R13
supplement rows, 79 executable bindings, and 1,661 original tracked files. The
contract implementation adds files to the final repository inventory; it does
not change those manuscript counts.

## Trusted baseline and review boundary

The baseline is a compact fingerprint index. A full literal JSON snapshot is
generated on demand rather than committing another complete copy of the prose.
The retained `manifests/paper_contract.baseline.json` names source commit
`dc736524af4d273fa5d15aa4f2e548b6f7a99ed5`; it is a prior trusted comparison
snapshot, not the current-edition claim register. The live ledger is
`witnessed_difference_programme_claim_ledger.md`. Use `inspect` or `snapshot`
above to read its current statements. The 2.4.3 editorial synchronization does
not silently adopt a replacement trusted baseline.
Only `manifests/paper_contract.baseline.json` is excluded from its own file hash
inventory because its own hash would be self-referential. The checker separately
requires the candidate baseline's bytes to equal the independently trusted copy.

Obtain that trusted copy from a reviewed base commit, not from the proposed
change. Run the checker/model code from that same base commit. This prevents a
proposal from changing both the paper and its validator to approve itself.

```bash
git show BASE_COMMIT:PAPER_ROOT/manifests/paper_contract.baseline.json > /tmp/trusted-paper-baseline.json
python BASE_CHECKOUT/PAPER_ROOT/scripts/check_paper_contract.py check \
  --paper-root HEAD_CHECKOUT/PAPER_ROOT \
  --trusted-baseline /tmp/trusted-paper-baseline.json \
  --output /tmp/paper-changes.json
```

`check` returns 0 for an exact match, 1 for drift/integrity issues, and 2 for
invalid input or a refused scan. `baseline` requires an explicit output path and
does not confer approval. `model_copy(update=...)` bypasses validation in Pydantic;
external input must pass `model_validate_json`, as the supplied CLIs do.

The companion GitHub workflow runs the checker and baseline from the PR base.
Its first installation is explicitly a bootstrap: there is no prior baseline
to trust, so the initial baseline requires owner review. Later paper changes
fail the strict lock check even if they regenerate a local baseline. An intended
change therefore requires an owner-reviewed diff and an explicit maintainer
override/baseline adoption; there is no automatic self-approval mechanism.

To make this a merge barrier, repository administration must require the
`contract` job of `WDP paper contract`, require CODEOWNER review, dismiss stale
approvals, and prevent unreviewed edits to the workflow/owners/contract files.
The PR provides the ownership rules and workflow; creating it does not enable
those administrative settings. `AuthorityEffect: None` remains literal throughout.
