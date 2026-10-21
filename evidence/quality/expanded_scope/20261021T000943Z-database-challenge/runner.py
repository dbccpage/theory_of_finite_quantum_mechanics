"""Actual SQLite source challenges with compilation, binding and six outcomes."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys

import check_entrypoints as core

ROOT = Path(__file__).resolve().parents[4]
TEST = 'code/python/tests/test_database_integrity.py'
ADAPTER = 'code/python/src/databases/migrations.py'
BASE = 'code/python/src/databases/'
SPECS = {
    BASE+'schema.sql': {'kind':'sql','schema':'ledger','direction':'up',
        'selector':'ledger or down_refuses or install', 'mutants':[
        ('stage integer coercion admitted', 'stage_num ANY PRIMARY KEY', 'stage_num INTEGER PRIMARY KEY'),
        ('stage range omitted', "typeof(stage_num) = 'integer' AND stage_num BETWEEN 0 AND 1000000", "typeof(stage_num) = 'integer'"),
        ('receipt NUL admitted', 'AND instr(sha256, char(0)) = 0', ''),
        ('witness NUL admitted', 'AND instr(witness_id, char(0)) = 0', ''),
        ('nullable witness primary key admitted', ') STRICT, WITHOUT ROWID;\nCREATE INDEX idx_survivor_stage', ') STRICT;\nCREATE INDEX idx_survivor_stage'),
        ('missing witness parent admitted', "stage_id ANY NOT NULL CHECK (typeof(stage_id) = 'integer') REFERENCES genesis_stages(stage_num) ON DELETE RESTRICT ON UPDATE RESTRICT,\n    x_locus", "stage_id ANY NOT NULL CHECK (typeof(stage_id) = 'integer'),\n    x_locus"),
        ('retained bit domain widened', 'is_retained IN (0, 1)', 'is_retained BETWEEN -1 AND 7'),
        ('Stokes claim default promoted', 'stokes_verified ANY NOT NULL DEFAULT 0', 'stokes_verified ANY NOT NULL DEFAULT 1'),
        ('unreferenced Stokes claim admitted', 'CHECK (stokes_verified = 0 OR (stokes_verified = 1 AND evidence_sha256 IS NOT NULL))', 'CHECK (stokes_verified IN (0, 1))'),
        ('oversized locus admitted', 'length(trim(x_locus)) BETWEEN 1 AND 4096', 'length(trim(x_locus)) BETWEEN 1 AND 8192'),
        ('chain dimension domain widened', 'dimension BETWEEN 0 AND 64', 'dimension BETWEEN 0 AND 65'),
        *[(table+' row cap omitted', '(SELECT COUNT(*) FROM '+table+') >= 4096', '(SELECT COUNT(*) FROM '+table+') > 4096') for table in ['genesis_stages','ledger_receipts','survivor_witnesses','simplicial_chains']],
        ('atomic install BEGIN omitted', 'BEGIN IMMEDIATE;', '-- omitted BEGIN'),
    ]},
    BASE+'schema.down.sql': {'kind':'sql','schema':'ledger','direction':'down',
        'selector':'down_refuses or install_empty', 'mutants':[
        ('nonempty stages dropped', 'AND NOT EXISTS (SELECT 1 FROM genesis_stages)', ''),
        ('nonempty receipts dropped', 'AND NOT EXISTS (SELECT 1 FROM ledger_receipts)', ''),
        ('empty rollback guard inverted', 'THEN 1 ELSE 0 END;', 'THEN 0 ELSE 1 END;'),
        ('stage object left behind', 'DROP TABLE genesis_stages;', '-- omitted stage drop'),
        ('temporary guard left behind', 'DROP TABLE _finite_qm_ledger_down_guard;', '-- omitted guard drop'),
    ]},
    BASE+'fermion_sign_problem.sql': {'kind':'sql','schema':'signed_ensemble','direction':'up',
        'selector':'signed or empty_zero or down_refuses or install', 'mutants':[
        ('REAL magnitude coercion admitted', 'magnitude ANY NOT NULL', 'magnitude INTEGER NOT NULL'),
        ('REAL denominator coercion admitted', 'common_denominator ANY NOT NULL', 'common_denominator INTEGER NOT NULL'),
        ('magnitude envelope widened', 'magnitude BETWEEN 0 AND 1000000', 'magnitude BETWEEN 0 AND 1000001'),
        ('zero sign admitted', 'sign IN (-1, 1)', 'sign IN (-1, 0, 1)'),
        ('parent row cap omitted', '(SELECT COUNT(*) FROM signed_ensembles) >= 128', '(SELECT COUNT(*) FROM signed_ensembles) > 128'),
        ('path row cap omitted', '(SELECT COUNT(*) FROM signed_configurations) >= 4096', '(SELECT COUNT(*) FROM signed_configurations) > 4096'),
        ('denominator reinterpretation admitted', 'WHEN NEW.common_denominator != OLD.common_denominator', 'WHEN 0 AND NEW.common_denominator != OLD.common_denominator'),
        ('sign omitted from ensemble sum', 'COALESCE(SUM(c.magnitude * c.sign), 0) AS signed_numerator', 'COALESCE(SUM(c.magnitude), 0) AS signed_numerator'),
        ('integer division smuggled into ratio', 'THEN signed_numerator ELSE NULL END AS average_sign_num', 'THEN signed_numerator / unsigned_numerator ELSE NULL END AS average_sign_num'),
        ('undefined ratio assigned a denominator', 'THEN unsigned_numerator ELSE NULL END AS average_sign_den', 'THEN unsigned_numerator ELSE 1 END AS average_sign_den'),
        ('ensemble identity omitted from count partition', 'COUNT(*) OVER (PARTITION BY c.ensemble_id, c.orbit_id)', 'COUNT(*) OVER (PARTITION BY c.orbit_id)'),
        ('whole orbit replaced by running frame', 'SUM(c.magnitude) OVER (PARTITION BY c.ensemble_id, c.orbit_id)', 'SUM(c.magnitude) OVER (PARTITION BY c.ensemble_id, c.orbit_id ORDER BY c.path_id)'),
        ('negative or zero orbits omitted', 'FROM SignedPathWindowAudit;', 'FROM SignedPathWindowAudit WHERE orbit_signed_numerator > 0;'),
        ('signed orbit identifier NUL admitted', 'AND instr(orbit_id, char(0)) = 0', ''),
    ]},
    BASE+'fermion_sign_problem.down.sql': {'kind':'sql','schema':'signed_ensemble','direction':'down',
        'selector':'down_refuses or install_empty', 'mutants':[
        ('named ensemble discarded', 'AND NOT EXISTS (SELECT 1 FROM signed_ensembles)', ''),
        ('orbit view left behind', 'DROP VIEW SignedOrbitAudit;', '-- omitted orbit view drop'),
        ('temporary signed guard left behind', 'DROP TABLE _finite_qm_signed_down_guard;', '-- omitted guard drop'),
    ]},
    ADAPTER: {'kind':'python','module':'src.databases.migrations','selector':'', 'mutants':[
        ('string subclasses admitted', 'if type(schema) is not str or type(direction) is not str:', 'if not isinstance(schema, str) or not isinstance(direction, str):'),
        ('connection subclasses admitted', 'if type(connection) is not sqlite3.Connection:', 'if not isinstance(connection, sqlite3.Connection):'),
        ('caller transaction ownership ignored', 'if connection.in_transaction:', 'if False and connection.in_transaction:'),
        ('empty source accepted', 'if not raw:', 'if False and not raw:'),
        ('source byte cap omitted', 'if len(raw) > MAX_SCRIPT_BYTES:', 'if False and len(raw) > MAX_SCRIPT_BYTES:'),
        ('FK activation omitted', "cursor.execute('PRAGMA foreign_keys=ON')", 'pass  # missing FK activation'),
        ('FK activation verification omitted', "if cursor.execute('PRAGMA foreign_keys').fetchone()[0] != 1:", "if False and cursor.execute('PRAGMA foreign_keys').fetchone()[0] != 1:"),
        ('busy timeout dropped to zero', 'BUSY_TIMEOUT_MS = 1000', 'BUSY_TIMEOUT_MS = 0'),
        ('owned rollback omitted', 'if admitted is not None:', 'if False and admitted is not None:'),
        ('autocommit rollback becomes a no-op', "cursor.execute('ROLLBACK')", 'connection.rollback()'),
        ('interrupt cleanup omitted', 'except BaseException as error:', 'except Exception as error:'),
        ('partial transaction reported successful', 'if admitted.in_transaction:', 'if False and admitted.in_transaction:'),
        ('source digest invented', 'hashlib.sha256(raw).hexdigest()', "'0'*64"),
        ('rollback failure concealed', "raise MigrationError('rollback failed; connection state is unverified', getattr(error, 'sqlite_errorname', None)) from error", 'return'),
    ]},
}

SQL_CHILD = r'''
import hashlib,json,pathlib,sqlite3,sys
root,source,temp,*tests=sys.argv[1:]
root=pathlib.Path(root);raw=pathlib.Path(source).read_bytes()
sys.path.insert(0,str(root/'code/python'))
con=sqlite3.connect(':memory:')
try:
    con.execute('PRAGMA foreign_keys=ON')
    if TARGET_DIRECTION=='down':
        up='schema.sql' if TARGET_SCHEMA=='ledger' else 'fermion_sign_problem.sql'
        con.executescript((root/'code/python/src/databases'/up).read_bytes().decode())
    con.executescript(raw.decode('utf-8'))
except UnicodeDecodeError as error:
    print(json.dumps({'phase':'compile','status':'INVALID','error':type(error).__name__}));sys.exit(4)
except sqlite3.IntegrityError:
    pass # Compiles but semantically refuses a valid empty migration: eligible.
except sqlite3.Error as error:
    status='INVALID' if getattr(error,'sqlite_errorname',None)=='SQLITE_ERROR' else 'INCONCLUSIVE'
    print(json.dumps({'phase':'compile','status':status,'error':str(error)}));sys.exit(4)
finally:
    con.close()
from src.databases import migrations as module
class SourcePath:
    def __init__(self,value): self.real=pathlib.Path(value)
    def resolve(self): self.real=self.real.resolve();return self
    def with_name(self,name):
        return pathlib.Path(source) if name==TARGET_FILENAME else self.real.with_name(name)
module.Path=SourcePath
try:
    observed=module._source((TARGET_SCHEMA,TARGET_DIRECTION))
    if observed!=raw:raise RuntimeError('SQL_CANDIDATE_BINDING_MISMATCH')
except Exception as error:
    print(json.dumps({'phase':'binding','error':type(error).__name__}));sys.exit(3)
print(json.dumps({'phase':'sql_candidate_binding','source_sha256':hashlib.sha256(observed).hexdigest(),'schema':TARGET_SCHEMA,'direction':TARGET_DIRECTION}))
import pytest
args=[*tests,'-q','--basetemp',temp,'-p','no:cacheprovider']
if TARGET_SELECTOR:args+=['-k',TARGET_SELECTOR]
result=pytest.main(args)
print(json.dumps({'phase':'pytest','exit_code':int(result)}));sys.exit(result)
'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute(raw, folder, tag, spec):
    candidate=folder/(tag+('.sql' if spec['kind']=='sql' else '.py'))
    candidate.write_bytes(raw)
    if spec['kind']=='python':
        try: compile(raw,str(candidate),'exec')
        except (SyntaxError,ValueError) as error:
            return {'status':'INVALID','reason':str(error),'source_sha256':sha(candidate)}
    try:
        result=subprocess.run([sys.executable,'-B',str(folder/'child.py'),str(ROOT),str(candidate),
            str(ROOT/'.pytest_cache/database-candidates'/folder.parent.name/folder.name/tag),TEST],
            cwd=ROOT,text=True,capture_output=True,timeout=60)
    except subprocess.TimeoutExpired as error:
        log=folder/(tag+'.log');log.write_bytes((error.stdout or b'')+(error.stderr or b''))
        return {'status':'INCONCLUSIVE','reason':'60 second child timeout','source_sha256':sha(candidate),'log_sha256':sha(log)}
    log=folder/(tag+'.log');log.write_bytes((result.stdout+result.stderr).encode())
    try:last=json.loads(result.stdout.strip().splitlines()[-1])
    except (IndexError,json.JSONDecodeError):last={}
    status=('SURVIVED' if result.returncode==0 and last=={'phase':'pytest','exit_code':0}
        else 'KILLED' if result.returncode==1 and last=={'phase':'pytest','exit_code':1}
        else 'INVALID' if last.get('phase')=='compile' and last.get('status')=='INVALID'
        else 'INCONCLUSIVE')
    return {'status':status,'exit_code':result.returncode,'last_status':last,'source_sha256':sha(candidate),'log_sha256':sha(log)}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--subject',action='append',default=[]);parser.add_argument('--only',action='append',default=[])
    args=parser.parse_args()
    specs={name:{**spec,'mutants':[m for m in spec['mutants'] if not args.only or m[0] in args.only]}
        for name,spec in SPECS.items() if not args.subject or name in args.subject}
    assert specs and all(row['mutants'] for row in specs.values())
    folder=ROOT/'evidence/quality/expanded_scope'/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-database-challenge');folder.mkdir()
    inputs={TEST,ADAPTER,'SCORING.md','code/python/tests/conftest.py',*SPECS}
    pins={name:sha(ROOT/name) for name in sorted(inputs)}
    for name in pins:
        target=folder/'inputs'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((ROOT/name).read_bytes())
    (folder/'runner.py').write_bytes(Path(__file__).read_bytes())
    (folder/'configuration.json').write_bytes((json.dumps(specs,indent=2)+'\n').encode())
    receipt={'AuthorityEffect':'None','inputs':pins,'python':sys.version,'sqlite_version':sqlite3.sqlite_version,'runner_sha256':sha(Path(__file__)),
        'configuration_sha256':sha(folder/'configuration.json'),'files':{},
        'scope':'Named SQL migrations and Python lifecycle only. Fresh SQLite syntax/name-resolution probe rejects invalid SQL before mutation accounting. Constraint refusals are eligible semantic outcomes. Candidate bytes are imported/bound at the actual tested migration source path.',
        'trust':'CPython, SQLite and pytest plus conftest/provider transitive code and host OS remain trusted, not a security sandbox or a whole-database proof.'}
    for name,spec in specs.items():
        work=folder/Path(name).name;work.mkdir()
        if spec['kind']=='python':
            child=core.CHILD.replace('TARGET_MODULE',repr(spec['module'])).replace('TARGET_SOURCE',repr(name))
        else:
            child=SQL_CHILD
            for key,value in [('TARGET_FILENAME',Path(name).name),('TARGET_SCHEMA',spec['schema']),('TARGET_DIRECTION',spec['direction']),('TARGET_SELECTOR',spec['selector'])]:child=child.replace(key,repr(value))
        (work/'child.py').write_bytes(child.encode())
        raw=(ROOT/name).read_bytes();baseline=execute(raw,work,'baseline',spec)
        result={'source':name,'source_sha256':pins[name],'baseline':baseline,'baseline_passed':baseline['status']=='SURVIVED','mutants':[]}
        for i,(title,old,new) in enumerate(spec['mutants']):
            if not result['baseline_passed']:outcome={'status':'UNRUN','reason':'baseline failed or inconclusive'}
            elif raw.decode().count(old)!=1:outcome={'status':'INVALID','reason':'site not unique','matches':raw.decode().count(old)}
            else:outcome=execute(raw.decode().replace(old,new,1).encode(),work,f'mutant-{i:02d}',spec)
            result['mutants'].append({'name':title,**outcome});print(json.dumps({'subject':name,'name':title,**outcome}),flush=True)
        counts=Counter(m['status'] for m in result['mutants']);result['outcomes']=dict(counts)
        eligible=sum(counts[k] for k in ['KILLED','SURVIVED','INCONCLUSIVE','UNRUN'])
        result['detection_fraction']={'numerator':counts['KILLED'],'denominator':eligible} if eligible else None
        result['status']='PASS' if result['baseline_passed'] and counts['KILLED']==len(spec['mutants']) else 'REVIEW_OUTCOMES'
        receipt['files'][name]=result
    receipt['inputs_unchanged']=all(sha(ROOT/name)==digest for name,digest in pins.items())
    receipt['status']='PASS' if receipt['inputs_unchanged'] and all(row['status']=='PASS' for row in receipt['files'].values()) else 'REVIEW_OUTCOMES'
    (folder/'receipt.json').write_bytes((json.dumps(receipt,indent=2)+'\n').encode())
    print(json.dumps({'path':folder.relative_to(ROOT).as_posix(),'status':receipt['status'],'outcomes':{n:r['outcomes'] for n,r in receipt['files'].items()}}),flush=True)


if __name__=='__main__':
    main()
