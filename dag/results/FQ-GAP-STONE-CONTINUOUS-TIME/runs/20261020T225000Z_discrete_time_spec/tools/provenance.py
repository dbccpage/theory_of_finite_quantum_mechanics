"""Record the prior evidence this run builds on, with exact digests; nothing is modified."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[1]
ROOT=next(p for p in B.parents if (p/'lean4/lakefile.lean').is_file())
PRIOR=['lean4/H055DiscreteDynamicsStone.lean','lean4/H016ContinuousDynamicsFork.lean','lean4/H061DynamicsDichotomy.lean','lean4/PromptDynamics.lean','dag/operads/fq_gap_stone_continuous_time.yaml','dag/prompts/finite_qm_dynamics_fq_gap_stone_continuous_time_conditional.yaml','papers/core/finite_quantum_mechanics.md','docs/QM_PROBLEM_AND_PROOF_ATLAS.md','dag/results/FQ-GAP-BORN-UNIQUENESS-GLEASON/runs/20261020T205000Z_effect_valuation_lean/tools/replay.py','lean4/lean-toolchain','lean4/lake-manifest.json']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
if __name__=='__main__':
    entries=[{'path':p,'bytes':(ROOT/p).stat().st_size,'sha256':sha(ROOT/p)} for p in PRIOR]
    (B/'provenance.json').write_text(json.dumps({'authority_effect':'None','prior_evidence':entries,'scalar_results_complemented':'Uncommitted working-copy modules U1PythagoreanObstruction.lean and U1PowerMapInjectivity.lean (not on any branch at the time of this run, hence not pinned here) establish the scalar facts on the rational circle; this run specifies the carrier-level (matrix) notions and derives the 2 x 2 obstruction independently.','replay_tool':'tools/replay.py is byte-identical to the one of the effect-valuation run.','unchanged':'Prior sealed bundles, canonical operad collections and the earlier staged run of this node are not modified.'},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'prior_entries':len(entries)}))
