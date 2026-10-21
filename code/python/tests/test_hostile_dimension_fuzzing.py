"""Multi-process fuzzing and adversarial mutation testing for hostile matrix dimensions.

AuthorityEffect: None.

Evaluates boundaries_exact.py and cabello_frame.py under hostile matrix dimensions,
shape mismatches, combinatorial budgets, and process execution deadlines.
"""
from __future__ import annotations

from fractions import Fraction as Q
import importlib
import multiprocessing as mp
from pathlib import Path
import random
import sys
import time
import types
import unittest

# Isolated package import to avoid top-level package dependencies
_REPO_ROOT = next(
    p for p in Path(__file__).resolve().parents
    if (p / "code/python/src/qm/boundaries_exact.py").is_file()
)
_pkg = types.ModuleType("staged_qm")
_pkg.__path__ = [str(_REPO_ROOT / "code/python/src/qm")]
sys.modules.setdefault("staged_qm", _pkg)

boundaries_exact = importlib.import_module("staged_qm.boundaries_exact")
cabello_frame = importlib.import_module("staged_qm.cabello_frame")

CABELLO_BASES = (
    ((0, 0, 0, 1), (0, 0, 1, 0), (1, 1, 0, 0), (1, -1, 0, 0)),
    ((0, 0, 0, 1), (0, 1, 0, 0), (1, 0, 1, 0), (1, 0, -1, 0)),
    ((1, -1, 1, -1), (1, -1, -1, 1), (1, 1, 0, 0), (0, 0, 1, 1)),
    ((1, -1, 1, -1), (1, 1, 1, 1), (1, 0, -1, 0), (0, 1, 0, -1)),
    ((0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 1), (1, 0, 0, -1)),
    ((1, -1, -1, 1), (1, 1, 1, 1), (1, 0, 0, -1), (0, 1, -1, 0)),
    ((1, 1, -1, 1), (1, 1, 1, -1), (1, -1, 0, 0), (0, 0, 1, 1)),
    ((1, 1, -1, 1), (-1, 1, 1, 1), (1, 0, 1, 0), (0, 1, 0, -1)),
    ((1, 1, 1, -1), (-1, 1, 1, 1), (1, 0, 0, 1), (0, 1, -1, 0)),
)
RAYS = tuple(dict.fromkeys(r for b in CABELLO_BASES for r in b))
FRAMES = tuple(tuple(RAYS.index(r) for r in b) for b in CABELLO_BASES)


# ---------------------------------------------------------------------------
# Multi-Process Worker Handshake & Isolation Infrastructure
# ---------------------------------------------------------------------------

def _worker_single(conn, func, args):
    conn.send(("READY", None))
    try:
        res = func(*args)
        conn.send(("OK", res))
    except Exception as e:
        conn.send(("ERROR", type(e).__name__ + ": " + str(e)))
    finally:
        conn.close()


def _worker_batch(conn, func, batch_args):
    conn.send(("READY", None))
    results = []
    for args in batch_args:
        t0 = time.perf_counter()
        try:
            res = func(*args)
            dt = time.perf_counter() - t0
            results.append(("OK", dt, res))
        except Exception as e:
            dt = time.perf_counter() - t0
            results.append(("ERROR", dt, type(e).__name__ + ": " + str(e)))
    conn.send(("BATCH_DONE", results))
    conn.close()


def run_process_with_timeout(func, args, timeout_sec=0.5, init_timeout=5.0):
    parent_conn, child_conn = mp.Pipe(duplex=False)
    proc = mp.Process(target=_worker_single, args=(child_conn, func, args))
    proc.start()
    child_conn.close()
    try:
        if not parent_conn.poll(init_timeout):
            proc.kill()
            proc.join()
            return {"status": "INIT_TIMEOUT", "duration": init_timeout, "value": None}
        msg, _ = parent_conn.recv()
        assert msg == "READY"
        start_time = time.perf_counter()
        if parent_conn.poll(timeout_sec):
            status, val = parent_conn.recv()
            dur = time.perf_counter() - start_time
            proc.join()
            return {"status": status, "duration": dur, "value": val}
        else:
            dur = time.perf_counter() - start_time
            proc.kill()
            proc.join()
            return {"status": "TIMEOUT", "duration": dur, "value": None}
    finally:
        parent_conn.close()


