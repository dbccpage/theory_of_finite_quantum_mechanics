@echo off
setlocal EnableExtensions
cd /d "%~dp0.."
set "NB=jupyter_notebooks\02_rigorous_observer_cochains.ipynb"
if not exist "%NB%" (
  echo ERROR: %NB% not found under %CD%
  exit /b 1
)
echo.
echo  Rigorous notebook launcher — 006_vector_and_quantum_observer_geometries
echo  Package root: %CD%
echo  Opening:      %NB%
echo  Deps: jupyter + ipywidgets + numpy + scipy + matplotlib via uv
echo.
uv run --with jupyter --with ipywidgets --with numpy --with scipy --with matplotlib jupyter notebook "%NB%"
