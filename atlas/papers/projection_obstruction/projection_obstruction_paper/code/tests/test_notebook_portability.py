"""Guard the minimum Python the deposit advertises.

Added 2026-09-03. `observer_carriers_demo.ipynb` crashed for an external
reviewer while passing here, because it formatted an exact `Fraction` with a
width spec:

    f"{instance.tallies.I:>15}"

`Fraction.__format__` was added in CPython 3.12 (gh-100227). Before that the
call falls through to `object.__format__`, which raises

    TypeError: unsupported format string passed to Fraction.__format__

`pyproject.toml` declares ``requires-python = ">=3.11"``, so the notebook was
broken on a version the deposit claims to support. It ran locally only because
the development interpreter is newer. This is the same failure shape as the
release archive that was only ever built outside its documented output
directory: verified in the author's configuration, not the advertised one.

These tests simulate the 3.11 behaviour by calling ``object.__format__``
directly, so they fail on any interpreter if the deposit starts depending on
the newer builtin.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
import re
import sys
from fractions import Fraction
from pathlib import Path

import pytest

_CODE = str(Path(__file__).resolve().parents[1])
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

PACKAGE_ROOT = Path(_CODE).parent
NOTEBOOKS = PACKAGE_ROOT / "jupyter_notebooks"

# A format spec applied to one of these is the trap: they are exact rationals.
EXACT_VALUED = ("tallies.I", "tallies.J", "tallies.Lambda", "raw_tally",
                "quotient", "distance")


def test_declared_minimum_python_is_still_3_11():
    """If the floor moves to 3.12 these guards can be retired, not before."""
    text = (PACKAGE_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'requires-python\s*=\s*"([^"]+)"', text)
    assert match, "pyproject does not declare requires-python"
    assert match.group(1) == ">=3.11", (
        f"requires-python is {match.group(1)!r}; if the floor changed, revisit "
        "the Fraction formatting guards in this module"
    )


def test_fraction_format_spec_is_a_real_hazard_below_3_12():
    """Document the mechanism, independent of the running interpreter."""
    with pytest.raises(TypeError, match="unsupported format string"):
        object.__format__(Fraction(6, 1), ">15")
    # str() first is always safe, on every supported version
    assert f"{str(Fraction(6, 1)):>4}" == "   6"


@pytest.mark.parametrize("path", sorted(NOTEBOOKS.glob("*.ipynb")),
                         ids=lambda p: p.name)
def test_no_notebook_formats_an_exact_value_directly(path):
    """No notebook may apply a format spec to an exact rational.

    Matches ``{<expr containing an exact-valued attribute>:<spec>}`` while
    allowing the safe ``{str(...):<spec>}`` form.
    """
    nb = json.loads(path.read_text(encoding="utf-8"))
    offenders = []
    for index, cell in enumerate(nb["cells"]):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell["source"])
        for match in re.finditer(r"\{([^{}]+):[^{}]+\}", source):
            expr = match.group(1)
            if "str(" in expr:
                continue
            if any(token in expr for token in EXACT_VALUED):
                offenders.append(f"cell {index}: {match.group(0)}")
    assert offenders == [], (
        f"{path.name} formats an exact rational directly, which raises on "
        f"Python 3.11: {offenders}. Wrap the value in str() first."
    )


@pytest.mark.parametrize("path", sorted(NOTEBOOKS.glob("*.ipynb")),
                         ids=lambda p: p.name)
def test_every_notebook_cell_has_a_stable_id(path):
    """nbformat warns today and is expected to make this an error."""
    nb = json.loads(path.read_text(encoding="utf-8"))
    missing = [i for i, cell in enumerate(nb["cells"]) if not cell.get("id")]
    assert missing == [], f"{path.name} has cells without ids: {missing}"


@pytest.mark.parametrize("path", sorted(NOTEBOOKS.glob("*.ipynb")),
                         ids=lambda p: p.name)
def test_notebooks_ship_without_stale_outputs(path):
    """A reproducible archive carries no saved outputs or execution counts.

    Mixed counts with output attached to cells whose execution_count is null
    are worse than none: they imply a run that never happened in that order.
    """
    nb = json.loads(path.read_text(encoding="utf-8"))
    dirty = [
        i for i, cell in enumerate(nb["cells"])
        if cell.get("cell_type") == "code"
        and (cell.get("outputs") or cell.get("execution_count") is not None)
    ]
    assert dirty == [], f"{path.name} ships saved outputs in cells {dirty}"


def test_replica_notebook_does_not_revive_the_withdrawn_independence_claim():
    """The five-way RE independence claim is withdrawn; the notebook said otherwise.

    The paper states that once RE3 and RE5 are assumed, RE1, RE2 and RE4 are
    redundant for the unweighted conclusion, and that only the RE3-drop and
    RE5-drop countermodels survive. An earlier version of this notebook
    asserted that every axiom is load-bearing -- the withdrawn claim -- while
    also stating at the end that it had been withdrawn.
    """
    nb = json.loads((NOTEBOOKS / "replica_hierarchy_demo.ipynb").read_text(encoding="utf-8"))
    text = " ".join("".join(c["source"]) for c in nb["cells"]).lower()
    for banned in (
        "each of those assumptions is doing real work",
        "each assumption is **load-bearing**",
        "all five are independent",
    ):
        assert banned.lower() not in text, f"withdrawn claim reappeared: {banned!r}"
    assert "redundant" in text, (
        "the notebook should say RE1, RE2 and RE4 are redundant given RE3 and RE5"
    )
