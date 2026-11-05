"""Source identity controls independent of the companion's checksum claims."""
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
from audit_source import AuditFailure
from verify_sources import check_references, check_sources, verify_origin


def test_all_citations_and_exact_pinned_blobs():
    result = check_sources()
    assert result["exact_pinned_mechanization_blobs"] == 120
    assert result["cited_source_records"] == 38
    assert result["local_manuscript_references"] >= 25


@pytest.mark.parametrize("change", [lambda data: data.replace(b"\n", b"\r\n"),
                                   lambda data: data + b"altered\n"])
def test_source_mutation_fails_even_with_rewritten_companion_hashes(change):
    manifest = json.loads((ROOT / "manifests/cited_sources.json").read_text(encoding="utf-8"))
    record = next(row for row in manifest["files"] if row["source"] == "code/derivation/model.py")
    original = (ROOT / record["path"]).read_bytes()
    data = change(original)
    rewritten = dict(record, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                     git_blob_sha1=hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest())
    origin = {"git_blob_sha1": record["git_blob_sha1"], "size_bytes": len(original)}
    with pytest.raises(AuditFailure, match="pinned Git inventory"):
        verify_origin(data, rewritten, origin)


@pytest.mark.parametrize("manuscript", [
    "[private](https://github.com/dbccpage/19L57G1/blob/main/paper/paper.md)",
    "[escape](../paper.md)",
    "[missing](code/absent.py)",
    "[line](code/derivation/model.py#L999999)",
    "[unrecorded](code/derivation/model.py)",
    "[undefined][missing]",
    "[same]: README.md\n[same]: paper.md\n",
])
def test_unfollowable_or_unpinned_citation_fails(manuscript):
    with pytest.raises((AuditFailure, OSError)):
        check_references(ROOT, manuscript, set())
