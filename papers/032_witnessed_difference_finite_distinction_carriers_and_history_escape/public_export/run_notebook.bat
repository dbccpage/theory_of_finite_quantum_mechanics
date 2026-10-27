@echo off
rem SPDX-License-Identifier: Apache-2.0
cd /d "%~dp0.."
if errorlevel 1 exit /b 1
jupyter notebook jupyter_notebooks/001_reviewer_wd2_finite_distinction_carriers_and_history_escape.ipynb
