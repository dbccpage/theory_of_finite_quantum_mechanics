"""Forwarder for code_scoring_evaluator from operations.cicd.

AuthorityEffect: None.
Origin: code/python/operations/cicd/code_scoring_evaluator.py
Claim: urn:omega:operations:code_scoring_evaluator:forwarder:v2
Profile: Non-Numeric
"""

from pathlib import Path
import sys

_current_dir = Path(__file__).resolve().parent
if str(_current_dir) not in sys.path:
    sys.path.insert(0, str(_current_dir))

try:
    from .cicd.code_scoring_evaluator import (
        CodeScoringReceipt,
        FileScoreRecord,
        GateScore,
        GRADE_ORDER,
        GRADE_RANKS,
        score_source_file,
        evaluate_scoring_rubric,
        main,
    )
except (ImportError, ValueError):
    from cicd.code_scoring_evaluator import (
        CodeScoringReceipt,
        FileScoreRecord,
        GateScore,
        GRADE_ORDER,
        GRADE_RANKS,
        score_source_file,
        evaluate_scoring_rubric,
        main,
    )

if __name__ == '__main__':
    sys.exit(main())
