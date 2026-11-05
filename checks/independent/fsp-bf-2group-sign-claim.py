"""Multiplicative Z2 cocycle and normalized rephasing audit. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.binary_sign_cochain import BinarySignCochain
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.outcome import Outcome


@dataclass(frozen=True, slots=True, init=False)
class SignCocycleControls:
    """Owns a degree-three candidate for the stated finite obstruction."""
    cocycle: BinarySignCochain

    def __init__(self, cocycle: object = None) -> None:
        value = BinarySignCochain.generator() if cocycle is None else cocycle
        if type(value) is not BinarySignCochain or value.degree != 3:
            raise Violation("input", "candidate must be an admitted degree-three sign cochain")
        object.__setattr__(self, "cocycle", value)

    def _verify(self) -> dict[str, int]:
        cases = Cases()
        pentagon_cases = 0
        for point in product((0, 1), repeat=4):
            cases.require(self.cocycle._pentagon(point) == 1, "cocycle identity")
            pentagon_cases += 1
        cases.require(self.cocycle.is_normalized(), "cocycle normalization")
        cochains = 0
        normalized = 0
        for phases in product((-1, 1), repeat=4):
            cochains += 1
            beta = BinarySignCochain(2, phases)
            if not beta.is_normalized():
                continue
            normalized += 1
            boundary = beta._coboundary()
            transformed = self.cocycle._multiply(boundary)
            cases.require(boundary._at((1, 1, 1)) == 1, "normalized generator coboundary")
            cases.require(boundary.phases != self.cocycle.phases, "coboundary obstruction")
            cases.require(transformed._at((1, 1, 1)) == -1, "negative generator survives")
            cases.require(any(value == -1 for value in transformed.phases), "rephasing is not all positive")
        cases.require(normalized == 2, "normalized cochain population")
        return {"pentagon_cases": pentagon_cases, "cochains": cochains,
                "normalized_cochains": normalized, "generator_phase": self.cocycle._at((1, 1, 1)),
                "failures": 0, "checks": cases.checks}

    def verify(self) -> Outcome[dict[str, int]]:
        return evaluate(self._verify)


def _main() -> None:
    result = SignCocycleControls()._verify()
    print(f"pentagon_cases={result['pentagon_cases']} cochains={result['cochains']} "
          f"normalized_cochains={result['normalized_cochains']} "
          f"generator_phase={result['generator_phase']} failures={result['failures']}")


def main() -> int:
    return cli(_main)


if __name__ == "__main__":
    raise SystemExit(main())
