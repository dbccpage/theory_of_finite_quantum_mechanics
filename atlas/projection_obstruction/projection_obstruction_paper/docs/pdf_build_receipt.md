# PO000 PDF build receipt

Built and visually reviewed 2026-11-05; typesetting evidence only.

- Canonical Markdown SHA-256: 154cc6e37c382c717179b977c94c9870711b6839ff0e65d254c96425514191c9
- TeX SHA-256: c2906bfa25861dfe131060b585a81bf92d7d42e6eeeb7425d66bcae763584463
- PDF SHA-256: 7f3f3c125f1da210970a157fed07d9fd92fa4dc94a0d643071bd4fbc60b1ca01
- Pandoc 3.7.0.2; Tectonic 0.17.0 (XeTeX engine), explicit Latin Modern font files.
- 74 pages; zero missing-glyph and overfull-box diagnostics.
- Inspected title, changed analytic sections, and final supplemental scope pages.
- Commands: `python scripts/build_paper_artifacts.py --tex-only`, then `tectonic --untrusted --keep-logs --keep-intermediates projection_obstruction.tex`.
- PDF bytes depend on the named typesetting toolchain; no cross-platform PDF byte identity is asserted.
