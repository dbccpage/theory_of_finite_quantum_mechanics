"""Independent finite controls for the six narrowed COMP-C2/C3/C6/C7/C8 cases.

AuthorityEffect: None. Imports checker infrastructure, never the production
computation implementation. Finite rewrite witnesses and bounded searches do
not establish Genesis Step3 encoding, M0/Code.eval agreement, a computable
infinite-language reduction, the extended R0-prime rule set, or minimality.
"""
from __future__ import annotations

from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import hole, integer, sequence
from checker_support.outcome import Outcome

Word = tuple[int, ...]
RewriteRule = tuple[Word, Word]
MAX_WORD_LENGTH = 64
MAX_STATES = 4096
MAX_RULE_TRIALS = 65536


def _natural(value: object, name: str) -> int:
    admitted = integer(value, name, 0)
    if admitted.bit_length() > 4096:
        raise Violation("resource", name + " exceeds 4096 bits")
    return admitted


def _word(value: object, maximum: int = MAX_WORD_LENGTH) -> Word:
    return tuple(integer(token, "word symbol", 0, 4095)
                 for token in sequence(value, "word", maximum=maximum))


@dataclass(frozen=True, slots=True, init=False)
class FiniteWordSystem:
    """Finite-word rewriting aggregate with owned alphabet/rules and a length bound.

    Alphabet: 1..32 distinct natural symbols <=4095. Rules: at most 32 distinct
    pairs of words, with empty sides admitted. Words have at most 64 symbols;
    search keeps only words within max_length. Exhaustion of a work/state budget
    is a typed resource refusal, never a negative reachability certificate.
    """

    alphabet: frozenset[int]
    rules: tuple[RewriteRule, ...]
    max_length: int

    def __init__(self, alphabet: object, rules: object, max_length: object = 8) -> None:
        symbols = tuple(integer(token, "alphabet symbol", 0, 4095)
                        for token in sequence(alphabet, "alphabet", maximum=32))
        if not symbols or len(set(symbols)) != len(symbols):
            raise Violation("input", "alphabet must be nonempty with distinct symbols")
        object.__setattr__(self, "alphabet", frozenset(symbols))
        object.__setattr__(self, "max_length", integer(max_length, "word length bound", 0, MAX_WORD_LENGTH))
        admitted = []
        for rule in sequence(rules, "rules", maximum=32):
            left, right = sequence(rule, "rewrite rule", 2)
            admitted.append((self.admit_word(left), self.admit_word(right)))
        if len(set(admitted)) != len(admitted):
            raise Violation("duplicate", "rewrite rules must be distinct")
        object.__setattr__(self, "rules", tuple(admitted))

    def admit_word(self, value: object) -> Word:
        word = _word(value)
        if any(token not in self.alphabet for token in word):
            raise Violation("input", "word contains a symbol outside the alphabet")
        return word

    def in_bound(self, value: object) -> bool:
        return len(self.admit_word(value)) <= self.max_length

    def apply(self, word: object, rule_index: object, prefix: object, suffix: object) -> Word:
        """Verify the stated one-hole context and return its exact replacement."""
        source, left, right = self.admit_word(word), self.admit_word(prefix), self.admit_word(suffix)
        index = integer(rule_index, "rule index", 0)
        if index >= len(self.rules):
            raise Violation("input", "rule index is outside this system")
        before, after = self.rules[index]
        replaced = hole(source, left, before, after, right)
        return self.admit_word(replaced)

    def _successors(self, word: Word) -> Iterator[Word]:
        """Internal ordered expansion; the caller reserves the entire trial cost."""
        for before, after in self.rules:
            for index in range(len(word) + 1):
                if word[index:index+len(before)] == before:
                    candidate = word[:index] + after + word[index+len(before):]
                    if len(candidate) <= self.max_length:
                        yield candidate

    @staticmethod
    def _path(parents: dict[Word, Word | None], target: Word) -> tuple[Word, ...]:
        route = []
        cursor: Word | None = target
        while cursor is not None:
            route.append(cursor)
            cursor = parents[cursor]
        return tuple(reversed(route))

    def _find_path(self, source: object, target: object, max_states: object, max_rule_trials: object) -> tuple[Word, ...] | None:
        state_budget = integer(max_states, "state budget", 1, MAX_STATES)
        trial_budget = integer(max_rule_trials, "rule-trial budget", 0, MAX_RULE_TRIALS)
        start, goal = self.admit_word(source), self.admit_word(target)
        if len(start) > self.max_length:
            raise Violation("input", "search source lies outside the declared length bound")
        if len(goal) > self.max_length:
            return None
        if start == goal:
            return (start,)
        parents: dict[Word, Word | None] = {start: None}
        frontier = deque([start])
        trials = 0
        while frontier:
            word = frontier.popleft()
            trials += len(self.rules) * (len(word) + 1)
            if trials > trial_budget:
                raise Violation("resource", "bounded search exhausted its rule-trial budget")
            for candidate in self._successors(word):
                if candidate in parents:
                    continue
                if len(parents) >= state_budget:
                    raise Violation("resource", "bounded search exhausted its state budget")
                parents[candidate] = word
                if candidate == goal:
                    return self._path(parents, candidate)
                frontier.append(candidate)
        return None

    def find_path(self, source: object, target: object, max_states: object = 1024,
                  max_rule_trials: object = MAX_RULE_TRIALS) -> Outcome[tuple[Word, ...] | None]:
        """Return a shortest bounded path, proved finite exhaustion (None), or refusal."""
        return evaluate(self._find_path, source, target, max_states, max_rule_trials)

    def _verify_trace(self, candidate: object, max_rule_trials: object) -> tuple[Word, ...]:
        budget = integer(max_rule_trials, "rule-trial budget", 0, MAX_RULE_TRIALS)
        trace = tuple(self.admit_word(word) for word in sequence(candidate, "trace", maximum=MAX_STATES))
        if not trace or any(len(word) > self.max_length for word in trace):
            raise Violation("input", "trace must be nonempty and inside the length bound")
        trials = 0
        for source, target in zip(trace, trace[1:]):
            trials += len(self.rules) * (len(source) + 1)
            if trials > budget:
                raise Violation("resource", "trace verification exhausted its rule-trial budget")
            if not any(word == target for word in self._successors(source)):
                raise Violation("check", "trace contains a step absent from the rewrite system")
        return trace

    def verify_trace(self, candidate: object, max_rule_trials: object = MAX_RULE_TRIALS) -> Outcome[tuple[Word, ...]]:
        return evaluate(self._verify_trace, candidate, max_rule_trials)


