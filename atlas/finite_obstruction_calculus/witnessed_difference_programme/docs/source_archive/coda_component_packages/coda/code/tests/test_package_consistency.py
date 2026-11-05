"""Historical custody and claim/status checks on isolated fixture packages."""
import json
import shutil
from pathlib import Path

import pytest
import verify_package as check
from build_claim_index import destinations, render_lean_map
from build_notebook import build
from run_examples import exact_json

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def package(tmp_path):
    root = tmp_path / "package"
    for relative in check.files(ROOT):
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    return root


def save(root, name, value):
    (root / name).write_text(json.dumps(value), encoding="utf-8")


def test_current_claims_custody_and_local_proof_scopes(package):
    assert len(check.source_custody(package)) == 17
    claims = check.validate_claims(package)
    assert len(claims["claims"]) == 26
    statuses = {r["id"]: r["status"] for r in claims["claims"]}
    assert statuses["CODA-05"] == "PROVED_PROSE"
    assert statuses["CODA-17"] == "OPEN"
    assert check.validate_lean(package, claims) == 20
    assert check.validate_examples_and_notebook(package) == 8
    assert check.validate_links(package, check.files(package), check.source_custody(package)) > 20
    assert render_lean_map(claims) == (package / "docs/lean_claim_map.md").read_text(encoding="utf-8")


@pytest.mark.parametrize("kind", ["baseline", "count", "source_duplicate", "preserved_duplicate", "size", "sha", "blob", "escape"])
def test_source_custody_rejects_tampering(package, kind):
    m = check.load(package / "source_manifest.json")
    if kind == "baseline":
        m["baseline_commit"] = "0" * 40
    elif kind == "count":
        m["sources"].pop()
    elif kind == "source_duplicate":
        m["sources"][1]["source_path"] = m["sources"][0]["source_path"]
    elif kind == "preserved_duplicate":
        m["sources"][1]["preserved_path"] = m["sources"][0]["preserved_path"]
    elif kind == "escape":
        m["sources"][0]["preserved_path"] = "../outside"
    else:
        key = {"size": "bytes", "sha": "sha256", "blob": "git_blob"}[kind]
        m["sources"][0][key] = 0 if key == "bytes" else "0" * len(m["sources"][0][key])
    save(package, "source_manifest.json", m)
    with pytest.raises(ValueError):
        check.source_custody(package)


def test_immutable_original_is_checked_independently_of_active_code(package):
    (package / "code/coda_discipline_core.py").write_text("# maintained derivative", encoding="utf-8")
    assert len(check.source_custody(package)) == 17
    original = package / "docs/source_archive/coda_discipline_core.py.txt"
    original.write_bytes(original.read_bytes() + b"\n# alteration")
    with pytest.raises(ValueError, match="Source bytes"):
        check.source_custody(package)


@pytest.mark.parametrize("kind", ["index", "map", "missing_marker", "duplicate_marker", "ledger"])
def test_claim_maps_reject_status_and_number_drift(package, kind):
    if kind == "index":
        m = check.load(package / "claim_index.json")
        m["claims"][4]["status"] = "PROVED_LOCAL"
        save(package, "claim_index.json", m)
    elif kind == "map":
        (package / "docs/lean_claim_map.md").write_text("CODA-17 PROVED_LOCAL", encoding="utf-8")
    else:
        name = "coda_claim_ledger.md" if kind == "ledger" else "coda.md"
        p = package / name
        text = p.read_text(encoding="utf-8")
        text = text.replace("CODA-01", "MISSING-01") if kind != "duplicate_marker" else text + " (CODA-01)"
        p.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError):
        check.validate_claims(package)


