"""Test Acceptance Criterion 3: Deterministic Replay and Certificate Verification.

Verifies:
In projection_obstruction_paper:
python code/replay.py --output <tmp>/replay-current.json
python code/verify_certificate.py <tmp>/replay-current.json
succeed with verdict: pass and errors: [].

AuthorityEffect: None.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from .config import PO000_DIR


def test_ac3_replay_and_certificate_verification(tmp_path: Path):
    """AC3: Execute replay mechanization and verify certificate validator emits verdict pass."""
    cert_path = tmp_path / "replay-current.json"

    # Step 1: Run replay.py to generate certificate
    replay_cmd = [
        sys.executable,
        "code/replay.py",
        "--output",
        str(cert_path),
    ]

    proc_replay = subprocess.run(
        replay_cmd,
        cwd=PO000_DIR,
        capture_output=True,
        text=True,
        timeout=180,
    )

    assert proc_replay.returncode == 0, (
        f"replay.py failed with exit code {proc_replay.returncode}:\n"
        f"STDOUT:\n{proc_replay.stdout}\n"
        f"STDERR:\n{proc_replay.stderr}"
    )

    assert cert_path.is_file(), f"Expected certificate output file was not created at {cert_path}"

    # Step 2: Validate certificate with independent verify_certificate.py
    verify_cmd = [
        sys.executable,
        "code/verify_certificate.py",
        str(cert_path),
    ]

    proc_verify = subprocess.run(
        verify_cmd,
        cwd=PO000_DIR,
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert proc_verify.returncode == 0, (
        f"verify_certificate.py failed with exit code {proc_verify.returncode}:\n"
        f"STDOUT:\n{proc_verify.stdout}\n"
        f"STDERR:\n{proc_verify.stderr}"
    )

    # Step 3: Parse output JSON and check contract
    try:
        report = json.loads(proc_verify.stdout.strip())
    except Exception as e:
        pytest.fail(f"verify_certificate.py stdout is not valid JSON ({e}):\n{proc_verify.stdout}")

    assert report.get("verdict") == "pass", (
        f"Certificate verifier verdict is not 'pass': {report.get('verdict')}\nFull report:\n{report}"
    )
    assert report.get("errors") == [], (
        f"Certificate verifier reported errors: {report.get('errors')}"
    )
    assert report.get("authority_effect") == "None", (
        f"Unexpected authority_effect in certificate: {report.get('authority_effect')}"
    )
