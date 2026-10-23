"""Source-byte mutations must fail independently of the release manifests."""
import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify_package import ROOT, verify_grammars, verify_references, verify_sources


def test_current_sources_links_and_grammar_controls():
    assert verify_sources() == 34
    assert verify_references() >= 8
    counts = verify_grammars()
    assert set(counts) == {"pre_genesis", "sn", "mssn"}
    assert all(x > 0 for x in counts.values())


@pytest.mark.parametrize("mutation", ["newline", "text", "missing"])
def test_changed_source_refused(tmp_path, mutation):
    manifest = json.loads((ROOT / "manifests/imported_sources.json").read_text(encoding="utf-8"))
    (tmp_path / "manifests").mkdir()
    shutil.copyfile(ROOT / "manifests/imported_sources.json", tmp_path / "manifests/imported_sources.json")
    for row in manifest["files"]:
        dest = tmp_path / row["path"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / row["path"], dest)
    target = tmp_path / manifest["files"][0]["path"]
    if mutation == "missing":
        target.unlink()
    else:
        original = target.read_bytes()
        target.write_bytes(original.replace(b"\n", b"\r\n") if mutation == "newline" else original+b"changed")
    with pytest.raises((ValueError, FileNotFoundError)):
        verify_sources(tmp_path)
