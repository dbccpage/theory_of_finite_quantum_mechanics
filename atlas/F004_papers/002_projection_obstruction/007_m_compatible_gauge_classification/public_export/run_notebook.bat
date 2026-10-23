@echo off
setlocal EnableExtensions
cd /d "%~dp0.."
set "NB="
if exist "jupyter_notebooks\interactive_gauge_classification_master.ipynb" (
  set "NB=jupyter_notebooks\interactive_gauge_classification_master.ipynb"
) else (
  for %%F in ("jupyter_notebooks\reviewer_*.ipynb" "jupyter_notebooks\*.ipynb") do (
    set "NB=%%F"
    goto :found
  )
)
:found
if not defined NB (
  echo ERROR: no notebook found under %CD%\jupyter_notebooks
  exit /b 1
)
echo.
echo  Interactive notebook launcher — 007_m_compatible_gauge_classification
echo  Package root: %CD%
echo  Opening:      %NB%
echo  Deps: jupyter + ipywidgets + numpy + matplotlib via uv
echo.
uv run --with jupyter --with ipywidgets --with numpy --with matplotlib jupyter notebook "%NB%"
