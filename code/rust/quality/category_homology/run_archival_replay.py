"""Verify one inactive module with full Rust items and actual native compilation.

The temporary AST program uses pinned offline syn dependencies. It does not edit
the calibrated complexity tool. Its binary is removed after the native campaign;
small source/dependency snapshots remain. AuthorityEffect: None.
"""
from datetime import datetime, timezone
import json
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
import shutil
import sys

from archival_inventory import BOUNDARY
from run_audit import (ROOT, RUST, bind_dependencies, clear_debug_outputs,
                       dependency_inventory, digest, execute, execute_build,
                       inventory, write_json)


def main():
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    output = ROOT/'evidence/quality/category_homology'/(stamp+'-archival-ast')
    output.mkdir(parents=True)
    captures = output/'inventories'
    captures.mkdir()
    work = RUST/'target/archival'/stamp
    work.mkdir(parents=True)
    if work.resolve().parent != (RUST/'target/archival').resolve():
        raise RuntimeError('Invalid owned AST work directory')
    (work/'src').mkdir()
    quality = Path(__file__).resolve().parent
    original = quality/'rust_metrics'
    for name in ['Cargo.toml','Cargo.lock']:
        text = (original/name).read_text(encoding='utf-8')
        if text.count('name = "tfqm_rust_metrics"') != 1:
            raise RuntimeError('Review offline package identity adapter')
        (work/name).write_text(text.replace('name = "tfqm_rust_metrics"',
            'name = "tfqm_archival_inventory"'),encoding='utf-8',newline='\n')
    _copy_record_file(quality/'archival_inventory.rs',work/'src/main.rs')
    for source in [Path(__file__),quality/'archival_inventory.py',quality/'archival_inventory.rs']:
        _copy_record_file(source,output/source.name)
    write_json(output/'tool_source_manifest.json',{
        str(path):digest(path) for path in [work/'Cargo.toml',work/'Cargo.lock',work/'src/main.rs']})
    inputs = inventory()
    write_json(output/'source_manifest.json',inputs)
    roots, dependencies = bind_dependencies(work,output)
    build, binary = work/'target', work/'archival_inventory.exe'
    built, replay, native, before_binary, after_binary, rows = None, None, None, None, None, []
    try:
        try:
            built = execute_build(['cargo','build','--offline','--locked','--jobs','1',
                '--manifest-path',str(work/'Cargo.toml'),'--target-dir',str(build)],work,output/'build.log')
            if built['exit_code'] == 0:
                _copy_record_file(build/'debug/tfqm_archival_inventory.exe',binary)
        finally:
            clear_debug_outputs(build,work)
        if built['exit_code'] != 0:
            raise RuntimeError('Archival AST tool build failed; retained build log')
        before_binary = digest(binary)
        key = 'code/rust/src/category_theory/grothendieck_construction.rs'
        source = (ROOT/key).read_text(encoding='utf-8')
        if BOUNDARY in source:
            raise RuntimeError('Archival boundary collides with recorded source')
        anchor = source[-140:]
        if source.count(anchor) != 1:
            raise RuntimeError('Review archival tail anchor')
        activations = [
            'pub fn activated_archival() {}',
            'pub const ACTIVATED: usize = 1;',
            'pub struct Activated;',
            'pub enum Activated { Value }',
            'pub trait Activated {}',
            'pub mod activated { pub fn value() {} }',
            'pub type Activated = usize;',
            'pub use std::collections::BTreeMap as Activated;',
            'macro_rules! activated { () => { pub struct Activated; } } activated!();',
        ]
        policy = quality/'archival_boundaries.json'
        write_json(policy,{'AuthorityEffect':'None','records':[{'family':'','path':key,
            'sha256':digest(ROOT/key),'ast_binary':binary.as_posix(),
            'ast_binary_sha256':before_binary,'ast_inventory_dir':captures.as_posix(),
            'faults':[[anchor,anchor+'\n'+item+'\n'] for item in activations]}]})
        _copy_record_file(policy,output/policy.name)
        replay = execute([sys.executable,str(quality/'run_root_records.py'),'--policy',str(policy)],
            ROOT,output/'native-driver.log',timeout=1800)
        if replay['exit_code'] != 0:
            raise RuntimeError('Archival native controls failed; retained native-driver log')
        receipts = [line.split('Receipt:',1)[1].strip() for line in (output/'native-driver.log').read_text(encoding='utf-8').splitlines() if line.startswith('Receipt:')]
        if len(receipts) != 1:
            raise RuntimeError('Cannot identify the one archival native receipt')
        native = Path(receipts[0])
        summary = json.loads((native/'summary.json').read_text(encoding='utf-8'))
        if summary['generated'] != 9 or summary['mutation_accounting'] != dict(killed=9,survived=0,demonstrably_equivalent=0,invalid=0,inconclusive=0,unrun=0):
            raise RuntimeError('Archival fault campaign has unresolved outcomes')
        controls = json.loads((native/'controls.json').read_text(encoding='utf-8'))
        faults = json.loads((native/'mutations.json').read_text(encoding='utf-8'))
        for index,row in enumerate(controls+faults):
            candidate = ROOT/row['candidate_path']
            record_path = captures/(candidate.stem+'.json')
            record = json.loads(record_path.read_text(encoding='utf-8'))
            raw = candidate.read_bytes().split(BOUNDARY.encode(),1)[0]
            if not record['valid_syntax'] or record['prefix_utf8_bytes'] != len(raw):
                raise RuntimeError('AST parse/byte-view validity failed')
            if record['non_doc_inner_attributes'] != 0:
                raise RuntimeError('Unknown active inner attribute in archive view')
            expected = source if index == 0 else source.replace(anchor,anchor+'\n'+activations[index-1]+'\n',1)
            if raw.decode('utf-8').replace('\r\n','\n').rstrip('\n') != expected.rstrip('\n'):
                raise RuntimeError('Parsed prefix is not the canonical/one-fault source')
            if (record['top_level_item_count']==0) != (index==0):
                raise RuntimeError('AST activation sensitivity mismatch')
            rows.append({'id':row['id'],'source_candidate':row['candidate_path'],
                'candidate_sha256':digest(candidate),'parsed_prefix_sha256':__import__('hashlib').sha256(raw).hexdigest(),
                'canonical_or_one_fault_prefix_verified':True,'inventory':record_path.relative_to(ROOT).as_posix(),
                'inventory_sha256':digest(record_path),'observed':record})
        after_binary = digest(binary)
        if before_binary != after_binary:
            raise RuntimeError('AST verifier executable drifted during native campaign')
        write_json(output/'full_item_inventory.json',rows)
    finally:
        binary.unlink(missing_ok=True)
        if build.exists():
            clear_debug_outputs(build,work)
            if build.resolve().parent != work.resolve():
                raise RuntimeError('Unsafe AST build cleanup')
            shutil.rmtree(build)
        stable_dependencies = dependencies == dependency_inventory(roots)
        receipt = {'AuthorityEffect':'None','build':built,'native_driver':replay,
            'native_receipt':None if native is None else native.relative_to(ROOT).as_posix(),
            'source_manifest_sha256':digest(output/'source_manifest.json'),
            'source_unchanged':inputs==inventory(),'dependencies_unchanged':stable_dependencies,
            'dependency_receipt_sha256':digest(output/'dependency_receipt.json'),
            'tool_binary_sha256_before':before_binary,'tool_binary_sha256_after':after_binary,
            'tool_sources_sha256':digest(output/'tool_source_manifest.json'),
            'canonical_and_mutant_inventories_complete':len(rows)==10,
            'full_item_inventory_sha256':digest(output/'full_item_inventory.json') if (output/'full_item_inventory.json').exists() else None,
            'build_outputs_removed':not build.exists() and not binary.exists(),
            'scope':'Actual native compiler validates canonical and nine one-fault modules. Auxiliary pinned syn source program inspects every top-level item and inner attribute in an exact canonical/one-fault prefix before the appended fixture; this is not the calibrated complexity tool, macro expansion, generic Rust verification or a Grothendieck algorithm.'}
        write_json(output/'receipt.json',receipt)
    if not stable_dependencies or not receipt['source_unchanged']:
        raise RuntimeError('Archival source/tool dependency drift')
    print('Archival AST receipt:',output,flush=True)
    print('Primary native receipt:',native,flush=True)
    return 0


if __name__=='__main__':
    raise SystemExit(main())
