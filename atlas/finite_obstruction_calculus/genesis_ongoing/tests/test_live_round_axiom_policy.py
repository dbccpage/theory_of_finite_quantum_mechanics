"""Current round report policy through real wrappers, with Lake intercepted."""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest

CODE = Path(__file__).resolve().parents[1] / "code"
ROUNDS = ("twentysecond", "twentythird", "twentyfourth", "twentyfifth")
TOOLCHAIN = "+leanprover/lean4:v4.35.0"


@pytest.fixture(params=ROUNDS, ids=ROUNDS)
def round_report(request, monkeypatch):
    monkeypatch.syspath_prepend(str(CODE))
    module = importlib.import_module(f"{request.param}.leanreport")
    assert Path(module.__file__).resolve() == (CODE / request.param / "leanreport.py").resolve()
    return module


def _report_dependency(module, lean_dir: Path, axiom: str):
    (lean_dir / "Fixture.lean").write_text(
        "theorem fixture : True := by trivial\n", encoding="utf-8"
    )
    census = f"'Fixture.result' depends on axioms: [{axiom}]\n"
    calls = []

    def recorded_runner(command, cwd):
        assert Path(cwd) == lean_dir
        assert command[0] == "lake"
        calls.append(tuple(command))
        if "build" in command:
            return 0, "Build completed successfully.\n"
        assert command[-1] == module.AXIOMS_FILE
        return 0, census

    text = module.report(lean_dir, runner=recorded_runner)
    return text, calls


def test_live_round_accepts_classical_choice(round_report, tmp_path):
    text, calls = _report_dependency(round_report, tmp_path, "Classical.choice")
    assert "'Fixture.result' depends on axioms: [Classical.choice]" in text
    assert len(calls) == 2


@pytest.mark.parametrize("axiom", ("sorryAx", "Fixture.injectedAxiom"))
def test_live_round_rejects_nonstandard_axioms(round_report, tmp_path, axiom):
    with pytest.raises(RuntimeError, match="axiom") as caught:
        _report_dependency(round_report, tmp_path, axiom)
    assert axiom in str(caught.value)


def test_live_round_uses_active_toolchain(round_report, tmp_path):
    _text, calls = _report_dependency(round_report, tmp_path, "Quot.sound")
    assert calls == [
        ("lake", TOOLCHAIN, "build", round_report.AXIOMS_FILE.split("/", 1)[0]),
        ("lake", TOOLCHAIN, "env", "lean", round_report.AXIOMS_FILE),
    ]
