"""Build a curated manuscript preprint without modifying the historical archive."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from deposit_paths import safe_path

STAGE = ROOT / "zenodo" / "preprint"
FILES = (
    "mub6.md", "mub6.tex", "mub6.pdf", "render_binding.json", "LICENSE", "LICENSE-CODE",
    "zenodo_metadata.json", "release_identity.json", "docs/descriptions.md", "docs/references.md",
    "docs/keywords.md", "docs/quick_start.md", "scripts/build_pdf.py", "scripts/paper_code_wrap.lua",
    "scripts/verify_publication.py", "code/deposit_paths.py",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build() -> None:
    payload = {name: (ROOT / name).read_bytes() for name in FILES}
    payload["README.md"] = (ROOT / "docs/preprint_readme.md").read_bytes()
    expected_stage = set(payload) | {"MANIFEST.sha256", "SHA256SUMS"}
    if STAGE.exists():
        actual = {p.relative_to(STAGE).as_posix() for p in STAGE.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
        if actual - expected_stage:
            raise ValueError(f"Unmanaged staging files: {sorted(actual - expected_stage)}")
    def manifest(items):
        return "".join(f"{digest(data)}  {name}\n" for name, data in sorted(items.items())).encode("utf-8")
    payload["MANIFEST.sha256"] = manifest(payload)
    payload["SHA256SUMS"] = manifest(payload)
    for name, data in payload.items():
        destination = safe_path(STAGE, name)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.is_symlink():
            raise ValueError(f"Symlink in staging tree: {name}")
        destination.write_bytes(data)
    identity = json.loads(payload["release_identity.json"])
    year, month, day = map(int, identity["publication_date"].split("-"))
    archive = ROOT / "mub6_publication.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(payload.items()):
            info = zipfile.ZipInfo(name, (year, month, day, 12, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    archive.with_suffix(".zip.sha256").write_text(
        f"{digest(archive.read_bytes())}  {archive.name}\n", encoding="utf-8", newline="\n")
    subprocess.run([sys.executable, str(ROOT / "scripts/verify_publication.py"),
                    "--root", str(STAGE), "--archive", str(archive)], check=True, timeout=60)
    print(f"Prepared {archive.name}: {len(payload)} members. Publication approval remains outstanding.")


if __name__ == "__main__":
    build()
