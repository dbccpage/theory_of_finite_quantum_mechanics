#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
NB="${1:-}"
if [[ -z "$NB" ]]; then
  if [[ -f "jupyter_notebooks/visual_gauge_rigidity_and_separation.ipynb" ]]; then
    NB="jupyter_notebooks/visual_gauge_rigidity_and_separation.ipynb"
  elif [[ -f "jupyter_notebooks/so_k_invariant_gauge_classification.ipynb" ]]; then
    NB="jupyter_notebooks/so_k_invariant_gauge_classification.ipynb"
  else
    shopt -s nullglob
    NBS=(jupyter_notebooks/*.ipynb)
    if [[ ${#NBS[@]} -eq 0 ]]; then
      echo "ERROR: no notebooks found under $(pwd)/jupyter_notebooks" >&2
      exit 1
    fi
    NB="${NBS[0]}"
  fi
fi
echo
echo " Visual notebook launcher — 008_so_k_invariant_gauge_classification"
echo " Package root: $(pwd)"
echo " Opening:      ${NB}"
echo " Deps: locked pyproject notebook extra via uv"
echo
uv run --frozen --extra notebooks jupyter notebook "${NB}"
