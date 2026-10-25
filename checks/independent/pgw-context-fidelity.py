"""Independent check for the narrowed two-value case of PGW-CONTEXT-FIDELITY.

No repository imports. Exact Booleans and integers only.
"""
from __future__ import annotations

CHECKS = 0
FAILURES = 0

SUPPLY = "supplyDiamond"
DESIGNATE = "designateA"
ONLY = "assertOnlyDiamond"
HAS = "assertHasA"


def check(cond: bool, msg: str) -> None:
    global CHECKS, FAILURES
    CHECKS += 1
    if not cond:
        FAILURES += 1
        print(f"FAIL {msg}")


def replay(history: list[str]) -> bool:
    state = False
    for event in history:
        if event == SUPPLY:
            state = state
        elif event == DESIGNATE:
            state = True
        else:
            raise ValueError(event)
    return state


def step_valid(state: bool, step: str) -> bool:
    if step == ONLY:
        return state is False
    if step == HAS:
        return state is True
    raise ValueError(step)


def valid_trace(state: bool, trace: list[str]) -> bool:
    return all(step_valid(state, step) for step in trace)


def separating_step(state: bool) -> str:
    return HAS if state else ONLY


def separating_trace(state: bool) -> list[str]:
    return [separating_step(state)]


def answer_only_diamond(history: list[str]) -> str:
    return "verified" if replay(history) is False else "retracted"


def main() -> None:
    states = [False, True]
    unequal = [(s, sp) for s in states for sp in states if s is not sp]
    check(len(unequal) == 2, "2 unequal state pairs")
    for replayed, declared in unequal:
        trace = separating_trace(declared)
        check(valid_trace(declared, trace), f"trace valid at declared {declared}")
        check(not valid_trace(replayed, trace), f"trace invalid at replayed {replayed}")
        check(len(trace) == 1, "separating trace has one step")
    for state in states:
        trace = separating_trace(state)
        check(valid_trace(state, trace), f"separating trace valid at {state}")
        check(valid_trace(state, []), f"empty trace valid at {state}")

    events = [SUPPLY, DESIGNATE]
    histories = (
        [[]]
        + [[event] for event in events]
        + [[e1, e2] for e1 in events for e2 in events]
    )
    check(len(histories) == 7, "7 histories of length at most 2")
    for history in histories:
        once = replay(history)
        twice = replay(list(history))
        check(once is twice, f"replay is a function on {history}")

    trunc = [SUPPLY]
    full = [SUPPLY, DESIGNATE]
    check(replay(trunc) is False, "supplyDiamond replays to false")
    check(replay(full) is True, "supplyDiamond then designateA replays to true")
    check(answer_only_diamond(trunc) == "verified", "truncated history answers verified")
    check(answer_only_diamond(full) == "retracted", "full history answers retracted")
    check(answer_only_diamond(trunc) != answer_only_diamond(full), "answers differ")

    def accept_equal(context: bool, history: list[str]) -> bool:
        return context is replay(history)

    def preserves(accept) -> bool:
        for context in states:
            for history in histories:
                if not accept(context, history):
                    continue
                for declared, _replayed in unequal:
                    trace = separating_trace(declared)
                    if context is declared and valid_trace(context, trace):
                        if not valid_trace(replay(history), trace):
                            return False
                if not valid_trace(replay(history), []):
                    return False
        return True

    check(preserves(accept_equal), "equality contract preserves the checked traces")
    for context in states:
        for history in histories:
            if accept_equal(context, history):
                check(context is replay(history), "accepted binding equals replay")

    def accept_stale(context: bool, history: list[str]) -> bool:
        return context is False and history == full

    check(accept_stale(False, full), "stale contract accepts false on the full history")
    check(replay(full) is True, "full history replay is true")
    check(False is not replay(full), "stale context differs from full replay")
    stale_trace = separating_trace(False)
    check(valid_trace(False, stale_trace), "only-diamond step valid at false")
    check(not valid_trace(replay(full), stale_trace), "only-diamond step invalid at true")
    check(not preserves(accept_stale), "stale contract does not preserve validity")

    if FAILURES:
        print(f"FAILED {FAILURES} of {CHECKS}")
        raise SystemExit(1)
    print(f"checked {CHECKS} conditions, 0 failures")
    print("unequal pairs 2; histories of length at most 2: 7")
    print("replay([supplyDiamond]) = false; replay([supplyDiamond, designateA]) = true")
    print("answers: verified on the first history, retracted on the second")


if __name__ == "__main__":
    main()
