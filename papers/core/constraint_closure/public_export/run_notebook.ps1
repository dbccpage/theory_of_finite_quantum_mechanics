Write-Host "Running Paper 002 Constraint Closure & L1 Structure Notebooks (Levels 1-5)..."
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $ScriptDir "..")
python code/run_notebook.py --all $args
