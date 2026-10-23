"""The Python scripts read governance/policy.json the same way the Rust governance crate does.

Run: python -I -X utf8 -m pytest scripts/test_governance_policy.py -q -p no:cacheprovider
The glob cases mirror code/rust/src/governance/src/policy.rs::tests::globs.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import contract_scores  # noqa: E402
import score_scope_contracts as scope  # noqa: E402

POLICY = json.loads((ROOT / "governance" / "policy.json").read_text(encoding="utf-8"))


def test_glob_cases_match_the_rust_matcher():
    cases = [
        ("code/**/*.rs", "code/a.rs", True),
        ("code/**/*.rs", "code/rust/src/a/b.rs", True),
        ("code/**/*.rs", "code/rust/src/a/b.rs.bak", False),
        ("code/**/*.rs", "lean4/a.rs", False),
        ("code/**/*.rs", "code", False),
        ("papers/**/archive/**", "papers/x/y/archive/z.py", True),
        ("papers/**/archive/**", "papers/archive/z.py", True),
        ("papers/**/archive/**", "papers/x/archived/z.py", False),
        ("dag/results/**", "dag/results/a/b.py", True),
        ("dag/results/**", "dag/resultsx/a.py", False),
        ("a/?.rs", "a/b.rs", True),
        ("a/?.rs", "a/bc.rs", False),
        ("a/?.rs", "a/.rs", False),
        ("a/*", "a/", True),
        ("*", "x", True),
        ("*", "x/y", False),
        ("**", "x/y", True),
        ("a/b", "a", False),
        ("a/**/b/**/c", "a/x/b/y/z/c", True),
        ("a/**/b/**/c", "a/x/c", False),
        ("*.contract.*", "m.contract.score.yaml", True),
        ("\u00e9?/*", "\u00e9x/\u00fc.py", True),
        ("*a" * 30 + "b", "a" * 200, False),
        ("**/" * 30 + "x", "/".join(["a"] * 60), False),
    ]
    for pattern, path, expected in cases:
        assert scope.glob_match(pattern, path) is expected, (pattern, path)


def test_population_and_exclusions_come_from_the_policy():
    assert scope.population_language("code/rust/src/governance/src/lib.rs") == "Rust"
    assert scope.population_language("code/python/src/x.py") == "Python"
    assert scope.population_language("lean4/HilbertLiftOperators.lean") == "Lean 4"
    assert scope.population_language("lean4/.lake/packages/m/M.lean") is None
    assert scope.population_language("code/rust/target/debug/build/x.rs") is None
    assert scope.population_language("scripts/contract_scores.py") is None
    assert scope.population_language("code/rust/Cargo.toml") is None
    assert scope.SCHEMA == contract_scores.SCHEMA == POLICY["companion"]["document_schema"]
    assert scope.COMPANION_SUFFIX == contract_scores.SUFFIX == POLICY["companion"]["suffix"]
    assert list(contract_scores.GRADE_RANK) == POLICY["grade_order"] == ["E", "D", "C", "B", "A", "A+"]
    assert POLICY["floor"]["min_level"] == "L4" and POLICY["floor"]["min_grade"] == "D"


def test_build_hook_is_pinned_by_exact_bytes():
    template = (ROOT / "governance" / "hook" / "build.rs").read_bytes()
    digest = hashlib.sha256(template).hexdigest()
    assert scope.pinned_boilerplate("code/rust/src/mub/build.rs", digest) is not None
    assert scope.pinned_boilerplate("code/rust/src/mub/build.rs", "0" * 64) is None
    assert scope.pinned_boilerplate("code/rust/src/mub/lib.rs", digest) is None
    hooks = sorted((ROOT / "code" / "rust").glob("**/build.rs"))
    hooks = [h for h in hooks if "target" not in h.parts]
    assert hooks, "every workspace package carries the hook"
    for hook in hooks:
        assert hook.read_bytes() == template, hook


def test_companion_naming_handles_twins(tmp_path, monkeypatch):
    monkeypatch.setattr(scope, "ROOT", tmp_path)
    (tmp_path / "code").mkdir()
    rs = tmp_path / "code" / "m.rs"
    rs.write_text("", encoding="utf-8")
    assert scope.companion_for(rs).name == "m.contract.score.yaml"
    (tmp_path / "code" / "m.py").write_text("", encoding="utf-8")
    assert scope.companion_for(rs).name == "m.rs.contract.score.yaml"
