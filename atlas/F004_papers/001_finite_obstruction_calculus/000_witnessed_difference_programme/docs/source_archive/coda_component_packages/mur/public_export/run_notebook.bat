@echo off
cd /d "%~dp0.."
uv run --with jupyter --with ipywidgets --with numpy --with matplotlib jupyter notebook jupyter_notebooks/000_moving_a_picture_to_a_coarser_one.ipynb
