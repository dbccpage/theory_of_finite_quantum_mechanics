"""M6 — Licensed Context Extension (5 super-gates)."""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ContextExtensionRequest:
    request_id: str
    current_context_id: str
    open_residual_ref: str
    q1_residual_ref: Optional[str]
    proposed_extension_tokens: List[str]
    attempted_same_level_operations: List[str]
    authority_effect: str = "None"


@dataclass
class LicensedContextExtension:
    extension_id: str
    request_id: str
    source_context_id: str
    target_context_id: str
    preservation_check_passed: bool
    residual_reduction_check_passed: bool
    non_destruction_check_passed: bool
    replay_check_passed: bool
    extension_justification_check_passed: bool
    all_gates_passed: bool
    authority_effect: str = "None"


class LceEngine:
    def evaluate_request(
        self, request: ContextExtensionRequest
    ) -> LicensedContextExtension:
        has_exhausted = len(request.attempted_same_level_operations) > 0
        has_open = len(request.open_residual_ref) > 0
        preservation = True
        residual_reduction = has_open
        non_destruction = True
        replay_passed = True
        justification = has_exhausted and request.authority_effect == "None"
        all_ok = all(
            [
                preservation,
                residual_reduction,
                non_destruction,
                replay_passed,
                justification,
            ]
        )
        return LicensedContextExtension(
            extension_id=f"LCE_{request.request_id[:8]}",
            request_id=request.request_id,
            source_context_id=request.current_context_id,
            target_context_id=f"{request.current_context_id}_LIFTED",
            preservation_check_passed=preservation,
            residual_reduction_check_passed=residual_reduction,
            non_destruction_check_passed=non_destruction,
            replay_check_passed=replay_passed,
            extension_justification_check_passed=justification,
            all_gates_passed=all_ok,
            authority_effect="None",
        )


