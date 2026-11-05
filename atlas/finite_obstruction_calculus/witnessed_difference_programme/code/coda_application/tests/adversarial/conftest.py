# -*- coding: utf-8 -*-
"""
Fixtures for the adversarial CODA suite. Helpers live in ``_support``.

AuthorityEffect: None.
"""

from __future__ import annotations

import pytest

from coda_application.domain.anomalon_registry import AnomalonRegistry


@pytest.fixture(autouse=True)
def _isolated_registry():
    AnomalonRegistry.reset()
    yield
    AnomalonRegistry.reset()
