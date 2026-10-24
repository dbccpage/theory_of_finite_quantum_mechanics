"""Independent census of the finite-QM claims list.

No repository imports. Reads two pinned YAML files as text.
"""

from collections import Counter
from pathlib import Path

failures = 0
checked = 0


def check(cond, msg):
    global failures, checked
    checked += 1
    if not cond:
        failures += 1
        print("FAIL", msg)


root = Path("sources/atlas/F004_papers/006_finite_qm/claims")
ledger_lines = (root / "claim_ledger.yaml").read_text(encoding="utf-8").splitlines()
gap_lines = (root / "gap_register.yaml").read_text(encoding="utf-8").splitlines()

start = ledger_lines.index("claims:") + 1
end = ledger_lines.index("application_claims:")
region = ledger_lines[start:end]
types = []
current = None
seen_id = False
for line in region:
    if line.startswith("- id:"):
        if seen_id:
            types.append(current)
        seen_id = True
        current = None
    elif line.startswith("  type:") and current is None:
        current = line.split(":", 1)[1].strip()
if seen_id:
    types.append(current)

counts = Counter(types)
order = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
expected = [
    ("FINITE COMPUTATION", 160),
    ("SCOPE FENCE", 156),
    ("OPEN", 115),
    ("DEFINITION", 104),
    ("EXACT FINITE ALGEBRA", 80),
    ("CONDITIONAL", 57),
    ("UNTYPED", 48),
    ("ASSERTED", 36),
    ("REFUTED BY AUDIT", 31),
    ("DECLARED", 17),
    ("FINITE FIXTURE", 12),
    ("REFUTED BY COMPUTATION", 10),
    ("REFUSAL", 7),
    ("PARTIAL", 1),
]

check(len(types) == 834, "claims list length")
check(all(item is not None for item in types), "every claim has a type")
check(len(counts) == 14, "fourteen type labels")
check(order == expected, "descending type census")
check(order[6] == ("UNTYPED", 48), "index 6 is UNTYPED 48")
for label, count in expected:
    check(counts[label] == count, label)
check(sum(count for _, count in order) == 834, "counts sum to 834")
check(counts["UNTYPED"] == 48, "UNTYPED count")
check(sum(1 for label, _ in order if label == "UNTYPED") == 1, "one UNTYPED label")
check(48 != 24, "48 != 24")
check(834 != 189, "834 != 189")
check(len([line for line in ledger_lines if line.startswith("- id:")]) != 834, "file-wide id lines are a larger list")

gap_start = gap_lines.index("- gap_id: GAP-FQM-002")
gap_block = []
for line in gap_lines[gap_start + 1 :]:
    if line.startswith("- gap_id:"):
        break
    gap_block.append(line)
title = next(line for line in gap_block if line.startswith("  title:")).split(":", 1)[1].strip()
description = " ".join(
    line.strip().strip("'") for line in gap_block if line.startswith("  description:") or line.startswith("    ")
)
check(title == "24 claim rows carry no parseable type", "GAP-FQM-002 title")
check("24 of 189" in description, "GAP-FQM-002 description")

print(f"checked {checked} claims, failures {failures}")
raise SystemExit(failures)
