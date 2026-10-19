"""Tests for the 65-question QM Problem & Proof Atlas and textbook problem solvers (Q58-Q65)."""
from __future__ import annotations

from pathlib import Path
import sys
import subprocess
import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT / "code" / "python") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "code" / "python"))
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

from src.qm.textbook_problems import (  # noqa: E402
    build_qm_question_atlas,
    run_textbook_atlas,
    solve_q58_infinite_square_well,
    solve_q59_harmonic_oscillator_fock,
    solve_q60_potential_barrier_transfer,
    solve_q61_stern_gerlach_and_rabi,
    solve_q62_clebsch_gordan_two_spins,
    solve_q63_perturbation_and_stark,
    solve_q64_pancharatnam_berry_phase,
    solve_q65_fermi_golden_rule_and_revival,
)
from install_qm_atlas_hook import install_pre_commit_hook  # noqa: E402
from verify_qm_atlas_loc import verify_qm_atlas_loc  # noqa: E402


@pytest.fixture(autouse=True)
def isolate_git_configuration(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config = tmp_path / "empty_git_config"
    config.write_bytes(b"")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(config))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")


def test_textbook_problems_q58_to_q65_exact_invariants() -> None:
    q58 = solve_q58_infinite_square_well()
    assert q58["trace_l3"] == "6"
    assert q58["det_l3"] == "4"
    assert q58["mode_node_counts"] == [0, 1, 2]
    assert q58["sturm_oscillation_verified"] is True

    q59 = solve_q59_harmonic_oscillator_fock()
    assert q59["interior_energies"] == ["1/2", "3/2", "5/2"]
    assert q59["commutator_diagonal"] == ["1", "1", "1", "-3"]
    assert q59["commutator_trace"] == "0"
    assert q59["interior_canonical_spacing_verified"] is True

    q60 = solve_q60_potential_barrier_transfer()
    assert q60["transfer_det"] == "1"
    assert q60["sub_barrier_transmission"] == "16/25"
    assert q60["sub_barrier_reflection"] == "9/25"
    assert q60["flux_conservation_verified"] is True

    q61 = solve_q61_stern_gerlach_and_rabi()
    assert q61["two_filter_prob"] == "0"
    assert q61["three_filter_regeneration_prob"] == "1/4"
    assert q61["rabi_survival_prob"] == "49/625"
    assert q61["rabi_flip_prob"] == "576/625"
    assert q61["regeneration_and_unitarity_verified"] is True

    q62 = solve_q62_clebsch_gordan_two_spins()
    assert q62["singlet_projector_trace"] == "1"
    assert q62["triplet_projector_trace"] == "3"
    assert q62["singlet_casimir"] == "0"
    assert q62["triplet_casimir"] == "2"
    assert q62["decomposition_verified"] is True

    q63 = solve_q63_perturbation_and_stark()
    assert q63["rs_second_order_e1"] == "7/8"
    assert q63["rs_second_order_e2"] == "25/8"
    assert q63["stark_linear_splitting"] == "3/5"
    assert q63["secular_diagonalization_verified"] is True

    q64 = solve_q64_pancharatnam_berry_phase()
    assert q64["gauge_loop_factor_re"] == "1"
    assert q64["gauge_loop_factor_im"] == "0"
    assert q64["octant_bargmann_re"] == "1"
    assert q64["octant_bargmann_im"] == "1"
    assert q64["u1_rephasing_invariance_verified"] is True
    assert q64["octant_phase_tan_eq_one_verified"] is True

    q65 = solve_q65_fermi_golden_rule_and_revival()
    assert q65["short_time_exact_cayley"] == "400/10201"
    assert q65["short_time_fgr_quadratic"] == "1/25"
    assert q65["turnover_transition_prob"] == "1"
    assert q65["revival_survival_prob"] == "1"
    assert q65["onset_and_heisenberg_revival_verified"] is True


def test_qm_atlas_all_65_questions_and_loc_verifier() -> None:
    atlas = build_qm_question_atlas()
    assert len(atlas) == 65

    suite_report = run_textbook_atlas()
    assert suite_report["total_questions"] == 65
    assert suite_report["all_textbook_problems_verified"] is True
    assert suite_report["all_65_verified"] is True

    loc_report = verify_qm_atlas_loc(REPO_ROOT)
    assert loc_report["all_passed"] is True, f"LOC verifier errors: {loc_report}"
    assert loc_report["verified_links"] >= 400
    assert loc_report["verified_window_symbols"] >= 195
    assert loc_report["missing_q_ids"] == []
    assert loc_report["loc_errors"] == []
    assert loc_report["window_symbol_errors"] == []
    assert loc_report["symbol_errors"] == []
    assert loc_report["rust_python_parity"] is True
    assert loc_report["forbidden_hits"] == []


def test_qm_atlas_pre_commit_hook_installed(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    subprocess.run(["git", "init", "--quiet", str(repo)], check=True)
    hook_path = install_pre_commit_hook(repo)
    assert hook_path.is_file()
    hook_text = hook_path.read_text(encoding="utf-8")
    assert "scripts/verify_qm_atlas_loc.py" in hook_text
    assert "code/python/tests/test_qm_atlas_loc.py" in hook_text



def test_qm_atlas_hook_resolves_linked_worktree(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    worktree = tmp_path / "worktree"
    empty_hooks = tmp_path / "empty_hooks"
    empty_hooks.mkdir()
    subprocess.run(["git", "init", "--quiet", str(repo)], check=True)
    subprocess.run([
        "git", "-C", str(repo), "-c", "user.name=Atlas fixture", "-c",
        "user.email=atlas-fixture@example.invalid", "-c", "core.hooksPath=" + str(empty_hooks),
        "commit", "--allow-empty", "-m", "Fixture for linked worktree path resolution",
    ], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "worktree", "add", "--detach", str(worktree)],
                   check=True, capture_output=True)
    assert (worktree / ".git").is_file()
    hook = install_pre_commit_hook(worktree)
    expected = subprocess.check_output(
        ["git", "rev-parse", "--git-path", "hooks/pre-commit"], cwd=worktree, text=True,
    ).strip()
    expected_path = Path(expected)
    if not expected_path.is_absolute():
        expected_path = worktree / expected_path
    assert hook == expected_path.resolve()
    assert install_pre_commit_hook(worktree) == hook
    assert "scripts/verify_qm_atlas_loc.py" in hook.read_text(encoding="utf-8")


def test_qm_atlas_hook_preserves_unmanaged_hook(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    subprocess.run(["git", "init", "--quiet", str(repo)], check=True)
    hook = repo / ".git" / "hooks" / "pre-commit"
    original = b"#!/bin/sh\necho user-owned-hook\n"
    hook.write_bytes(original)
    with pytest.raises(ValueError, match="unmanaged"):
        install_pre_commit_hook(repo)
    assert hook.read_bytes() == original
