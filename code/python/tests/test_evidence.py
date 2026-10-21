"""Tests for evidence.py verification routines and fail-closed admission."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import pytest

from src.qm.evidence import verify_bets


def _init_test_repo(repo: Path):
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    cargo = repo / "omega_engine" / "crates_rs"
    cargo.mkdir(parents=True)
    (cargo / "Cargo.toml").write_text("[package]\nname = 'test'\n", encoding="utf-8")


def test_verify_bets_refuses_duplicate_and_contradictory_bets(tmp_path: Path):
    """Finding 1 reproduction: verify_bets must fail-closed on duplicate bet IDs."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_test_repo(repo)

    prefix = repo / "omega_engine_projects" / "finite_qm" / "campaigns" / "c750"
    prefix.mkdir(parents=True)

    # Malformed registry with duplicate bet ID and contradictory hash
    registry = {
        "citation": "test_citation",
        "sealed_targets": [
            {
                "bet_id": "BET-CLAUDE-C750-B01",
                "sha256": "a186b28c53bca455085fcb07cd01fad27245c2f24a0a9a752c656bf3080492ef",
            },
            {
                "bet_id": "BET-JC-C750-B01",
                "sha256": "c6e481932897f8555cf92d862c99674a07b0bc6fc7c964f4f94d7fb34b2490c0",
            },
            {
                "bet_id": "BET-CLAUDE-C750-B01",
                "sha256": "bad0000000000000000000000000000000000000000000000000000000000000",
            },
        ],
    }
    (prefix / "sealed_targets.json").write_text(json.dumps(registry), encoding="utf-8")

    # Add an unrevealed plaintext file in an arbitrary directory in the prefix tree
    extra_dir = prefix / "nested" / "deep_folder"
    extra_dir.mkdir(parents=True)
    (extra_dir / "BET-CLAUDE-C750-B01.txt").write_text("plaintext secret", encoding="utf-8")

    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "initial commit"], cwd=repo, check=True, capture_output=True)

    rev = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo).decode().strip()

    receipt = verify_bets(repo, rev)

    assert receipt["verified"] is False
    assert receipt["b01_digests_matched"] is False
    assert receipt["refusal_reason"] is not None
    assert "Duplicate bet entries in registry" in receipt["refusal_reason"]
    assert "BET-CLAUDE-C750-B01" in receipt["details"]["duplicate_bets_found"]
    assert receipt["details"]["checked_paths_count"] >= 2


def test_verify_bets_refuses_unrevealed_plaintext(tmp_path: Path):
    """Finding 1 reproduction: verify_bets must fail-closed if plaintext exists anywhere in tree."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_test_repo(repo)

    prefix = repo / "omega_engine_projects" / "finite_qm" / "campaigns" / "c750"
    prefix.mkdir(parents=True)

    registry = {
        "citation": "test_citation",
        "sealed_targets": [
            {
                "bet_id": "BET-CLAUDE-C750-B01",
                "sha256": "a186b28c53bca455085fcb07cd01fad27245c2f24a0a9a752c656bf3080492ef",
            },
            {
                "bet_id": "BET-JC-C750-B01",
                "sha256": "c6e481932897f8555cf92d862c99674a07b0bc6fc7c964f4f94d7fb34b2490c0",
            },
        ],
    }
    (prefix / "sealed_targets.json").write_text(json.dumps(registry), encoding="utf-8")

    # Add an unrevealed plaintext file in an arbitrary directory in the prefix tree
    extra_dir = prefix / "nested" / "additional_folder"
    extra_dir.mkdir(parents=True)
    (extra_dir / "BET-JC-C750-B01.txt").write_text("plaintext secret", encoding="utf-8")

    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "initial commit"], cwd=repo, check=True, capture_output=True)

    rev = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo).decode().strip()

    receipt = verify_bets(repo, rev)

    assert receipt["verified"] is False
    assert receipt["refusal_reason"] is not None
    assert "Unrevealed bet plaintext(s) found in executor path" in receipt["refusal_reason"]
    assert len(receipt["readable_plaintexts_found"]) == 1


def test_verify_bets_invalid_schema(tmp_path: Path):
    """Schema validation errors must raise ValueError."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_test_repo(repo)

    prefix = repo / "omega_engine_projects" / "finite_qm" / "campaigns" / "c750"
    prefix.mkdir(parents=True)

    (prefix / "sealed_targets.json").write_text(json.dumps(["not a dict"]), encoding="utf-8")

    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "initial commit"], cwd=repo, check=True, capture_output=True)

    rev = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo).decode().strip()

    with pytest.raises(ValueError, match="INVALID_SEALED_TARGETS_OBJECT"):
        verify_bets(repo, rev)
