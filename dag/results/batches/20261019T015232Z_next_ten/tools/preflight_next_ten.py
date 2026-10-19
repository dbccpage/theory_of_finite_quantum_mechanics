from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode=True
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
BATCH=ROOT/'dag/results/batches/20261019T015232Z_next_ten'
spec=importlib.util.spec_from_file_location('native',BATCH/'native.py');native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
LEAN=str(Path.home()/'.elan/bin/lean.exe')
jobs=[('FQ-BORN-NORMALIZATION-REDUNDANCY','BornRedundancy'),('FQ-ENTROPY-DICHOTOMY-BAKER','EntropyDichotomy'),('FQ-CABELLO-NO-INTEGER-FRAME','H054GleasonCyclotomicObstruction'),('FQ-CARRIER-CONTRACT-V2','H052CyclotomicTowerDirected'),('FQ-CONTEXTUALITY-CECH-F2','ContextualityObstruction')]


def compile(job):
    node,name=job;source=ROOT/'lean4'/(name+'.lean');out=native.LIB/(name+'.olean');out.parent.mkdir(parents=True,exist_ok=True)
    folder=ROOT/'dag/results'/node/'runs/20261019T015232Z_staged/p0/native'
    receipt=native.record(folder,'source_'+name,[LEAN,'-o',str(out),str(source)],cwd=ROOT/'lean4',sources=[source,ROOT/'lean4/lean-toolchain',ROOT/'lean4/lake-manifest.json'])
    return {'node':node,'source':name,'exit_code':receipt['exit_code'],'seconds':receipt['seconds']}


with ThreadPoolExecutor(max_workers=3) as pool:
    for future in as_completed([pool.submit(compile,job) for job in jobs]):
        print(json.dumps(future.result()),flush=True)
