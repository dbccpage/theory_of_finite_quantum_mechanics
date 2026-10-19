import os
import re

lean_dir = 'lean4'
matrix_text = open('TRACEABILITY_MATRIX.md', encoding='utf-8').read()

# Pattern for table rows
# Table columns: | Claim ID | ... | Lean 4 Module & Theorem | ...
# Let's extract table rows that have Lean 4 modules
rows = re.findall(r'\|\s*(\*\*[A-Z0-9-]+\*\*)\s*\|.*', matrix_text)
print(f"Found {len(rows)} claim table rows")

lean_refs = []
# Match table rows:
for line in matrix_text.splitlines():
    if not line.strip().startswith('|'):
        continue
    cols = [c.strip() for c in line.split('|')[1:-1]]
    if len(cols) >= 6:
        claim_id = cols[0]
        # Look for the column that contains .lean or theorem names or N/A
        lean_col = None
        for col in cols:
            if '.lean' in col or 'N/A' in col:
                lean_col = col
                break
        if lean_col and claim_id.startswith('**'):
            lean_refs.append((claim_id, lean_col))

print(f"Found {len(lean_refs)} claim Lean references")

# Now check each reference
valid_refs = 0
na_refs = 0
missing_modules = []
missing_theorems = []

for cid, ref in lean_refs:
    if 'N/A' in ref:
        na_refs += 1
        continue
    # Format typically: `ModuleName.lean` (theorem1, theorem2)
    # or `ModuleName.lean`
    m = re.search(r'`?([A-Za-z0-9_]+)\.lean`?(?:\s*\((.*?)\))?', ref)
    if not m:
        print(f"Could not parse ref: {cid} -> {ref}")
        continue
    mod_name = m.group(1)
    theorems_str = m.group(2)
    lean_file = os.path.join(lean_dir, mod_name + '.lean')
    if not os.path.exists(lean_file):
        missing_modules.append((cid, mod_name, lean_file))
        continue
    
    file_content = open(lean_file, encoding='utf-8', errors='ignore').read()
    if theorems_str:
        # Split theorems by comma
        theorems = [t.strip() for t in theorems_str.split(',') if t.strip()]
        for thm in theorems:
            # Check if theorem / def / lemma / structure / inductive exists
            pattern = rf'\b(theorem|def|lemma|inductive|structure|axiom)\s+{re.escape(thm)}\b'
            if not re.search(pattern, file_content):
                # Also check without \b in case of qualified names or constructors
                if thm not in file_content:
                    missing_theorems.append((cid, mod_name, thm))
    valid_refs += 1

print(f"Audited Lean references: Valid modules={valid_refs}, N/A={na_refs}")
print(f"Missing modules count: {len(missing_modules)}")
for mm in missing_modules:
    print(f"  Missing module: {mm}")
print(f"Missing theorems count: {len(missing_theorems)}")
for mt in missing_theorems:
    print(f"  Missing theorem: {mt}")
