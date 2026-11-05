"""Two-episode operator growth and reuse control over T = {a, b, c} (SG-48).

AuthorityEffect: None.
"""

from __future__ import annotations

CARRIER: tuple[str, str, str] = ("a", "b", "c")
INITIAL_REGISTRY: dict[str, dict[str, str]] = {
    "id": {"a": "a", "b": "b", "c": "c"},
    "swap_ab": {"a": "b", "b": "a", "c": "c"},
}
CANDIDATE_SWAP_BC: dict[str, str] = {"a": "a", "b": "c", "c": "b"}


def _reachable(start: str, registry: dict[str, dict[str, str]]) -> set[str]:
    seen = {start}
    frontier = [start]
    while frontier:
        curr = frontier.pop()
        for op in registry.values():
            nxt = op[curr]
            if nxt not in seen:
                seen.add(nxt)
                frontier.append(nxt)
    return seen


def _verify_bijection_involution(op: dict[str, str]) -> bool:
    if set(op.keys()) != set(CARRIER) or set(op.values()) != set(CARRIER):
        return False
    return all(op[op[x]] == x for x in CARRIER)


def run_sg_48_episodes(
    candidate_op: dict[str, str] | None = None,
    verify_stage_5_before_use: bool = True,
    task2_sealed_during_ep1: bool = True,
    reuse_ep1_receipt_for_ep2: bool = False,
    mutate_task1_target: str = "c",
    promote_uncertified_metalift: bool = False,
) -> dict[str, object]:
    """Execute Episode 1 (failure -> operator admission -> solve a->c) and Episode 2 (reuse on b->c)."""
    if (
        type(verify_stage_5_before_use) is not bool
        or type(task2_sealed_during_ep1) is not bool
        or type(reuse_ep1_receipt_for_ep2) is not bool
        or type(mutate_task1_target) is not str
        or type(promote_uncertified_metalift) is not bool
    ):
        raise ValueError("invalid SG-48 control flags")
    if not task2_sealed_during_ep1:
        raise ValueError("task_2 must remain sealed until Episode 1 Stage 5 admission")
    if mutate_task1_target != "c":
        raise ValueError("task_1 target mutation refused")
    if promote_uncertified_metalift:
        raise ValueError("uncertified MetaLift promotion refused")
    if not verify_stage_5_before_use:
        raise ValueError("pre-verification operator execution refused")
    if reuse_ep1_receipt_for_ep2:
        raise ValueError("cached Episode 1 receipt refused for Episode 2 task_2")

    op = dict(CANDIDATE_SWAP_BC if candidate_op is None else candidate_op)
    registry = {k: dict(v) for k, v in INITIAL_REGISTRY.items()}

    reach_r0 = _reachable("a", registry)
    if "c" in reach_r0:
        raise RuntimeError("expected reachability gap under R0")

    if not _verify_bijection_involution(op):
        raise ValueError("Stage 5 host verifier rejected non-involution candidate operator")

    registry["swap_bc"] = op
    ep1_state = registry["swap_bc"][registry["swap_ab"]["a"]]
    if ep1_state != "c":
        raise ValueError("Episode 1 composition swap_bc(swap_ab(a)) did not reach c")

    ep1_receipt = {
        "episode": 1,
        "task": "a->c",
        "initial_reachable": tuple(sorted(reach_r0)),
        "admitted_operator": "swap_bc",
        "word": ("swap_ab", "swap_bc"),
        "terminal_state": ep1_state,
    }

    # Episode 2 unsealed after Episode 1 admission
    ep2_state = registry["swap_bc"]["b"]
    if ep2_state != "c":
        raise ValueError("Episode 2 reuse swap_bc(b) did not reach c")

    ep2_receipt = {
        "episode": 2,
        "task": "b->c",
        "reused_operator": "swap_bc",
        "word": ("swap_bc",),
        "terminal_state": ep2_state,
    }

    return {
        "r0_size": 2,
        "r1_size": len(registry),
        "episode_1_receipt": ep1_receipt,
        "episode_2_receipt": ep2_receipt,
        "task2_unsealed_after_ep1_stage5": True,
    }


def witness() -> dict[str, object]:
    return run_sg_48_episodes()
