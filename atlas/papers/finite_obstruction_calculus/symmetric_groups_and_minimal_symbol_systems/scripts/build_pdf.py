"""Build the manuscript with Pandoc and three XeLaTeX passes.

The generated TeX is standalone.
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
    
    header = """<div align="center"># From Admitted Distinctions to S(n) and MSS-N: Presentations, Retractions, and Obstruction</div>
<div align="center">Jeremy H. Carroll</div>
<div align="center">2026-10-09</div>
<div align="center">Version 1.0.0</div>"""
    if header not in source:
        raise RuntimeError("Manuscript title block does not match the PDF header")
    source = source.replace(header, r"""\begin{center}
{\LARGE\bfseries From Admitted Distinctions to S(n) and MSS-N: Presentations, Retractions, and Obstruction\par}
Jeremy H. Carroll\par
2026-10-09\par
Version 1.0.0\par
\end{center}""")

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
    
    text = re.sub(r"\\texttt\{([A-Za-z0-9._/\\-]+)\}",
                  lambda m: r"\nolinkurl{" + m[1].replace(r"\_", "_") + "}", text)
    text = text.replace(r"\begin{document}", r"""\usepackage{xurl}
\usepackage{newunicodechar}
\usepackage{needspace}
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
\newunicodechar{²}{\ensuremath{{}^2}}
\newunicodechar{³}{\ensuremath{{}^3}}
\newunicodechar{φ}{\ensuremath{\varphi}}
\newunicodechar{Σ}{\ensuremath{\Sigma}}
\newunicodechar{Γ}{\ensuremath{\Gamma}}
\setlength{\emergencystretch}{3em}
\begin{document}""")
    (ROOT / "paper.tex").write_text(text, encoding="utf-8", newline="\n")
    with tempfile.TemporaryDirectory(prefix="sn-mssn-pdf-") as directory:
        output = Path(directory)
        for _ in range(3):
            run = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error",
                                  "-no-shell-escape", f"-output-directory={output}", "paper.tex"],
                                 cwd=ROOT, capture_output=True, text=True,
                                 encoding="utf-8", errors="replace")
            if run.returncode:
                raise RuntimeError(run.stdout[-6000:] + run.stderr[-2000:])
        shutil.copyfile(output / "paper.pdf", ROOT / "paper.pdf")
    print("PDF built in three passes successfully")


if __name__ == "__main__":
    build()
