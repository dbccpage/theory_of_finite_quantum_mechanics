@echo off
setlocal EnableExtensions
cd /d "%~dp0.."
set "NB=jupyter_notebooks\refutation_sandbox.ipynb"
if not exist "%NB%" (
  echo ERROR: %NB% not found under %CD%
  exit /b 1
)
echo.
echo  Refutation sandbox launcher — 007_m_compatible_gauge_classification
echo  Package root: %CD%
echo  Opening:      %NB%
echo  Deps: jupyter + ipywidgets + numpy + matplotlib via uv
echo.
uv run --with jupyter --with ipywidgets --with numpy --with matplotlib jupyter notebook "%NB%"
