from pathlib import Path

from prose_proofs import load_nodes, proof_sections, section_errors


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
