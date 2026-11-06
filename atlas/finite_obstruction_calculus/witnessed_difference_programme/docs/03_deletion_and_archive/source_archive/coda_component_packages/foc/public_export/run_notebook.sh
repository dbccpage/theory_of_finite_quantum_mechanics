#!/usr/bin/env bash
cd "$(dirname "$0")/.."
uv run --locked --extra verification --extra notebook jupyter notebook jupyter_notebooks/000_what_is_a_defect.ipynb
