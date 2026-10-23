#!/usr/bin/env bash
cd "$(dirname "$0")/.."
uv run --with jupyter --with ipywidgets --with numpy --with matplotlib jupyter notebook jupyter_notebooks/000_two_pairs_need_to_agree.ipynb
