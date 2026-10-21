import sys,os
from pathlib import Path
import pytest

def guard(event,args):
    if event in {"socket.connect","subprocess.Popen","os.system"}:
        raise RuntimeError("Diagnostic collection refuses network and child processes")
    if event=="open" and isinstance(args[0],(str,bytes)):
        name=Path(os.fsdecode(args[0])).name
        if name==".env" or name.startswith(".env."):
            raise RuntimeError("Credential files are outside diagnostic collection")
sys.addaudithook(guard)
raise SystemExit(pytest.main(["--collect-only","--maxfail=5","-q","code/python/src/majorana/tests","-p","no:cacheprovider"]))
