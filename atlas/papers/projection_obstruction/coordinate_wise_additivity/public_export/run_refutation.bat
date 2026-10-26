@echo off
setlocal EnableExtensions
cd /d "%~dp0.."
set "NB=jupyter_notebooks\refutation_sandbox.ipynb"
if not exist "%NB%" (
  echo ERROR: %NB% not found under %CD%
  exit /b 1
)
echo.
echo  Refutation sandbox launcher — coordinate_wise_additivity
echo  Package root: %CD%
echo  Opening:      %NB%
echo  Deps: locked pyproject notebook extra via uv
echo.
uv run --frozen --extra notebooks jupyter notebook "%NB%"
