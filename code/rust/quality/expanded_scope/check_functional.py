"""Source-bound primal/dual certificate, ownership and checker challenges."""
from pathlib import Path
import sys

import check_entrypoints as core

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "code/python"))
from src.functional import test_exported_zero_phi1 as exported
sys.path.insert(0, str(ROOT / "code/python/tests"))
import test_l1_seminorm as backend_checks

SPECS = {
    "src.functional.l1_seminorm": {
        "source": "code/python/src/functional/l1_seminorm.py",
        "old_tests": "code/python/tests/test_l1_seminorm.py",
        "mutants": [
            *backend_checks._MUTANTS,
            ("Fraction subclass arithmetic admitted", "if type(value) is Fraction:", "if isinstance(value, Fraction):"),
            ("raw mutable certificate fields retained", "return (omega, rows, weights, alpha, residual, dual, reported)", "return (cert.omega, cert.d0, cert.weights, cert.alpha, cert.primal_residual, cert.dual_witness, reported)"),
            ("public verified constructor bypassed", "parts = _verified_parts(certificate, presentation)", "parts = (tuple(certificate.omega), tuple(tuple(row) for row in certificate.d0), tuple(certificate.weights), tuple(certificate.alpha), tuple(certificate.primal_residual), tuple(certificate.dual_witness), certificate.reported_value)"),
            ("presentation binding omitted", "_require_binding(rows, weights, presentation._boundary, presentation._weights)", "pass  # presentation binding omitted"),
            ("input bit budget omitted", "if value.bit_length() > limit:", "if False and value.bit_length() > limit:"),
            ("vector entry budget omitted", "if len(values) > MAX_VECTOR_LENGTH:", "if False and len(values) > MAX_VECTOR_LENGTH:"),
            ("coordinate budget omitted", "if len(sequence) > MAX_COORDINATES:\n        raise _refuse(\"coordinate budget exceeded\", limit=MAX_COORDINATES)", "if False and len(sequence) > MAX_COORDINATES:\n        raise _refuse(\"coordinate budget exceeded\", limit=MAX_COORDINATES)"),
            ("boundary width budget omitted", "if len(row) > MAX_BOUNDARY_COLUMNS:", "if False and len(row) > MAX_BOUNDARY_COLUMNS:"),
            ("boundary height budget omitted", "if len(sequence) > MAX_COORDINATES:\n        raise _refuse(\"boundary height budget exceeded\", role=role, limit=MAX_COORDINATES)", "if False and len(sequence) > MAX_COORDINATES:\n        raise _refuse(\"boundary height budget exceeded\", role=role, limit=MAX_COORDINATES)"),
            ("boundary entry budget omitted", "if entries > MAX_BOUNDARY_ENTRIES:", "if False and entries > MAX_BOUNDARY_ENTRIES:"),
            ("dot work budget omitted", '_work_fraction(total, "dot product")', "pass  # dot budget omitted"),
            ("cost work budget omitted", '_work_fraction(total, "weighted l1")', "pass  # cost budget omitted"),
            ("column work budget omitted", '_work_fraction(total, "dual column pairing")', "pass  # column budget omitted"),
            ("verified value reinitialized", 'if hasattr(self, "_parts"):', 'if False and hasattr(self, "_parts"):'),
            ("presentation reinitialized", 'if hasattr(self, "_boundary"):', 'if False and hasattr(self, "_boundary"):'),
            ("untrusted certificate type admitted", "if type(cert) is not ExactPhi1Certificate:", "if False and type(cert) is not ExactPhi1Certificate:"),
            ("unbounded diagnostic role admitted", "if len(role) > limit:", "if False and len(role) > limit:"),
        ],
    },
    "src.functional": {
        "source": "code/python/src/functional/__init__.py",
        "old_tests": "code/python/src/functional/test_exported_zero_phi1.py",
        "mutants": [
            *exported._LIBRARY_MUTANTS,
            ("integer witness budget omitted", "if value.bit_length() > MAX_INPUT_BITS:", "if False and value.bit_length() > MAX_INPUT_BITS:"),
            ("hostile tuple callback admitted", "if type(value) is not tuple or len(value) != 2:", "if not issubclass(type(value), tuple) or len(value) != 2:"),
        ],
    },
    "src.functional.test_exported_zero_phi1": {
        "source": "code/python/src/functional/test_exported_zero_phi1.py",
        "old_tests": "code/python/src/functional/test_exported_zero_phi1.py",
        "mutants": [
            *exported._SELF_MUTANTS,
            ("invalid candidate counted as killed", 'raise _fail("candidate could not be assessed; not counted as a kill", name=label, error=type(error).__name__) from error', "survived = False"),
            ("oracle infrastructure failure silenced", "except (ClaimCheckError, ValueError, ArithmeticError, AssertionError):", "except Exception:"),
            ("self oracle infrastructure failure silenced", "except ClaimCheckError:\n        return False", "except Exception:\n        return False"),
            ("previous module binding lost", "sys.modules[name] = previous", "sys.modules.pop(name, None)"),
        ],
    },
}
for name, definition in SPECS.items():
    old = "if issubclass(type(value), float):"
    if ".test_" in name:
        old = 'def parse_exact_entry(value: object) -> int:\n    """Refuse float and bool before an exact witness entry is accepted."""\n    ' + old
    definition["mutants"].insert(0, ("user class callback introduced", old, old.replace("issubclass(type(value), float)", "isinstance(value, float)")))
    definition["dependencies"] = [value["source"] for value in SPECS.values()]


if __name__ == "__main__":
    selected = {name: definition for name, definition in SPECS.items() if not sys.argv[1:] or name in sys.argv[1:]}
    if not selected:
        raise SystemExit("No named module matched the declared functional subjects")
    core.main(selected, "code/python/tests/test_functional_integrity.py", "functional")
