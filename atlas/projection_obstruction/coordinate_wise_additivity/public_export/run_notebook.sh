#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
NB="jupyter_notebooks/reviewer_coordinate_additivity.ipynb"
if [[ ! -f "$NB" ]]; then
  echo "ERROR: $NB not found under $(pwd)" >&2
  exit 1
fi
echo
echo " Reviewer notebook launcher — coordinate_wise_additivity"
echo " Package root: $(pwd)"
echo " Opening:      ${NB}"
echo " Deps: locked pyproject notebook extra via uv"
echo
exec uv run --frozen --extra notebooks jupyter notebook "${NB}"
