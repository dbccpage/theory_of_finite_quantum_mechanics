@echo off
rem Install once from the package root: python -m pip install -e ".[replay]"
cd /d "%~dp0.." || exit /b 1
python -m notebook jupyter_notebooks/000_what_is_left_over.ipynb
