"""Build the manuscript with Pandoc and three XeLaTeX passes.

The generated TeX is standalone. Missing glyphs and overfull boxes fail the
build even when the TeX engine exits successfully.
"""
from pathlib import Path
import hashlib
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def build():
    source = (ROOT / "paper.md").read_text(encoding="utf-8")
    source = re.sub(r"\A---\n.*?\n---\n", "", source, count=1, flags=re.S)
    header = """<div align="center"># From Pre-Genesis to MSS-N</div>
<div align="center">Jeremy H. Carroll</div>
<div align="center">2026-10-09</div>
<div align="center">Version 1.0.0</div>"""
    if header not in source:
        raise RuntimeError("Manuscript title block does not match the PDF header")
    source = source.replace(header, r"""\begin{center}
{\LARGE\bfseries From Pre-Genesis to MSS-N\par}
Jeremy H. Carroll\par
2026-10-09\par
Version 1.0.0\par
\end{center}""")
    # Relative companion files remain relative to the paper package; the
    # historical source references in the manuscript already use pinned URLs.
    subprocess.run(["pandoc", "--standalone", "--from",
                        "markdown+tex_math_dollars+tex_math_single_backslash+raw_tex+pipe_tables",
                        "--to", "latex", "--pdf-engine", "xelatex", "--no-highlight",
                        "-V", "geometry:margin=25mm", "-V", "fontsize=11pt",
                        "-V", "mainfont=Latin Modern Roman", "-V", "monofont=Latin Modern Mono",
                        "-V", "colorlinks=true", "-o", str(ROOT / "paper.tex")],
                   input=source, text=True, encoding="utf-8", check=True)
    text = (ROOT / "paper.tex").read_text(encoding="utf-8")
    source_sha = hashlib.sha256((ROOT / "paper.md").read_bytes()).hexdigest()
    text = f"% manuscript-sha256: {source_sha}\n" + text
    # xurl permits breaks in long theorem names and commit hashes without
    # shrinking mathematical text or changing manuscript content.
    text = re.sub(r"\\texttt\{([A-Za-z0-9._/\\-]+)\}",
                  lambda m: r"\nolinkurl{" + m[1].replace(r"\_", "_") + "}", text)
    text = text.replace(r"\begin{document}", r"""\usepackage{xurl}
\usepackage{newunicodechar}
\usepackage{needspace}
\usepackage{pdflscape}
\newunicodechar{∎}{\ensuremath{\square}}
\newunicodechar{→}{\ensuremath{\to}}
\newunicodechar{←}{\ensuremath{\leftarrow}}
\newunicodechar{↦}{\ensuremath{\mapsto}}
\newunicodechar{≠}{\ensuremath{\ne}}
\newunicodechar{⊆}{\ensuremath{\subseteq}}
\newunicodechar{∩}{\ensuremath{\cap}}
\newunicodechar{∪}{\ensuremath{\cup}}
\newunicodechar{∅}{\ensuremath{\varnothing}}
\newunicodechar{∈}{\ensuremath{\in}}
\newunicodechar{∉}{\ensuremath{\notin}}
\newunicodechar{⊔}{\ensuremath{\sqcup}}
\newunicodechar{−}{\ensuremath{-}}
\newunicodechar{ε}{\ensuremath{\varepsilon}}
\newunicodechar{α}{\ensuremath{\alpha}}
\newunicodechar{β}{\ensuremath{\beta}}
\newunicodechar{γ}{\ensuremath{\gamma}}
\newunicodechar{²}{\ensuremath{{}^2}}
\newunicodechar{³}{\ensuremath{{}^3}}
\newunicodechar{φ}{\ensuremath{\varphi}}
\newunicodechar{Σ}{\ensuremath{\Sigma}}
\newunicodechar{Γ}{\ensuremath{\Gamma}}
\setlength{\emergencystretch}{3em}
\begin{document}""")
    # Reserve enough room for this inventory; avoid a fixed break that can
    # strand the previous paragraph on an otherwise empty page.
    text = text.replace(r"\subsection{Mechanism inventory}",
                        r"\Needspace{480pt}" + "\n" + r"\subsection{Mechanism inventory}")
    # Keep each short entrance/profile comparison with its introducing heading.
    for heading, reserve in [
        (r"\\subsection\{\d+\. The finite-stage\s+crosswalk\}", 430),
        (r"\\subsection\{\d+\. Profiles, parsers and evidence\s+scope\}", 260),
    ]:
        text = re.sub(heading, lambda m: rf"\Needspace{{{reserve}pt}}" + "\n" + m[0], text)
    # The three-row frozen-status summary should fit on one page.
    text = re.sub(r"\\begin\{longtable\}.*?\\end\{longtable\}",
                  lambda match: (r"\Needspace{100pt}" + "\n"
                                 if "Axis & Final source status" in match[0] else "") + match[0],
                  text, flags=re.S)
    text = text.replace(r"\subsection{Appendix A.",
                        "\\clearpage\n\\begin{landscape}\n" + r"\subsection{Appendix A.")
    def inventory_widths(match):
        block = match[0]
        if "Canonical input" in block and "Start symbol" in block:
            widths = iter(("0.05", "0.20", "0.20", "0.55"))
            block = re.sub(r"\\real\{[0-9.]+\}",
                           lambda _: r"\real{" + next(widths) + "}", block, count=4)
        return block
    text = re.sub(r"\\begin\{longtable\}.*?\\end\{longtable\}",
                  inventory_widths, text, flags=re.S)
    # Keep the four-profile comparison together, including each multiline row.
    # Starred row breaks tell longtable not to split this short comparison.
    text = re.sub(r"\\begin\{longtable\}.*?\\end\{longtable\}",
                  lambda m: m[0].replace(" \\\\", " \\\\*")
                  if "Selected profile" in m[0] else m[0], text, flags=re.S)
    text = text.replace(r"\end{document}", "\\end{landscape}\n" + r"\end{document}")
    (ROOT / "paper.tex").write_text(text, encoding="utf-8", newline="\n")
    with tempfile.TemporaryDirectory(prefix="genesis-pdf-") as directory:
        output = Path(directory)
        for _ in range(3):
            run = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error",
                                  "-no-shell-escape", f"-output-directory={output}", "paper.tex"],
                                 cwd=ROOT, capture_output=True, text=True,
                                 encoding="utf-8", errors="replace")
            if run.returncode:
                raise RuntimeError(run.stdout[-6000:] + run.stderr[-2000:])
        log = (output / "paper.log").read_text(encoding="utf-8", errors="replace")
        issues = [line for line in log.splitlines() if "Missing character:" in line or "Overfull" in line]
        if issues:
            raise RuntimeError("\n".join(issues))
        shutil.copyfile(output / "paper.pdf", ROOT / "paper.pdf")
    print("PDF built in three passes; no missing glyphs or overfull boxes")


if __name__ == "__main__":
    build()
