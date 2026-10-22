"""Re-pin the current-state fields of the tensor receipts after a change to the DAG, its views or lean4/lakefile.lean.

    python -I -X utf8 dag/research/repin_tensor_receipts.py --run "branch <name>" --reason "<what changed and why>"

Run it from the repository root, LAST, after every sync and generator. It keeps the lean_replay blocks and the rebound
history, and records every change under `rebound` with the given run label and reason:
  - dag/research/tensor_countermodel_validation.json: node/route/record counts and the sha256 of every pinned file;
  - dag/research/tensor_measurement_validation.json: the counts only.
`--check` exits 1 if anything would change (nothing is written).
"""
import argparse, hashlib, json, sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--run', required=False, default='unspecified', help='label of the branch or run doing the re-pin')
    ap.add_argument('--reason', required=False, default='', help='what changed in the pinned files, and why')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    dag = json.loads(Path('dag/derivation_dag.json').read_text(encoding='utf-8'))
    records = Path('dag/theory_of_finite_qm.jsonl').read_text(encoding='utf-8').splitlines()
    counts = {'dag_nodes': len(dag['nodes']), 'dag_routes': len(dag['routes']), 'master_records': len(records)}
    if not args.check and not args.reason.strip():
        sys.exit('--reason is required when writing: say what changed in the pinned files')
    stale = []
    for name, rehash in (('tensor_countermodel_validation.json', True), ('tensor_measurement_validation.json', False)):
        p = Path('dag/research') / name
        raw = p.read_text(encoding='utf-8')
        r = json.loads(raw)
        if r['counts'] != counts:
            stale.append('%s counts %s -> %s' % (name, r['counts'], counts))
            r['rebound'].append({'field': 'counts', 'previous': r['counts'], 'current': counts,
                                 'reason': args.reason, 'run': args.run})
            r['counts'] = counts
        if rehash:
            for k, old in list(r['sha256'].items()):
                new = hashlib.sha256(Path(k).read_bytes()).hexdigest()
                if new != old:
                    stale.append('%s sha %s' % (name, k))
                    r['rebound'].append({'field': 'sha256', 'path': k, 'previous': old, 'current': new,
                                         'reason': 'current-file digest rebound: ' + args.reason, 'run': args.run})
                    r['sha256'][k] = new
        if not args.check:
            indent = 2 if raw.startswith('{\n  "') else None
            p.write_text(json.dumps(r, ensure_ascii=False, indent=indent) + ('\n' if raw.endswith('\n') else ''),
                         encoding='utf-8', newline='\n')
    for line in stale:
        print(('stale: ' if args.check else 'rebound: ') + line)
    print('receipts current' if not stale else ('%d stale pin(s)' % len(stale)))
    return 1 if (args.check and stale) else 0


if __name__ == '__main__':
    sys.exit(main())
