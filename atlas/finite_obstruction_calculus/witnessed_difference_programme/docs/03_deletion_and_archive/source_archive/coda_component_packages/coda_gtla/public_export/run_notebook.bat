@echo off
cd /d "%~dp0.."
uv run --with jupyter --with ipywidgets --with numpy --with matplotlib jupyter notebook jupyter_notebooks/000_six_jobs_not_one_machine.ipynb
