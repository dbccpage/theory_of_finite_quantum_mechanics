"""Unit tests for DDATapeDFA validation."""

import pytest
from omega_engine_governance.contracts.dda_packets import DDATapeDFA, DDATapeValidationError


def test_valid_dda_tapes():
    assert DDATapeDFA.validate("C . R . E . I . T") is True
    assert DDATapeDFA.validate("C-R-M-T") is True
    assert DDATapeDFA.validate("C R Λ I T") is True
    assert DDATapeDFA.validate("C R D I T") is True


def test_invalid_dda_letter():
    with pytest.raises(DDATapeValidationError, match="Invalid DDA letter 'Z'"):
        DDATapeDFA.validate("C R Z T")


def test_terminal_absorption_violation():
    with pytest.raises(DDATapeValidationError, match="T absorption rule violated"):
        DDATapeDFA.validate("C R T E")


def test_refusal_without_terminal():
    with pytest.raises(
        DDATapeValidationError, match="Refusal letter M must be followed by terminal T"
    ):
        DDATapeDFA.validate("C R M E T")


