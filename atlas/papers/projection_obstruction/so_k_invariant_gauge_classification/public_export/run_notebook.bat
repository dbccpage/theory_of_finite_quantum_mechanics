@echo off
setlocal EnableExtensions
cd /d "%~dp0.."
set "NB=%~1"
if not defined NB (
  if exist "jupyter_notebooks\visual_gauge_rigidity_and_separation.ipynb" (
    set "NB=jupyter_notebooks\visual_gauge_rigidity_and_separation.ipynb"
  ) else if exist "jupyter_notebooks\so_k_invariant_gauge_classification.ipynb" (
    set "NB=jupyter_notebooks\so_k_invariant_gauge_classification.ipynb"
  ) else (
    for %%F in ("jupyter_notebooks\*.ipynb") do (
      set "NB=%%F"
      goto :found
    )
  )
)
:found
if not defined NB (
  echo ERROR: no notebook found under %CD%\jupyter_notebooks
  exit /b 1
)
echo.
echo  Visual notebook launcher — so_k_invariant_gauge_classification
echo  Package root: %CD%
echo  Opening:      %NB%
echo  Deps: locked pyproject notebook extra via uv
echo.
uv run --frozen --extra notebooks jupyter notebook "%NB%"
