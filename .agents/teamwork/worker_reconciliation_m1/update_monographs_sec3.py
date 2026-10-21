import json
from pathlib import Path
import re

with open('dag/pfp/filename_custody.json', encoding='utf-8') as f:
    custody = json.load(f)

custody_paper_paths = {a['path'] for a in custody['artifacts'] if a.get('kind') == 'paper'}
print(f"Custody monographs (protected, will NOT touch): {len(custody_paper_paths)}")

with open('dag/theory_of_finite_qm.jsonl', encoding='utf-8') as f:
    jsonl_nodes = {row['id']: row for row in (json.loads(line) for line in f)}

non_custody = [Path(p) for p in sorted(Path('dag/derivations').glob('*/*.md')) if p.as_posix() not in custody_paper_paths]
print(f"Non-custody monographs to update: {len(non_custody)}")

def format_sec3(row):
    lines = ['## 3. Multi-Tier Code & Proof Witnesses', '']
    # Lean 4
    if row.get('lean4'):
        lines.append('### Lean 4 Theorems')
        for item in row['lean4']:
            lines.append(f"- [`{item}`](../../lean4/)")
        lines.append('')
    else:
        lines.append('### Lean 4 Formalization')
        lines.append('*Formalization active. Proof obligations tracked under zero-sorry regime.*')
        lines.append('')
    # Rust
    if row.get('rust'):
        lines.append('### Sovereign Rust Certifiers (Exact Rational Arithmetic)')
        for item in row['rust']:
            lines.append(f"- [`{item}`](../../code/rust/src/)")
        lines.append('')
    else:
        lines.append('### Sovereign Rust Certifiers')
        lines.append('*Computational witness tracked under `theory_of_finite_qm` crate.*')
        lines.append('')
    # Python
    if row.get('python'):
        lines.append('### Python Oracles & Numerical Evaluators')
        for item in row['python']:
            lines.append(f"- [`{item}`](../../code/python/)")
        lines.append('')
    lines.append('---')
    return '\n'.join(lines)

updated_count = 0
for p in non_custody:
    txt = p.read_text(encoding='utf-8')
    m_id = re.search(r'# \[(TFQ-\d{4})\]', txt)
    if not m_id:
        print(f"Error: No ID in {p}")
        continue
    nid = m_id.group(1)
    row = jsonl_nodes[nid]
    new_sec3 = format_sec3(row)
    
    # Replace Section 3: from ## 3. Multi-Tier Code & Proof Witnesses to ## 4. Downstream Derivations
    pattern = re.compile(r'## 3\. Multi-Tier Code & Proof Witnesses.*?\n---\s*\n\s*## 4\. Downstream Derivations', re.DOTALL)
    replacement = new_sec3 + '\n\n## 4. Downstream Derivations'
    
    new_txt, count = pattern.subn(replacement, txt)
    if count == 0:
        # Try without the trailing --- if any
        pattern2 = re.compile(r'## 3\. Multi-Tier Code & Proof Witnesses.*?\n## 4\. Downstream Derivations', re.DOTALL)
        new_txt, count2 = pattern2.subn(replacement, txt)
        if count2 == 0:
            print(f"Failed to match Section 3 in {p}")
            continue
    
    # Check claim hygiene before saving
    for forbidden in ['proves', 'guarantees', 'mathematically verifies', 'fundamentally', 'true intelligence', 'impossible', 'universal', 'flawless', 'perfectly', 'clearly', 'obviously', 'simply', 'merely', 'weaponized']:
        if re.search(r'\b' + re.escape(forbidden) + r'\b', new_txt, re.IGNORECASE):
            print(f"Error: Forbidden word {forbidden} found in {p} after update!")
            raise ValueError(f"Forbidden word in {p}")
            
    p.write_text(new_txt, encoding='utf-8')
    updated_count += 1

print(f"Successfully updated Section 3 in {updated_count} / {len(non_custody)} non-custody monographs.")
