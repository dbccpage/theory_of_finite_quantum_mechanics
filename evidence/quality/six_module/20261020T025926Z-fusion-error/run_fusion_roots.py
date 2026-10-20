"""One actual full fusion package per root mutation, sharing only dependencies.

Each variant has its own crate root and actual support sources; no type stubs or
source projection. Full canonical-suite evidence is a separate fusion audit.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'category_homology'))
from run_audit import (ROOT,RUST,bind_dependencies,clear_debug_outputs,
                       dependency_inventory,digest,execute,execute_build,write_json)

def passed(run):
    return run['exit_code']==0 and not run['timed_out'] and bool(re.search(
        r'test result: ok\. [1-9][0-9]* passed;', (ROOT/run['log']).read_text(encoding='utf-8')))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--subject',choices=('lib','mod','fusion_ring','scalar','error'),required=True)
    name=parser.parse_args().subject
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    output=ROOT/'evidence/quality/six_module'/(stamp+'-fusion-'+name)
    output.mkdir(parents=True)
    work=RUST/'target/six-module'/(stamp+'-fusion-'+name)
    work.mkdir(parents=True)
    folder=RUST/'src/fusion_categories'
    sources={p.relative_to(ROOT).as_posix():digest(p) for p in sorted(folder.iterdir())
             if p.suffix=='.rs' or p.name=='Cargo.toml'}
    write_json(output/'source_manifest.json',sources)
    policy=json.loads((HERE/('fusion_'+name+'_boundaries.json')).read_text(encoding='utf-8'))
    source=ROOT/policy['subject']['path']
    if digest(source)!=policy['subject']['sha256']:raise ValueError('Source/policy drift')
    text=source.read_text(encoding='utf-8')
    fixture_name = 'fusion_'+name+'_challenges.rs' if name in ('fusion_ring','scalar','error') else 'fusion_root_challenges.rs'
    test_filter = {'fusion_ring':'ring_review::','scalar':'scalar_review::','error':'error_review::'}.get(name,'sum_review::')
    fixture=(HERE/fixture_name).read_text(encoding='utf-8')
    candidates=[text];records=[];support=[]
    for item in policy['faults']:
        if text.count(item['needle'])!=1:raise ValueError('Fault occurrence: '+item['id'])
        candidates.append(text.replace(item['needle'],item['replacement']))
        records.append({**item,'outcome':'unrun'})
    members=[]
    for index,candidate in enumerate(candidates):
        package=work/f'p{index}'
        package.mkdir();members.append(f'p{index}')
        for path,value in sources.items():
            dest=package/Path(path).name
            shutil.copyfile(ROOT/path,dest)
            if path.endswith('.rs') and Path(path).name!=name+'.rs':
                support.append({'path':dest.relative_to(ROOT).as_posix(),'source':path,'sha256':value})
        manifest=package/'Cargo.toml'
        m=manifest.read_text(encoding='utf-8').replace('name = "tfqm_fusion_categories"',f'name = "tfqm_fusion_root_{index}"')
        m=m.replace('path = "lib.rs"', 'path = "mod.rs"' if name=='mod' else 'path = "lib.rs"')
        manifest.write_text(m,encoding='utf-8')
        path=package/(name+'.rs')
        path.write_text(candidate+'\n'+fixture,encoding='utf-8')
        if index:records[index-1].update(candidate=path.relative_to(ROOT).as_posix(),sha256=digest(path))
    (work/'Cargo.toml').write_text('[workspace]\nmembers='+json.dumps(members)+'\nresolver="2"\n'
        '[profile.dev]\ndebug=0\n[profile.test]\ndebug=0\n',encoding='utf-8')
    for f in (Path(__file__).name,fixture_name,'fusion_'+name+'_boundaries.json'):
        shutil.copyfile(HERE/f,output/f)
    write_json(output/'support_sources.json',{'AuthorityEffect':'None','copies':support})
    write_json(output/'mutations.json',records)
    roots,dependencies=bind_dependencies(work,output)
    build=work/'target';binaries={};baseline=[];restored=[];builds=[]
    try:
        try:
            run=execute_build(['cargo','test','--offline','--locked','--workspace','--lib','--no-run',
                '--message-format=json','--jobs','1','--target-dir',str(build)],work,output/'build.log')
            builds.append(run)
            if run['exit_code']==0:
                for line in (output/'build.log').read_text(encoding='utf-8').splitlines():
                    try:item=json.loads(line)
                    except ValueError:continue
                    if item.get('reason')=='compiler-artifact' and item.get('executable'):
                        index=int(item['target']['name'].rsplit('_',1)[1])
                        binary=work/f'tests{index}.exe';shutil.copyfile(item['executable'],binary);binaries[index]=binary
        finally:clear_debug_outputs(build,work)
        if len(binaries)==len(candidates):
            baseline=[execute([str(binaries[0]),test_filter,'--test-threads=1'],work,output/'control.log')]
            if all(passed(x) for x in baseline):
                for index,record in enumerate(records,1):
                    result=execute([str(binaries[index]),test_filter,'--test-threads=1'],work,output/f'fault-{index}.log',timeout=60)
                    log=(ROOT/result['log']).read_text(encoding='utf-8')
                    record['outcome']=('inconclusive' if result['timed_out'] else 'survived' if passed(result)
                        else 'killed' if result['exit_code']!=0 and 'test result: FAILED' in log else 'inconclusive')
                    record['run']=result;write_json(output/'mutations.json',records)
            restored=[execute([str(binaries[0]),test_filter,'--test-threads=1'],work,output/'restored-control.log')]
    finally:
        for binary in binaries.values():binary.unlink(missing_ok=True)
        if build.exists():
            if build.resolve().parent!=work.resolve():raise ValueError('Cleanup escaped run')
            shutil.rmtree(build)
    counts=Counter(item['outcome'] for item in records)
    accounting={k:counts[k] for k in ('killed','survived','demonstrably_equivalent','invalid','inconclusive','unrun')}
    eligible=sum(accounting[k] for k in ('killed','survived','inconclusive','unrun'))
    summary={'AuthorityEffect':'None','baseline_ok':bool(baseline) and all(passed(x) for x in baseline),
        'restored_ok':bool(restored) and all(passed(x) for x in restored),'baseline':baseline,'restored':restored,'builds':builds,
        'mutation_accounting':accounting,'conservative_ratio':counts['killed']/eligible if eligible else None,
        'source_unchanged':all(digest(ROOT/p)==v for p,v in sources.items()),
        'dependencies_unchanged':dependency_inventory(roots)==dependencies,
        'build_outputs_removed':not build.exists() and not any(x.exists() for x in binaries.values()),
        'subject':policy['subject'],'runner_sha256':digest(output/Path(__file__).name),
        'policy_sha256':digest(output/('fusion_'+name+'_boundaries.json')),
        'fixture_sha256':digest(output/fixture_name),
        'scope':'Actual full fusion packages, one source fault each. Subject-specific independent boundary replay; full canonical fusion suites are separately bound. No projection/stubs or whole-workspace result.'}
    write_json(output/'summary.json',summary)
    print('Receipt:',output,flush=True)
    print(json.dumps({k:v for k,v in summary.items() if isinstance(v,bool) or k=='mutation_accounting'}),flush=True)
    return 0 if all(v for v in summary.values() if isinstance(v,bool)) else 1

if __name__=='__main__':raise SystemExit(main())
