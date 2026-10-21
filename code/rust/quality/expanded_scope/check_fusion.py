"""Pinned exact-fusion and checker fault challenges; no category reconstruction."""
import sys
from pathlib import Path

import check_entrypoints as core

sys.path.insert(0, str(core.ROOT / "code/python"))
from src.fusion_categories import test_fusion_control as legacy


def faults(rows):
    return [(name, "".join(old), "".join(new)) for name, old, new in rows]


SPECS = {
    "src.fusion_categories.fusion_ring": {
        "source": "code/python/src/fusion_categories/fusion_ring.py",
        "old_tests": "code/python/tests/test_fusion_ring.py",
        "mutants": [
            *faults(legacy.LIBRARY_MUTANTS),
            ("integer subclass admitted", "if type(value) is int:\n        _require_bits(value, role)\n        return value", "if isinstance(value, int):\n        _require_bits(value, role)\n        return value"),
            ("rational subclass admitted", "if type(value) is Fraction:", "if isinstance(value, Fraction):"),
            ("scalar bit budget omitted", "if value.bit_length() > limit:", "if False and value.bit_length() > limit:"),
            ("ordinary value class callback introduced", "if issubclass(type(value), float):\n        raise _fail(\"float refused at the fusion boundary\", role=role, received=\"float\")\n    if type(value) is bool:\n        raise _fail(\"boolean refused where an integer was required\", role=role)", "if isinstance(value, float):\n        raise _fail(\"float refused at the fusion boundary\", role=role, received=\"float\")\n    if type(value) is bool:\n        raise _fail(\"boolean refused where an integer was required\", role=role)"),
            ("canonical rational field lost", "if radical == 0:\n        return real, Fraction(0), 1", "if radical == 0:\n        return real, Fraction(0), disc"),
            ("quadratic operand callback introduced", "if type(other) is not QuadraticRational:", "if not isinstance(other, QuadraticRational):"),
            ("quadratic operand admission omitted", "if type(left) is not QuadraticRational or type(right) is not QuadraticRational:", "if False:"),
            ("quadratic discriminant budget omitted", "if disc > MAX_DISCRIMINANT:", "if False and disc > MAX_DISCRIMINANT:"),
            ("quadratic reinitialization admitted", 'if hasattr(self, "a"):', "if False:"),
            ("group reinitialization admitted", 'if hasattr(self, "_moduli"):', "if False:"),
            ("table reinitialization admitted", 'if hasattr(self, "_rank"):', "if False:"),
            ("ring reinitialization admitted", 'if hasattr(self, "_table"):', "if False:"),
            ("non-table trusted", "if type(table) is not FusionTable:", "if False:"),
            ("sequence callbacks admitted", "if type(value) not in (list, tuple):", "if not isinstance(value, (list, tuple)):"),
            ("sequence quota omitted", "if len(value) > limit:", "if False and len(value) > limit:"),
            ("name quota omitted", "if len(item) > MAX_LABEL_CHARACTERS:", "if False and len(item) > MAX_LABEL_CHARACTERS:"),
            ("law product preflight omitted", '_operation_budget(2 * self.rank ** 5, "fusion laws")', "pass  # law product budget omitted"),
            ("path product preflight omitted", '_operation_budget(len(factors) * self.rank ** 2, "fusion paths")', "pass  # path product budget omitted"),
            ("path work-bit quota omitted", '_require_bits(nxt[target], "fusion path count", MAX_WORK_BITS)', "pass  # path arithmetic budget omitted"),
            ("associativity check omitted", "defect = _associativity_defect(self)", "defect = None"),
            ("commutativity check omitted", "defect = _commutativity_defect(self)", "defect = None"),
            ("quadratic mixed-field addition corrupted", "return QuadraticRational(left.a + right.a, left.b + right.b, disc)", "return QuadraticRational(left.a + right.a, left.b + right.b, left.disc)"),
            ("quadratic mixed-field multiplication corrupted", "return QuadraticRational(real, radical, disc)", "return QuadraticRational(real, radical, left.disc)"),
            ("closed output stream escapes", "except (OSError, ValueError):\n        return 2", "except ArithmeticError:\n        return 2"),
            ("diagnostic output stream escapes", "except (OSError, ValueError):\n            return 2", "except ArithmeticError:\n            return 2"),
        ],
    },
    "src.fusion_categories": {
        "source": "code/python/src/fusion_categories/__init__.py",
        "old_tests": "code/python/src/fusion_categories/test_fusion_control.py",
        "mutants": [
            *faults(legacy.PACKAGE_MUTANTS),
            ("integer subclass admitted", "if type(value) is int:", "if isinstance(value, int):"),
            ("scalar bit budget omitted", "if value.bit_length() > MAX_INPUT_BITS:", "if False and value.bit_length() > MAX_INPUT_BITS:"),
            ("ordinary value callback introduced", "if issubclass(type(value), float):", "if isinstance(value, float):"),
            ("closed output stream escapes", "except (OSError, ValueError):\n        return 2", "except ArithmeticError:\n        return 2"),
            ("diagnostic output stream escapes", "except (OSError, ValueError):\n            return 2", "except ArithmeticError:\n            return 2"),
        ],
    },
    "src.fusion_categories.test_fusion_control": {
        "source": "code/python/src/fusion_categories/test_fusion_control.py",
        "old_tests": "code/python/src/fusion_categories/test_fusion_control.py",
        "mutants": [
            *faults(legacy.HARNESS_MUTANTS),
            ("integer subclass admitted", "if type(value) is int:", "if isinstance(value, int):"),
            ("scalar quota omitted", "if value.bit_length() > MAX_INPUT_BITS:", "if False and value.bit_length() > MAX_INPUT_BITS:"),
            ("ordinary class callback introduced", "def _require_int(value: object, role: str) -> int:\n    if issubclass(type(value), float):", "def _require_int(value: object, role: str) -> int:\n    if isinstance(value, float):"),
            ("invalid candidate falsely counted as killed", 'raise _fail("candidate could not be assessed; not counted as a kill", error=type(error).__name__) from error', "return True"),
            ("oracle infrastructure error silenced", "return oracle(namespace) is False", "try:\n            return oracle(namespace) is False\n        except Exception:\n            return True"),
            ("previous module binding lost", "sys.modules[name] = previous", "sys.modules.pop(name, None)"),
        ],
    },
}

for definition in SPECS.values():
    definition["dependencies"] = [item["source"] for item in SPECS.values()]


if __name__ == "__main__":
    selected = {name: definition for name, definition in SPECS.items() if not sys.argv[1:] or name in sys.argv[1:]}
    if not selected:
        raise SystemExit("No declared fusion module matched")
    core.main(selected, "code/python/tests/test_fusion_integrity.py", "fusion")
