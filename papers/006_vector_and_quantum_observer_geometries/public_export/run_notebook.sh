#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
NB="${1:-}"
if [[ -z "$NB" ]]; then
  if [[ -f "jupyter_notebooks/01_intuitive_vector_quantum_geometry.ipynb" ]]; then
    NB="jupyter_notebooks/01_intuitive_vector_quantum_geometry.ipynb"
  elif [[ -f "jupyter_notebooks/02_rigorous_observer_cochains.ipynb" ]]; then
    NB="jupyter_notebooks/02_rigorous_observer_cochains.ipynb"
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
echo " Intuitive notebook launcher — 006_vector_and_quantum_observer_geometries"
echo " Package root: $(pwd)"
echo " Opening:      ${NB}"
echo " Deps: jupyter + ipywidgets + numpy + scipy + matplotlib via uv"
echo
uv run --with jupyter --with ipywidgets --with numpy --with scipy --with matplotlib jupyter notebook "${NB}"
