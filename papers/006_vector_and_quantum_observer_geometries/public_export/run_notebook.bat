@echo off
setlocal EnableExtensions
cd /d "%~dp0.."
set "NB=%~1"
if not defined NB (
  if exist "jupyter_notebooks\01_intuitive_vector_quantum_geometry.ipynb" (
    set "NB=jupyter_notebooks\01_intuitive_vector_quantum_geometry.ipynb"
  ) else if exist "jupyter_notebooks\02_rigorous_observer_cochains.ipynb" (
    set "NB=jupyter_notebooks\02_rigorous_observer_cochains.ipynb"
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
echo  Intuitive notebook launcher — 006_vector_and_quantum_observer_geometries
echo  Package root: %CD%
echo  Opening:      %NB%
echo  Deps: jupyter + ipywidgets + numpy + scipy + matplotlib via uv
echo.
uv run --with jupyter --with ipywidgets --with numpy --with scipy --with matplotlib jupyter notebook "%NB%"
