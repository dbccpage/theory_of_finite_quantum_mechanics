@echo off
echo Running Paper 002 Constraint Closure & L1 Structure Notebooks (Levels 1-5)...
cd /d "%~dp0\.."
python code/run_notebook.py --all %*
pause
