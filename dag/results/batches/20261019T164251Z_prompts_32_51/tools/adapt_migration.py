"""Add exact upstream path-baseline support without rewriting frozen run evidence."""
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');B=ROOT/'dag/results/batches/20261019T164251Z_prompts_32_51'
def edit(name,change):
    p=B/name;old=p.read_bytes();copy=B/'upstream/tools_before'/name
    if copy.exists():raise ValueError('Refuse overwrite '+str(copy))
    copy.parent.mkdir(parents=True,exist_ok=True);copy.write_bytes(old)
    p.write_bytes(change(old.decode()).encode())
def verify(t):
    marker="    rows=load(BATCH/'selection.json')['nodes'];"
    extra="""    migration=load(BATCH/'upstream/reconciliation_plan.json')
    upstream_index=load(BATCH/'upstream/index.git.json')
    raw=(BATCH/'upstream/index.git.json').read_bytes()
    require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\\0'+raw).hexdigest()==migration['upstream_index_git_blob'],'upstream index Git blob')
    for n in migration['nodes'].values():
        raw=(ROOT/n['upstream_collection_snapshot']).read_bytes()
        require(hashlib.sha256(raw).hexdigest()==n['upstream_collection_sha256'],'upstream baseline sha256')
        require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\\0'+raw).hexdigest()==n['upstream_collection_git_blob'],'upstream collection Git blob')
"""
    t=t.replace(marker,extra+marker)
    t=t.replace("[n for n in before['nodes'] if n['node_id'] not in ids]==[n for n in current['nodes'] if n['node_id'] not in ids]", "[n for n in upstream_index['nodes'] if n['node_id'] not in ids]==[n for n in current['nodes'] if n['node_id'] not in ids]")
    t=t.replace("collection=yaml.safe_load((ROOT/node['operad_collection']).read_bytes())", "mapped=migration['nodes'][task];collection=yaml.safe_load((ROOT/mapped['operad_collection']).read_bytes());baseline=yaml.safe_load((ROOT/mapped['upstream_collection_snapshot']).read_bytes())")
    t=t.replace("require(original[key]==collection[key],'historical claim mutated '+key)", "require(baseline[key]==collection[key],'upstream canonical metadata mutated '+key)")
    needle="        for attempt in load(run/'p1/review_contract.json')['attempts']:"
    t=t.replace(needle,"        require(original['target']['source_statement']==baseline['target']['source_statement'],'mathematical target changed in migration')\n"+needle)
    return t
edit('verify_batch.py',verify)
def finalize(t):
    t=t.replace("selection=json.loads", "migration=json.loads((BATCH/'upstream/reconciliation_plan.json').read_bytes())\nselection=json.loads",1)
    t=t.replace("p=s.ROOT/node['operad_collection']", "p=s.ROOT/migration['nodes'][task]['operad_collection']")
    t=t.replace('Source labels and original prompts remain unchanged historical annotations.', 'All captured prompts, source labels and original stage bytes remain sealed. The concurrent upstream naming migration is preserved in canonical prompt/operad paths; upstream baseline Git blobs and the unchanged mathematical statements are verified separately.')
    t=t.replace("Dedicated per-prompt README", "A concurrent upstream merge changed path naming and enhanced E003/E005. The batch preserves the incoming canonical metadata and root list, retains its exact earlier source versions, and rebuilds all 33 required local Lean modules on the integrated tree. The single root-list conflict retained PromptDynamics and each upstream foundation module once. upstream/ stores the pinned base, Git-blob baselines and reconciliation receipt.\\n\\nDedicated per-prompt README")
    return t
edit('tools/finalize.py',finalize)
def stage(t):
    t=t.replace("if git('rev-parse','HEAD',text=True).strip()!=selection['base_commit']:raise ValueError('Base SHA changed')", "integration=json.loads((BATCH/'upstream/integration_head.json').read_bytes())\nif git('rev-parse','HEAD',text=True).strip()!=integration['integrated_head']:raise ValueError('Integrated HEAD changed')\nfor parent in [selection['base_commit'],integration['upstream_commit']]:\n    subprocess.run(['git','merge-base','--is-ancestor',parent,'HEAD'],cwd=ROOT,check=True)")
    return t
edit('tools/git_prepare.py',stage)
p=B/'tools/adapt_migration.py'
if p.exists():raise ValueError('Already installed')
p.write_bytes(Path(__file__).read_bytes())
print('Added pinned upstream baseline support; retained all predecessor tool bytes.')
