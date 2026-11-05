# Primitive difference toward Hamilton and Noether

Start with the [two-page v5 PDF](two_sheets_v5.pdf): nine picture strips on one A3 sheet and the mathematical assumptions on the other.

- [Picture sheet](picture_sheet_v5.png) and [scalable SVG](picture_sheet_v5.svg)
- [Math sheet](math_sheet_v5.pdf) and [searchable text](math_sheet_v5.md)
- [Two sheets on Everett](everett/README.md)
- [Panel captions](panel_captions_v5.md)
- [Complete contents and review history](START_HERE.md)

The pictures follow comparison, joining and cancellation, a report that loses direction, balance, a quarter-turn, area preservation, Hamiltonian motion, and a Noether example. The companion explicitly distinguishes supplied structures from derived consequences. This is a conditional teaching construction toward the larger many-worlds project; it does not derive Born probabilities, Everett's interpretation, Bell correlations, or physical laws from marks alone.

## Review record

The independent adversary reviewed v4 and found four issues. Version v5 repairs the return-arrow visibility, vector-field/flow distinction, circle-completion premises, and full matrix-algebra hypotheses. The focused v5 recheck found no resulting mathematical or visual defect; novice comprehension remains untested.

- [v4 criticism, unchanged](11_adversary_v4_verbatim.md)
- [Response to all four findings](13_response_to_v4_review.md)
- [v5 recheck, unchanged](12_adversary_v5_verbatim.md)

All prior reviews and drafts are retained, including mistakes and subsequent source corrections. The source-reading notes are bounded readings, not fresh Lean builds or verified publication receipts.

## Reproduce the current sheets

Use Python 3 with the versions in [requirements.txt](requirements.txt). From this directory:

```text
python -m pip install -r requirements.txt
python render_sheets_v5.py
```

The v5 renderer deliberately imports the retained v4 and v3 renderers. Run in a copy if preserving the archived exports: rendering writes PNG, SVG, PDF, Markdown, and caption outputs. PDF/SVG metadata may change between renders. The checked-in exports are the reviewed artifacts.

## Preservation and portability

The 69 original files were copied byte-for-byte from this chat's artifact directory on 2026-11-03. [import_manifest.json](import_manifest.json) records their SHA-256 values; the folder attributes prevent Git line-ending conversion. Virtual environments and Python caches are excluded.

Historical reviewer notes retain their original absolute Windows source locations and line references. Those links are provenance, not portable repository navigation, and source files may since have moved or changed. The relative links above and in START_HERE.md open the packaged artifacts. Do not rewrite historical remarks to update their pointers; add a separate correction instead.

This folder belongs to the Codex draft. Other material under `education/l1_to_many_worlds` is outside this package.
