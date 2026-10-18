"""Exercise the catalog CLI against a real index containing release artifacts."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import yaml

PAPER = Path(__file__).resolve().parents[2]
ENTRYPOINT = Path("python/src/qm/entrypoints/review_estate.py")


def test_tracked_release_outputs_cannot_enter_catalog_cycle(tmp_path: Path) -> None:
    root = tmp_path / "checkout"
    workspace_marker = root / "omega_engine/crates_rs/Cargo.toml"
    workspace_marker.parent.mkdir(parents=True)
    workspace_marker.write_text("[workspace]\n")
    paper = root / "omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm"
    entrypoint = paper / ENTRYPOINT
    entrypoint.parent.mkdir(parents=True)
    shutil.copyfile(PAPER / ENTRYPOINT, entrypoint)
    (paper / "README.md").write_text("Reviewed source.\n")
    catalog = paper / "finite_qm_file_manifest.yaml"
    catalog.write_text("metadata: {}\nfiles: []\n")
    (paper / "SHA256SUMS").write_text("A separate generated checksum catalog.\n")
    outputs = [
        paper / "dist/v0.54.1/release.zip",
        paper / "dist/v0.54.1/receipt.json",
        paper / "earlier_release.ZIP",
    ]
    for path in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"First release bytes.\n")
    historical_archive = paper / "sources/frozen/historical.zip"
    historical_archive.parent.mkdir(parents=True)
    historical_archive.write_bytes(b"Historical evidence bytes.\n")
    subprocess.run(["git", "init", "--quiet", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)

    def run(mode: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(entrypoint), mode, "--manifest", "--paper-only"],
            cwd=paper,
            capture_output=True,
            text=True,
            check=False,
        )

    written = run("--write")
    assert written.returncode == 0, written.stdout + written.stderr
    rows = yaml.safe_load(catalog.read_text())["files"]
    assert {row["path"] for row in rows} == {
        "README.md", ENTRYPOINT.as_posix(), "sources/frozen/historical.zip"
    }
    original_catalog = catalog.read_bytes()

    for path in outputs:
        path.write_bytes(b"Rebuilt release bytes.\n")
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    checked = run("--check")
    assert checked.returncode == 0, checked.stdout + checked.stderr
    assert catalog.read_bytes() == original_catalog

    historical_archive.write_bytes(b"Altered historical evidence.\n")
    checked = run("--check")
    assert checked.returncode != 0
    assert "Paper file manifest differs" in checked.stderr
    historical_archive.write_bytes(b"Historical evidence bytes.\n")

    (paper / "README.md").write_text("Unreviewed changed source.\n")
    checked = run("--check")
    assert checked.returncode != 0
    assert "Paper file manifest differs" in checked.stderr
