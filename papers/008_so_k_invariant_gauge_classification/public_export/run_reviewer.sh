#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
NB="jupyter_notebooks/so_k_invariant_gauge_classification.ipynb"
if [[ ! -f "$NB" ]]; then
  echo "ERROR: $NB not found under $(pwd)" >&2
  exit 1
fi
echo
echo " Reviewer notebook launcher — 008_so_k_invariant_gauge_classification"
echo " Package root: $(pwd)"
echo " Opening:      ${NB}"
echo " Deps: locked pyproject notebook extra via uv"
echo
uv run --frozen --extra notebooks jupyter notebook "${NB}"
