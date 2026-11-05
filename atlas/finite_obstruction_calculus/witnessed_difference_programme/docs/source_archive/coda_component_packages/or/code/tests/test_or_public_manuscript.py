"""Public OR manuscript matches the first-deposit metadata."""

from __future__ import annotations

from pathlib import Path

import fitz

PKG = Path(__file__).resolve().parents[2]
MD = PKG / "coda_or.md"
TEX = PKG / "coda_or.tex"
PDF = PKG / "coda_or.pdf"
ZENODO = PKG / "zenodo_metadata.json"


def test_or_status_is_first_public_preprint() -> None:
    md = MD.read_text(encoding="utf-8")
    tex = TEX.read_text(encoding="utf-8")
    zenodo = ZENODO.read_text(encoding="utf-8")
    assert "**Status:** first public preprint" in md
    assert "published Zenodo release" not in md
    assert r"\textbf{Status:} first public preprint" in tex
    assert "published Zenodo release" not in tex
    assert "first CODA-titled OR deposit" in zenodo
    assert "GTOR-21" not in zenodo


def test_or_tex_does_not_break_typewriter_underscores() -> None:
    tex = TEX.read_text(encoding="utf-8")
    assert "hyphenat" not in tex
    assert r"\allowbreak" not in tex
    assert r"\symbol{95}" not in tex


def test_or_pdf_carries_preprint_status_and_unbroken_identifiers() -> None:
    # Invariant: the shipped PDF matches md/tex; hyphenat must not split Lean names.
    doc = fitz.open(PDF)
    try:
        page1 = doc[0].get_text()
        body = "\n".join(page.get_text() for page in doc)
    finally:
        doc.close()
    assert "first public preprint" in page1
    assert "published Zenodo release" not in body
    assert "pair_gluing" in body
    assert "Algebra.lean" in body