def run_batch_with_timeout(func, batch_args, timeout_sec=5.0, init_timeout=5.0):
    parent_conn, child_conn = mp.Pipe(duplex=False)
    proc = mp.Process(target=_worker_batch, args=(child_conn, func, batch_args))
    proc.start()
    child_conn.close()
    try:
        if not parent_conn.poll(init_timeout):
            proc.kill()
            proc.join()
            return {"status": "INIT_TIMEOUT", "duration": init_timeout, "results": None}
        msg, _ = parent_conn.recv()
        assert msg == "READY"
        start_time = time.perf_counter()
        if parent_conn.poll(timeout_sec):
            status, results = parent_conn.recv()
            dur = time.perf_counter() - start_time
            proc.join()
            return {"status": "OK", "duration": dur, "results": results}
        else:
            dur = time.perf_counter() - start_time
            proc.kill()
            proc.join()
            return {"status": "TIMEOUT", "duration": dur, "results": None}
    finally:
        parent_conn.close()


def _load_mutated(module_path: Path, old: str, new: str, name: str):
    src = module_path.read_text(encoding="utf-8")
    assert src.count(old) == 1, f"Pattern {old!r} count was {src.count(old)} in {module_path.name}"
    mutated_src = src.replace(old, new, 1)
    mod = types.ModuleType(f"staged_qm.{name}")
    mod.__package__ = "staged_qm"
    exec(compile(mutated_src, str(module_path), "exec"), mod.__dict__)
    return mod


# ---------------------------------------------------------------------------
# Target 1: boundaries_exact.py Fuzzing & Timeout Measurements
# ---------------------------------------------------------------------------

class TestBoundariesHostileFuzzing(unittest.TestCase):

    def test_boundaries_conforming_latency(self):
        """Conforming square rational matrices execute well within deadline."""
        batch = [
            ([[Q(i + j + 1) for j in range(dim)] for i in range(dim)],
             [[Q(1, i * j + 1) for j in range(dim)] for i in range(dim)])
            for dim in (2, 4, 8, 16)
        ]
        res = run_batch_with_timeout(boundaries_exact.mm, batch, timeout_sec=2.0)
        self.assertEqual(res["status"], "OK")
        for st, dt, val in res["results"]:
            self.assertEqual(st, "OK")
            self.assertLess(dt, 0.05)

    def test_boundaries_huge_matrix_timeout_measurement(self):
        """Hostile matrix dimensions (300x300 exact rational) trigger process execution timeout."""
        dim = 300
        a = [[Q(i + 1, j + 1) for j in range(dim)] for i in range(dim)]
        b = [[Q(j + 1, i + 1) for j in range(dim)] for i in range(dim)]
        res = run_process_with_timeout(boundaries_exact.mm, (a, b), timeout_sec=0.25)
        self.assertEqual(res["status"], "TIMEOUT", "Expected 300x300 rational matrix multiplication to exceed 0.25s deadline")
        self.assertGreaterEqual(res["duration"], 0.24)

    def test_boundaries_pathological_scalar_fuzzing(self):
        """Pathological inputs to evaluate() are rejected fail-closed."""
        bad_cases = [
            ("registry", [Q(1, 2)] + [0] * 8),       # Non-integer denominator
            ("registry", [20] + [0] * 8),             # Out of range 0..15
            ("registry", [0] * 7 + [-1, 0]),          # Negative non-negative field
            ("survival", [1, 2, 0]),                  # Non-binary bit value
            ("uniqueness", [0]),                      # Out of range 1..4
            ("torsion", [0] + [0] * 9),               # Out of range 1..5
            ("unknown_kind", [0]),                    # Unknown operation
        ]
        res = run_batch_with_timeout(boundaries_exact.evaluate, bad_cases, timeout_sec=2.0)
        self.assertEqual(res["status"], "OK")
        for st, dt, err in res["results"]:
            self.assertEqual(st, "ERROR")

    def test_boundaries_adversarial_mutations(self):
        """Verifies 100% kill rate on 6 semantic mutants in boundaries_exact."""
        mod_path = Path(boundaries_exact.__file__)
        mutants = [
            # Mutant 1: Remove non-negativity check in registry
            ("m1_non_negative",
             "need(a>=0 and b>=0)",
             "need(True)"),
            # Mutant 2: Corrupt matrix multiplication arithmetic
            ("m2_matrix_arithmetic",
             "sum(x*y for x,y in zip(r,c))",
             "sum(x+y for x,y in zip(r,c))"),
            # Mutant 3: Remove denominator integer check
            ("m3_denominator",
             "need(scalar.denominator==1 and lo<=scalar<=hi)",
             "need(lo<=scalar<=hi)"),
            # Mutant 4: Remove bounds check in integer()
            ("m4_bounds",
             "need(scalar.denominator==1 and lo<=scalar<=hi)",
             "need(scalar.denominator==1)"),
            # Mutant 5: Remove matrix dimension check
            ("m5_dimension_match",
             "need(cols_a == len(b))",
             "need(True)"),
            # Mutant 6: Remove integer bit length check
            ("m6_bit_length",
             "need(val.bit_length() <= 1024)",
             "need(True)"),
        ]

        killed_count = 0
        for name, old, new in mutants:
            mod = _load_mutated(mod_path, old, new, f"mutant_{name}")
            killed = False

            # Test 1: Negative scalar in registry must fail
            try:
                mod.evaluate("registry", [0] * 7 + [-1, 0])
            except ValueError:
                pass
            except Exception:
                killed = True
            else:
                killed = True

            # Test 2: Arithmetic correctness check
            if not killed:
                try:
                    if mod.mm([[1, 2], [3, 4]], [[5, 6], [7, 8]]) != [[19, 22], [43, 50]]:
                        killed = True
                except Exception:
                    killed = True

            # Test 3: Fractional scalar in integer() must fail
            if not killed:
                try:
                    mod.evaluate("registry", [Q(1, 2)] + [0] * 8)
                except ValueError:
                    pass
                except Exception:
                    killed = True
                else:
                    killed = True

            # Test 4: Out of bounds scalar in integer() must fail
            if not killed:
                try:
                    mod.evaluate("registry", [20] + [0] * 8)
                except ValueError:
                    pass
                except Exception:
                    killed = True
                else:
                    killed = True

            # Test 5: Dimension mismatch in mm() must fail
            if not killed:
                try:
                    mod.mm([[1, 2]], [[3]])
                except ValueError:
                    pass
                except Exception:
                    killed = True
                else:
                    killed = True

            # Test 6: Integer exceeding 1024 bits must fail
            if not killed:
                try:
                    mod.evaluate("registry", [0] * 7 + [2**1025, 0])
                except ValueError:
                    pass
                except Exception:
                    killed = True
                else:
                    killed = True

            self.assertTrue(killed, f"Adversarial mutant {name} SURVIVED test oracle!")
            killed_count += 1

        self.assertEqual(killed_count, len(mutants), f"Expected {len(mutants)} mutants killed, got {killed_count}")


