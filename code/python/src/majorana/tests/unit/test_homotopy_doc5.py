"""Narrow tests for py_updates_5.md defect fixes in omega_homotopy_type_theory.

Patch B (Refusal unification): the HoTT ``types.py`` must use the canonical
``omega_types.refusal.Refusal`` so a HoTT-produced refusal is the same class the
rest of the pipeline checks with ``isinstance``. ``Success`` / ``Result`` stay
local (canonical refusal has no Success wrapper).

Patch C (replay gating): ``safe_trans`` must return a typed ``Refusal`` (not
raise) when two paths do not compose, and a ``Path`` on valid concatenation.
The raising ``Path.trans`` is preserved for utility-level use.
"""

from omega_engine.crates.homotopy_type_theory.types import Path, Refusal, Success, safe_trans
import omega_engine.crates.type.refusal as canonical_refusal


def test_hott_refusal_is_canonical():
    # The Refusal exported by HoTT types is the canonical class, so isinstance
    # checks at omega_types.refusal boundaries recognize a HoTT-produced refusal.
    assert Refusal is canonical_refusal.Refusal
    r = Refusal("x")
    assert isinstance(r, canonical_refusal.Refusal)


def test_success_and_result_remain_local():
    # Success is HoTT-local (canonical refusal has no Success wrapper); dependents
    # like fibration.py / invariants.py rely on this Success-wrapped Result.
    s = Success(42)
    assert s.value == 42


def test_safe_trans_refuses_on_mismatched_endpoints():
    p = Path("a", "b")
    other = Path("c", "d")  # other.source != p.target

    # Sanity: the raising concatenation is preserved (utility level).
    raised = False
    try:
        p.trans(other)
    except ValueError:
        raised = True
    assert raised, "Path.trans must still raise on mismatch (utility level)"

    result = safe_trans(p, other)
    assert isinstance(result, Refusal)
    assert "safe_trans" in result.reason


def test_safe_trans_returns_path_on_valid_concatenation():
    p = Path("a", "b")
    other = Path("b", "c")
    result = safe_trans(p, other)
    assert isinstance(result, Path)
    assert (result.source, result.target) == ("a", "c")


