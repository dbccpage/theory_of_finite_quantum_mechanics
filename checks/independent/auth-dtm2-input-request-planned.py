"""Independent check for one closed AUTH-DTM2 request list.

Recomputes the concatenation and one missing header.
Does not import repository code. No evaluator.
"""
from __future__ import annotations

header = 1
fuel = 2
machine_length = 1
machine_segment = [7]
input_word = [3, 4]

failures = 0


def check(name: str, cond: bool) -> None:
    global failures
    print(f"{name}: {cond}")
    if not cond:
        failures += 1


encoded = [header, fuel, machine_length] + machine_segment + input_word
missing = [0, 2, 1, 7, 3, 4]
check("header_is_1", header == 1)
check("fuel_is_2", fuel == 2)
check("machine_length_is_1", machine_length == 1)
check("segment_is_7", machine_segment == [7])
check("input_is_3_4", input_word == [3, 4])
check("encode_request", encoded == [1, 2, 1, 7, 3, 4])
check("length_6", len(encoded) == 6)
check("missing_begins_with_0", missing[0] == 0)
check("zero_differs_from_header", missing[0] != header)
print(f"failures={failures}")
raise SystemExit(failures)
