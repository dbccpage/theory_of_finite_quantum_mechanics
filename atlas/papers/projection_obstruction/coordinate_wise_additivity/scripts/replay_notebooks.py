#!/usr/bin/env python3
"""Replay the exact reviewed notebook inventory without rewriting source files.

Successful execution is a computational receipt only.  It does not establish
the paper's mathematical claims, publication readiness, or authority.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = ROOT / "jupyter_notebooks"
NOTEBOOK_NAMES = (
    "inline_code_companion.ipynb",
    "refutation_sandbox.ipynb",
    "reviewer_coordinate_additivity.ipynb",
)


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_notebook_paths() -> list[Path]:
    expected = set(NOTEBOOK_NAMES)
    actual = {path.name for path in NOTEBOOK_DIR.glob("*.ipynb")}
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValueError(f"notebook inventory mismatch: missing={missing}, extra={extra}")
    return [NOTEBOOK_DIR / name for name in NOTEBOOK_NAMES]


def main(argv: list[str]) -> int:
    if argv:
        print("usage: replay_notebooks.py", file=sys.stderr)
        return 2
    try:
        notebooks = exact_notebook_paths()
        with tempfile.TemporaryDirectory(prefix="paper009-notebook-replay-") as temporary:
            output_dir = Path(temporary)
            for source in notebooks:
                command = [
                    sys.executable,
                    "-m",
                    "jupyter",
                    "nbconvert",
                    "--to",
                    "notebook",
                    "--execute",
                    "--ExecutePreprocessor.timeout=180",
                    "--output-dir",
                    str(output_dir),
                    str(source),
                ]
                process = subprocess.run(
                    command,
                    cwd=ROOT.parent,
                    capture_output=True,
                    text=True,
                )
                if process.returncode != 0:
                    raise RuntimeError(
                        f"replay failed for {source.name}:\n"
                        f"{process.stdout}\n{process.stderr}"
                    )
                executed = output_dir / source.name
                if not executed.is_file():
                    raise RuntimeError(f"replay produced no output for {source.name}")
                print(
                    f"OK {source.name}: source={sha256_of(source)} "
                    f"executed={sha256_of(executed)}"
                )
    except (OSError, RuntimeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("Notebook replay passed; this is not a mathematical or publication claim.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
