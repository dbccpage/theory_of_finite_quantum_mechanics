"""Regression tests for plan-byte custody; all repository writes use private fixtures."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import pytest

IMPORTER = Path(__file__).with_name('import_sources.py')


def fixture(tmp_path):
    root = tmp_path / 'repo'
    (root / 'dag/fragments').mkdir(parents=True)
    (root / 'dag/derivation_dag.json').write_text('{"nodes": []}', encoding='utf-8')
    source = tmp_path / 'source.lean'
    source.write_bytes(b'example : True := True.intro\n')
    data = source.read_bytes()
    row = dict(status='verified', atlas_path='atlas/family/source.lean', family='family', rel='source.lean',
               ana_path=str(source), git_sha256=hashlib.sha256(data).hexdigest(), size=len(data))
    return root, source, row


def run(root, rows, optimized, write=True):
    plan = root.parent / 'plan.json'
    plan.write_text(json.dumps(rows), encoding='utf-8')
    return subprocess.run([sys.executable, '-I', *(['-O'] if optimized else []), str(IMPORTER), str(root), str(plan),
                           *(['--write'] if write else [])], capture_output=True, text=True)


@pytest.mark.parametrize('optimized', [False, True])
def test_exact_copy_and_provenance(tmp_path, optimized):
    root, source, row = fixture(tmp_path)
    result = run(root, [row], optimized)
    assert result.returncode == 0, result.stderr
    assert (root / 'sources/atlas/F004_papers/family/source.lean').read_bytes() == source.read_bytes()
    entry = json.loads((root / 'sources/atlas/PROVENANCE.json').read_text())['files'][0]
    assert entry['sha256'] == entry['in_repo_sha256'] == row['git_sha256']


@pytest.mark.parametrize('optimized', [False, True])
@pytest.mark.parametrize('fault', ['changed_source', 'wrong_size', 'wrong_digest', 'escape', 'bad_status', 'duplicate', 'stale_twin', 'bad_match', 'empty', 'bool_size'])
def test_invalid_plan_refuses_before_writing(tmp_path, optimized, fault):
    root, source, row = fixture(tmp_path)
    bad = dict(row, atlas_path='atlas/second.lean', rel='second.lean')
    rows = [row, bad]
    if fault == 'changed_source':
        source.write_bytes(b'changed')
    elif fault == 'wrong_size':
        bad['size'] += 1
    elif fault == 'wrong_digest':
        bad['git_sha256'] = '0' * 64
    elif fault == 'escape':
        bad['rel'] = '../../escaped.lean'
    elif fault == 'bad_status':
        bad['status'] = 'missing_in_ana'
    elif fault == 'duplicate':
        bad['atlas_path'] = row['atlas_path']
    elif fault == 'bool_size':
        bad['size'] = True
    elif fault == 'empty':
        rows = []
    else:
        (root / 'existing.lean').write_bytes(b'different')
        bad['resolved_to_existing'] = {'path': 'existing.lean', 'match': 'identical' if fault == 'stale_twin' else 'unknown'}
    result = run(root, rows, optimized)
    assert result.returncode != 0
    assert 'refusing:' in result.stderr
    assert not (root / 'sources').exists()
    assert (root / 'dag/derivation_dag.json').read_text() == '{"nodes": []}'


@pytest.mark.parametrize('optimized', [False, True])
def test_newline_equivalent_twin_has_its_own_digest(tmp_path, optimized):
    root, source, row = fixture(tmp_path)
    twin = source.read_bytes().replace(b'\n', b'\r\n')
    (root / 'existing.lean').write_bytes(twin)
    row['resolved_to_existing'] = {'path': 'existing.lean', 'match': 'newline_equivalent'}
    result = run(root, [row], optimized)
    assert result.returncode == 0, result.stderr
    entry = json.loads((root / 'sources/atlas/PROVENANCE.json').read_text())['files'][0]
    assert entry['sha256'] == row['git_sha256']
    assert entry['in_repo_sha256'] == hashlib.sha256(twin).hexdigest() != entry['sha256']


@pytest.mark.parametrize('optimized', [False, True])
def test_dry_run_has_no_writes(tmp_path, optimized):
    root, _, row = fixture(tmp_path)
    before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()}
    assert run(root, [row], optimized, write=False).returncode == 0
    assert before == {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()}
