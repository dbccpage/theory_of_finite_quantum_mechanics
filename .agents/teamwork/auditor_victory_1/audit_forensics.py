import os
import glob
import re

print("=== Forensic Anti-Cheating & Facade Audit ===")

py_src = glob.glob("code/python/src/**/*.py", recursive=True)
suspicious_stubs = []
mock_occurrences = []

for f in py_src:
    with open(f, "r", encoding="utf-8", errors="ignore") as fp:
        content = fp.read()

    # Find functions that only do pass or return True/constant
    matches = re.finditer(r'def\s+([a-zA-Z0-9_]+)\s*\([^)]*\)\s*->?\s*[^:]*:\s*(?:"""[\s\S]*?"""\s*)?([^\n]+)', content)
    for m in matches:
        fn_name = m.group(1)
        first_line = m.group(2).strip()
        if fn_name.startswith("verify_") or fn_name.startswith("check_") or fn_name.startswith("certify_"):
            if first_line in ("return True", "pass", "return {}", "return []", "return None"):
                suspicious_stubs.append((f, fn_name, first_line))

    # Search for mock
    for idx, line in enumerate(content.splitlines()):
        if re.search(r'\b(mock_|mock\b|dummy_|fake_)', line, re.IGNORECASE) and not "mock-free" in line.lower():
            mock_occurrences.append((f, idx + 1, line.strip()))

print(f"Suspicious verification stubs (only return True/pass): {len(suspicious_stubs)}")
for s in suspicious_stubs:
    print(f"  {s[0]}:{s[1]} -> {s[2]}")

print(f"Mock / dummy occurrences in code/python/src: {len(mock_occurrences)}")
for m in mock_occurrences[:10]:
    print(f"  {m[0]}:{m[1]} -> {m[2]}")

print("\n=== E2E Test Suite Assertion & Mutation Check ===")
e2e_files = glob.glob("code/python/tests/e2e/*.py")
assert_count = 0
test_count = 0
for f in e2e_files:
    with open(f, "r", encoding="utf-8", errors="ignore") as fp:
        content = fp.read()
    test_count += len(re.findall(r'def test_', content))
    assert_count += len(re.findall(r'\bassert\b', content))

print(f"E2E test files: {len(e2e_files)}")
print(f"E2E test functions: {test_count}")
print(f"E2E assert statements: {assert_count} (avg {assert_count / max(test_count, 1):.1f} asserts/test)")

print("\n=== Claim Hygiene Audit in TRACEABILITY_MATRIX.md ===")
with open("TRACEABILITY_MATRIX.md", "r", encoding="utf-8") as fp:
    tm_text = fp.read()

forbidden = [
    "proves", "guarantees", "mathematically verifies", "fundamentally",
    "true intelligence", "impossible", "flawless", "perfectly",
    "clearly", "obviously", "simply", "merely", "weaponized"
]
found_forbidden = []
for word in forbidden:
    for m in re.finditer(rf'\b{re.escape(word)}\b', tm_text, re.IGNORECASE):
        start = max(0, m.start() - 25)
        end = min(len(tm_text), m.end() + 25)
        snippet = tm_text[start:end].replace('\n', ' ')
        found_forbidden.append((word, snippet))

print(f"Forbidden words found in TRACEABILITY_MATRIX.md: {len(found_forbidden)}")
for w, snip in found_forbidden:
    print(f"  [{w}]: ...{snip}...")

print("\n=== Section 6 Mandatory Summaries Audit ===")
sec6_headings = [
    "### 6.1 MUB(6) Four-Point Summary",
    "### 6.2 Fermion Sign Problem (FSP) Four-Point Summary",
    "### 6.3 Majorana Problem Four-Point Summary"
]
for h in sec6_headings:
    present = h in tm_text
    print(f"Heading '{h}': {'PRESENT' if present else 'MISSING'}")

required_bullets = [
    "1. **What it supports:**",
    "2. **What it does not support:**",
    "3. **The narrowest defensible claim:**",
    "4. **The next test needed:**"
]
for b in required_bullets:
    count = tm_text.count(b)
    print(f"Bullet '{b}': count={count} (expected >= 3)")
