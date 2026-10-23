"""Staged chain-complex repair episode control over Z on the triangle graph (SG-40).

AuthorityEffect: None.
"""

from __future__ import annotations

PARTIAL_1: tuple[tuple[int, int, int], ...] = (
    (-1, 0, 1),
    (1, -1, 0),
    (0, 1, -1),
)
CYCLE_Z: tuple[int, int, int] = (1, 1, 1)


def _mat_vec_mul(mat: tuple[tuple[int, ...], ...], vec: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(row[j] * vec[j] for j in range(len(vec))) for row in mat)


def run_sg_40_episode(
    partial_2: tuple[int, int, int] = (1, 1, 1),
    beta: int = 1,
    extension_declared: bool = True,
    receipt_issuer: str = "host_stage_5",
) -> dict[str, object]:
    """Execute Stages 0..8 of the SG-40 triangle chain-complex repair episode."""
    if (
        len(partial_2) != 3
        or any(type(v) is not int for v in partial_2)
        or type(beta) is not int
        or type(extension_declared) is not bool
        or type(receipt_issuer) is not str
    ):
        raise ValueError("invalid SG-40 episode parameters")
    if receipt_issuer != "host_stage_5":
        raise ValueError("parser self-receipt refused: Stage 5 host verifier required")
    if not extension_declared:
        raise ValueError("undeclared 2-cell attachment refused")

    # Stage 0..4: problem specification, cycle check, initial obstruction
    d1_z = _mat_vec_mul(PARTIAL_1, CYCLE_Z)
    if d1_z != (0, 0, 0):
        raise ValueError(f"z is not a 1-cycle: d1(z) = {d1_z}")

    rank_d1 = 2
    before_h1_rank = 3 - rank_d1 - 0
    before_receipt = {
        "issuer": receipt_issuer,
        "d1_z": d1_z,
        "rank_d1": rank_d1,
        "free_h1_rank": before_h1_rank,
        "z_is_boundary": False,
    }

    # Stage 5: host integer verification of proposed 2-cell attachment partial_2 and witness beta
    d1_d2 = _mat_vec_mul(PARTIAL_1, partial_2)
    if d1_d2 != (0, 0, 0):
        raise ValueError(f"chain complex identity d1 * d2 = 0 failed: got {d1_d2}")

    d2_beta = tuple(v * beta for v in partial_2)
    if d2_beta != CYCLE_Z:
        raise ValueError(f"witness equation d2 * beta = z failed: got {d2_beta} != {CYCLE_Z}")

    rank_d2 = 1 if partial_2 != (0, 0, 0) else 0
    after_h1_rank = 3 - rank_d1 - rank_d2
    after_receipt = {
        "issuer": receipt_issuer,
        "d1_d2": d1_d2,
        "d2_beta": d2_beta,
        "rank_d2": rank_d2,
        "free_h1_rank": after_h1_rank,
        "z_is_boundary": True,
    }

    stages = tuple(range(9))
    return {
        "stages_executed": stages,
        "before_receipt": before_receipt,
        "after_receipt": after_receipt,
        "answer_verified": after_h1_rank == 0 and after_receipt["z_is_boundary"] is True,
    }


def witness() -> dict[str, object]:
    return run_sg_40_episode()
