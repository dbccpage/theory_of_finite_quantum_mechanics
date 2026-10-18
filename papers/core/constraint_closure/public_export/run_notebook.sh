#!/usr/bin/env bash
echo "Running Paper 002 Constraint Closure & L1 Structure Notebooks (Levels 1-5)..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."
python code/run_notebook.py --all "$@"
