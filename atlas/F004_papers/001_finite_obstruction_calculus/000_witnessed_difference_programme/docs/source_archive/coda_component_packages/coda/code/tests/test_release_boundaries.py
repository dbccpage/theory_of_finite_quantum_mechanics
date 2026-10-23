"""Custody, disposition, and exact-certificate boundary regressions."""

import json
import shutil
import sys
from dataclasses import replace
from importlib.machinery import SourceFileLoader
from pathlib import Path
from types import ModuleType, SimpleNamespace

import audit_legacy_embedding as legacy
import pytest
import verify_package as check
from build_claim_index import build_index, render_lean_map
from coda_core import coordinate_packet, parity_sections, verify_coordinate_certificate

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = "docs/source_archive/coda_discipline_core.py.txt"


def copy_package(target, omit=None):
    for relative in check.files(ROOT):
        if Path(relative).parts[0] == omit:
            continue
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, path)
    return target


@pytest.mark.parametrize("fault", ["duplicate", "empty_destination", "foreign_destination"])
def test_legacy_disposition_checks_are_independent_of_index_generation(tmp_path, fault):
    package = copy_package(tmp_path / "package")
    ledger = package / "coda_claim_ledger.md"
    text = ledger.read_text(encoding="utf-8")
    if fault == "duplicate":
        text = text.replace("| FDN-02 |", "| FDN-01 |", 1)
    elif fault == "empty_destination":
        text = text.replace("| FDN-01 | CODA-01 |", "| FDN-01 | none |", 1)
    else:
        text = text.replace("| FDN-01 | CODA-01 |", "| FDN-01 | CODA-99 |", 1)
    ledger.write_text(text, encoding="utf-8")
    index = build_index(package)
    # The generated sidecars agree exactly; the semantic disposition check
    # must still reject a duplicated identity or an unrealized destination.
    (package / "claim_index.json").write_text(json.dumps(index), encoding="utf-8")
    (package / "docs/lean_claim_map.md").write_text(render_lean_map(index), encoding="utf-8")
    expected = "48 distinct" if fault == "duplicate" else "valid destination"
    with pytest.raises(ValueError, match=expected):
        check.validate_claims(package)


@pytest.mark.parametrize("directory", ["code", "lean4", "jupyter_notebooks", "images"])
def test_package_verifier_refuses_missing_required_directory(tmp_path, directory):
    package = copy_package(tmp_path / "incomplete", omit=directory)
    if directory == "images":
        # Preserved image custody is checked before the directory inventory.
        with pytest.raises(FileNotFoundError) as error:
            check.verify(package)
        assert "images" in Path(error.value.filename).parts
    else:
        with pytest.raises(ValueError, match=f"Missing requested directory: {directory}"):
            check.verify(package)


def test_complete_isolated_package_writes_then_verifies_inventory(tmp_path):
    package = copy_package(tmp_path / "complete")
    written = check.verify(package, write=True)
    verified = check.verify(package)
    assert written["integrity_action"] == "written"
    assert verified["integrity_action"] == "verified"
    assert verified["source_files_preserved"] == 17
    assert verified["legacy_dispositions"] == 48
    assert verified["executed_notebook_cells_recorded"] == 8


@pytest.fixture
def archived_package(tmp_path, monkeypatch):
    package = tmp_path / "archive"
    (package / "code").mkdir(parents=True)
    destination = package / ARCHIVE
    destination.parent.mkdir(parents=True)
    shutil.copyfile(ROOT / ARCHIVE, destination)
    manifest = json.loads((ROOT / "source_manifest.json").read_text(encoding="utf-8"))
    row = next(row for row in manifest["sources"] if row["preserved_path"] == ARCHIVE)
    (package / "source_manifest.json").write_text(json.dumps({"sources": [row]}), encoding="utf-8")
    monkeypatch.setattr(legacy, "__file__", str(package / "code/audit_legacy_embedding.py"))
    prior_module = sys.modules.get("coda_legacy_discipline")
    sys.modules["coda_legacy_discipline"] = ModuleType("coda_legacy_discipline")
    try:
        yield package
    finally:
        if prior_module is None:
            sys.modules.pop("coda_legacy_discipline", None)
        else:
            sys.modules["coda_legacy_discipline"] = prior_module


def test_legacy_audit_rejects_altered_original_before_import(archived_package, monkeypatch):
    original = archived_package / ARCHIVE
    original.write_bytes(original.read_bytes() + b"\n# altered archived bytes\n")

    def importing_is_forbidden(*args, **kwargs):
        raise AssertionError("hash rejection must precede importing")

    monkeypatch.setattr(legacy.importlib.util, "spec_from_loader", importing_is_forbidden)
    with pytest.raises(ValueError, match="source hash mismatch"):
        legacy.audit()


@pytest.mark.parametrize("spec", [None, SimpleNamespace(loader=None)])
def test_legacy_audit_rejects_missing_loader(archived_package, monkeypatch, spec):
    monkeypatch.setattr(legacy.importlib.util, "spec_from_loader", lambda *args: spec)
    with pytest.raises(ImportError, match="Cannot load spec"):
        legacy.audit()


def test_legacy_audit_rejects_changed_collision_result(archived_package, monkeypatch):
    class ChangedResultLoader(SourceFileLoader):
        def exec_module(self, module):
            super().exec_module(module)
            point = object()

            def changed_embedding(groupoid):
                return SimpleNamespace(
                    embed_morphism=lambda name: SimpleNamespace(
                        p1=point,
                        p2=point,
                        mid_size=1,
                        left_map=(0,),
                        right_map=(0,),
                        ext_cost=0 if name == "e" else 1,
                    ),
                    check_faithfulness=lambda: True,
                )

            module.FaithfulGroupoidEmbedding = changed_embedding

    monkeypatch.setattr(legacy, "SourceFileLoader", ChangedResultLoader)
    with pytest.raises(AssertionError, match="no longer reproduces the collision"):
        legacy.audit()


@pytest.mark.parametrize("field", ["state", "residual", "dual"])
def test_coordinate_certificate_rejects_truncated_vectors(field):
    good = coordinate_packet((1, 2, 3))
    malformed = replace(good, **{field: getattr(good, field)[:2]})
    assert not verify_coordinate_certificate(malformed)


@pytest.mark.parametrize("vertices", [-1, 17, True, 1.5])
def test_parity_enumerator_refuses_undeclared_vertex_domains(vertices):
    with pytest.raises(ValueError, match="0 through 16"):
        parity_sections(vertices, ())
