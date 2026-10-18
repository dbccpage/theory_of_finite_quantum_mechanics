# TPP PowerShell Launcher Script for Paper Package 002
$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Write-Host "Running TPP Reviewer Notebook launcher..." -ForegroundColor Cyan
python "$PSScriptRoot\run_notebook.py"
