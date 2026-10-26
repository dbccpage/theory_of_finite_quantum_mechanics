from pathlib import Path

from prose_proofs import ROOT, heading_anchor, load_nodes, proof_sections, render_index, section_errors


def test_every_proof_section_names_a_proved_node_and_resolves():
    nodes = load_nodes()
    errs = [e for s in proof_sections() for e in section_errors(s, nodes)]
    assert errs == []


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


def test_index_from_nodes_to_sections_is_current():
    assert (ROOT / "dag" / "prose_proofs.md").read_text(encoding="utf-8") == render_index()


def test_heading_anchor():
    seen = {}
    assert heading_anchor(" 1.4 Which maps descend to $p$?", seen) == "14-which-maps-descend-to-p"
    assert heading_anchor(" 1.4 Which maps descend to $p$?", seen) == "14-which-maps-descend-to-p-1"
