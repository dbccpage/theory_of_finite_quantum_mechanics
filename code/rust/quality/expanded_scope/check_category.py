"""Source-bound category, factorization and checker integrity challenges."""
from pathlib import Path
import sys

import check_entrypoints as core

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "code/python"))
from src.category_theory import test_finite_category as category
from src.category_theory import test_arrow_decoder as facade

SPECS = {
    "src.category_theory.finite_category": {
        "source": "code/python/src/category_theory/finite_category.py",
        "old_tests": "code/python/src/category_theory/test_finite_category.py",
        "mutants": [
            *category._LIBRARY_MUTANTS,
            ("composition domain/type check omitted", "if not self._morphism_endpoints() or not self._composition_typing():", "if not self._morphism_endpoints():"),
            ("extra identity keys accepted", "if self.identities.keys() != self.objects:", "if False and self.identities.keys() != self.objects:"),
            ("associativity omitted", "return self._associative()", "return True"),
            ("common factorization carrier ignored", "if report.keys() != query.keys():", "if False and report.keys() != query.keys():"),
            ("caller morphism dictionary alias retained", "return MappingProxyType({_label(name): _label_pair(pair) for name, pair in entries.items()})", "return MappingProxyType(value)"),
            ("presentation reinitialization admitted", 'if hasattr(self, "objects"):', 'if False and hasattr(self, "objects"):'),
            ("integer label budget omitted", "if value.bit_length() > MAX_INTEGER_BITS:", "if False and value.bit_length() > MAX_INTEGER_BITS:"),
            ("factorization source budget omitted", "if len(values) > MAX_FACTOR_SOURCES:", "if False and len(values) > MAX_FACTOR_SOURCES:"),
            ("label length budget omitted", "if len(value) > MAX_LABEL_CHARACTERS:", "if False and len(value) > MAX_LABEL_CHARACTERS:"),
            ("object budget omitted", "if len(value) > MAX_OBJECTS:", "if False and len(value) > MAX_OBJECTS:"),
            ("table entry budget omitted", "if len(value) > limit:", "if False and len(value) > limit:"),
            ("hostile dictionary callback admitted", "if type(values) is not dict or len(values) == 0:", "if not issubclass(type(values), dict) or len(values) == 0:"),
        ],
    },
    "src.category_theory": {
        "source": "code/python/src/category_theory/__init__.py",
        "old_tests": "code/python/src/category_theory/test_arrow_decoder.py",
        "mutants": [
            *facade._LIBRARY_MUTANTS,
            ("duplicate witness keys overwritten", "if key in result:", "if False and key in result:"),
            ("witness table budget omitted", "if len(rows) > MAX_FACTOR_SOURCES:", "if False and len(rows) > MAX_FACTOR_SOURCES:"),
            ("integer label budget omitted", "if value.bit_length() > MAX_INTEGER_BITS:", "if False and value.bit_length() > MAX_INTEGER_BITS:"),
            ("hostile tuple callback admitted", "if type(rows) is not tuple or len(rows) == 0:", "if not issubclass(type(rows), tuple) or len(rows) == 0:"),
        ],
    },
}
for module, source, harness in [
    ("src.category_theory.test_finite_category", "code/python/src/category_theory/test_finite_category.py", category),
    ("src.category_theory.test_arrow_decoder", "code/python/src/category_theory/test_arrow_decoder.py", facade),
]:
    SPECS[module] = {"source": source, "old_tests": source, "mutants": [
        *harness._SELF_MUTANTS,
        ("invalid candidate falsely counted as killed", 'raise _fail("candidate could not be assessed; not counted as a kill", name=label, error=type(error).__name__) from error', "survived = False"),
        ("oracle infrastructure failure silenced", "except (ClaimCheckError, ValueError, ArithmeticError, AssertionError):", "except Exception:"),
        ("self oracle infrastructure failure silenced", "except ClaimCheckError:\n        return False", "except Exception:\n        return False"),
        ("previous module binding destroyed", "sys.modules[name] = previous", "sys.modules.pop(name, None)"),
    ]}

for name, definition in SPECS.items():
    old = "if issubclass(type(value), float):"
    if ".test_" in name:
        old = 'def parse_exact_label(value: object) -> int:\n    """Refuse float and bool before an exact label is accepted."""\n    ' + old
    definition["mutants"].insert(0, ("user class callback introduced", old, old.replace("issubclass(type(value), float)", "isinstance(value, float)")))
    definition["dependencies"] = [value["source"] for value in SPECS.values()]


if __name__ == "__main__":
    selected = {name: definition for name, definition in SPECS.items() if not sys.argv[1:] or name in sys.argv[1:]}
    if not selected:
        raise SystemExit("No named module matched the declared category subjects")
    core.main(selected, "code/python/tests/test_category_integrity.py", "category")
