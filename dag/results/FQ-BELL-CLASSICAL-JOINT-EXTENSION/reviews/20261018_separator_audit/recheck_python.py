"""Fresh Python solver execution; compare complete certificates to sealed input."""
from collections import Counter
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'dag/pfp/prepare_stage.py').is_file())
RUN = HERE.parent.parent/'runs/20261018T233710Z_separator_extension'
spec = importlib.util.spec_from_file_location('fresh_bell_separator', ROOT/'code/python/src/qm/bell_separator_extension.py')
bell = importlib.util.module_from_spec(spec); sys.modules[spec.name] = bell; spec.loader.exec_module(bell)
public = json.loads((RUN/'public_cases.json').read_bytes())
candidate = json.loads((RUN/'p3/candidate.json').read_bytes())
if len(public) != len(candidate['cases']):
    raise ValueError('native:case_count')
counts = Counter()
for case, expected in zip(public, candidate['cases']):
    result = bell.construct_extension([[Q(q) for q in row] for row in case['pairs']])
    answer = {'id': case['id'], 'status': 'extended' if result.weights is not None else 'blocked',
              'lower': list(map(str, result.analysis.lower)), 'upper': list(map(str, result.analysis.upper)),
              'facets': list(map(str, result.analysis.facets)), 'separator': None if result.separator is None else str(result.separator),
              'triples': None if result.triples is None else [list(map(str, t)) for t in result.triples],
              'weights': None if result.weights is None else list(map(str, result.weights)), 'violating_mask': result.violating_mask}
    if answer != expected:
        raise ValueError('native:Python_difference:' + case['id'])
    counts[answer['status']] += 1
print(json.dumps({'cases_checked': len(public), 'counts': dict(counts), 'mode': 'fresh native Python; complete certificates compared'}, indent=2))
