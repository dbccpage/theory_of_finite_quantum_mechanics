from pathlib import Path

from prose_proofs import ROOT, covered_ids, heading_anchor, lean_ref_resolves, proof_sections, render_index, section_errors


def test_section_rules(tmp_path: Path):
    (tmp_path / "lean4").mkdir()
    (tmp_path / "lean4" / "A.lean").write_text("theorem good : True := trivial\n", encoding="utf-8")
    (tmp_path / "papers").mkdir()
    (tmp_path / "papers" / "p.md").write_text(
        "## 1\n\nDAG node: `N1`\n\n*Proof.* Clear.\n\nLean: `lean4/A.lean::good`.\n"
        "## 2\n\nDAG node: `N2`\n\nNo proof here. `lean4/A.lean::missing`\n"
        "## 3\n\nDAG node: `N3`\n\n*Proof.* x\n",
        encoding="utf-8",
    )
    nodes = {
        "N1": {"status": "PROVED_LEAN", "lean": ["lean4/A.lean::good"]},
        "N2": {"status": "PROVED_LEAN", "lean": ["lean4/A.lean::good"]},
        "N3": {"status": "OPEN", "lean": []},
    }
    sections = proof_sections(tmp_path)
    assert [s["ids"] for s in sections] == [["N1"], ["N2"], ["N3"]]
    assert section_errors(sections[0], nodes, tmp_path) == []
    errs2 = " ".join(section_errors(sections[1], nodes, tmp_path))
    assert "no *Proof.*" in errs2 and "does not resolve" in errs2 and "cites none" in errs2
    assert "takes no proof" in " ".join(section_errors(sections[2], nodes, tmp_path))


def test_lean_reference_rejects_comments_strings_prefixes_and_wrong_namespaces(tmp_path: Path):
    (tmp_path / "lean4").mkdir()
    (tmp_path / "lean4" / "A.lean").write_text(
        '-- theorem commented : True := trivial\n'
        '/- nested /- theorem nested : True := trivial -/ comment -/\n'
        'def text := "theorem stringOnly : True := trivial"\n'
        'namespace Actual\n'
        'theorem good_longer : True := trivial\n'
        'theorem good : True := trivial\n'
        'end Actual\n'
        'namespace Second\n'
        'theorem good : True := trivial\n'
        'end Second\n', encoding="utf-8")
    for name in ("commented", "nested", "stringOnly", "good_long", "Wrong.good", "good"):
        assert not lean_ref_resolves(tmp_path, "lean4/A.lean", name)
    assert lean_ref_resolves(tmp_path, "lean4/A.lean", "Actual.good")
    assert not lean_ref_resolves(tmp_path, "lean4/../lean4/A.lean", "Actual.good")
    (tmp_path / "papers").mkdir()
    (tmp_path / "papers" / "Original.lean").write_text(
        'namespace Original\ntheorem result : True := trivial\nend Original\n', encoding="utf-8")
    assert lean_ref_resolves(tmp_path, "papers/Original.lean", "Original.result")
    assert not lean_ref_resolves(tmp_path, "papers/Original.lean", "Wrong.result")
    assert not lean_ref_resolves(tmp_path, "papers/../lean4/A.lean", "Actual.good")
    (tmp_path / "Outside.lean").write_text('theorem result : True := trivial\n', encoding="utf-8")
    assert not lean_ref_resolves(tmp_path, "Outside.lean", "result")


def test_coverage_excludes_invalid_sections_and_fenced_examples(tmp_path: Path):
    (tmp_path / "papers").mkdir()
    (tmp_path / "papers" / "p.md").write_text(
        '```markdown\nDAG node: `EXAMPLE`\n*Proof.* Example.\n```\n'
        'DAG node: `INVALID`\nThe token *Proof.* is not a proof paragraph.\n'
        '# next\nDAG node: `VALID`\n*Proof.* Text.\n', encoding="utf-8")
    nodes = {key: {"status": "PROVED_PROSE", "lean": []} for key in ("EXAMPLE", "INVALID", "VALID")}
    assert [s["ids"] for s in proof_sections(tmp_path)] == [["INVALID"], ["VALID"]]
    assert covered_ids(tmp_path, nodes) == {"VALID"}


def test_index_from_nodes_to_sections_is_current():
    assert (ROOT / "dag" / "prose_proofs.md").read_text(encoding="utf-8") == render_index()


def test_heading_anchor():
    seen = {}
    assert heading_anchor(" 1.4 Which maps descend to $p$?", seen) == "14-which-maps-descend-to-p"
    assert heading_anchor(" 1.4 Which maps descend to $p$?", seen) == "14-which-maps-descend-to-p-1"
