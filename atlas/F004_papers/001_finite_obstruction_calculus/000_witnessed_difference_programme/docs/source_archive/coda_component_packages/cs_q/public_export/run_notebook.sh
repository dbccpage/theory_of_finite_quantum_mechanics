#!/usr/bin/env bash
set -euo pipefail
# Install once from the package root: python -m pip install -e ".[replay]"
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
exec python -m notebook jupyter_notebooks/000_two_dots_do_not_make_a_curve.ipynb
