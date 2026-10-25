"""Independent check for one direct-candidate ceiling slice.

Recomputes the closed status strings and the selected flag.
Does not import repository code. No other candidate.
"""
from __future__ import annotations

record_admission = "open"
direct_id = "AIT-DTM0"
direct_admission = "partial"
syntax_status = "partial"
execution_status = "partial"
universality_status = "open"
direct_selected = False

failures = 0


def check(name: str, cond: bool) -> None:
    global failures
    print(f"{name}: {cond}")
    if not cond:
        failures += 1


check("record_open", record_admission == "open")
check("direct_id", direct_id == "AIT-DTM0")
check("direct_partial", direct_admission == "partial")
check("syntax_partial", syntax_status == "partial")
check("execution_partial", execution_status == "partial")
check("universality_open", universality_status == "open")
check("selected_false", direct_selected is False)
check("open_length_4", len(record_admission) == 4)
check("partial_length_7", len(direct_admission) == 7)
check("id_length_8", len(direct_id) == 8)
print(f"failures={failures}")
raise SystemExit(failures)
