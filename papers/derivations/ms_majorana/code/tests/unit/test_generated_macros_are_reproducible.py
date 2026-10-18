"""`macros.rs` is generated, and running its generator must reproduce it exactly.

`omega_contracts/src/enforcement/macros.rs` is 503 lines of contract-enforcement
macros written by `generate_macros.py`. Nothing checked that the generator still
produces what is committed, and it did not -- in three separate ways:

1. The generator wrote CRLF. This repository is LF-only (`* text eol=lf`), so
   running it rewrote every line of its own output and dirtied the tree.
2. It never ran rustfmt, though `GOV-002` invariant 2 requires generated Rust to
   be "formatted according to rustfmt". The committed file had been formatted by
   hand or by a separate step, leaving 13 hunks of pure formatting difference.
3. It did not know about `License`. `traits::execution::Engine` declares
   `type License` and takes `_license` on `step`; both had been hand-patched
   into the generated file and never taught to the generator.

Defect 3 is the consequential one. Regenerating dropped `type License = String;`
and the `_license` parameter, so the emitted `Engine` impl no longer satisfied
its own trait -- the crate stopped compiling. A generated file that cannot be
regenerated is not generated; it is a hand-maintained file with a misleading
provenance comment, and the next person to run the generator finds that out the
hard way.

These tests run the generator into a temporary directory. The committed file is
never touched.
"""

from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys
import tempfile

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
ENFORCEMENT = (
    REPO_ROOT / "omega_engine/crates_rs/omega_contracts/src/enforcement"
)
GENERATOR = ENFORCEMENT / "generate_macros.py"
COMMITTED = ENFORCEMENT / "macros.rs"
EXECUTION_TRAIT = (
    REPO_ROOT / "omega_engine/crates_rs/omega_contracts/src/traits/execution.rs"
)


def _regenerate() -> bytes:
    """Run the generator in a temp directory and return what it wrote.

    The generator writes beside its own `__file__`, so copying it elsewhere is
    enough to keep the committed file untouched.
    """
    with tempfile.TemporaryDirectory() as raw:
        tmp = pathlib.Path(raw)
        shutil.copy(GENERATOR, tmp / GENERATOR.name)
        result = subprocess.run(
            [sys.executable, str(tmp / GENERATOR.name)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise AssertionError(
                "the macro generator failed to run:\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )
        produced = tmp / "macros.rs"
        if not produced.is_file():
            raise AssertionError("the generator produced no macros.rs")
        return produced.read_bytes()


@pytest.fixture(scope="module")
def regenerated() -> bytes:
    return _regenerate()


def test_rustfmt_is_available():
    """Asserted, not skipped.

    A skip here would be indistinguishable from a pass, and this estate treats
    skip as a fatal outcome. rustfmt ships with the Rust toolchain the
    repository already requires; if it is missing, that is a broken environment
    and the suite should say so rather than quietly certify nothing.
    """
    found = shutil.which("rustfmt")
    assert found, (
        "rustfmt is not on PATH. The generator formats its output, and "
        "GOV-002 invariant 2 requires it; without rustfmt the reproducibility "
        "claim cannot be checked at all."
    )


def test_the_generator_and_its_output_both_exist():
    assert GENERATOR.is_file()
    assert COMMITTED.is_file()
    assert COMMITTED.stat().st_size > 10_000, "macros.rs is suspiciously small"


def test_running_the_generator_reproduces_the_committed_file(regenerated):
    """The whole point.

    Byte-for-byte, not "semantically equivalent". A generator whose output has
    to be reformatted or hand-patched before it matches is one nobody can run.
    """
    committed = COMMITTED.read_bytes()
    assert regenerated == committed, (
        "regenerating macros.rs does not reproduce the committed file "
        f"(generated {len(regenerated)} bytes, committed {len(committed)}). "
        "Either the generator or the committed file has been edited without "
        "the other; the generator is the source of truth."
    )


def test_the_committed_output_is_lf_without_bom():
    raw = COMMITTED.read_bytes()
    assert b"\r\n" not in raw, "macros.rs contains CRLF in an LF-only repository"
    assert not raw.startswith(b"\xef\xbb\xbf")


def test_the_generated_output_is_lf(regenerated):
    """The generator itself must emit LF, not rely on git to normalise it."""
    assert b"\r\n" not in regenerated


def test_the_engine_trait_still_requires_a_license():
    """Grounds the next test in the trait rather than in a string.

    If `Engine` ever stops requiring `License`, the pin below becomes a check on
    a vestigial line and should be removed deliberately -- this test is what
    makes that visible instead of silent.
    """
    assert "type License;" in EXECUTION_TRAIT.read_text(encoding="utf-8")


def test_the_generator_emits_the_license_binding(regenerated):
    """The regression that was live in the tree.

    `type License` and `_license` were hand-patched into the generated file. A
    regeneration dropped both, and the `Engine` impl then failed to satisfy its
    own trait.
    """
    text = regenerated.decode("utf-8")
    assert "type License = String;" in text
    assert "_license: &Self::License," in text


def test_the_generator_source_names_the_license_binding():
    """Pins the fix at its source, not only in the output.

    The output test above would also pass if someone hand-patched the committed
    file again. This one fails unless the generator itself knows.
    """
    source = GENERATOR.read_text(encoding="utf-8")
    assert "type License = String;" in source
    assert "_license: &Self::License" in source


def test_the_generator_forces_lf_on_write():
    """A behaviour a passing output test cannot distinguish from luck.

    On a Linux runner the default newline is already "\\n", so the CRLF defect
    is invisible there. Pinning the argument keeps the fix from being dropped by
    someone who only ever runs the suite on a platform where it does not bite.
    """
    source = GENERATOR.read_text(encoding="utf-8")
    assert 'newline="\\n"' in source


def test_the_generator_runs_rustfmt():
    source = GENERATOR.read_text(encoding="utf-8")
    assert "rustfmt" in source


def test_the_generated_stub_module_is_still_empty():
    """`generated.rs` says it is populated by codegen. Nothing populates it.

    Recorded rather than deleted: removing a module another crate may reference
    is a bigger change than this sprint's scope, and an empty file that claims
    to be generated is worth having a test point at.
    """
    stub = ENFORCEMENT / "generated.rs"
    assert stub.is_file()
    body = [
        line for line in stub.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("//")
    ]
    assert body == [], (
        "generated.rs now has content; if codegen genuinely populates it, this "
        "test should be replaced with one that checks what it produces"
    )
