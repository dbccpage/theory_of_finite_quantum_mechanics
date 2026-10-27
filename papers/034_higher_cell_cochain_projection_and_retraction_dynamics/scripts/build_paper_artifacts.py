"""Build the corrected PO-034 manuscript; typesetting is not mathematical evidence."""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM = ROOT.name


def build(tex_only: bool = False) -> None:
    metadata = json.loads((ROOT / "zenodo_metadata.json").read_text(encoding="utf-8"))
    source = (ROOT / f"{STEM}.md").read_text(encoding="utf-8").split("\n", 1)[1]
    source = re.sub(r"(?m)^\*\*Jeremy H\. Carroll\*\*.*\n", "", source)
    source = re.sub(r"(?m)^\*\*Date:\*\*.*\n", "", source)
    day = datetime.date.fromisoformat(metadata["publication_date"])
    epoch = int(datetime.datetime.combine(day, datetime.time(), datetime.timezone.utc).timestamp())
    with tempfile.TemporaryDirectory(prefix="po034-pdf-") as raw:
        work = Path(raw)
        (work / "body.md").write_text(source, encoding="utf-8")
        shutil.copytree(ROOT / "public_export", work / "public_export")
        subprocess.run(
            [
                "pandoc",
                "body.md",
                "--from",
                "markdown+tex_math_single_backslash",
                "--to",
                "latex",
                "--standalone",
                "--wrap",
                "preserve",
                "--include-in-header",
                str(ROOT / "scripts/obstruction-preamble.tex"),
                "--lua-filter",
                str(ROOT / "scripts/latex_inline_code.lua"),
                "--metadata",
                "title=" + metadata["title"],
                "--metadata",
                "author=Jeremy H. Carroll",
                "--metadata",
                "date=Technical preprint v0.3, " + day.isoformat(),
                "-V",
                "fontsize=11pt",
                "-V",
                "geometry:margin=1in",
                "-V",
                "colorlinks=true",
                "-V",
                "linkcolor=RoyalBlue",
                "-o",
                f"{STEM}.tex",
            ],
            cwd=work,
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        tex = (work / f"{STEM}.tex").read_text(encoding="utf-8")
        if tex_only:
            (ROOT / f"{STEM}.tex").write_text(tex, encoding="utf-8", newline="\n")
            print("TeX regenerated; PDF has not been rebuilt")
            return
        env = dict(os.environ, SOURCE_DATE_EPOCH=str(epoch), FORCE_SOURCE_DATE="1")
        for _ in range(2):
            result = subprocess.run(
                [
                    "xelatex",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    f"{STEM}.tex",
                ],
                cwd=work,
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            if result.returncode:
                raise RuntimeError(result.stdout[-7000:] + result.stderr)
        log = (work / f"{STEM}.log").read_text(errors="replace")
        bad = [
            line for line in log.splitlines() if "Overfull" in line or "Missing character" in line
        ]
        if bad:
            raise RuntimeError("Layout diagnostics:\n" + "\n".join(bad))
        if "Output written on" not in log:
            raise RuntimeError("no PDF completion in the XeLaTeX log")
        (ROOT / f"{STEM}.tex").write_text(tex, encoding="utf-8", newline="\n")
        (ROOT / f"{STEM}.pdf").write_bytes((work / f"{STEM}.pdf").read_bytes())
        for suffix in (".log", ".aux", ".toc"):
            output = work / f"{STEM}{suffix}"
            if output.exists():
                shutil.copyfile(output, ROOT / output.name)
        print("PASS: TeX/PDF rebuilt; no overfull boxes or missing characters")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tex-only", action="store_true")
    build(parser.parse_args().tex_only)


if __name__ == "__main__":
    main()
