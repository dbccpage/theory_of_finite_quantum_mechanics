"""
End-to-End (E2E) Test Suite for PO-000 Projection Obstruction.
Verifies complete system workflow execution from CLI commands down to full
certificate generation and verification.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

_code_dir = Path(__file__).resolve().parents[1]
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

import replay
import artifact_bundle
import verify_certificate


def test_cli_e2e_workflow():
    """Verify full CLI execution workflow of replay -> bundle -> verify."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        cert_path = tmp_path / "mechanization_run.json"
        man_path = tmp_path / "SHA256SUMS"

        # Step 1: Replay CLI
        ret_replay = replay.main(["--output", str(cert_path)])
        assert ret_replay == 0
        assert cert_path.exists()

        # Step 2: Bundle CLI
        ret_bundle = artifact_bundle.main(["--certificate", str(cert_path), "--manifest", str(man_path)])
        assert ret_bundle == 0
        assert man_path.exists()
        assert b"\r\n" not in cert_path.read_bytes()
        assert b"\r\n" not in man_path.read_bytes()

        # Step 3: Verifier CLI
        ret_verify = verify_certificate.main([str(cert_path)])
        assert ret_verify == 0
