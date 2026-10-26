#!/usr/bin/env python3
"""Remove the known mismatched DOI from the frozen MUR release PDF.

This is a bounded byte-level release repair for the checked-in PDF when a TeX
engine is unavailable. The Markdown and TeX sources remain canonical and carry
the same replacement text. Regenerating the PDF from TeX supersedes this patch.
"""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "mur" / "coda_mur.pdf"
SOURCE_SHA256 = "2002d00d8fb6407088a112fcea800d246cd061897461801808bed8d40932b677"
BAD_TEXT = "https://doi.org/10.5281/zenodo.20677250"
REPLACEMENT = "DOI not asserted."


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    document = pymupdf.open(PDF)
    existing = [
        (page_number, rectangle)
        for page_number, page in enumerate(document)
        for rectangle in page.search_for(BAD_TEXT)
    ]
    if not existing:
        text = "\n".join(page.get_text() for page in document)
        if REPLACEMENT in text and BAD_TEXT not in text:
            print("OK: MUR PDF citation already patched")
            return 0
        raise ValueError("expected mismatched DOI was not found")
    if sha256(PDF) != SOURCE_SHA256 or len(existing) != 1:
        raise ValueError("MUR PDF bytes or DOI occurrence count differ from the reviewed input")

    page_number, rectangle = existing[0]
    page = document[page_number]
    for link in page.get_links():
        if link.get("uri") == BAD_TEXT:
            page.delete_link(link)
    redaction = pymupdf.Rect(
        rectangle.x0 - 0.5,
        rectangle.y0 - 0.5,
        rectangle.x1 + 0.5,
        rectangle.y1 + 0.5,
    )
    page.add_redact_annot(redaction, fill=(1, 1, 1))
    page.apply_redactions()
    page.insert_text(
        (rectangle.x0, 284.58),
        REPLACEMENT,
        fontname="cour",
        fontsize=9.2728,
        color=(0, 0, 0),
    )

    with tempfile.NamedTemporaryFile(
        prefix=".coda_mur-citation-", suffix=".pdf", dir=PDF.parent, delete=False
    ) as handle:
        temporary = Path(handle.name)
    try:
        document.save(temporary, garbage=4, deflate=True, clean=True)
        document.close()
        temporary.replace(PDF)
    finally:
        temporary.unlink(missing_ok=True)
    print("OK: replaced mismatched MUR DOI in checked-in PDF")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