def merge01(value: int) -> int:
    token = _natural(value, "merge argument")
    return 0 if token == 1 else token


def write_halt(value_to_write: int, halted: bool, cell_value: int) -> tuple[bool, int]:
    proposed, current = _natural(value_to_write, "write value"), _natural(cell_value, "cell value")
    if type(halted) is not bool:
        raise Violation("input", "halted requires an exact bool")
    return (True, current) if halted else (True, proposed)


def eval_const(value: int, argument: int) -> int:
    result = _natural(value, "constant value")
    _natural(argument, "evaluation argument")
    return result


def start_word(code: int) -> tuple[int, int]:
    return integer(code, "finite code", 0, 4095), 0


def word_pred(word: object) -> bool:
    return _word(sequence(word, "encoded pair", 2)) == (1, 0)


def append_blank(word: object) -> list[int]:
    return [*_word(word, MAX_WORD_LENGTH - 1), 0]


def check_word_moves(cases: Cases) -> None:
    system = FiniteWordSystem((0, 1), (((), (1,)), ((), (0, 1)), ((1,), ())))
    cases.append(("c2.append_mark", system.apply((0,), 0, (0,), ()) == (0, 1)))
    cases.append(("c2.append_block", system.apply((0, 1), 1, (0, 1), ()) == (0, 1, 0, 1)))
    cases.append(("c2.erase_mark", system.apply((0, 1), 2, (0,), ()) == (0,)))
    cases.append(("c2.merge_distinct", merge01(0) == merge01(1) == 0 and len({0, 1}) == 2))
    cases.append(("c2.fix_other", merge01(2) == 2))


