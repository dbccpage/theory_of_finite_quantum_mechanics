import json
from pathlib import Path

with open('dag/pfp/filename_custody.json', encoding='utf-8') as f:
    custody = json.load(f)

custody_paper_paths = {a['path'] for a in custody['artifacts'] if a.get('kind') == 'paper'}

with open('dag/theory_of_finite_qm.jsonl', encoding='utf-8') as f:
    jsonl_nodes = {row['id']: row for row in (json.loads(line) for line in f)}

non_custody = [Path(p) for p in sorted(Path('dag/derivations').glob('*/*.md')) if p.as_posix() not in custody_paper_paths]

diff_count = 0
for p in non_custody:
    txt = p.read_text(encoding='utf-8')
    # extract node id
    for nid, row in jsonl_nodes.items():
        if f"# [{nid}]" in txt:
            # check if legacy paths are present in txt
            has_legacy = ('omega_engine/crates_rs' in txt or 'lean4/quantum_mechanics' in txt)
            if has_legacy:
                diff_count += 1
            break

print(f"Non-custody monographs with legacy witness paths: {diff_count} / {len(non_custody)}")
