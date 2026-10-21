"""Record the prior evidence this run builds on, with exact digests; nothing is modified."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[1]
ROOT=next(p for p in B.parents if (p/'lean4/lakefile.lean').is_file())
PRIOR=[
    'dag/operads/fq_gap_u1_circle.yaml',
    'dag/prompts/finite_qm_core_fq_gap_u1_circle_conditional.yaml',
    'dag/results/FQ-GAP-U1-CIRCLE/reviews/20261019_scope_audit/scope_review.json',
    'dag/results/FQ-GAP-U1-CIRCLE/reviews/20261019_scope_audit/operad_delta.yaml',
    'dag/derivations/08_l1_to_l2/tfq_0294_circle_phases_as_an_imported_unit_group.md',
    'dag/derivations/12_finite_qm_structure/tfq_0253_conditional_complex_carrier_selector.md',
    'lean4/H011Circle.lean',
    'lean4/H011U1SelectorBoundary.lean',
    'lean4/U1AngleAddition.lean',
    'lean4/U1TorsionExclusion.lean',
    'lean4/PromptPhaseScope.lean',
    'code/python/src/qm/phase_scope.py',
    'code/rust/src/finite_probability/phase_scope.rs',
    'lean4/lean-toolchain',
    'lean4/lake-manifest.json',
]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
if __name__=='__main__':
    entries=[{'path':p,'bytes':(ROOT/p).stat().st_size,'sha256':sha(ROOT/p)} for p in PRIOR]
    (B/'provenance.json').write_text(json.dumps({
        'authority_effect':'None',
        'prior_evidence':entries,
        'prior_scope':'runs/20261019T145000Z_staged and reviews/20261019_scope_audit established the cleared Cayley identity and the linear half-angle constraint a^2=4/5 on retained cases, leaving the unbounded non-square proof for 4/5, full power-map injectivity n -> u^n, the additive-Q homomorphism obstruction, and the explicit algebraic-to-compact-circle completion structure open.',
        'replay_tool':'tools/replay.py follows the exact source-only receipt protocol of runs/20261020T205000Z_effect_valuation_lean.',
        'unchanged':'Prior sealed bundles, staged runs and scope audit records under dag/results/FQ-GAP-U1-CIRCLE are not modified by this run.'
    },indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'prior_entries':len(entries)}))
