"""Replay the TFQ-0413 countermodels and their tensor proof dependencies.

Uses the pinned prebuilt Mathlib dependencies, but a fresh output directory for
every project module. Compilers run sequentially with one worker to bound memory use. No installation or download is performed. Example:
  python -B dag/research/replay_tensor_countermodels.py --lean <lean.exe> \
    --packages <pinned-project/.lake/packages> --result <replay.json>
"""
from pathlib import Path
import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
MATHLIB_SHA = '56a005855ea17e0b0958f73ec801ae140b0a1679'
LEVELS = [
    ('TensorConeReconstruction', 'TensorTomography', 'TensorSchmidt'),
    ('TensorCoordinates', 'TensorReachability'),
    ('TensorOperationalCone',),
    ('TensorComposition',), ('TensorEffectOrder',), ('TensorEffectCone',),
    ('TensorMeasurements',), ('TensorPartialTranspose',),
    ('TensorCountermodelCones', 'TensorHiddenCoordinates'),
    ('TensorCountermodelWitnesses',), ('TensorCountermodelEmbeddings',),
]
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', required=True, type=Path)
    parser.add_argument('--packages', required=True, type=Path)
    parser.add_argument('--result', required=True, type=Path)
    args = parser.parse_args()
    lean, packages = args.lean.resolve(), args.packages.resolve()
    version = subprocess.check_output([str(lean), '--version'], text=True, encoding='utf-8').strip()
    if not re.search(r'version 4\.35\.0[, )]', version):
        raise ValueError('unexpected Lean version: ' + version)
    sha = subprocess.check_output(['git', '-C', str(packages / 'mathlib'), 'rev-parse', 'HEAD'], text=True).strip()
    if sha != MATHLIB_SHA:
        raise ValueError('unexpected Mathlib source revision: ' + sha)
    output_parent = ROOT / 'lean4/.lake'
    output_parent.mkdir(parents=True, exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix='tensor-countermodel-replay-', dir=output_parent))
    env = dict(os.environ, LEAN_PATH=os.pathsep.join([str(output)] +
               [str(p / '.lake/build/lib/lean') for p in sorted(packages.iterdir()) if p.is_dir()]))
    results = []

    def check(module):
        path = ROOT / 'lean4' / (module + '.lean')
        before = path.read_bytes()
        start = time.monotonic()
        run = subprocess.run([str(lean), '-j', '1', path.name, '-o', str(output / (module + '.olean'))],
                             cwd=ROOT / 'lean4', env=env, text=True, encoding='utf-8',
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        axioms = re.findall(r'depends on axioms: \[([^]]*)\]', run.stdout)
        valid = bool(axioms) and all(set(re.split(r',\s*', a.strip())) <= ALLOWED_AXIOMS for a in axioms)
        code = re.sub(r'/\-.*?\-/|--[^\n]*', '', before.decode('utf-8'), flags=re.S)
        clean = not re.search(r'\b(sorry|admit|axiom|sorryAx|unsafe)\b', code)
        result = {'module': module, 'exit_code': run.returncode,
                  'seconds': round(time.monotonic() - start, 2),
                  'sha256': hashlib.sha256(before).hexdigest(),
                  'source_unchanged_during_build': before == path.read_bytes(),
                  'admission_scan_passed': clean, 'axiom_audit_passed': valid,
                  'output': run.stdout}
        print(f'{module}: exit={run.returncode}, axiom_audit={valid}, admissions_absent={clean}', flush=True)
        return result

    def passed(r):
        return (r['exit_code'] == 0 and r['source_unchanged_during_build'] and
                r['admission_scan_passed'] and r['axiom_audit_passed'])

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        for level in LEVELS:
            checked = list(pool.map(check, level))
            results.extend(checked)
            if not all(map(passed, checked)):
                for r in checked:
                    if not passed(r):
                        print(r['output'], flush=True)
                break
    report = {'lean_version': version, 'mathlib_source_sha': sha,
              'build_directory': str(output), 'results': results}
    args.result.write_bytes((json.dumps(report, indent=2, ensure_ascii=False) + '\n').encode('utf-8'))
    success = len(results) == sum(map(len, LEVELS)) and all(map(passed, results))
    print('Fresh project replay ' + ('PASS' if success else 'FAIL'), flush=True)
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