def check_no_rule_bound(cases: Cases) -> None:
    system = FiniteWordSystem((0,), (), 1)
    start, empty, long = (0,), (), (0, 0)
    cases.append(("c3.lengths", (len(start), len(empty), len(long)) == (1, 0, 2)))
    cases.append(("c3.membership", system.in_bound(start) and system.in_bound(empty) and not system.in_bound(long)))
    own, other, excluded = system.find_path(start, start), system.find_path(start, empty), system.find_path(start, long)
    cases.append(("c3.reflexive", own.ok and own.value == (start,)))
    cases.append(("c3.no_other", other.ok and other.value is None and excluded.ok and excluded.value is None))
    inside = [word for word in (empty, start, long) if system.in_bound(word)]
    outcomes = {start: own, empty: other, long: excluded}
    reached = [word for word in inside if outcomes[word].ok and outcomes[word].value is not None]
    cases.append(("c3.bounded_slice", inside == [empty, start] and reached == [start]))


def check_constant_writer(cases: Cases) -> None:
    for value in range(5):
        halted, stored = write_halt(value, False, 0)
        cases.append((f"c6.write.{value}", halted is True and stored == value))
        for argument in range(4):
            cases.append((f"c6.constant.{value}.{argument}", eval_const(value, argument) == stored))


def check_predicate_composition(cases: Cases) -> None:
    cases.append(("c7.encoding.zero", start_word(0) == (0, 0)))
    cases.append(("c7.encoding.one", start_word(1) == (1, 0)))
    cases.append(("c7.predicate.false", word_pred((0, 0)) is False))
    cases.append(("c7.predicate.true", word_pred((1, 0)) is True))
    cases.append(("c7.composition.false", word_pred(start_word(0)) is False))
    cases.append(("c7.composition.true", word_pred(start_word(1)) is True))


def check_fixed_target(cases: Cases) -> None:
    system = FiniteWordSystem((0, 1, 2), (((1,), ()), ((2,), ())), 2)
    for symbol, rule in ((1, 0), (2, 1)):
        result = system.apply((symbol, 0), rule, (), (0,))
        trace = system.verify_trace(((symbol, 0), result))
        cases.append((f"c7.fixed_target.{symbol}", result == (0,) and trace.ok and trace.value == ((symbol, 0), (0,))))


def check_marked_tape(cases: Cases) -> None:
    mark_a, mark_b, blank = 1, 2, 0
    word = append_blank((mark_a, mark_b))
    for name, condition in (("mark_a", mark_a == 1), ("mark_b", mark_b == 2), ("blank", blank == 0),
                            ("word", word == [1, 2, 0]), ("length", len(word) == 3),
                            ("blank_not_a", blank != mark_a), ("blank_not_b", blank != mark_b)):
        cases.append(("c8."+name, condition))


def run_checks() -> dict[str, object]:
    cases = Cases()
    for operation in (check_word_moves, check_no_rule_bound, check_constant_writer,
                      check_predicate_composition, check_fixed_target, check_marked_tape):
        operation(cases)
    failures = [name for name, passed in cases if not passed]
    return {"scope": "six finite computation controls", "authority_effect": "None",
            "total_checks": len(cases), "failed_checks": len(failures),
            "failures": failures, "all_passed": not failures}


def main() -> int:
    result = run_checks()
    print(json.dumps(result, indent=2))
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(cli(main))
