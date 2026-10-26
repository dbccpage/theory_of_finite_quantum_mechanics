"""Publication profiles and adversarial release-custody regressions."""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys
import zipfile
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import build_release_zip as archive_builder
import regen_sha256sums as manifest_builder
import verify_deposit as verifier
from build_release_zip import canonical_bytes
from ffi import NativeMeasurementUnavailable, measurement_call
from regen_sha256sums import check_manifests, regenerate, render
from release_custody import identity, snapshot, traversal_error, unchanged


@pytest.fixture
def envelope(tmp_path):
    root = tmp_path / "package"
    root.mkdir()
    (root / "payload.txt").write_text("payload\n", encoding="utf-8")
    regenerate(root)
    archive = tmp_path / "release.zip"
    archive.write_bytes(canonical_bytes(root))
    sidecar = archive.with_suffix(".zip.sha256")
    sidecar.write_bytes(f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n".encode())
    return root, archive, sidecar


def test_independent_version_identities():
    release = identity(ROOT)
    assert release["manuscript_version"] == release["release_version"] == "6.9.18"
    assert release["code_version"] == "6.9.6"
    assert release["code_version"] != release["release_version"]


def test_standalone_cannot_use_ambient_native_host(monkeypatch):
    monkeypatch.setenv("PO000_NATIVE_INTEGRATION", "0")
    with pytest.raises(NativeMeasurementUnavailable, match="NATIVE_INTEGRATION_NOT_REQUESTED"):
        measurement_call("measurement_evaluate", {})


@pytest.mark.parametrize("profile,selection,opt_in", [
    ("standalone", ["-m", "not native_integration"], "0"),
    ("native", [], "1"),
])
def test_profile_subprocess_contract(monkeypatch, profile, selection, opt_in):
    calls = []

    def run(command, **kwargs):
        calls.append((command, kwargs))
        return SimpleNamespace(returncode=0, stdout="2 passed\n", stderr="")

    monkeypatch.setattr(verifier.subprocess, "run", run)
    monkeypatch.setenv("PYTHONPATH", "ambient-untrusted")
    assert verifier.run_tests(ROOT, profile) == (0, "2 passed", [])
    command, kwargs = calls[0]
    assert kwargs["env"]["PYTHONPATH"].split(os.pathsep) == [str(ROOT / "code"), str(ROOT / "scripts")]
    assert kwargs["env"]["PO000_NATIVE_INTEGRATION"] == opt_in
    assert command[-1] == "code/tests"
    assert command[-3:-1] == selection if selection else "not native_integration" not in command


def test_unexpected_skips_fail_even_with_zero_exit(monkeypatch):
    monkeypatch.setattr(verifier.subprocess, "run", lambda *args, **kwargs:
                        SimpleNamespace(returncode=0, stdout="2 passed, 1 skipped\n", stderr=""))
    assert verifier.run_tests(ROOT)[0] == 1


def test_old_lean_flag_is_rejected():
    with pytest.raises(SystemExit) as error:
        verifier.main(["--lean"])
    assert error.value.code == 2


def test_lexical_scan_does_not_claim_elaboration(tmp_path):
    (tmp_path / "lean4").mkdir()
    (tmp_path / "lean4" / "invalid.lean").write_text("def broken := unresolved_identifier\n", encoding="utf-8")
    assert verifier.scan_lean_sources(tmp_path) == ([], 1)


@pytest.mark.parametrize("mutation", ["prefix", "suffix", "duplicate", "case", "metadata"])
def test_entire_archive_envelope_is_bound(envelope, mutation):
    root, archive, sidecar = envelope
    verifier.check_selected_archive(archive, root)
    data = archive.read_bytes()
    if mutation in ("prefix", "suffix"):
        data = b"unparsed-prefix" + data if mutation == "prefix" else data + b"unparsed-suffix"
    else:
        source = zipfile.ZipFile(io.BytesIO(data))
        changed = io.BytesIO()
        with zipfile.ZipFile(changed, "w") as target:
            for entry in source.infolist():
                if mutation == "metadata":
                    entry.date_time = (2000, 1, 1, 0, 0, 0)
                target.writestr(entry, source.read(entry.filename))
            if mutation in ("duplicate", "case"):
                entry = source.infolist()[0]
                name = entry.filename if mutation == "duplicate" else entry.filename.upper()
                with pytest.warns(UserWarning) if mutation == "duplicate" else __import__("contextlib").nullcontext():
                    target.writestr(name, source.read(entry.filename))
        data = changed.getvalue()
    archive.write_bytes(data)
    sidecar.write_bytes(f"{hashlib.sha256(data).hexdigest()}  {archive.name}\n".encode())
    with pytest.raises(ValueError, match="complete ZIP envelope"):
        verifier.check_selected_archive(archive, root)


@pytest.mark.parametrize("control", ["manifest", "secondary_manifest", "archive", "sidecar"])
def test_same_byte_link_swap_after_initial_verification(envelope, control):
    root, archive, sidecar = envelope
    verifier.check_selected_archive(archive, root)
    initial = snapshot(root)
    path = {"manifest": root / "SHA256SUMS", "secondary_manifest": root / "MANIFEST.sha256",
            "archive": archive, "sidecar": sidecar}[control]
    saved = path.with_name(path.name + ".saved")
    path.rename(saved)
    try:
        path.symlink_to(saved)
    except OSError:
        saved.rename(path)
        pytest.fail("symlink capability required for this custody regression")
    with pytest.raises(ValueError, match="non-regular"):
        if control == "manifest":
            unchanged(root, initial)
        else:
            verifier.check_selected_archive(archive, root)


def test_manifest_pair_has_exact_noncircular_coverage(envelope):
    root, archive, _ = envelope
    primary = verifier.parse_manifest(root / "SHA256SUMS", root)
    secondary = verifier.parse_manifest(root / "MANIFEST.sha256", root)
    assert set(secondary) == {"payload.txt"}
    assert set(primary) == {"payload.txt", "MANIFEST.sha256"}
    assert verifier.check_hashes(primary, root) == []
    assert verifier.check_manifest_pair(primary, root) == []
    assert check_manifests(root) == []
    verifier.check_selected_archive(archive, root)


def test_stale_secondary_is_rejected_even_with_rehashed_primary_and_archive(envelope, monkeypatch):
    root, archive, sidecar = envelope
    secondary = root / "MANIFEST.sha256"
    secondary.write_text(f"{'0' * 64}  payload.txt\n", encoding="utf-8")
    # An attacker updates the outer hash to faithfully cover the stale control.
    (root / "SHA256SUMS").write_bytes(render(root).encode("utf-8"))
    primary = verifier.parse_manifest(root / "SHA256SUMS", root)
    assert verifier.check_hashes(primary, root) == []
    assert verifier.sweep_unlisted(primary, root) == []
    assert any("MANIFEST.sha256" in problem
               for problem in verifier.check_manifest_pair(primary, root))
    assert check_manifests(root) == ["MANIFEST.sha256 differs from retained payload"]

    # Rehash an otherwise canonical envelope too: rejection must come from the
    # invalid inner content, rather than a stale ZIP sidecar or member metadata.
    changed = io.BytesIO()
    with zipfile.ZipFile(archive) as source, zipfile.ZipFile(changed, "w") as target:
        for entry in source.infolist():
            relative = entry.filename.split("/", 1)[1]
            target.writestr(entry, (root / relative).read_bytes())
    archive.write_bytes(changed.getvalue())
    sidecar.write_bytes(
        f"{hashlib.sha256(changed.getvalue()).hexdigest()}  {archive.name}\n".encode("utf-8")
    )
    with pytest.raises(ValueError, match="MANIFEST.sha256"):
        canonical_bytes(root)
    with pytest.raises(ValueError, match="MANIFEST.sha256"):
        verifier.check_selected_archive(archive, root)

    before = {path.name: path.read_bytes() for path in root.iterdir()}
    monkeypatch.setattr(manifest_builder, "package_root", lambda: root)
    assert manifest_builder.main(["--check"]) == 1
    monkeypatch.setattr(archive_builder, "PACKAGE_ROOT", root)
    assert archive_builder.main(["--check", "--output", str(root / "dist")]) == 1
    assert {path.name: path.read_bytes() for path in root.iterdir()} == before


def test_secondary_manifest_cannot_include_either_control(envelope):
    root, _, _ = envelope
    secondary = root / "MANIFEST.sha256"
    original = secondary.read_text(encoding="utf-8")
    for name in ("SHA256SUMS", "MANIFEST.sha256"):
        secondary.write_text(original + f"{'0' * 64}  {name}\n", encoding="utf-8")
        (root / "SHA256SUMS").write_bytes(render(root).encode("utf-8"))
        primary = verifier.parse_manifest(root / "SHA256SUMS", root)
        assert f"file outside MANIFEST.sha256 coverage: {name}" in verifier.check_manifest_pair(
            primary, root
        )


def test_regeneration_refreshes_both_controls_after_payload_change(envelope, monkeypatch):
    root, _, _ = envelope
    (root / "payload.txt").write_text("new payload\n", encoding="utf-8")
    monkeypatch.setattr(archive_builder, "PACKAGE_ROOT", root)
    archive_builder.regenerate_manifest()
    primary = verifier.parse_manifest(root / "SHA256SUMS", root)
    assert verifier.check_hashes(primary, root) == []
    assert verifier.check_manifest_pair(primary, root) == []
    assert check_manifests(root) == []


def test_normalized_archive_has_valid_inner_and_outer_manifest(tmp_path):
    root = tmp_path / "source"
    root.mkdir()
    (root / "payload.txt").write_bytes(b"first\r\nsecond\rthird\n")
    regenerate(root)
    data = canonical_bytes(root)
    destination = tmp_path / "extracted"
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        archive.extractall(destination)
    extracted = destination / "projection_obstruction_paper"
    assert (extracted / "payload.txt").read_bytes() == b"first\nsecond\nthird\n"
    primary = verifier.parse_manifest(extracted / "SHA256SUMS", extracted)
    assert verifier.check_hashes(primary, extracted) == []
    assert verifier.check_manifest_pair(primary, extracted) == []
    assert check_manifests(extracted) == []


def test_nonregular_control_refused(envelope):
    root, archive, sidecar = envelope
    sidecar.unlink()
    sidecar.mkdir()
    with pytest.raises(ValueError, match="non-regular"):
        verifier.check_selected_archive(archive, root)


def test_traversal_failure_is_fatal(monkeypatch, tmp_path):
    def fail_walk(*args, onerror, **kwargs):
        onerror(PermissionError("unreadable retained directory"))
        yield
    monkeypatch.setattr("release_custody.os.walk", fail_walk)
    with pytest.raises(PermissionError, match="unreadable"):
        snapshot(tmp_path)
    with pytest.raises(PermissionError):
        traversal_error(PermissionError("denied"))


def test_nested_build_directory_is_payload(tmp_path):
    child = tmp_path / "retained" / "build"
    child.mkdir(parents=True)
    (child / "result.txt").write_text("retain", encoding="utf-8")
    assert "retained/build/result.txt" in snapshot(tmp_path)


def test_payload_mutation_after_verification_is_refused(envelope):
    root, _, _ = envelope
    initial = snapshot(root)
    (root / "payload.txt").write_text("changed", encoding="utf-8")
    with pytest.raises(ValueError, match="changed after initial"):
        unchanged(root, initial)


def test_replay_guard_runs_after_each_subprocess(monkeypatch, tmp_path):
    events = []
    def run(command, **kwargs):
        events.append(Path(command[1]).name)
        if "--output" in command:
            Path(command[-1]).write_text(json.dumps({"finite_certificates": {}}), encoding="utf-8")
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        return SimpleNamespace(returncode=0, stdout='{"verdict":"pass","errors":[]}\n', stderr="")
    monkeypatch.setattr(verifier.subprocess, "run", run)
    assert verifier.run_replay_and_certificate(tmp_path, guard=lambda: events.append("guard")) == []
    assert events == ["replay.py", "guard", "verify_certificate.py", "guard"]
    assert verifier.run_replay_and_certificate(tmp_path, profile="native") == [
        "native profile did not verify every measurement record"]


def test_err01_absent_archive_does_not_claim_archive_verified(monkeypatch, capsys):
    monkeypatch.setattr(verifier, "parse_manifest", lambda *a, **kw: {"payload.txt": "0" * 64})
    monkeypatch.setattr(verifier, "check_hashes", lambda *a, **kw: [])
    monkeypatch.setattr(verifier, "sweep_unlisted", lambda *a, **kw: [])
    monkeypatch.setattr(verifier, "check_required", lambda *a, **kw: [])
    monkeypatch.setattr(verifier, "check_manifest_pair", lambda *a, **kw: [])
    monkeypatch.setattr(verifier, "run_tests", lambda *a, **kw: (0, "1 passed", []))
    monkeypatch.setattr(verifier, "run_replay_and_certificate", lambda *a, **kw: [])
    monkeypatch.setattr(verifier, "check_archive_reproducibility", lambda *a, **kw: [])
    monkeypatch.setattr(verifier, "snapshot", lambda *a, **kw: {})
    monkeypatch.setattr(verifier, "unchanged", lambda *a, **kw: None)

    nonexistent = verifier.ROOT / "dist" / "nonexistent_archive_for_test.zip"

    args = verifier.argparse.Namespace(
        archive=None,
        require_archive=False,
        profile="standalone",
        integrity_only=False,
        lean_source_scan=False,
    )
    monkeypatch.setattr(verifier, "identity", lambda *a, **kw: {"release_version": "nonexistent_ver_999"})

    ret = verifier.verify(args)
    assert ret == 0
    captured = capsys.readouterr().out
    assert "bare repository payload verified" in captured
    assert "archive verification NOT performed" in captured
    assert "selected archive, Python tests and scoped replay verified" not in captured

    args_req = verifier.argparse.Namespace(
        archive=None,
        require_archive=True,
        profile="standalone",
        integrity_only=False,
        lean_source_scan=False,
    )
    with pytest.raises(ValueError, match="required release archive not found"):
        verifier.verify(args_req)

    args_missing = verifier.argparse.Namespace(
        archive=nonexistent,
        require_archive=False,
        profile="standalone",
        integrity_only=False,
        lean_source_scan=False,
    )
    with pytest.raises((ValueError, SystemExit, FileNotFoundError)):
        verifier.verify(args_missing)


def test_err01_valid_archive_claims_archive_verified(envelope, monkeypatch, capsys):
    root, archive, sidecar = envelope
    monkeypatch.setattr(verifier, "parse_manifest", lambda *a, **kw: {"payload.txt": "0" * 64})
    monkeypatch.setattr(verifier, "check_hashes", lambda *a, **kw: [])
    monkeypatch.setattr(verifier, "sweep_unlisted", lambda *a, **kw: [])
    monkeypatch.setattr(verifier, "check_required", lambda *a, **kw: [])
    monkeypatch.setattr(verifier, "check_manifest_pair", lambda *a, **kw: [])
    monkeypatch.setattr(verifier, "run_tests", lambda *a, **kw: (0, "1 passed", []))
    monkeypatch.setattr(verifier, "run_replay_and_certificate", lambda *a, **kw: [])
    monkeypatch.setattr(verifier, "check_archive_reproducibility", lambda *a, **kw: [])
    monkeypatch.setattr(verifier, "snapshot", lambda *a, **kw: {})
    monkeypatch.setattr(verifier, "unchanged", lambda *a, **kw: None)
    monkeypatch.setattr(
        verifier,
        "check_selected_archive",
        lambda *a, **kw: {str(archive): verifier.sha256_of(archive), str(sidecar): verifier.sha256_of(sidecar)},
    )

    args = verifier.argparse.Namespace(
        archive=archive,
        require_archive=False,
        profile="standalone",
        integrity_only=False,
        lean_source_scan=False,
    )
    ret = verifier.verify(args)
    assert ret == 0
    captured = capsys.readouterr().out
    assert "exact selected archive and sidecar verified" in captured
    assert "selected archive, Python tests and scoped replay verified." in captured
    assert "archive verification NOT performed" not in captured


def test_err02_strict_test_profile_rejects_xfail_and_requires_passes(tmp_path):
    root1 = tmp_path / "case1"
    tests1 = root1 / "code" / "tests"
    tests1.mkdir(parents=True)
    (tests1 / "test_xfail.py").write_text(
        "import pytest\n@pytest.mark.xfail\ndef test_bad():\n    assert False\n",
        encoding="utf-8",
    )
    ret, summary, problems = verifier.run_tests(root_dir=root1, profile="standalone")
    assert ret != 0 or len(problems) > 0

    root2 = tmp_path / "case2"
    tests2 = root2 / "code" / "tests"
    tests2.mkdir(parents=True)
    (tests2 / "test_mixed.py").write_text(
        "import pytest\ndef test_ok():\n    assert True\n@pytest.mark.xfail\ndef test_bad():\n    assert False\n",
        encoding="utf-8",
    )
    ret, summary, problems = verifier.run_tests(root_dir=root2, profile="standalone")
    assert ret != 0 or len(problems) > 0

    root3 = tmp_path / "case3"
    tests3 = root3 / "code" / "tests"
    tests3.mkdir(parents=True)
    (tests3 / "test_ok.py").write_text(
        "def test_good():\n    assert True\n",
        encoding="utf-8",
    )
    ret, summary, problems = verifier.run_tests(root_dir=root3, profile="standalone")
    assert ret == 0
    assert problems == []
    assert "1 passed" in summary
