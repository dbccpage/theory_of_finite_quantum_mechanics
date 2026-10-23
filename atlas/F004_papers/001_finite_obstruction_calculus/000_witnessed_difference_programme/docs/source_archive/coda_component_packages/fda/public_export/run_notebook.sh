#!/usr/bin/env bash
cd "$(dirname "$0")/.."
uv run --with jupyter --with ipywidgets --with numpy --with matplotlib jupyter notebook jupyter_notebooks/000_a_proposal_is_not_a_decision.ipynb
