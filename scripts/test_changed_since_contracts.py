"""Origin: scripts/test_changed_since_contracts.py
Claim: check --changed-since reads only the changed in-scope sources, passes when that set is empty, refuses a source with no companion, and does not rewrite the tracked coverage audit
AuthorityEffect: None
Scope Fence: this file does not score the estate and does not run the whole-tree check
Level: L4
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import contract_scores as scores  # noqa: E402
import score_scope_contracts as scope  # noqa: E402

PROBE = scope.ROOT / "code" / "python" / "_changed_since_probe.py"
# A deliberately corrupt companion, written for the test and removed after it. (The
# test used lean4/HilbertLiftOperators.contract.score.yaml until that file was repaired.)
BAD = "code/python/_changed_since_bad.contract.score.yaml"


def _audit_stamp():
    path = scope.AUDIT_PATH
    stat = path.stat()
    return stat.st_mtime_ns, stat.st_size, path.read_bytes()


def test_clean_change_passes_without_writing_the_audit():
    before = _audit_stamp()
    assert scope.main(["check", "--changed-since", "HEAD"]) == 0
    scores.main(["check", "--changed-since", "HEAD"])
    assert _audit_stamp() == before


def test_missing_companion_on_a_changed_source_is_refused_and_the_audit_stays():
    before = _audit_stamp()
    PROBE.write_text("probe = 1\n", encoding="utf-8", newline="\n")
    try:
        assert scope.main(["check", "--changed-since", "HEAD"]) == 1
        with pytest.raises(SystemExit) as caught:
            scores.main(["check", "--changed-since", "HEAD"])
        assert caught.value.code == 1
        assert _audit_stamp() == before
    finally:
        PROBE.unlink(missing_ok=True)


def test_an_empty_change_set_does_not_read_the_known_bad_companion():
    scores.check(changed=set())


def test_a_named_bad_companion_is_still_refused():
    bad = scope.ROOT / BAD
    bad.write_text('{"schema_version": "tfqm.contract-score.v1" "broken": true}\n', encoding="utf-8", newline="\n")
    try:
        with pytest.raises(SystemExit) as caught:
            scores.check(changed={BAD})
        assert caught.value.code == 1
    finally:
        bad.unlink(missing_ok=True)


def test_prepare_rejects_changed_since():
    with pytest.raises(SystemExit) as caught:
        scope.main(["prepare", "--changed-since", "HEAD"])
    assert caught.value.code == 2
