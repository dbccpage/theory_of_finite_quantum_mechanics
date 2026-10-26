"""Concrete independent witness controls; full stage cases use the domain predicate."""
import importlib.util, json, sys, unittest
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'dag/pfp/prepare_stage.py').exists())
spec = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/l1_import_exact.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
sys.path.insert(0, str(ROOT / 'dag/pfp'))
from l1_import_checker import verify

B = ROOT / 'dag/results/batches/20261019T232430Z_prompts_112_131'
rows = json.loads((B / 'tools/witness_cases.json').read_bytes())


class ExactControls(unittest.TestCase):
    def test_adversarial_rejections(self):
        # 1. Float rejection
        with self.assertRaises(TypeError):
            m.evaluate("edge", [1.0, 2, 3, 4])
        # 2. Boolean rejection
        with self.assertRaises(TypeError):
            m.evaluate("edge", [True, 2, 3, 4])
        # 3. 1025-bit integer rejection
        huge = 1 << 1025
        with self.assertRaises(ValueError):
            m.evaluate("edge", [huge, 2, 3, 4])
        # 4. Domain validation without assert bypass
        with self.assertRaises(ValueError):
            m.evaluate("circle", [5])
        with self.assertRaises(ValueError):
            m.evaluate("time", [0])
        with self.assertRaises(ValueError):
            m.evaluate("hilbert", [9])


def _make_test(row):
    def run(self):
        y = m.evaluate(row['kind'], row['input'])
        i = row['start']
        self.assertEqual(y[i:i + len(row['expected'])], row['expected'])
        verify(row['kind'], row['input'], y)
    return run


for row in rows:
    setattr(ExactControls, 'test_' + row['kind'], _make_test(row))

if __name__ == '__main__':
    unittest.main()


def test_bounded_rational_grammar_and_exact_arity():
    from fractions import Fraction
    import pytest
    class FractionOverride(Fraction):
        @property
        def numerator(self):
            raise AssertionError("untrusted scalar method executed")
    for value in ["1e1000000000", "1.25", "1_000", "1/0", 1 << 1024, Fraction(1, 1 << 1024)]:
        with pytest.raises((ValueError, ZeroDivisionError)):
            m.evaluate("edge", [value, 2, 3, 4])
    with pytest.raises(TypeError):
        m.evaluate("edge", [FractionOverride(1), 2, 3, 4])
    for kind, values in [("circle", []), ("circle", [2, 3]), ("kkt", [1] * 11),
                         ("quotient", [1] * 10), ("mass", []), ("unknown", [])]:
        with pytest.raises(ValueError):
            m.evaluate(kind, values)
    assert m.evaluate("edge", ["3/5", "4/5", 1, 1])[:2] == ["3/5", "4/5"]


def test_domain_checks_survive_optimization():
    import subprocess
    script = f"""
import importlib.util
spec = importlib.util.spec_from_file_location('subject', {str(ROOT / 'code/python/src/qm/l1_import_exact.py')!r})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
for kind, values in [('circle', [5]), ('time', [0]), ('hilbert', [9]), ('dilation', [2, 0, -1])]:
    try:
        module.evaluate(kind, values)
    except ValueError:
        continue
    raise SystemExit('invalid domain admitted under -O: ' + kind)
"""
    subprocess.run([sys.executable, "-I", "-O", "-c", script], check=True, capture_output=True, text=True)
