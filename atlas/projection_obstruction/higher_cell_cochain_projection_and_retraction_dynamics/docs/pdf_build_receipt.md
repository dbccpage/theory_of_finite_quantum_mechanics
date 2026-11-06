# PO034 PDF build receipt

Built and visually reviewed 2026-11-05; typesetting evidence only.

- Canonical Markdown SHA-256: bd152a54bc44887280527130e240caa05090457d00996ca122b67bca3cd6d4af
- TeX SHA-256: 9a5593c36f3eb17d6d5e2e93dfbafe4f61b9939ff23b8f25f031ccac367a0724
- PDF SHA-256: 79b5aa413fb08d744350c3e306cff0e4df86d5aef959276097e34535019bfc6f
- Figure SHA-256: a7acfc14966f9e6c1b6405180d55be424c086e6e5a67e1f537ed85e9f820f083
- Pandoc 3.7.0.2; Tectonic 0.17.0 (XeTeX engine), explicit Latin Modern font files.
- 26 pages; zero missing-glyph and overfull-box diagnostics.
- Inspected title, changed analytic sections, and final supplemental scope pages.
- Commands: `python scripts/build_paper_artifacts.py --tex-only`, then `tectonic --untrusted --keep-logs --keep-intermediates higher_cell_cochain_projection_and_retraction_dynamics.tex`.
- PDF bytes depend on the named typesetting toolchain; no cross-platform PDF byte identity is asserted.