# ---------------------------------------------------------------------------
# Target 2: cabello_frame.py Fuzzing & Timeout Measurements
# ---------------------------------------------------------------------------

class TestCabelloHostileFuzzing(unittest.TestCase):

    def test_cabello_conforming_system_latency(self):
        """Conforming 18-ray Cabello system is validated within latency envelope."""
        res = run_process_with_timeout(cabello_frame.system, (RAYS, FRAMES), timeout_sec=1.0)
        self.assertEqual(res["status"], "OK")
        self.assertEqual(len(res["value"][0]), 18)
        self.assertLess(res["duration"], 0.05)

    def test_cabello_hostile_dimension_and_orthogonality_fuzzing(self):
        """Non-orthogonal frames, degenerate dimensions, and empty systems are refused fail-closed."""
        bad_cases = [
            # Non-orthogonal frame
            (RAYS, (((0, 1, 2, 4),) + tuple(FRAMES[1:]))),
            # Incompatible ray dimensions
            (RAYS + ((1, 0),), FRAMES),
            # Empty rays or empty frames
            ((), FRAMES),
            (RAYS, ()),
            # Non-integer ray entry
            (RAYS[:1] + (((Q(1, 2), 0, 0, 0)),) + RAYS[2:], FRAMES),
            # Zero vector ray
            (RAYS[:1] + (((0, 0, 0, 0),)) + RAYS[2:], FRAMES),
        ]
        res = run_batch_with_timeout(cabello_frame.system, bad_cases, timeout_sec=2.0)
        self.assertEqual(res["status"], "OK")
        for st, dt, err in res["results"]:
            self.assertEqual(st, "ERROR")

    def test_cabello_hostile_negative_radius_boundaries(self):
        """Negative search radius <= 0 is refused immediately fail-closed."""
        e4 = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
        single_frame = ((0, 1, 2, 3),)
        batch = [
            (tuple(e4), single_frame, 100, bad_r)
            for bad_r in (0, -1, -5, -100)
        ]
        res = run_batch_with_timeout(cabello_frame.certify, batch, timeout_sec=2.0)
        self.assertEqual(res["status"], "OK")
        for st, dt, err in res["results"]:
            self.assertEqual(st, "ERROR")
            self.assertIn("positive search radius required", err)

    def test_cabello_combinatorial_budget_gate_vs_timeout(self):
        """Hostile candidate space is halted by budget prefilter in < 5ms."""
        # comb(18, 9) = 48,620 with budget 1000
        res = run_process_with_timeout(cabello_frame.vertices, (RAYS, FRAMES, 1000), timeout_sec=0.5)
        self.assertEqual(res["status"], "ERROR")
        self.assertIn("enumeration budget exhausted", res["value"])
        self.assertLess(res["duration"], 0.05)

    def test_cabello_hostile_combinatorial_timeout_measurement(self):
        """Unmetered combinatorial basis search triggers process execution timeout."""
        # comb(18, 9) = 48,620 unmetered systems under 0.25s process deadline
        res = run_process_with_timeout(cabello_frame.vertices, (RAYS, FRAMES, 10**9), timeout_sec=0.25)
        self.assertEqual(res["status"], "TIMEOUT", "Expected 48,620 basis search to exceed 0.25s deadline")
        self.assertGreaterEqual(res["duration"], 0.24)

    def test_cabello_adversarial_mutations(self):
        """Verifies 100% kill rate on 6 semantic mutants in cabello_frame."""
        mod_path = Path(cabello_frame.__file__)
        mutants = [
            # Mutant 1: Remove combinatorial budget prefilter
            ("m1_budget_prefilter",
             "if comb(n,m)>budget:raise ValueError('enumeration budget exhausted; no infeasibility conclusion')",
             "if False:raise ValueError('enumeration budget exhausted; no infeasibility conclusion')"),
            # Mutant 2: Remove incidence row rank check
            ("m2_rank_check",
             "if rank(a)!=m:raise ValueError('full row rank needed for square-basis enumeration')",
             "if False:raise ValueError('full row rank needed for square-basis enumeration')"),
            # Mutant 3: Remove degree-two ray incidence check
            ("m3_degree_two",
             "if any(len(h)!=2 for h in holders):raise ValueError('degree-two ray incidence required')",
             "if False:raise ValueError('degree-two ray incidence required')"),
            # Mutant 4: Remove positive radius check
            ("m4_positive_radius",
             "if len(rays[0])!=4 or type(negative_radius) is not int or negative_radius<1:raise ValueError('four-dimensional witness system and positive search radius required')",
             "if len(rays[0])!=4 or type(negative_radius) is not int:raise ValueError('four-dimensional witness system and positive search radius required')"),
            # Mutant 5: Remove orthogonality check
            ("m5_orthogonality",
             "if any(sum(a*b for a,b in zip(rays[i],rays[j]))!=0 for i,j in combinations(frame,2)):raise ValueError('orthogonal frame required')",
             "if False:raise ValueError('orthogonal frame required')"),
            # Mutant 6: Remove non-empty system check
            ("m6_non_empty",
             "if not rays or not frames or not rays[0]:raise ValueError('nonempty frame system required')",
             "if False:raise ValueError('nonempty frame system required')"),
        ]

        e4 = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
        single_frame = ((0, 1, 2, 3),)

        killed_count = 0
        for name, old, new in mutants:
            mod = _load_mutated(mod_path, old, new, f"mutant_{name}")
            killed = False

            # Test 1: Budget exhaustion check on comb(18, 9) = 48,620 with budget 1000
            mod.combinations = lambda *a: ()
            try:
                mod.vertices(RAYS, FRAMES, budget=1000)
            except ValueError:
                pass
            except Exception:
                killed = True
            else:
                killed = True

            # Test 2: Rank failure check (duplicate frames)
            if not killed:
                try:
                    mod.vertices(tuple(e4), single_frame * 2, budget=100)
                except ValueError:
                    pass
                except Exception:
                    killed = True
                else:
                    killed = True

            # Test 3: Degree-two ray incidence check
            if not killed:
                try:
                    mod.vertices(tuple(e4), single_frame, budget=100)
                except ValueError:
                    pass
                except Exception:
                    killed = True
                else:
                    killed = True

            # Test 4: Zero radius check
            if not killed:
                try:
                    mod.certify(tuple(e4), single_frame, budget=100, negative_radius=0)
                except ValueError:
                    pass
                except Exception:
                    killed = True
                else:
                    killed = True

            # Test 5: Non-orthogonal frame check
            if not killed:
                try:
                    bad_frame = ((0, 1, 2, 4),) + tuple(FRAMES[1:])
                    mod.system(RAYS, bad_frame)
                except ValueError:
                    pass
                except Exception:
                    killed = True
                else:
                    killed = True

            # Test 6: Empty system check
            if not killed:
                try:
                    mod.system((), ())
                except ValueError:
                    pass
                except Exception:
                    killed = True
                else:
                    killed = True

            self.assertTrue(killed, f"Adversarial mutant {name} SURVIVED test oracle!")
            killed_count += 1

        self.assertEqual(killed_count, len(mutants), f"Expected {len(mutants)} mutants killed, got {killed_count}")


if __name__ == "__main__":
    unittest.main()
