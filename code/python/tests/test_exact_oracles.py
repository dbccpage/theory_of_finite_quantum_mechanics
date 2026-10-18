import subprocess
import sys
from pathlib import Path

# Repo root is 3 levels up from code/python/tests/
repo_root = Path(__file__).resolve().parents[3]
oracles_dir = repo_root / "code" / "python" / "oracles"
dag_dir = repo_root / "dag"

if str(oracles_dir) not in sys.path:
    sys.path.insert(0, str(oracles_dir))
if str(dag_dir) not in sys.path:
    sys.path.insert(0, str(dag_dir))


def test_no_signalling_exact_rational_receipt():
    """Verify that no-signalling theorem holds exactly in Gaussian rational arithmetic Q(i)."""
    try:
        from src.qm.campaigns import no_signalling
    except ImportError:
        import no_signalling

    receipt = no_signalling.emit_no_signalling_receipt()
    assert receipt["verdict"] == "NO_SIGNALLING_DERIVED_FROM_ADMITTED_COMPOSITION"
    assert receipt["no_signalling_exact"] is True
    assert receipt["bell_states_checked_count"] == 4
    assert receipt["partial_trace_uniqueness"]["dim_2x2"] is True


def test_derivation_dag_structure_and_claim_hygiene():
    """Verify derivation DAG 177 nodes, 172 routes, acyclicity, and zero forbidden hype words."""
    dag_script = repo_root / "dag" / "validate_derivation_dag.py"
    res = subprocess.run(
        [sys.executable, str(dag_script), "--no-files"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert "failures=0" in res.stdout
