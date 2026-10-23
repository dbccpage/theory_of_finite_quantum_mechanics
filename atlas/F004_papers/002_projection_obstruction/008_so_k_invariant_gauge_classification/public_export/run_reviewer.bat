@echo off
setlocal EnableExtensions
cd /d "%~dp0.."
set "NB=jupyter_notebooks\so_k_invariant_gauge_classification.ipynb"
if not exist "%NB%" (
  echo ERROR: %NB% not found under %CD%
  exit /b 1
)
echo.
echo  Reviewer notebook launcher — 008_so_k_invariant_gauge_classification
echo  Package root: %CD%
echo  Opening:      %NB%
echo  Deps: locked pyproject notebook extra via uv
echo.
uv run --frozen --extra notebooks jupyter notebook "%NB%"
