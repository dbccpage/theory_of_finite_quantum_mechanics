"""Adversarial controls for custody, release, and exact-admission review findings."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

import pytest

from scripts import build_deposit_zip as deposit
from scripts import check_coverage as coverage
from scripts import check_ideal_prices as prices
from scripts import check_ideal_swaps as swaps
from scripts import check_causal_execution as causal
from scripts import verify_finite_derivations as lean_gate
from scripts import verify_genesis_bridge_sources as genesis
from scripts import verify_observer_source_archive as observer


def _pinned(tmp_path):
    root = tmp_path / 'package'
    root.mkdir()
    source = root / 'source.txt'
    source.write_bytes(b'checked bytes')
    manifest = root / 'SHA256SUMS'
    manifest.write_text(hashlib.sha256(source.read_bytes()).hexdigest() + '  source.txt\n')
    return root, source, manifest


def test_zip_uses_the_bytes_it_checked_even_if_inputs_change(monkeypatch, tmp_path):
    root, source, manifest = _pinned(tmp_path)
    expected_manifest = manifest.read_bytes()
    write = zipfile.ZipFile.writestr

    def change_inputs(archive, info, data, **kwargs):
        source.write_bytes(b'changed after hash')
        manifest.write_bytes(b'changed manifest')
        return write(archive, info, data, **kwargs)

    monkeypatch.setattr(zipfile.ZipFile, 'writestr', change_inputs)
    out = tmp_path / 'deposit.zip'
    assert deposit.build_archive(root, manifest, out) == 2
    with zipfile.ZipFile(out) as archive:
        assert archive.read('package/source.txt') == b'checked bytes'
        assert archive.read('package/SHA256SUMS') == expected_manifest


def test_zip_refuses_output_aliases_and_linked_source_ancestors(tmp_path):
    root, source, manifest = _pinned(tmp_path)
    original = source.read_bytes()
    for out in (source, manifest):
        with pytest.raises(ValueError, match='aliases'):
            deposit.build_archive(root, manifest, out)
    alias = tmp_path / 'alias.zip'
    alias.hardlink_to(source)
    with pytest.raises(ValueError, match='aliases'):
        deposit.build_archive(root, manifest, alias)
    assert source.read_bytes() == original
    link = tmp_path / 'linked'
    link.symlink_to(root, target_is_directory=True)
    with pytest.raises(ValueError, match='linked'):
        deposit.build_archive(link, link / 'SHA256SUMS', tmp_path / 'out.zip')


def _report():
    summary = {'covered_lines': 2, 'num_statements': 2,
               'covered_branches': 1, 'num_branches': 1}
    return {'totals': dict(summary), 'files': {'module.py': {'summary': summary}}}


@pytest.mark.parametrize('bad', [float('nan'), float('inf'), True, -1, 1.5, 3])
def test_coverage_refuses_noninteger_nonfinite_or_impossible_counts(bad):
    payload = _report()
    payload['totals']['covered_lines'] = bad
    payload['files']['module.py']['summary']['covered_lines'] = bad
    with pytest.raises(ValueError):
        coverage.strict_report(json.dumps(payload))


def test_coverage_reconciles_totals_and_refuses_duplicate_keys():
    payload = _report()
    assert coverage.strict_report(json.dumps(payload)) == payload
    payload['totals']['num_statements'] = 3
    with pytest.raises(ValueError, match='sum of file'):
        coverage.strict_report(json.dumps(payload))
    with pytest.raises(ValueError, match='duplicate'):
        coverage.strict_report('{"files":{},"files":{}}')


@pytest.mark.parametrize('threshold', ['nan', 'inf', '-1', '101'])
def test_coverage_refuses_invalid_thresholds(monkeypatch, tmp_path, threshold):
    report = tmp_path / 'coverage.json'
    report.write_text(json.dumps(_report()))
    monkeypatch.setattr('sys.argv', ['check_coverage', str(report), '--line-min', threshold])
    with pytest.raises(SystemExit) as error:
        coverage.main()
    assert error.value.code == 2


def test_exact_schedule_and_price_identifiers_reject_boolean_aliases():
    assert swaps.minimum_swap_receipt((0,), 0, 1, (0,), (0,)).inversion_count == 0
    with pytest.raises(ValueError, match='integer event'):
        swaps.minimum_swap_receipt((0,), 0, 1, (False,), (0,))
    assert isinstance(prices.analyze_prices((0,), {(0, 0): (1,)}), prices.ExactPrices)
    with pytest.raises(ValueError, match='pairs of integers'):
        prices.analyze_prices((0,), {(False, False): (1,)})
    for checker in (prices, swaps):
        for text in ('{"x":0,"x":1}', '{"x":NaN}', '{"x":1.0}'):
            with pytest.raises(ValueError):
                checker.strict_json(text)


@pytest.mark.parametrize('reader', [observer.regular, genesis.regular, causal.sha])
def test_custody_rejects_a_linked_ancestor(tmp_path, reader):
    real = tmp_path / 'real'
    real.mkdir()
    (real / 'source').write_bytes(b'content')
    link = tmp_path / 'link'
    link.symlink_to(real, target_is_directory=True)
    reader(real / 'source')
    with pytest.raises(ValueError):
        reader(link / 'source')


def test_unprinted_lean_admission_is_detected_from_a_real_compiler_diagnostic(tmp_path):
    lean = shutil.which('lean')
    if lean is None:
        pytest.skip('Lean compiler unavailable for negative control')
    source = tmp_path / 'Admission.lean'
    source.write_text('theorem unprinted_admission : False := by sorry\n'
                      'theorem printed_truth : True := True.intro\n'
                      '#print axioms printed_truth\n')
    run = subprocess.run([lean, str(source)], text=True, capture_output=True, check=False)
    assert run.returncode == 0
    output = run.stdout + run.stderr
    assert 'sorryAx' not in output  # The selected declaration alone is clean.
    assert lean_gate.contains_admission(output)


def test_deposit_sweep_includes_archive_component_named_b(tmp_path):
    import verify_deposit
    historical = tmp_path / 'docs/source_archive/components/b/unlisted.py'
    historical.parent.mkdir(parents=True)
    historical.write_text('historical source\n')
    generated = tmp_path / 'code/coda_application/build/lib/generated.py'
    generated.parent.mkdir(parents=True)
    generated.write_text('generated source\n')
    errors = verify_deposit.sweep_unlisted({}, tmp_path)
    assert len(errors) == 1 and 'components/b/unlisted.py' in errors[0]
    link = tmp_path / 'redirected'
    link.symlink_to(historical.parent, target_is_directory=True)
    with pytest.raises(ValueError):
        verify_deposit.sha256_of(link / 'unlisted.py')
    assert any('non-regular' in error for error in verify_deposit.sweep_unlisted({}, tmp_path))
