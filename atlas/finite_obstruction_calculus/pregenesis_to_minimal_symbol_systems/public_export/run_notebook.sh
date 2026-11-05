#!/usr/bin/env bash
cd "$(dirname "$0")/.."
uv run --with jupyter jupyter notebook jupyter_notebooks/000_pre_genesis_to_mssn_walkthrough.ipynb
