"""Reducer for accepted obstruction candidates."""

import math
from typing import Optional

from omega_engine.crates.type.obstruction_runtime import EvaluatedCandidate, ObstructionVerdict


class CandidateSelector:
    def select(self, evaluated: list[EvaluatedCandidate]) -> Optional[EvaluatedCandidate]:
        raise NotImplementedError


def select_best_accepted(evaluated: list[EvaluatedCandidate]) -> Optional[EvaluatedCandidate]:
    best = None
    for candidate in evaluated:
        if ObstructionVerdict.is_accepted(candidate.verdict) and math.isfinite(candidate.score):
            if best is None or candidate.score > best.score:
                best = candidate
    return best


class BestScoreSelector(CandidateSelector):
    def select(self, evaluated: list[EvaluatedCandidate]) -> Optional[EvaluatedCandidate]:
        return select_best_accepted(evaluated)


__all__ = ["BestScoreSelector", "CandidateSelector", "select_best_accepted"]
