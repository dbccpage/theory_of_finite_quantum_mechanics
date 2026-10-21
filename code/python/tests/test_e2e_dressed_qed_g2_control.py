"""Exact E2E tests for QM-212: dressed graph polynomials (DFM) and rational QED g-2 enclosure.

AuthorityEffect: None.

Unit, integration, and negative tests.

Origin: code/python/src/qm/campaigns/dressed_qed.py
Claim: dressed_qed_g2_control certificate locked by exact checks in this file
Mutation-Kills: 1 non-equivalent
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from finite_qm.use_cases import dressed_qed_g2_control as dqc
from finite_qm.use_cases import holonomy_bridge_control as hbc


@pytest.fixture(scope="module")
def control() -> dict:
    return dqc.evaluate_dressed_qed_g2_control(conductor=12)


def test_unit_symanzik_u_matches_kirchhoff_dual_cofactor_on_diamond_and_triangle(
    control: dict,
) -> None:
    s = control["dfm_symanzik"]
    assert s["diamond_spanning_tree_count"] == 8
    assert s["diamond_first_betti_number"] == 2
    assert s["u_diamond_unit"] == "8"
    assert s["u_diamond_prime_weights"] == "101"
    assert s["kirchhoff_identity_holds_on_diamond"]
    assert s["kirchhoff_identity_holds_on_triangle"]


def test_ravera_dfm_tree_dressing_is_idempotent_and_gauge_invariant(
    control: dict,
) -> None:
    s = control["dfm_symanzik"]
    assert s["dfm_retraction_idempotent"]
    assert s["dfm_retraction_gauge_invariant"]
    assert s["dfm_every_spanning_tree_neutralizes_its_tree_edges"]
    assert s["dressed_symanzik_gauge_invariant"]
    assert s["all_trees_unimodular_basis_change"]


def test_changing_cotree_holonomy_changes_dressed_symanzik_value() -> None:
    diamond = hbc.FiniteCarrierGraph(4, ((0, 1), (0, 2), (1, 3), (2, 3), (1, 2)))
    z = lambda k: hbc.root_of_unity(12, k)
    c1 = hbc.U1Cochain(diamond, (z(1), z(0), z(2), z(5), z(7)))
    c2 = hbc.U1Cochain(diamond, (z(1), z(0), z(2), z(8), z(7)))
    tree = diamond.spanning_tree()
    d1 = dqc.dress_cochain_on_tree(c1, tree)
    d2 = dqc.dress_cochain_on_tree(c2, tree)
    alphas1 = [Fraction(1 + hbc.root_exponent(v)) for v in d1.values]
    alphas2 = [Fraction(1 + hbc.root_exponent(v)) for v in d2.values]
    assert dqc.symanzik_u_polynomial(diamond, alphas1) != dqc.symanzik_u_polynomial(
        diamond, alphas2
    )


def test_rational_period_intervals_enclose_known_convergent_values() -> None:
    coeffs = dqc.qed_loop_coefficients()
    assert coeffs["pi"].width < Fraction(1, 10**25)
    coarse_pi = dqc.RationalInterval(
        Fraction(3141592653589793, 10**15),
        Fraction(3141592653589794, 10**15),
    )
    assert coarse_pi.contains(coeffs["pi"])
    assert coeffs["ln2"].width < Fraction(1, 10**15)
    assert coeffs["zeta3"].width < Fraction(1, 10**14)
    assert coeffs["zeta5"].width < Fraction(1, 10**12)


def test_qed_c1_c2_c3_and_ae_enclosure_to_twelve_decimals(control: dict) -> None:
    q = control["qed_g2"]
    assert q["c1_exact"] == "1/2"
    assert q["c2_width_lt_1e14"]
    assert q["c2_decimal_12"] == "-0.328478965579"
    assert q["c3_width_lt_1e12"]
    assert q["c3_decimal_12"] == "1.181241456587"
    assert q["ae_1_to_3_width_lt_1e15"]
    assert q["ae_1_to_3_12_digits_agree"]
    assert q["ae_1_to_3_decimal_12"] == "0.001159652231"
    assert q["ae_1_to_4_width_lt_1e12"]
    assert q["ae_1_to_4_12_digits_agree"]
    assert q["ae_1_to_4_decimal_12"] == "0.001159652175"
    assert q["ae_1_to_4_12_digits_enclose_115965217"]


def test_negative_nonpositive_edge_weight_or_inverted_interval_is_refused() -> None:
    diamond = hbc.FiniteCarrierGraph(4, ((0, 1), (0, 2), (1, 3), (2, 3), (1, 2)))
    with pytest.raises(dqc.DressedQedControlRefusal):
        dqc.symanzik_u_polynomial(diamond, [Fraction(1), Fraction(0), Fraction(1), Fraction(1), Fraction(1)])
    with pytest.raises(dqc.DressedQedControlRefusal):
        dqc.RationalInterval(Fraction(2), Fraction(1))
    with pytest.raises(dqc.DressedQedControlRefusal):
        dqc.RationalInterval(Fraction(-1), Fraction(1)).reciprocal()


def test_non_spanning_edge_subset_is_refused_by_dressing() -> None:
    diamond = hbc.FiniteCarrierGraph(4, ((0, 1), (0, 2), (1, 3), (2, 3), (1, 2)))
    z = lambda k: hbc.root_of_unity(12, k)
    cochain = hbc.U1Cochain(diamond, (z(1), z(0), z(2), z(5), z(7)))
    with pytest.raises(dqc.DressedQedControlRefusal):
        dqc.dress_cochain_on_tree(cochain, (0, 1, 4))


def test_residual_import_ledger_names_three_layers(control: dict) -> None:
    ledger = control["residual_import_ledger"]
    assert [row["layer"] for row in ledger] == [
        "finite invariant",
        "completion",
        "residual import",
    ]
    assert ledger[0]["status"] == "COMPUTED"
    assert ledger[2]["status"] == "IMPORTED"


_MODULE_PATH = __import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'qm' / 'dressed_qed.py'


def test_integration_origin_locks_the_source_module() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert 'dressed_qed_g2_control' in source
    assert _MODULE_PATH.is_file()


import json
import subprocess
import sys

_ALIAS_NAMES = ('src.qm.campaigns.dressed_qed', 'finite_qm.use_cases.dressed_qed', 'src.qm.campaigns.dressed_qed_g2_control', 'finite_qm.use_cases.dressed_qed_g2_control')
_USE_SHIM = True
_MUTANTS = (('reciprocal:95', '        return RationalInterval(Fraction(1) / self.hi, Fraction(1) / self.lo)', '        return RationalInterval(Fraction(2) / self.hi, Fraction(1) / self.lo)'),)
_CHILD = '\nimport importlib\nimport importlib.util\nimport json\nimport sys\nimport tempfile\nfrom pathlib import Path\n\npayload = json.loads(sys.stdin.read())\nfor root in payload["roots"]:\n    if root not in sys.path:\n        sys.path.insert(0, root)\nif payload["shim"]:\n    import tests.conftest\nprimary = payload["modules"][0]\nreal = importlib.import_module(primary)\nspec = importlib.util.spec_from_loader(primary, loader=None)\nmodule = importlib.util.module_from_spec(spec)\nmodule.__package__ = real.__package__\nmodule.__file__ = payload["origin"]\nif hasattr(real, "__path__"):\n    module.__path__ = list(real.__path__)\nfor name in payload["modules"]:\n    sys.modules[name] = module\n    parent, _, child = name.rpartition(".")\n    if parent in sys.modules:\n        setattr(sys.modules[parent], child, module)\nexec(compile(payload["source"], payload["origin"], "exec"), module.__dict__)\ntest_spec = importlib.util.spec_from_file_location("certificate_probe", payload["test"])\ntest_mod = importlib.util.module_from_spec(test_spec)\ntest_spec.loader.exec_module(test_mod)\n\n\ndef _unwrap(fn):\n    wrapped = getattr(fn, "__wrapped__", None)\n    if callable(wrapped):\n        return wrapped\n    holder = getattr(fn, "__pytest_wrapped__", None)\n    obj = getattr(holder, "obj", None)\n    if callable(obj):\n        return obj\n    return fn\n\n\ndef _fixture(name):\n    if name == "tmp_path":\n        return Path(tempfile.mkdtemp())\n    fix = getattr(test_mod, name, None)\n    if not callable(fix):\n        return None\n    target = _unwrap(fix)\n    code = getattr(target, "__code__", None)\n    if code is None or code.co_argcount != 0:\n        return None\n    return target()\n\n\nran = 0\ntry:\n    for name in dir(test_mod):\n        if not name.startswith("test_"):\n            continue\n        if "mutation" in name:\n            continue\n        if name == "test_integration_origin_locks_the_source_module":\n            continue\n        fn = getattr(test_mod, name)\n        code = getattr(fn, "__code__", None)\n        if code is None:\n            continue\n        values = []\n        ready = True\n        for arg in code.co_varnames[: code.co_argcount]:\n            value = _fixture(arg)\n            if value is None:\n                ready = False\n                break\n            values.append(value)\n        if ready is False:\n            continue\n        fn(*values)\n        ran += 1\n    if ran == 0:\n        print("FAIL none")\n    else:\n        print("PASS " + str(ran))\nexcept Exception as exc:\n    print("FAIL " + type(exc).__name__)\n'

def _suite_passes(source: str) -> bool:
    payload = json.dumps({
        "modules": list(_ALIAS_NAMES),
        "source": source,
        "origin": str(_MODULE_PATH),
        "test": str(__import__("pathlib").Path(__file__).resolve()),
        "shim": _USE_SHIM,
        "roots": [str(__import__("pathlib").Path(__file__).resolve().parents[1]), str(__import__("pathlib").Path(__file__).resolve().parents[1] / "src")],
    })
    completed = subprocess.run(
        [sys.executable, "-c", _CHILD],
        input=payload,
        capture_output=True,
        text=True,
        check=False,
    )
    lines = completed.stdout.strip().splitlines()
    status = lines[-1] if lines else ""
    return status.startswith("PASS")

def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = _MODULE_PATH.read_text(encoding="utf-8")
    if _suite_passes(source) is False:
        raise AssertionError("baseline suite failed")
    killed = 0
    for name, old, new in _MUTANTS:
        if source.count(old) != 1:
            raise AssertionError(name)
        if _suite_passes(source.replace(old, new, 1)) is not False:
            raise AssertionError(name)
        killed += 1
    if killed != len(_MUTANTS):
        raise AssertionError(str(killed))
    record = f"Mutation-Kills: {killed} non-equivalent"
    if record not in __import__('pathlib').Path(__file__).read_text(encoding="utf-8"):
        raise AssertionError(record)
