"""Check a multi-episode continuation trace, not a first-answer arena policy.

The outer wrapper starts at level 1, solves once, learns/checks/installs a
task-bound rule, transports to level 2, then emits both original child answers.
An episode emission returns to this wrapper, NOT to a fresh fuel account.
This module imports no arena optimizer or certificate producer.
"""

from fractions import Fraction as Q

from .core import (X0, bundle_matches, decode, packet_digest, parent_packet,
                   rejects, valid)


def check_trace(rows, *, budget=18):
    try:
        phase, spent, level = "parent_propose", Q(0), 1
        parent_identity, candidate, child_answers = "finite-d1-parent", None, set()
        parent_answer, bundle = None, None
        packet = parent_packet(d=1, level=1)
        for row in rows:
            if set(row) != {"parent", "task", "operation", "charge", "spent"}:
                raise ValueError("malformed ledger row")
            if row["parent"] != parent_identity or row["task"] != 1:
                raise ValueError("parent or task changed during re-entry")
            operation = row["operation"]
            if phase == "parent_propose" and operation == "parent proposal X1 (1,-1)":
                candidate, price, phase = (1, -1), Q(1), "parent_check"
                if decode(level, candidate) != (0, 1):
                    raise ValueError("invalid parent carrier or decoder")
            elif phase == "parent_check" and operation == "parent check":
                if not valid(level, 1, candidate):
                    raise ValueError("parent check failed")
                price, phase = Q(2), "parent_emit"
            elif phase == "parent_emit" and operation == "parent emit (0,1)":
                parent_answer = decode(level, candidate)
                price, phase, candidate = Q(1), "learn", None
            elif phase == "learn" and operation == "learn":
                bundle = {"parent_sha256": packet_digest(packet), "task": 1, "level": 1}
                price, phase = Q(1), "bundle_check"
            elif phase == "bundle_check" and operation == "bundle check":
                if not bundle_matches(bundle, packet):
                    raise ValueError("stale bundle")
                if any(rejects(1, 1, p, "parameterized") for p in
                       (q for q in map(tuple, packet["carrier"]) if valid(1, 1, q))):
                    raise ValueError("unsafe bundle")
                price, phase = Q(1), "install"
            elif phase == "install" and operation == "install":
                if not bundle_matches(bundle, packet):
                    raise ValueError("parent changed before installation")
                price, phase = Q(1), "transport"
            elif phase == "transport" and operation == "transport 12":
                price, phase, level = Q(1), "child_propose", 2
            elif phase == "child_propose" and operation in ("child proposal (1,0)", "child proposal (1,2)"):
                candidate = (1, 0) if operation == "child proposal (1,0)" else (1, 2)
                decode(level, candidate)  # Exact carrier admission; raises off-image.
                price, phase = Q(1), "child_guard"
            elif phase == "child_guard" and operation == "guard":
                if rejects(level, 1, candidate, "parameterized"):
                    raise ValueError("child guard rejected")
                price, phase = Q(1, 2), "child_check"
            elif phase == "child_check" and operation == "child check":
                if not valid(level, 1, candidate):
                    raise ValueError("child check failed")
                price, phase = Q(2), "child_emit"
            elif phase == "child_emit" and operation in ("emit (0,1)", "emit (1,0)"):
                answer = decode(level, candidate)
                if operation != f"emit ({answer[0]},{answer[1]})":
                    raise ValueError("emitted answer does not commute with decoder")
                child_answers.add(answer)
                required = {p for p in X0 if valid(0, 1, p)}
                phase = "done" if child_answers == required else "child_propose"
                price, candidate = Q(1), None
            else:
                raise ValueError("operation not enabled in this continuation phase")
            charge = Q(row["charge"])
            if charge != price or charge <= 0:
                raise ValueError("incorrect operation charge")
            spent += charge
            if spent > budget or Q(row["spent"]) != spent:
                raise ValueError("budget exceeded or cumulative fuel reset")
        if phase != "done" or parent_answer != (0, 1):
            raise ValueError("incomplete parent/child continuation")
        return {"accepted": True, "scope": "finite multi-episode wrapper, not arena optimality",
                "spent": str(spent), "remaining": str(Q(budget) - spent),
                "child_answers": [[int(x), int(y)] for x, y in sorted(child_answers)], "authority_effect": "None"}
    except (ValueError, TypeError, KeyError, ZeroDivisionError) as error:
        return {"accepted": False, "reason": str(error), "authority_effect": "None"}
