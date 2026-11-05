"""Independent bounded request-envelope codec for AUTH-DTM2.

AuthorityEffect: None. The recorded Lean theorem covers one closed word only.
This Python codec adds tested syntactic framing, not a machine-code verifier,
an evaluator, configuration agreement, execution permission or authorization.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli, evaluate, Violation
from checker_support.cases import Cases
from checker_support.domains import MAX_RATIONAL_BITS, MAX_SEQUENCE_LENGTH, integer, sequence
from checker_support.outcome import Outcome

HEADER_TAG = 1
MAX_TOKEN = (1 << MAX_RATIONAL_BITS) - 1
MAX_PAYLOAD = MAX_SEQUENCE_LENGTH - 3


def _tokens(value: object, name: str) -> tuple[int, ...]:
    return tuple(integer(token, name, 0, MAX_TOKEN)
                 for token in sequence(value, name, maximum=MAX_PAYLOAD))


@dataclass(frozen=True, slots=True)
class RequestEnvelope:
    """Immutable framing VO; fuel is a token budget, never executed here.

    Invariants: natural tokens of at most 4096 bits, detached tuple payloads,
    combined payload at most 4093 tokens. Empty machine/input segments are
    syntactically permitted; machine validity is outside this envelope codec.
    """

    fuel: int
    machine: tuple[int, ...]
    input_word: tuple[int, ...]

    def __post_init__(self) -> None:
        integer(self.fuel, "fuel", 0, MAX_TOKEN)
        machine = _tokens(self.machine, "machine segment")
        input_word = _tokens(self.input_word, "input word")
        if len(machine) + len(input_word) > MAX_PAYLOAD:
            raise Violation("resource", "combined request payload exceeds 4093 tokens")
        object.__setattr__(self, "machine", machine)
        object.__setattr__(self, "input_word", input_word)

    def encode(self) -> tuple[int, ...]:
        """Linear work and storage in the bounded payload length."""
        return (HEADER_TAG, self.fuel, len(self.machine)) + self.machine + self.input_word

    @staticmethod
    def decode(word: object) -> Outcome[RequestEnvelope]:
        """Parse framing only, returning a typed refusal for malformed input."""
        return evaluate(_decode, word)


def _decode(word: object) -> RequestEnvelope:
    tokens = sequence(word, "request word")
    if len(tokens) < 3:
        raise Violation("input", "request header requires tag, fuel and machine length")
    tag = integer(tokens[0], "header tag", 0, MAX_TOKEN)
    if tag != HEADER_TAG:
        raise Violation("input", "unsupported request header tag")
    fuel = integer(tokens[1], "fuel", 0, MAX_TOKEN)
    size = integer(tokens[2], "machine length", 0, MAX_PAYLOAD)
    if size > len(tokens)-3:
        raise Violation("input", "machine length exceeds the supplied payload")
    return RequestEnvelope(fuel, _tokens(tokens[3:3+size], "machine segment"),
                           _tokens(tokens[3+size:], "input word"))


def main() -> int:
    run = Cases()
    request = RequestEnvelope(2, (7,), (3, 4))
    expected = (1, 2, 1, 7, 3, 4)
    run.require(request.encode() == expected, "recorded closed request word")
    run.require(RequestEnvelope.decode(expected).value == request, "recorded request decoding")
    run.require(len(request.encode()) == 6, "recorded request length")
    for invalid in ((0, 2, 1, 7, 3, 4), (1, 2, 4, 7, 3, 4), (1, 2), (True, 2, 1, 7, 3, 4)):
        result = RequestEnvelope.decode(invalid)
        run.require(not result.ok and result.error is not None and result.error.kind == "input",
                    "malformed request framing is refused")
    print(f"checks={run.checks} failures=0 scope=syntactic_request_envelope authority=None")
    return 0


if __name__ == "__main__":
    raise SystemExit(cli(main))
