"""
Unit tests for DDC Operation T (Terminalization).
AuthorityEffect: None.
"""

from fractions import Fraction

from terminalization import TerminalizationEvaluator


def test_terminal_local_green():
    """Residual zero triggers LOCAL_GREEN_FOR_SCOPE."""
    evaluator = TerminalizationEvaluator()
    receipt = evaluator.evaluate(
        residual_norm=Fraction(0),
        remaining_budget=Fraction(10),
        residual_history=[Fraction(2), Fraction(1), Fraction(0)],
    )

    assert receipt.is_terminal is True
    assert receipt.verdict == "LOCAL_GREEN_FOR_SCOPE"


def test_terminal_out_of_budget():
    """Zero or negative budget triggers HALTED_OUT_OF_BUDGET."""
    evaluator = TerminalizationEvaluator()
    receipt = evaluator.evaluate(
        residual_norm=Fraction(3),
        remaining_budget=Fraction(0),
        residual_history=[Fraction(3)],
    )

    assert receipt.is_terminal is True
    assert receipt.verdict == "HALTED_OUT_OF_BUDGET"


def test_terminal_stagnant_progress():
    """Stagnant residuals over lookback window trigger HALTED_STAGNANT_PROGRESS."""
    evaluator = TerminalizationEvaluator(progress_lookback=3)
    receipt = evaluator.evaluate(
        residual_norm=Fraction(5),
        remaining_budget=Fraction(10),
        residual_history=[Fraction(5), Fraction(5), Fraction(5)],
    )

    assert receipt.is_terminal is True
    assert receipt.verdict == "HALTED_STAGNANT_PROGRESS"


def test_can_continue():
    """Decreasing residual with positive budget allows continuation."""
    evaluator = TerminalizationEvaluator(progress_lookback=3)
    receipt = evaluator.evaluate(
        residual_norm=Fraction(2),
        remaining_budget=Fraction(10),
        residual_history=[Fraction(6), Fraction(4), Fraction(2)],
    )

    assert receipt.is_terminal is False
    assert receipt.verdict == "CAN_CONTINUE"
