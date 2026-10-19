# MUB(6): exact reductions, conditional interfaces and open gaps

**AuthorityEffect:** None.

> **Status:** incomplete. Whether seven mutually unbiased bases exist in
> dimension six is open. This deposit does not settle it. Gap G1 is OPEN in
> [the gap registry](research/mub6_gap_registry.json). The current scope is in
> [the paper](mub6.md) and [the claim ledger](mub6_claim_ledger.md).
> Some historical research files state stronger results; those statements are
> withdrawn in [the superseded notice](research/superseded_notice.md).

---

## 1. Summary

This deposit holds the manuscript, exact-arithmetic verifiers, receipts and
historical research records for a study of mutually unbiased bases (MUBs) in
dimension $d=6$. The Lean 4 sources it cites live in the source monorepo at
`lean4/research_programs/mub6/`. At the pinned source snapshot that directory holds
185 `.lean` files; the root module `Mub6.lean` imports 180 of them. Only three Lean export and audit
files are copied into this deposit under `lean4/`.

The checked results are exact reductions, finite computations and conditional
Lean theorems. Section 8 of the paper lists each claim with its evidence and
status.

## 2. Claim discipline

1. Every claim is scoped to the stated region, orbit, chart or premise.
2. Computational certifiers use exact rational ($\mathbb{Q}$) or cyclotomic
   ($\mathbb{Q}(\zeta_{24})$) arithmetic. Floating-point values are not
   accepted as certificates.
3. Conditional Lean theorems (for example `no_complete_mub6_via_route_c`) take
   their premises as hypotheses. They do not discharge those premises.
4. Files produced with LLM proposers (`code/mub_verify/openrouter_proposer.py`,
   `code/mub_verify/a2_llm_proposer.py`, the `*superbunny*` scripts and
   receipts) are exploratory records, not evidence. See
   [the provenance note](documentation/mub6_provenance_and_bridge_coverage.md).

## 3. Historical campaigns

Campaigns 1 to 8 are historical records. Their milestone names do not state
current results. The paper and the gap registry replace them.

## 4. Repository structure

```
010_mub6/
├── README.md                    # This document
├── agents.md                    # Agent rules for this deposit
├── LICENSE                      # CC-BY-4.0 (manuscript and documentation)
├── LICENSE-CODE                 # Apache License 2.0 (software)
├── mub6_global_proof_atlas.md   # Evidence index with status per surface
├── completion_supplement.md     # Historical replay notes (2026-09-25)
├── verify_deposit.py            # Deposit integrity verifier
├── mub6.md / mub6.tex / mub6.pdf # Canonical manuscript and synchronized renders
├── mub6_change_log.md            # Version history
├── mub6_claim_ledger.*           # Retained research indexes; excluded from preprint
├── research/                    # Gap registry, roadmap, historical records,
│                                # superseded_notice.md
├── artifacts/                   # Receipts and receipt manifest
├── code/mub_verify/             # Python research verifiers
├── scripts/                     # Receipt generators, release builder
├── lean4/                       # Three Lean export/audit files
├── rust/                        # Two Rust source files
├── tests/                       # Deposit pytest suite
└── zenodo/                      # Historical archive v1.0 and its manifests
```

## 5. Verification

From this directory:

```pwsh
py -3.12 verify_deposit.py --integrity-only
py -3.12 -m pytest tests -q -p no:cacheprovider
```

`verify_deposit.py` exits 0 on pass and 1 on any failure. It checks the paper
header with a schema kit from the source monorepo. Outside the monorepo, add
`--skip-header-schema`; the skip is printed as `SKIPPED`.

The Lean build and the Rust `omega_mub` tests need the source monorepo:

```pwsh
py -3.12 verify_deposit.py --integrity-only --lean --lean-root <monorepo>/lean4
cargo test -j 1 -p omega_mub --manifest-path <monorepo>/omega_engine/crates_rs/Cargo.toml
```

## 6. License

| Material | License |
| --- | --- |
| Manuscript text (`mub6.md` and its renders) | CC-BY-4.0 |
| Code, scripts and tests | Apache-2.0 (see `LICENSE-CODE`) |

## Publication candidate 1.1.1

All former `papers/` files are at this package root. The canonical manuscript
is [mub6.md](mub6.md), dated 2026-10-16, version 1.1.1. The public preprint is
`mub6_publication.zip` with `mub6_publication.zip.sha256`. Its staged contents
are under `zenodo/preprint/`; research ledgers, prompts, historical archives,
receipts and incomplete Lean export files are excluded from this preprint.

Run `python scripts/build_pdf.py`, then
`python scripts/build_publication_release.py` from this directory.
Use `python scripts/verify_publication.py --root zenodo/preprint --archive mub6_publication.zip`
for read-only verification. The whole research-tree check remains
`python verify_deposit.py --integrity-only` and is a different check.

The candidate metadata is [zenodo_metadata.json](zenodo_metadata.json).
Read [the description](docs/descriptions.md), [quick start](docs/quick_start.md)
and [release identity](release_identity.json). This is a prepared candidate:
complete formal replay and author review remain outstanding. No external
deposit, reserved DOI or published record is claimed.

Manuscript and documentation are CC-BY-4.0 (`LICENSE`); software and historical
data/receipt assets retain Apache-2.0 (`LICENSE-CODE`). Original third-party
attribution and licensing remain applicable to historical source materials.
