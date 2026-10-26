"""Multi-system parity verification between Python wdp_codec.py and Lean 4 WdpParser.

AuthorityEffect: None. GenesisEffect: None.
Verifies that:
1. Lean 4 package in witnessed_difference_programme/lean4/ builds cleanly via Lake.
2. The Lean 4 inductive parser `parseWdp?` exactly accepts and round-trips all positive
   conformance wire encodings accepted by Python's `wdp_codec.py`.
3. The Lean 4 parser cleanly rejects all invalid wire encodings rejected by Python's `wdp_codec.py`.
4. Cross-system generative AST parity: Randomly generated Python ASTs serialized to wire
   are recognized, parsed, and identically re-serialized by Lean 4's `wdp_parity_check`.
"""

from __future__ import annotations

import json
import random
import string
import subprocess
import sys
from pathlib import Path

import pytest

MODULE_ROOT = next(
    (
        p
        for p in Path(__file__).resolve().parents
        if (p / "levels").is_dir() or (p / "grammar").is_dir()
    ),
    Path(__file__).resolve().parents[2],
)
REPO_ROOT = next(
    (
        p
        for p in Path(__file__).resolve().parents
        if (p / ".git").exists() or (p / "pixi.toml").exists()
    ),
    Path(__file__).resolve().parents[5],
)
CODE_DIR = MODULE_ROOT / "code"
LEAN4_DIR = MODULE_ROOT / "lean4"
CASES_PATH = MODULE_ROOT / "grammar" / "wdp_conformance_cases.json"

sys.path.insert(0, str(CODE_DIR))

from wdp_codec import (
    REFUSAL_CODES,
    WITNESS_STATUSES,
    BalanceMatrix,
    D0Map,
    D1Map,
    DistinctCut,
    Glyph,
    HHomotopy,
    MarkedQuotient,
    QuotientWitness,
    SimplexPair,
    WdpNode,
    WdpRefusal,
    Word,
    serialize_wdp,
)


@pytest.fixture(scope="module")
def lean4_exe() -> Path:
    """Ensure the Lean 4 package is built and return the wdp_parity_check binary path."""
    exe_name = "wdp_parity_check.exe" if sys.platform == "win32" else "wdp_parity_check"
    exe_path = LEAN4_DIR / ".lake" / "build" / "bin" / exe_name

    if not exe_path.exists():
        res = subprocess.run(
            ["lake", "build"],
            cwd=str(LEAN4_DIR),
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode != 0:
            pytest.fail(f"lake build failed:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")

    assert exe_path.exists(), f"Lean 4 executable not found at {exe_path}"
    return exe_path


def run_lean_check(exe: Path, wire: str) -> tuple[int, str]:
    """Invoke the Lean 4 parity check CLI on a single wire token."""
    proc = subprocess.run(
        [str(exe), wire],
        cwd=str(LEAN4_DIR),
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode, proc.stdout.strip()


def test_lean4_build_artifact_exists(lean4_exe: Path):
    assert lean4_exe.is_file()


def test_lean4_conformance_parity(lean4_exe: Path):
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    for c in cases:
        text = c["text"]
        expected_accept = c["accept"]

        code, out = run_lean_check(lean4_exe, text)
        if expected_accept:
            assert code == 0, f"Lean 4 rejected valid case {c['id']}: {text!r}, out={out}"
            assert f"OK: {text}" in out, f"Unexpected output for {text!r}: {out}"
        else:
            assert code != 0, f"Lean 4 accepted invalid case {c['id']}: {text!r}, out={out}"
            assert f"REJECT: {text}" in out, f"Unexpected output for invalid {text!r}: {out}"


VALID_GLYPHS = string.ascii_lowercase + string.digits


def _random_glyph(rng: random.Random) -> Glyph:
    return Glyph(rng.choice(VALID_GLYPHS))


def _random_word(rng: random.Random, max_len: int = 8) -> Word:
    length = rng.randint(1, max_len)
    return Word("".join(rng.choice(VALID_GLYPHS) for _ in range(length)))


def _random_ast(rng: random.Random) -> WdpNode:
    tag = rng.randint(0, 8)
    if tag == 0:
        return DistinctCut(first=_random_glyph(rng), second=_random_glyph(rng))
    if tag == 1:
        return SimplexPair(first=_random_glyph(rng), second=_random_glyph(rng))
    if tag == 2:
        return MarkedQuotient(numerator=_random_glyph(rng), fiber=_random_word(rng))
    if tag == 3:
        return D0Map(target=_random_glyph(rng))
    if tag == 4:
        return D1Map(first=_random_glyph(rng), second=_random_glyph(rng))
    if tag == 5:
        return HHomotopy(first=_random_glyph(rng), second=_random_glyph(rng))
    if tag == 6:
        status = rng.choice(sorted(WITNESS_STATUSES))
        return QuotientWitness(fiber=_random_word(rng), status=status)
    if tag == 7:
        return BalanceMatrix(sites=rng.randint(0, 50), trace=rng.randint(0, 50))
    code = rng.choice(sorted(REFUSAL_CODES))
    return WdpRefusal(code=code)


def test_cross_system_generative_parity(lean4_exe: Path):
    """Property: for all generated Python ASTs, serialize_wdp produces wire that Lean 4 parses and reproduces."""
    rng = random.Random(20261005)
    for _ in range(50):
        ast = _random_ast(rng)
        wire = serialize_wdp(ast)

        code, out = run_lean_check(lean4_exe, wire)
        assert code == 0, f"Lean 4 rejected wire generated by Python AST: {wire}, out={out}"
        assert out == f"OK: {wire}", f"Lean 4 parity mismatch for {wire}: {out}"
