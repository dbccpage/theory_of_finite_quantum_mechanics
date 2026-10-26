#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
NB="jupyter_notebooks/refutation_sandbox.ipynb"
if [[ ! -f "$NB" ]]; then
  echo "ERROR: $NB not found under $(pwd)" >&2
  exit 1
fi
echo
echo " Refutation sandbox launcher — m_compatible_gauge_classification"
echo " Package root: $(pwd)"
echo " Opening:      $NB"
echo
exec uv run --with jupyter --with ipywidgets --with numpy --with matplotlib jupyter notebook "$NB"
