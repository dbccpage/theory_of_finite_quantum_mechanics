# Reproducing the preprint package

The upload candidate is `mub6_publication.zip`; `mub6.pdf` is its reader-facing
manuscript. Extract the ZIP into an empty directory. From the extracted root:

```text
python scripts/verify_publication.py
```

This uses only the Python 3.12+ standard library. It checks both manifests,
metadata, four-line header and render-source bindings without modifying files.
An archive qualified check additionally requires the ZIP and SHA-256 sidecar:

```text
python scripts/verify_publication.py --archive /path/to/mub6_publication.zip
```

To render again, install Pandoc, XeLaTeX, Times New Roman, Consolas and Latin
Modern Math, then run `python scripts/build_pdf.py`. Rendering changes the
source-bound artifacts and invalidates old manifests. The repository builder
`scripts/build_publication_release.py` recreates the candidate from maintained
sources; the extracted preprint is a sealed reader package.

The research supplement is external at the commit linked in the manuscript.
No Lean project, dependency cache, full axiom census or native Rust workspace
is included here. The complete formal replay is an outstanding release review
item, not an integrity-check result. No external deposit has been performed.