@pytest.mark.parametrize("kind", ["audit", "theorem", "placeholder", "axiom"])
def test_lean_map_rejects_uncovered_names_and_changed_axioms(package, kind):
    foundations = package / "lean4/Foundations.lean"
    path = package / ("lean4/AxiomAudit.lean" if kind == "audit" else
                      "lean4/axiom_report.txt" if kind == "axiom" else foundations)
    text = path.read_text(encoding="utf-8")
    if kind == "placeholder":
        text += "\nexample : False := by sorry\n"
    elif kind == "axiom":
        text = text.replace("Classical.choice", "untrusted_axiom")
    else:
        text = text.replace("witnessed_distinct", "wrong_name")
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError):
        check.validate_lean(package, check.load(package / "claim_index.json"))


@pytest.mark.parametrize("kind", ["examples", "legacy", "count", "execution", "error"])
def test_computational_and_notebook_receipts_reject_stale_outputs(package, kind):
    if kind == "examples":
        save(package, "code/fixtures/examples.json", {})
    elif kind == "legacy":
        p = "code/fixtures/legacy_counterexample.json"
        m = check.load(package / p)
        m["target_status"] = "PROVED_LOCAL"
        save(package, p, m)
    else:
        p = "jupyter_notebooks/01_coda_walkthrough.ipynb"
        m = check.load(package / p)
        cells = [c for c in m["cells"] if c["cell_type"] == "code"]
        if kind == "count":
            m["cells"].remove(cells[0])
        elif kind == "execution":
            cells[0]["execution_count"] = None
        else:
            cells[0]["outputs"] = [{"output_type": "error"}]
        save(package, p, m)
    with pytest.raises(ValueError):
        check.validate_examples_and_notebook(package)


def test_missing_link_and_duplicate_json_keys_are_refused(package):
    (package / "docs/invalid.md").write_text("[missing](missing.file)", encoding="utf-8")
    with pytest.raises(ValueError, match="Unresolved"):
        check.validate_links(package, ["docs/invalid.md"], set())
    assert check.unique_object([("a", 1)]) == {"a": 1}
    with pytest.raises(ValueError, match="Duplicate"):
        check.unique_object([("a", 1), ("a", 2)])
    assert destinations("CODA-01..03") == ["CODA-01", "CODA-02", "CODA-03"]
    assert destinations("XCODA-01") == []
    with pytest.raises(TypeError):
        exact_json(object())


def test_integrity_detects_altered_missing_and_extra_content(tmp_path):
    (tmp_path / "asset").write_bytes(b"original")
    check.integrity(tmp_path, ["asset"], True)
    check.integrity(tmp_path, ["asset"], False)
    (tmp_path / "asset").write_bytes(b"changed")
    with pytest.raises(ValueError, match="bytes changed"):
        check.integrity(tmp_path, ["asset"], False)
    with pytest.raises(ValueError, match="exactly"):
        check.integrity(tmp_path, [], False)


def test_notebook_builder_keeps_computation_separate_from_execution(tmp_path):
    target = tmp_path / "walkthrough.ipynb"
    build(target)
    m = check.load(target)
    cells = [c for c in m["cells"] if c["cell_type"] == "code"]
    assert len(cells) == 8 and all(c["execution_count"] is None for c in cells)
    assert any("audit()" in "".join(c["source"]) for c in cells)


def test_lean_lakefile_active_modules_and_unreviewed_boundaries(package):
    lakefile = package / "lean4/lakefile.lean"
    content = lakefile.read_text(encoding="utf-8")
    lakefile.write_text(content.replace("`Boundaries,", ""), encoding="utf-8")
    with pytest.raises(ValueError, match="The audit does not cover every local theorem"):
        check.validate_lean(package, check.load(package / "claim_index.json"))
    lakefile.write_text(content, encoding="utf-8")

    boundaries = package / "lean4/Boundaries.lean"
    b_text = boundaries.read_text(encoding="utf-8")
    boundaries.write_text(b_text + "\ntheorem unreviewed_extra : True := by trivial\n", encoding="utf-8")
    with pytest.raises(ValueError, match="The audit does not cover every local theorem"):
        check.validate_lean(package, check.load(package / "claim_index.json"))

    boundaries.write_text(b_text + "\nexample : True := by sorry\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Unreviewed proof escape"):
        check.validate_lean(package, check.load(package / "claim_index.json"))

