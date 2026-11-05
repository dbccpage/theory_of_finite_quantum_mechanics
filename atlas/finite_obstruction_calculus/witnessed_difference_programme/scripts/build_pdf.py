"""Regenerate Markdown-bound TeX for the canonical paper-edition compiler."""

from build_paper_artifacts import TEX_OUT, build_tex

if __name__ == "__main__":
    build_tex(TEX_OUT)
