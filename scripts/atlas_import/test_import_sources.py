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
    assert (root / 'sources/atlas/papers/family/source.lean').read_bytes() == source.read_bytes()
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


@pytest.fixture
def importer():
    import importlib.util
    spec = importlib.util.spec_from_file_location('atlas_importer_tested', IMPORTER)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def tree_bytes(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}


@pytest.mark.parametrize('optimized', [False, True])
def test_late_invalid_fragment_has_no_effect(tmp_path, optimized):
    root, _, row = fixture(tmp_path)
    (root / 'dag/fragments/z.json').write_bytes(b'{malformed')
    before = tree_bytes(root)
    result = run(root, [row], optimized)
    assert result.returncode != 0
    assert tree_bytes(root) == before
    assert not (root / 'sources').exists()


@pytest.mark.parametrize('fail_at', [0, 1, 2, 3])
def test_each_publish_failure_restores_original_tree(tmp_path, importer, monkeypatch, fail_at):
    root, _, row = fixture(tmp_path)
    dag = root / 'dag/derivation_dag.json'
    dag.write_text(json.dumps({'source': row['atlas_path'], 'statement': row['atlas_path']}))
    (root / 'dag/fragments/a.json').write_bytes(dag.read_bytes())
    before = tree_bytes(root)
    plan = importer.prepare(root, [row])
    replace = importer.os.replace
    count = 0

    def fail_one(source, target):
        nonlocal count
        if str(source).endswith('.new'):
            current = count
            count += 1
            if current == fail_at:
                raise OSError('injected publish failure')
        return replace(source, target)

    monkeypatch.setattr(importer.os, 'replace', fail_one)
    with pytest.raises(importer.ImportFailure) as caught:
        importer.apply(plan)
    assert caught.value.code == importer.FailureCode.IO
    assert tree_bytes(root) == before
    assert not (root / 'sources').exists()
    assert not (root / '.atlas-import.lock').exists()
    assert not list(root.glob('.atlas-import-stage-*'))


def test_stale_prepared_input_refuses(tmp_path, importer):
    root, _, row = fixture(tmp_path)
    plan = importer.prepare(root, [row])
    (root / 'dag/derivation_dag.json').write_bytes(b'{"changed": true}')
    before = tree_bytes(root)
    with pytest.raises(importer.ImportFailure) as caught:
        importer.apply(plan)
    assert caught.value.code == importer.FailureCode.STALE_INPUT
    assert tree_bytes(root) == before
    assert not (root / '.atlas-import.lock').exists()


def test_writer_lease_refuses_without_deleting_other_lease(tmp_path, importer):
    root, _, row = fixture(tmp_path)
    plan = importer.prepare(root, [row])
    lock = root / '.atlas-import.lock'
    lock.mkdir()
    (lock / 'owner').write_bytes(b'other writer')
    before = tree_bytes(root)
    with pytest.raises(importer.ImportFailure) as caught:
        importer.apply(plan)
    assert caught.value.code == importer.FailureCode.BUSY
    assert tree_bytes(root) == before


def test_existing_destination_cannot_be_overwritten(tmp_path, importer):
    root, _, row = fixture(tmp_path)
    dest = root / importer.DEST / 'family/source.lean'
    dest.parent.mkdir(parents=True)
    dest.write_bytes(b'valuable different bytes')
    with pytest.raises(importer.ImportFailure) as caught:
        importer.prepare(root, [row])
    assert caught.value.code == importer.FailureCode.STALE_INPUT
    assert dest.read_bytes() == b'valuable different bytes'


def test_repeat_apply_is_idempotent_and_only_paths_change(tmp_path, importer):
    root, _, row = fixture(tmp_path)
    original = row['atlas_path']
    dag = root / 'dag/derivation_dag.json'
    dag.write_text(json.dumps({'source': original, 'statement': original, 'f004_refs': [original],
        'nested': {'root': 'symbol_game', 'path': original}, 'python': 'absent: ' + original}))
    importer.apply(importer.prepare(root, [row]))
    after = tree_bytes(root)
    importer.apply(importer.prepare(root, [row]))
    assert tree_bytes(root) == after
    result = json.loads(dag.read_bytes())
    assert result['source'] == importer.DEST + '/family/source.lean'
    assert result['statement'] == original
    assert result['f004_refs'] == [original]
    assert result['python'] == 'absent: ' + original
    assert result['nested'] == {'root': 'local', 'path': result['source']}


