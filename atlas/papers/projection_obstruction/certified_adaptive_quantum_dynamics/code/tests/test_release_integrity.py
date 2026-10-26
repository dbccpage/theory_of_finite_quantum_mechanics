"""Negative controls for release inventory and evidence associations."""

import importlib.util
import json
import shutil
import warnings
import zipfile
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


release = load_module("caq_release_test", ROOT / "scripts/rebuild_release.py")


@pytest.fixture
def bundle(tmp_path):
    (tmp_path / "paper.md").write_text("A finite research fixture.\n")
    (tmp_path / "code").mkdir()
    (tmp_path / "code/engine.py").write_text("value = 1\n")
    release.generate_manifests(tmp_path)
    archive = tmp_path / release.ARCHIVE_NAME
    release.build_archive(tmp_path, archive)
    return tmp_path, archive


def rewrite_zip(archive, transform):
    with zipfile.ZipFile(archive) as source:
        members = [(info, source.read(info)) for info in source.infolist()]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(archive, "w") as target:
            for info, data in transform(members):
                target.writestr(info, data)


def test_release_roundtrip_is_deterministic_and_extracted_payload_verifies(bundle, tmp_path):
    root, archive = bundle
    assert release.verify_release(root, archive)
    original = archive.read_bytes()
    release.generate_manifests(root)
    release.build_archive(root, archive)
    assert archive.read_bytes() == original
    destination = tmp_path.parent / (tmp_path.name + "-extracted")
    with zipfile.ZipFile(archive) as payload:
        payload.extractall(destination)
    assert release.verify_release(destination / release.ARCHIVE_PREFIX, None)


def test_wrong_digest_rejected_even_when_zip_matches_tree(bundle):
    root, archive = bundle
    manifest = root / "MANIFEST.sha256"
    records = manifest.read_text().splitlines()
    records[0] = "0" * 64 + records[0][64:]
    manifest.write_text("\n".join(records) + "\n")
    sums = root / "SHA256SUMS"
    entries = release.parse_manifest(sums.read_text())
    entries["MANIFEST.sha256"] = release.sha256_of(manifest)
    sums.write_text("".join(f"{digest}  {name}\n" for name, digest in sorted(entries.items())))
    release.build_archive(root, archive)
    assert not release.verify_release(root, archive)


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "unexpected", "content"])
def test_archive_inventory_and_bytes_are_exact(bundle, mutation):
    root, archive = bundle
    def transform(members):
        if mutation == "missing":
            return members[:-1]
        if mutation == "duplicate":
            return [*members, members[0]]
        if mutation == "unexpected":
            info = zipfile.ZipInfo(release.ARCHIVE_PREFIX + "/../escape", release.ZIP_DATE)
            info.external_attr = 0o100644 << 16
            return [*members, (info, b"invalid")]
        info, data = members[0]
        return [(info, data + b"stale"), *members[1:]]
    rewrite_zip(archive, transform)
    assert not release.verify_release(root, archive)


@pytest.mark.parametrize("text", [
    "", "invalid", "a" * 64 + "  ../outside\n",
    "a" * 64 + "  /absolute\n", "a" * 64 + "  code/./engine.py\n",
    "a" * 64 + "  code\\engine.py\n",
    "a" * 64 + "  file\n" + "b" * 64 + "  file\n",
    "a" * 64 + "  FILE\n" + "b" * 64 + "  file\n",
])
def test_manifest_parser_rejects_ambiguous_inventory(text):
    with pytest.raises(ValueError):
        release.parse_manifest(text)


def test_unlisted_payload_and_symlink_are_rejected(bundle):
    root, archive = bundle
    extra = root / "unlisted.md"
    extra.write_text("not in the manifest")
    assert not release.verify_release(root, archive)
    extra.unlink()
    extra.symlink_to(root / "paper.md")
    assert not release.verify_release(root, archive)


def copy_files(destination, relatives):
    for relative in relatives:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)


def verifier(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT))
    return load_module("caq_verifier_test", ROOT / "verify_deposit.py")


@pytest.mark.parametrize("mutation", ["version", "creators", "rights", "scope"])
def test_metadata_mismatches_are_rejected(tmp_path, monkeypatch, mutation):
    copy_files(tmp_path, [".zenodo.json", "zenodo_metadata.json", "LICENSE-CODE",
                          "code/caqd/__init__.py", "code/pyproject.toml"])
    audit = verifier(monkeypatch)
    assert audit.check_zenodo_metadata(tmp_path)
    path = tmp_path / "zenodo_metadata.json"
    data = json.loads(path.read_text())
    if mutation == "version":
        data["version"] = "9.9.9"
    elif mutation == "creators":
        data["creators"] = []
    elif mutation == "rights":
        data["rights"][1]["id"] = "polyform-noncommercial-1.0.0"
    else:
        data["description"] = "Unconditional numerical certificate."
    path.write_text(json.dumps(data))
    assert not audit.check_zenodo_metadata(tmp_path)


@pytest.mark.parametrize("mutation", ["test", "function", "theorem", "id"])
def test_broken_evidence_associations_are_rejected(tmp_path, monkeypatch, mutation):
    data = yaml.safe_load((ROOT / "claim_ledger.yaml").read_text())
    paths = {"claim_ledger.yaml", "certified_adaptive_quantum_dynamics.md",
             "033_certified_adaptive_quantum_dynamics_claim_ledger.md"}
    for claim in data["claims"]:
        if "code_evidence" in claim:
            evidence = claim["code_evidence"]
            paths.add("code/" + evidence["module"].replace(".", "/") + ".py")
            paths.update("code/" + selector.split("::")[0] for selector in evidence["tests"])
        if "lean4_formalization" in claim:
            paths.add("lean4/" + claim["lean4_formalization"]["module"].replace(".", "/") + ".lean")
    copy_files(tmp_path, paths)
    audit = verifier(monkeypatch)
    assert audit.check_claim_ledger(tmp_path)
    claim = data["claims"][0]
    if mutation == "test":
        claim["code_evidence"]["tests"][0] = "tests/test_bounds.py::test_nonexistent"
    elif mutation == "function":
        claim["code_evidence"]["functions"][0] = "nonexistent"
    elif mutation == "theorem":
        claim["lean4_formalization"]["theorems"][0] = "nonexistent"
    else:
        claim["id"] = "PO033-C2"
    (tmp_path / "claim_ledger.yaml").write_text(yaml.safe_dump(data, sort_keys=False))
    assert not audit.check_claim_ledger(tmp_path)
