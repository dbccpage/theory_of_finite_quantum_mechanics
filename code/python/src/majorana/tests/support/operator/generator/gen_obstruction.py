"""Obstruction candidate generator interface."""


class CandidateGenerator:
    def generate(self, state) -> list:
        raise NotImplementedError


__all__ = ["CandidateGenerator"]