def test_multiple_sources_can_share_an_existing_twin(tmp_path, importer):
    root, source, row = fixture(tmp_path)
    (root / 'twin.lean').write_bytes(source.read_bytes())
    row['resolved_to_existing'] = {'path': 'twin.lean', 'match': 'identical'}
    other = dict(row, atlas_path='atlas/other.lean')
    plan = importer.prepare(root, [row, other])
    assert plan.resolved == 2
    importer.apply(plan)
    assert (root / 'twin.lean').read_bytes() == source.read_bytes()


@pytest.mark.parametrize('limit', ['file', 'total', 'rows'])
def test_resource_limits_refuse_before_writes(tmp_path, importer, monkeypatch, limit):
    root, _, row = fixture(tmp_path)
    before = tree_bytes(root)
    monkeypatch.setattr(importer, {'file': 'MAX_FILE', 'total': 'MAX_TOTAL', 'rows': 'MAX_ROWS'}[limit], 1)
    with pytest.raises(importer.ImportFailure):
        importer.prepare(root, [row, dict(row, atlas_path='atlas/other.lean', rel='other.lean')])
    assert tree_bytes(root) == before


def test_rollback_failure_retains_originals_and_blocks_reuse(tmp_path, importer, monkeypatch):
    root, _, row = fixture(tmp_path)
    dag = root / 'dag/derivation_dag.json'
    dag.write_text(json.dumps({'source': row['atlas_path']}))
    original = dag.read_bytes()
    (root / 'dag/fragments/z.json').write_bytes(original)
    plan = importer.prepare(root, [row])
    replace = importer.os.replace

    def fail_publish_and_rollback(source, target):
        if Path(source).name == '3.new' or str(source).endswith('.old'):
            raise OSError('injected recovery failure')
        return replace(source, target)

    monkeypatch.setattr(importer.os, 'replace', fail_publish_and_rollback)
    with pytest.raises(importer.ImportFailure) as caught:
        importer.apply(plan)
    assert caught.value.code == importer.FailureCode.RECOVERY
    stages = list(root.glob('.atlas-import-stage-*'))
    assert len(stages) == 1
    assert (stages[0] / '2.old').read_bytes() == original
    assert (stages[0] / 'journal.json').exists()
    assert (root / '.atlas-import.lock').is_dir()
    with pytest.raises(importer.ImportFailure) as blocked:
        importer.apply(plan)
    assert blocked.value.code == importer.FailureCode.BUSY


def test_stage_failure_has_no_output_changes(tmp_path, importer, monkeypatch):
    root, _, row = fixture(tmp_path)
    plan = importer.prepare(root, [row])
    before = tree_bytes(root)

    def fail_stage(*args):
        raise OSError('injected staging failure')

    monkeypatch.setattr(importer, 'stage_files', fail_stage)
    with pytest.raises(importer.ImportFailure) as caught:
        importer.apply(plan)
    assert caught.value.code == importer.FailureCode.IO
    assert tree_bytes(root) == before
    assert not (root / '.atlas-import.lock').exists()


