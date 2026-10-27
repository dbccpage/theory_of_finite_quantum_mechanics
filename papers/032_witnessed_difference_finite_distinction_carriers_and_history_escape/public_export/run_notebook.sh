#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
cd "$(dirname "$0")/.."
exec jupyter notebook jupyter_notebooks/001_reviewer_wd2_finite_distinction_carriers_and_history_escape.ipynb
