# PDF build receipt — 2026-10-02

Scope: unpublished repository draft following canonical v6.1.1. This records
typesetting and byte custody only; it assigns no version or mathematical status.

## Current build

- Command: `python scripts/render_paper.py`.
- Toolchain: Pandoc 3.1.3; XeTeX / XeLaTeX, TeX Live 2023/Debian.
- Fonts: packaged Latin Modern resources; deposited preamble and inline-code filter.
- Deterministic timestamp: `SOURCE_DATE_EPOCH=1790899200`.
- Result: two XeLaTeX passes, exit 0; no overfull boxes or missing-character warnings.
- Pages: 26.
- Verification: Poppler/pypdf metadata and text extraction; all pages rendered
  for visual inspection. Confirmed canonical DOI, draft date, open-status text,
  and all five counterexample headings.

## Current source and output SHA-256

| Artifact | SHA-256 |
|---|---|
| `coordinate_wise_additivity.md` | `52b3a55d4b07d03d4e4887097cd4e13796f95f4f6b06859b018c0a61ad9d03de` |
| `coordinate_wise_additivity.tex` | `ffe6fd3ea6efdbc7a6a4359e2c4968fbfd79f2b5daaab5ec37c995c7bea5ac57` |
| `coordinate_wise_additivity.pdf` | `936631a367e0efb120a3578676bc443946781051783de358aeb3f3edc2b40381` |

## Historical receipt retained below

The following receipt belongs to the earlier source/output snapshot. Its
digests do not describe the current checked-in PDF.

---

# Historical PDF build receipt — 2026-09-28

Date: 2026-09-28

Scope: unpublished repository draft following the canonical v6.1.1 publication.
This receipt attests only that the checked-in manuscript source produced the
checked-in PDF under the toolchain below. It does not change publication or DOI
status and is not evidence for any mathematical claim.

## Compiler custody

- Compiler: Tectonic 0.17.0
- Upstream repository: `tectonic-typesetting/tectonic`
- Release tag: `tectonic@0.17.0`
- Asset: `tectonic-0.17.0-x86_64-pc-windows-msvc.zip`
- Asset SHA-256:
  `f61ce51f0b0ade1015b7de7ef368541c5424e9756ecbd0d7af97d6d48030845f`
- Retrieval command:
  `gh release download tectonic@0.17.0 --repo tectonic-typesetting/tectonic --pattern tectonic-0.17.0-x86_64-pc-windows-msvc.zip --dir C:\wt\tectonic017`

The executable was extracted into the temporary directory
`C:\wt\tectonic017\bin`; it was not installed into the repository or system.

## Build

The source was copied unchanged to the short Windows scratch directory
`C:\wt\p009l` before compilation. The repository source selects Latin Modern
resources by TeX Live filename so Tectonic's bundle and an installed XeTeX
distribution resolve the same fonts.

Command:

```text
C:\wt\tectonic017\bin\tectonic.exe C:\wt\p009l\coordinate_wise_additivity.tex --outdir C:\wt\p009l --keep-logs --print
```

Result: exit 0. Tectonic completed its rerun and `xdvipdfmx` pass and produced
a 19-page PDF. The log contains non-fatal monospaced-font shape substitutions
and a replacement warning for one invalid UTF-8 byte in the bundled
`lineno.sty`; no manuscript content was omitted and the output was written
successfully.

## Output verification

- PDF SHA-256:
  `f12df0266029c3fe5c472f297676ac6e76303b37e06b840efefdf567a4d386aa`
- Page count: 19
- Extracted text characters: 35,226
- Metadata title:
  `Coordinate-Wise Additivity and Local ℓ¹ Gauge Selection (GS-000)`
- Metadata author: `Jeremy H. Carroll`
- Required extracted strings found:
  `10.5281/zenodo.20723753`, `v6.1.1`, `OPEN`, `NOT_VERIFIED`, and
  `2026-09-28`

Metadata and page count were checked with Poppler `pdfinfo`; text extraction
and required-string checks were performed with `pypdf` against the final PDF.
