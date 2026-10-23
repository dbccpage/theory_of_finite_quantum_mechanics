"""Verify LP refusal behavior in ordinary and optimized Python subprocesses."""
from pathlib import Path
import subprocess
import sys
import pytest

CHECKER = Path(__file__).resolve().parents[1] / 'checks/independent/foc035_observer_presheaf.py'

@pytest.mark.parametrize('optimized', [False, True])
@pytest.mark.parametrize('arguments', [
    '([1], [[1]], [1], [0], [0])',  # primal infeasible
    '([1], [[1]], [1], [1], [2])',  # dual infeasible
    '([1], [[1]], [1], [1], [0])',  # positive gap
    '([1], [[1]], [-1], [-1], [1])',  # negative primal
    '([1], [[1]], [1], [], [1])',
    '([1], [[1, 2]], [1], [1], [1])',
    '([1], [[1]], [1], [1], [])',
    '([1.0], [[1]], [1], [1], [1])',
    '([True], [[1]], [1], [1], [1])',
])
def test_invalid_certificate_is_refused(optimized, arguments):
    code = f"import runpy; d=runpy.run_path({str(CHECKER)!r}); d['verify_lp']{arguments}"
    result = subprocess.run([sys.executable, '-I', *(['-O'] if optimized else []), '-c', code], capture_output=True, text=True)
    assert result.returncode != 0
    assert 'ValueError:' in result.stderr

@pytest.mark.parametrize('optimized', [False, True])
def test_valid_exact_certificate_is_accepted(optimized):
    code = f"import runpy; from fractions import Fraction as F; d=runpy.run_path({str(CHECKER)!r}); print(d['verify_lp']([F(1,2)],[[1]],[1],[1],[F(1,2)]))"
    result = subprocess.run([sys.executable, '-I', *(['-O'] if optimized else []), '-c', code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == '1/2'
