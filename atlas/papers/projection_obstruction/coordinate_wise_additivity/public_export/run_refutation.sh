#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
NB="jupyter_notebooks/refutation_sandbox.ipynb"
if [[ ! -f "$NB" ]]; then
  echo "ERROR: $NB not found under $(pwd)" >&2
  exit 1
fi
echo ""
echo " Refutation sandbox launcher — coordinate_wise_additivity"
echo " Package root: $(pwd)"
echo " Opening:      $NB"
echo ""
exec uv run --frozen --extra notebooks jupyter notebook "$NB"
