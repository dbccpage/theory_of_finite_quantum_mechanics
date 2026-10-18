from __future__ import annotations
"""
Integration Test Suite for PO-000 Projection Obstruction.
Verifies multi-module integration between exact arithmetic, cochain presentation,
quantum lattice simulation, evidence serialization, and independent verification.
"""


import sys
import json
import tempfile
from pathlib import Path
from fractions import Fraction
import pytest

_code_dir = Path(__file__).resolve().parents[2] / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

import omega_engine.crates.projection_obstruction.po000_replay as replay
import omega_engine.crates.projection_obstruction.verify_certificate as verify_certificate
import omega_engine.crates.projection_obstruction.artifact_bundle as artifact_bundle
from omega_engine.crates.projection_obstruction.worked_examples import pass45_counterexample_replay
from omega_engine.crates.projection_obstruction.falsification_sandbox import run_all_breaks, assert_all_breaks_trip


def test_full_pipeline_integration():
    """Verify end-to-end integration across replay, artifact bundle, and verifier."""
    # 1. Run aggregate claim replay
    run = replay.build_mechanization_run()
    assert run.execution_completed
    assert run.executable_checks_passed
    assert run.paper_id == "PO-000"

    # 2. Run falsification sandbox
    breaks = run_all_breaks()
    assert len(breaks) == 4
    assert_all_breaks_trip(breaks)

    # 3. Write artifact bundle and verify certificate
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        cert_file = tmp_path / "cert.json"
        man_file = tmp_path / "SHA256SUMS"

        artifact_bundle.write_artifact_bundle(cert_file, man_file)
        assert cert_file.exists()
        assert man_file.exists()

        data = json.loads(cert_file.read_text(encoding="utf-8"))
        errors = verify_certificate.verify_document(data, verify_certificate.RELEASE_ROOT)
        assert errors == [], f"Independent verifier reported errors: {errors}"


