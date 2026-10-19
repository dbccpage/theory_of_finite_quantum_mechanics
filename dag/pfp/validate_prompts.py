"""Structural and provenance audit; this does not prove any mathematical target."""
from pathlib import Path
import hashlib
import json
import re
import yaml
from custody import Custody

ROOT=Path(__file__).resolve().parents[2]
REJECT=re.compile(r'stage_route_shadow_invariant|quotient_reduced_countermodel_defect|Set cochain_d1_d0_exact_zero|Set should_continue|exact 18 keys|which equals|raw_candidate_rival_int|countermodel_expected_int|P\* Cycle C_4')


def check_presentation(presentation):
    """Check declared arities/colours/graft slots; no semantic or coherence verdict."""
    errors=[]
    colours={c['id'] for c in presentation['colours']}
    generators={g['id']:g for g in presentation['generators']}
    relations={r['id'] for r in presentation['relations']}
    if len(generators)!=len(presentation['generators']): errors.append('duplicate generator')
    for generator in generators.values():
        if generator['arity']!=len(generator['ordered_inputs']): errors.append('arity mismatch')
        if not set(generator['ordered_inputs']+[generator['output']])<=colours: errors.append('unknown colour')
    def graft(outer,slot,inner):
        left,out=outer;right,received=inner
        if type(slot) is not int or not 0<=slot<len(left): raise ValueError('invalid graft slot')
        if left[slot]!=received: raise ValueError('graft colour mismatch')
        return left[:slot]+right+left[slot+1:],out
    def signature(tree):
        if isinstance(tree,str):
            g=generators[tree]
            return list(g['ordered_inputs']),g['output']
        return graft(signature(tree['outer']),tree['slot'],signature(tree['inner']))
    for composition in presentation['compositions']:
        try:
            graft(signature(composition['outer_operation']),composition['input_slot'],signature(composition['inner_operation']))
            if not set(composition['licensing_relations'])<=relations: errors.append('unknown licensing relation')
        except (KeyError,ValueError) as error: errors.append(str(error))
    for plan in presentation.get('composition_plans',[]):
        try:
            inputs,output=signature(plan['tree'])
            if inputs!=plan['ordered_inputs'] or output!=plan['output']: errors.append('composition plan signature mismatch')
        except (KeyError,ValueError) as error: errors.append(str(error))
    return errors


def validate():
    errors=[]
    files=sorted((ROOT/'dag/prompts').glob('*.yaml'))
    index=json.loads((ROOT/'dag/operads/index.json').read_text(encoding='utf-8'))
    indexed={row['node_id'] for row in index['nodes']}
    audit=json.loads((ROOT/'dag/pfp/prompt_audit.json').read_text(encoding='utf-8'))
    audited={row['node_id']:row for row in audit['nodes']}
    try:
        custody=Custody(ROOT)
    except (ValueError,KeyError,TypeError,OSError) as error:
        return {'prompts':len(files),'collections':len(indexed),'errors':['filename custody invalid: '+str(error)],'claim':'Custody failure; no mathematical acceptance.'}
    seen=set()
    for path in files:
        prompt=yaml.safe_load(path.read_bytes())
        node=prompt['node_id']
        if node in seen: errors.append(node+': duplicate node')
        seen.add(node)
        if prompt.get('default_stage')!='P0_MINE_OPERAD': errors.append(node+': entry stage')
        if prompt.get('authority_effect')!='None': errors.append(node+': authority')
        if REJECT.search(prompt['user_prompt']): errors.append(node+': legacy fabricated contract')
        if 'response_schema' in prompt or 'user_prompt_without_m3_ablation' in prompt: errors.append(node+': legacy answer schema')
        for key in ('workflow','mode','stage_contracts','operad_record'):
            target=(path.parent/prompt[key]).resolve()
            if not target.is_file() or ROOT not in target.parents:
                errors.append(node+': broken or escaping '+key)
        record=yaml.safe_load((path.parent/prompt['operad_record']).read_bytes())
        if record['node_id']!=node: errors.append(node+': wrong collection')
        if record['target']['source_statement'] not in prompt['user_prompt']: errors.append(node+': truncated target')
        if record['target']['statement_status']!='source_claim_to_scope_check_not_accepted_result': errors.append(node+': source status promoted')
        if record['collection_status']!='source_candidates_collected_semantic_mining_open': errors.append(node+': fabricated mining completion')
        for op in record['operation_candidates']:
            if not op.get('signature_excerpt') or not op.get('source_sha256') or op.get('status')!='source_candidate_requires_semantic_review':
                errors.append(node+': unsupported source candidate')
        errors.extend(node+': '+e for e in check_presentation(record['presentation']))
        for binding in record['source_bindings']:
            if binding['availability']=='local':
                p=ROOT/binding['path']
                if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=binding['sha256']:
                    errors.append(node+': local source pin changed '+binding['path'])
        for pin in record['target'].get('paper_source_pins',[]):
            if not custody.matches('paper',pin['path'],pin['sha256'],node):
                errors.append(node+': local paper source pin changed '+pin['path'])
        row=audited.get(node,{})
        if not custody.matches('prompt',path.relative_to(ROOT).as_posix(),row.get('after_sha256'),node): errors.append(node+': audit hash mismatch')
    if len(files)!=177 or seen!=indexed or seen!=set(audited): errors.append('corpus identity mismatch')
    try:
        custody.finish()
    except ValueError as error:
        errors.append(str(error))
    workflow=yaml.safe_load((ROOT/'dag/pfp/workflow.yaml').read_bytes())
    if workflow['entry_stage']!='P0_MINE_OPERAD': errors.append('workflow entry')
    if [s['id'] for s in workflow['stages']]!=['P0_MINE_OPERAD','P1_DERIVE','P2_VERIFY','P3_REPAIR','P4_CHALLENGE','P5_RECORD']:
        errors.append('stage sequence')
    if any('operad_delta' not in s['output'] for s in workflow['stages']): errors.append('missing per-stage collection')
    return {'prompts':len(files),'collections':len(indexed),'errors':errors,'claim':'Structural and local-source custody checks only; no operad or target theorem acceptance.'}


if __name__=='__main__':
    result=validate()
    print(json.dumps(result,indent=2))
    raise SystemExit(bool(result['errors']))