@pytest.fixture
def planner():
    import importlib.util
    path = IMPORTER.with_name('plan_sources.py')
    spec = importlib.util.spec_from_file_location('atlas_planner_tested', path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def git_fixture(repository, *arguments):
    result = subprocess.run(['git', '-C', str(repository), '-c', 'user.name=Fixture',
        '-c', 'user.email=fixture@example.invalid', *arguments], capture_output=True, check=True)
    return result.stdout.decode().strip()


def planner_fixture(tmp_path, planner):
    root = tmp_path / 'repo'
    sibling = tmp_path / 'sibling'
    restored = tmp_path / 'restored'
    for directory in (root, sibling, restored):
        directory.mkdir()
    for repository in (root, sibling):
        git_fixture(repository, 'init', '--quiet')
    family = 'fermion_sign_problem'
    original = planner.PREFIX + family + '/code/sample.py'
    historical = sibling / original
    historical.parent.mkdir(parents=True)
    historical.write_bytes(b'print("archive")\n')
    git_fixture(sibling, 'add', '.')
    git_fixture(sibling, 'commit', '--quiet', '-m', 'source')
    parent = git_fixture(sibling, 'rev-parse', 'HEAD')
    historical.unlink()
    git_fixture(sibling, 'add', '-u')
    git_fixture(sibling, 'commit', '--quiet', '-m', 'removal')
    commit = git_fixture(sibling, 'rev-parse', 'HEAD')
    copy = restored / family / 'code/sample.py'
    copy.parent.mkdir(parents=True)
    copy.write_bytes(b'print("archive")\n')
    inventory = {'paths': [{'path': original, 'removed_in_commit': True,
        'referenced_from': {'dag fragments (sync inputs)': ['node']}}]}
    config = planner.Configuration(root, restored, sibling, commit)
    return config, inventory, copy, parent


@pytest.mark.parametrize('twin', ['none', 'identical', 'newline_equivalent'])
@pytest.mark.parametrize('restored_state', ['valid', 'missing', 'different', 'newlines'])
def test_planner_exact_git_custody_and_outcomes(tmp_path, planner, twin, restored_state):
    config, inventory, copy, parent = planner_fixture(tmp_path, planner)
    expected = copy.read_bytes()
    if twin != 'none':
        target = config.repository / 'sample.py'
        target.write_bytes(expected if twin == 'identical' else expected.replace(b'\n', b'\r\n'))
        git_fixture(config.repository, 'add', '.')
    if restored_state == 'missing':
        copy.unlink()
    elif restored_state == 'different':
        copy.write_bytes(b'different')
    elif restored_state == 'newlines':
        copy.write_bytes(expected.replace(b'\n', b'\r\n'))
    rows = planner.build_plan(config, inventory)
    assert len(rows) == 1
    row = rows[0]
    assert row['git_sha256'] == hashlib.sha256(expected).hexdigest()
    assert row['resolved_git_commit'] == parent
    assert row['status'] == {'valid': 'verified', 'missing': 'missing_in_ana',
        'different': 'ana_differs', 'newlines': 'ana_newline_only_diff'}[restored_state]
    if restored_state == 'valid' and twin != 'none':
        assert row['resolved_to_existing'] == {'path': 'sample.py', 'match': twin}
    else:
        assert 'resolved_to_existing' not in row
    assert not list(config.repository.glob('.atlas-*'))


@pytest.mark.parametrize('fault', ['escape', 'duplicate', 'empty', 'bad_refs', 'missing_git', 'missing_tracked'])
def test_planner_invalid_inputs_refuse(tmp_path, planner, fault):
    config, inventory, copy, _ = planner_fixture(tmp_path, planner)
    if fault == 'escape':
        inventory['paths'][0]['path'] = planner.PREFIX + 'fermion_sign_problem/../../outside'
    elif fault == 'duplicate':
        inventory['paths'] *= 2
    elif fault == 'empty':
        inventory['paths'] = []
    elif fault == 'bad_refs':
        inventory['paths'][0]['referenced_from'] = []
    elif fault == 'missing_git':
        config = planner.Configuration(config.repository, config.restored, config.sibling, 'abcdef123456')
    else:
        absent = config.repository / 'missing.py'
        absent.write_bytes(b'needed')
        git_fixture(config.repository, 'add', '.')
        absent.unlink()
    with pytest.raises(planner.ImportFailure):
        planner.build_plan(config, inventory)
    assert copy.read_bytes() == b'print("archive")\n'


def test_planner_git_timeout_is_typed(tmp_path, planner, monkeypatch):
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired('git', 120)
    monkeypatch.setattr(planner.subprocess, 'run', timeout)
    with pytest.raises(planner.ImportFailure) as caught:
        planner.git(tmp_path, ['status'])
    assert caught.value.code.value == 'resource_limit'


def test_planner_atomic_output_preserves_existing_on_failure(tmp_path, planner, monkeypatch):
    destination = tmp_path / 'plan.json'
    destination.write_bytes(b'original plan')
    def fail_replace(*args):
        raise OSError('injected plan replacement failure')
    monkeypatch.setattr(planner.os, 'replace', fail_replace)
    with pytest.raises(OSError):
        planner.write_plan(destination, [{'status': 'verified'}])
    assert destination.read_bytes() == b'original plan'
    assert sorted(p.name for p in tmp_path.iterdir()) == ['plan.json']


def test_added_fragment_invalidates_prepared_snapshot(tmp_path, importer):
    root, _, row = fixture(tmp_path)
    plan = importer.prepare(root, [row])
    (root / 'dag/fragments/new.json').write_bytes(b'{}')
    before = tree_bytes(root)
    with pytest.raises(importer.ImportFailure) as caught:
        importer.apply(plan)
    assert caught.value.code == importer.FailureCode.STALE_INPUT
    assert tree_bytes(root) == before


@pytest.mark.parametrize('relative', ['../escape', 'C:/outside', '/outside', 'file:stream', '.'])
def test_import_path_boundary(tmp_path, importer, relative):
    with pytest.raises(importer.ImportFailure) as caught:
        importer.inside(tmp_path.resolve(), relative)
    assert caught.value.code == importer.FailureCode.INVALID_PATH
