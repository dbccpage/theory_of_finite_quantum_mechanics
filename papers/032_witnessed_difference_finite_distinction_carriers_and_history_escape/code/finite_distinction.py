"""Finite observational refinement for the WD2 manuscript.

Relations are the paper's horizon relations: R_0 is the kernel of the
observation, and R_{n+1} keeps two states together only when every one-step
update lands in one R_n class. Words are applied left to right.
"""

from __future__ import annotations

from typing import Callable, Hashable, Sequence


State = Hashable
Symbol = Hashable
Update = Callable[[State, Symbol], State]
Observe = Callable[[State], Hashable]
Report = Callable[[State, Symbol], Hashable]


class MooreMachine:
    """Finite deterministic Moore machine with a declared state tuple."""

    def __init__(
        self,
        states: Sequence[State],
        alphabet: Sequence[Symbol],
        update: Update,
        observe: Observe,
    ) -> None:
        self.states = tuple(states)
        self.alphabet = tuple(alphabet)
        self.update = update
        self.observe = observe

    def run(self, state: State, word: Sequence[Symbol]) -> State:
        current = state
        for symbol in word:
            current = self.update(current, symbol)
        return current

    def readout(self, state: State, word: Sequence[Symbol]) -> Hashable:
        return self.observe(self.run(state, word))


def horizon_signatures(machine: MooreMachine, steps: int) -> list[dict[State, tuple]]:
    """Return signatures for R_0 through R_steps."""
    signature = {state: (machine.observe(state),) for state in machine.states}
    history = [signature]
    for _ in range(steps):
        signature = {
            state: (machine.observe(state),)
            + tuple(signature[machine.update(state, symbol)] for symbol in machine.alphabet)
            for state in machine.states
        }
        history.append(signature)
    return history


def class_count(signature: dict[State, tuple], states: Sequence[State]) -> int:
    return len({signature[state] for state in states})


def same_partition(
    left: dict[State, tuple], right: dict[State, tuple], states: Sequence[State]
) -> bool:
    return all(
        (left[one] == left[other]) == (right[one] == right[other])
        for one in states
        for other in states
    )


def refinement_holds(history: Sequence[dict[State, tuple]], states: Sequence[State]) -> bool:
    """R_{n+1} is finer than R_n, and the first equality is permanent."""
    for index in range(len(history) - 1):
        finer = all(
            history[index + 1][one] != history[index + 1][other]
            or history[index][one] == history[index][other]
            for one in states
            for other in states
        )
        if not finer:
            return False
    for index in range(len(history) - 2):
        if same_partition(history[index], history[index + 1], states):
            if not same_partition(history[index], history[-1], states):
                return False
    return True


def stabilized(machine: MooreMachine) -> tuple[int, int, int]:
    """Return N, b_0, and the number of R_N classes."""
    steps = max(len(machine.states), 1)
    history = horizon_signatures(machine, steps)
    if not refinement_holds(history, machine.states):
        raise ValueError("horizon relations are not a refinement")
    initial = class_count(history[0], machine.states)
    for index in range(steps):
        if same_partition(history[index], history[index + 1], machine.states):
            return index, initial, class_count(history[index], machine.states)
    raise ValueError("finite machine did not stabilize")


def words(alphabet: Sequence[Symbol], length: int) -> tuple[tuple[Symbol, ...], ...]:
    if length == 0:
        return ((),)
    shorter = words(alphabet, length - 1)
    return tuple(prefix + (symbol,) for prefix in shorter for symbol in alphabet)


def word_kernel_agrees(machine: MooreMachine, horizon: int) -> bool:
    """Lemma L1 on this machine: R_horizon is the kernel of words of length at most horizon."""
    history = horizon_signatures(machine, horizon)
    signature = history[horizon]
    bundles: dict[tuple, list[State]] = {}
    for state in machine.states:
        bundles.setdefault(signature[state], []).append(state)
    readable = tuple(
        word
        for length in range(horizon + 1)
        for word in words(machine.alphabet, length)
    )
    for block in bundles.values():
        for word in readable:
            readouts = {machine.readout(state, word) for state in block}
            if len(readouts) != 1:
                return False
    for index, left in enumerate(machine.states):
        for right in machine.states[index + 1 :]:
            if signature[left] == signature[right]:
                continue
            if all(
                machine.readout(left, word) == machine.readout(right, word) for word in readable
            ):
                return False
    return True


def shortest_separating_length(machine: MooreMachine, left: State, right: State) -> int | None:
    """Length of a shortest separating word, or None when the states stay together."""
    horizon, _, _ = stabilized(machine)
    for length in range(horizon + 1):
        for word in words(machine.alphabet, length):
            if machine.readout(left, word) != machine.readout(right, word):
                return length
    return None


def sharp_chain(size: int) -> MooreMachine:
    """Manuscript sharpness witness: one symbol, a chain into the unique output 1."""
    if size < 0:
        raise ValueError("state count is non-negative")

    def update(state: State, symbol: Symbol) -> State:
        if symbol != "a" or not isinstance(state, int):
            raise ValueError("sharp chain has one symbol")
        return min(state + 1, size - 1) if size else state

    def observe(state: State) -> int:
        if not isinstance(state, int):
            raise ValueError("sharp chain states are integers")
        return 1 if size and state == size - 1 else 0

    return MooreMachine(tuple(range(size)), ("a",) if size else (), update, observe)


def sharp_profile(size: int) -> dict[str, object]:
    """Class counts of the sharpness witness through horizon size - 1."""
    machine = sharp_chain(size)
    history = horizon_signatures(machine, max(size, 1))
    horizon, initial, stable = stabilized(machine)
    counts = [class_count(history[index], machine.states) for index in range(size)]
    return {
        "states": size,
        "b0": initial,
        "N": horizon,
        "stable_classes": stable,
        "class_counts": counts,
        "bound": size - initial,
        "word_kernel": word_kernel_agrees(machine, horizon),
    }


def no_escape_profile() -> dict[str, object]:
    """Two states with equal output and update-stable classes. N is 0."""
    machine = MooreMachine((0, 1), ("a", "b"), lambda state, symbol: state, lambda state: 0)
    horizon, initial, stable = stabilized(machine)
    return {
        "N": horizon,
        "b0": initial,
        "stable_classes": stable,
        "separating": shortest_separating_length(machine, 0, 1),
        "word_kernel": word_kernel_agrees(machine, horizon),
    }


def factored_report_profile() -> dict[str, object]:
    """A report that factors through the two endpoint observations preserves R_n."""
    machine = sharp_chain(4)

    def report(state: State, symbol: Symbol) -> tuple:
        if not isinstance(state, int):
            raise ValueError("report state")
        return (machine.observe(state), symbol, machine.observe(machine.update(state, symbol)))

    history = horizon_signatures(machine, 2)
    preserved = True
    for length in range(3):
        for word in words(machine.alphabet, length):
            for left in machine.states:
                for right in machine.states:
                    if history[length][left] != history[length][right]:
                        continue
                    left_state: State = left
                    right_state: State = right
                    for symbol in word:
                        if report(left_state, symbol) != report(right_state, symbol):
                            preserved = False
                        left_state = machine.update(left_state, symbol)
                        right_state = machine.update(right_state, symbol)
    escape = shortest_separating_length(machine, 0, 1)
    return {"reports_preserved": preserved, "escape_length": escape}
