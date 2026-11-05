# -*- coding: utf-8 -*-
"""
Use cases layer for the CODA application.
Orchestrates application workflows across the 9 CODA domain layers.

AuthorityEffect: None.
"""

from coda_application.use_cases import anomalon_store
from coda_application.use_cases.audit_firewall import audit_authority_firewall
from coda_application.use_cases.evaluate_pipeline import (
    CodaPipelineEvaluator,
    evaluate_coda_pipeline,
    evaluate_evidence,
    evaluate_triad_pipeline,
)
from coda_application.use_cases.solve_l1_repair import solve_exact_l1_repair

# Retained anomalons persist beyond the process (see anomalon_store).
anomalon_store.install()

__all__ = [
    "CodaPipelineEvaluator",
    "audit_authority_firewall",
    "evaluate_coda_pipeline",
    "evaluate_evidence",
    "evaluate_triad_pipeline",
    "solve_exact_l1_repair",
]
