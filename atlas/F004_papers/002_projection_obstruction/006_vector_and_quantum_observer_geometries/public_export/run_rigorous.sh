#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
NB="jupyter_notebooks/02_rigorous_observer_cochains.ipynb"
if [[ ! -f "$NB" ]]; then
  echo "ERROR: $NB not found under $(pwd)" >&2
  exit 1
fi
echo
echo " Rigorous notebook launcher — 006_vector_and_quantum_observer_geometries"
echo " Package root: $(pwd)"
echo " Opening:      ${NB}"
echo " Deps: jupyter + ipywidgets + numpy + scipy + matplotlib via uv"
echo
uv run --with jupyter --with ipywidgets --with numpy --with scipy --with matplotlib jupyter notebook "${NB}"
