@echo off
rem Install once from the package root: python -m pip install -e ".[replay]"
cd /d "%~dp0.." || exit /b 1
python -m notebook jupyter_notebooks/000_two_dots_do_not_make_a_curve.ipynb
