import os
import re
import yaml

matrix_path = 'TRACEABILITY_MATRIX.md'
matrix_text = open(matrix_path, encoding='utf-8').read()

# 1. Check claim counts
mub6_ledger = yaml.safe_load(open('papers/core/mub6/mub6_claim_ledger.yaml', encoding='utf-8'))
fsp_ledger = yaml.safe_load(open('papers/core/fsp/claim_ledger.yaml', encoding='utf-8'))
maj_ledger = yaml.safe_load(open('papers/core/majorana/claim_ledger.yaml', encoding='utf-8'))

mub6_claim_ids = set()
for c in mub6_ledger.get('claims', []):
    mub6_claim_ids.add(c.get('claim_id') or c.get('id'))

fsp_claim_ids = set()
for c in fsp_ledger.get('claims', []):
    fsp_claim_ids.add(c.get('claim_id') or c.get('id'))

maj_claim_ids = set()
for c in maj_ledger.get('claims', []):
    maj_claim_ids.add(c.get('claim_id') or c.get('id'))

print(f"Source ledgers claim counts: MUB6={len(mub6_claim_ids)}, FSP={len(fsp_claim_ids)}, Majorana={len(maj_claim_ids)}")

# Find claim occurrences in matrix
matrix_mub6 = set(re.findall(r'\b(MUB6-C\d+)\b', matrix_text))
matrix_maj = set(re.findall(r'\b(MAJ-C\d+)\b', matrix_text))

# FSP claims
fsp_patterns = [r'\b(PO-023-C\d+)\b', r'\b(GIN-C\d+)\b', r'\b(NF-\d+)\b', r'\b(MERON-\d+)\b', r'\b(HUBBARD-\d+)\b', r'\b(ORIGIN-\d+)\b']
matrix_fsp = set()
for p in fsp_patterns:
    matrix_fsp.update(re.findall(p, matrix_text))

print(f"Matrix claim counts: MUB6={len(matrix_mub6)}, FSP={len(matrix_fsp)}, Majorana={len(matrix_maj)}")

missing_mub6 = mub6_claim_ids - matrix_mub6
missing_fsp = fsp_claim_ids - matrix_fsp
missing_maj = maj_claim_ids - matrix_maj

print(f"Missing MUB6 claims: {missing_mub6}")
print(f"Missing FSP claims: {missing_fsp}")
print(f"Missing Majorana claims: {missing_maj}")

# 2. Check forbidden words
forbidden_words = [
    'proves', 'guarantees', 'mathematically verifies', 'fundamentally',
    'true intelligence', 'impossible', 'universal', 'flawless', 'perfectly',
    'clearly', 'obviously', 'simply', 'merely', 'weaponized'
]

print("\n--- Forbidden Words Audit ---")
lines = matrix_text.splitlines()
found_forbidden = []
for line_idx, line in enumerate(lines, 1):
    for word in forbidden_words:
        # Check case-insensitive word boundary
        matches = list(re.finditer(rf'\b{re.escape(word)}\b', line, re.IGNORECASE))
        for m in matches:
            found_forbidden.append((line_idx, word, line.strip()))

print(f"Total forbidden word hits: {len(found_forbidden)}")
for hit in found_forbidden:
    print(f"  Line {hit[0]} [{hit[1]}]: {hit[2]}")
