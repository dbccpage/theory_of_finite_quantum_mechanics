#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
shopt -s nullglob
if [[ -f "jupyter_notebooks/interactive_gauge_classification_master.ipynb" ]]; then
  NB="jupyter_notebooks/interactive_gauge_classification_master.ipynb"
else
  NBS=(jupyter_notebooks/reviewer_*.ipynb jupyter_notebooks/*.ipynb)
  if [[ ${#NBS[@]} -eq 0 ]]; then
    echo "ERROR: no notebooks found under $(pwd)/jupyter_notebooks" >&2
    exit 1
  fi
  NB="${NBS[0]}"
fi
echo
echo " Interactive notebook launcher — 007_m_compatible_gauge_classification"
echo " Package root: $(pwd)"
echo " Opening:      ${NB}"
echo " Deps: jupyter + ipywidgets + numpy + matplotlib via uv"
echo
uv run --with jupyter --with ipywidgets --with numpy --with matplotlib jupyter notebook "${NB}"
