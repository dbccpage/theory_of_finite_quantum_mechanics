import os
import re

matrix_text = open('TRACEABILITY_MATRIX.md', encoding='utf-8').read()

# Find all file references ending with .py or .rs
py_files = set(re.findall(r'`?(code/python/[a-zA-Z0-9_/]+\.py)`?', matrix_text))
rs_symbols = set(re.findall(r'`?(tfqm_[a-z0-9_]+::[a-zA-Z0-9_/]+\.rs)`?', matrix_text))

print(f"Total Python files cited: {len(py_files)}")
print(f"Total Rust file symbols cited: {len(rs_symbols)}")

missing_py = []
for f in sorted(py_files):
    if not os.path.exists(f):
        missing_py.append(f)

print(f"Missing Python files: {len(missing_py)}")
for mp in missing_py:
    print(f"  Missing: {mp}")

missing_rs = []
for rs in sorted(rs_symbols):
    # e.g. tfqm_mub::mub6_fourier_landing_verifier.rs -> code/rust/src/mub/mub6_fourier_landing_verifier.rs or search in code/rust/src/
    crate, filename = rs.split('::')
    crate_name = crate.replace('tfqm_', '')
    target_path = os.path.join('code', 'rust', 'src', crate_name, filename)
    if not os.path.exists(target_path):
        # search recursively under code/rust/
        found = False
        for root, dirs, files in os.walk('code/rust'):
            if filename in files:
                found = True
                break
        if not found:
            missing_rs.append((rs, target_path))

print(f"Missing Rust files: {len(missing_rs)}")
for mr in missing_rs:
    print(f"  Missing: {mr}")
