
import importlib,importlib.abc,importlib.util,json,pathlib,sys,types
root, source, temp, *tests = sys.argv[1:]
sys.path.insert(0,str(pathlib.Path(root)/"code/python"))
name = 'src.databases.migrations'
origin=pathlib.Path(root)/'code/python/src/databases/migrations.py'
class CandidateLoader(importlib.abc.Loader):
    def create_module(self,spec):
        return None
    def exec_module(self,value):
        exec(compile(pathlib.Path(source).read_bytes(),source,"exec"),value.__dict__)
class CandidateFinder(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname==name:
            return importlib.util.spec_from_file_location(name,str(origin),loader=CandidateLoader(),
                submodule_search_locations=[str(origin.parent)] if origin.name=="__init__.py" else None)
sys.meta_path.insert(0,CandidateFinder())
try:
    module=importlib.import_module(name)
except Exception as error:
    print(json.dumps({"phase":"load","error":type(error).__name__,"detail":str(error)}));sys.exit(3)
import pytest
class CandidateBindings:
    def pytest_collection_modifyitems(self,session,config,items):
        checked=set()
        for item in items:
            for value in vars(item.module).values():
                if isinstance(value,(types.FunctionType,type)) and getattr(value,"__module__",None)==name:
                    symbol=value.__name__
                    if getattr(module,symbol,None) is not value:
                        raise RuntimeError("STALE_CANDIDATE_BINDING:"+name+":"+symbol)
                    checked.add(symbol)
        print(json.dumps({"phase":"candidate_bindings","checked_symbols":sorted(checked)}))
result=pytest.main([*tests,"-q","-k","not mutation","--basetemp",temp,"-p","no:cacheprovider"],plugins=[CandidateBindings()])
print(json.dumps({"phase":"pytest","exit_code":int(result)}));sys.exit(result)
