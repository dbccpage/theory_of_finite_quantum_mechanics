
import hashlib,json,pathlib,sqlite3,sys
root,source,temp,*tests=sys.argv[1:]
root=pathlib.Path(root);raw=pathlib.Path(source).read_bytes()
sys.path.insert(0,str(root/'code/python'))
con=sqlite3.connect(':memory:')
try:
    con.execute('PRAGMA foreign_keys=ON')
    if 'down'=='down':
        up='schema.sql' if 'ledger'=='ledger' else 'fermion_sign_problem.sql'
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
        return pathlib.Path(source) if name=='schema.down.sql' else self.real.with_name(name)
module.Path=SourcePath
try:
    observed=module._source(('ledger','down'))
    if observed!=raw:raise RuntimeError('SQL_CANDIDATE_BINDING_MISMATCH')
except Exception as error:
    print(json.dumps({'phase':'binding','error':type(error).__name__}));sys.exit(3)
print(json.dumps({'phase':'sql_candidate_binding','source_sha256':hashlib.sha256(observed).hexdigest(),'schema':'ledger','direction':'down'}))
import pytest
args=[*tests,'-q','--basetemp',temp,'-p','no:cacheprovider']
if 'down_refuses or install_empty':args+=['-k','down_refuses or install_empty']
result=pytest.main(args)
print(json.dumps({'phase':'pytest','exit_code':int(result)}));sys.exit(result)
