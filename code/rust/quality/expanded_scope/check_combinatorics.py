"""Challenge counting algorithms and their checker lifecycle at source boundaries."""
from pathlib import Path
import sys

import check_entrypoints as core

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "code/python"))
from src.combinatorics import test_finite_combinatorics as counting
from src.combinatorics import test_exported_binomial as exported

SPECS = {
    "src.combinatorics": {"source": "code/python/src/combinatorics/__init__.py",
        "old_tests": "code/python/src/combinatorics/test_exported_binomial.py", "mutants": [
            *exported._LIBRARY_MUTANTS,
            ("export input bit budget removed", "if value.bit_length() > MAX_INPUT_BITS:", "if False and value.bit_length() > MAX_INPUT_BITS:"),
        ]},
    "src.combinatorics.finite_combinatorics": {"source": "code/python/src/combinatorics/finite_combinatorics.py",
        "old_tests": "code/python/src/combinatorics/test_finite_combinatorics.py", "mutants": [
            ("input bit budget removed", "if value.bit_length() > MAX_INPUT_BITS:", "if False and value.bit_length() > MAX_INPUT_BITS:"),
            ("binomial iteration budget removed", "if min(right, left - right) > MAX_BINOMIAL_STEPS:", "if False and min(right, left - right) > MAX_BINOMIAL_STEPS:"),
            ("binomial result budget removed", "if result.bit_length() > MAX_BINOMIAL_BITS:", "if False and result.bit_length() > MAX_BINOMIAL_BITS:"),
            ("word length budget removed", "if width > MAX_WORD_LENGTH:", "if False and width > MAX_WORD_LENGTH:"),
            ("word count budget removed", "if total > limit:", "if False and total > limit:"),
            ("word storage budget removed", "if total * width > MAX_WORD_CELLS:", "if False and total * width > MAX_WORD_CELLS:"),
            ("partition count budget removed", "if count > MAX_PARTITIONS:", "if False and count > MAX_PARTITIONS:"),
            ("partition input budget removed", "if size > MAX_PARTITION_N:", "if False and size > MAX_PARTITION_N:"),
            ("partition values replaced with zero", "prefix + (part,)", "prefix + (0,)"),
            ("plane record polynomials unchecked", "if any(type(value) is not int for value in actual) or actual != expected:", "if False and (any(type(value) is not int for value in actual) or actual != expected):"),
            ("plane record reinitialized", 'if hasattr(self, "order_q"):', 'if False and hasattr(self, "order_q"):'),
            ("binomial exact division removed", "result = result * (n - k + index) // index", "result = result * (n - k + index)"),
        ]},
}
for module, source, harness in [
    ("src.combinatorics.test_finite_combinatorics", "code/python/src/combinatorics/test_finite_combinatorics.py", counting),
    ("src.combinatorics.test_exported_binomial", "code/python/src/combinatorics/test_exported_binomial.py", exported),
]:
    SPECS[module] = {"source": source, "old_tests": source, "mutants": [
        *harness._SELF_MUTANTS,
        ("invalid library mutant falsely counted as kill", 'raise _fail("mutant could not be assessed; not counted as a kill", name=label, error=type(error).__name__) from error', 'survived = False'),
        ("invalid self mutant falsely counted as kill", 'raise _fail("self mutant could not be assessed; not counted as a kill", name=label, error=type(error).__name__) from error', 'survived = False'),
        ("oracle infrastructure failure silently counted", "except (ClaimCheckError, ValueError, ArithmeticError, AssertionError):", "except Exception:"),
        ("previous module binding lost", "sys.modules[name] = previous", "sys.modules.pop(name, None)"),
    ]}


for name, definition in SPECS.items():
    old = "if issubclass(type(value), float):"
    if ".test_" in name:
        old = 'def parse_exact_size(value: object) -> int:\n    """Refuse float and bool before an exact size is accepted."""\n    ' + old
    definition["mutants"].insert(0, ("user class callback introduced", old, old.replace("issubclass(type(value), float)", "isinstance(value, float)")))
    definition["dependencies"] = [value["source"] for value in SPECS.values()]

if __name__ == "__main__":
    selected = {name: definition for name, definition in SPECS.items() if not sys.argv[1:] or name in sys.argv[1:]}
    if not selected:
        raise SystemExit("No named module matched the declared combinatorics subjects")
    core.main(selected, "code/python/tests/test_combinatorics_resources.py", "combinatorics")
