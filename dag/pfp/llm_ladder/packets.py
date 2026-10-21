"""Compile a staged PFP prompt into a compact, typed OEPFP-style packet with a closed response schema.

AuthorityEffect: None.

The staged prompt (dag/prompts/*.yaml + dag/pfp/prepare_stage.py) is prose a human or a large model can
read. The compiled packet keeps only what the model needs to fill the P0 operad slots:
  @TARGET/@BOTTLENECK/@ASSUME  the public input (statement, bottleneck, declared assumptions);
  @SRC                         declarations the host already found, the ONLY ones citable as existing;
  @KNOWN+ / @KNOWN-            verified entries and host-refused entries of this node and its DAG neighbours;
  @FILL                        the typed slots to fill, enforced by a JSON schema (generators, relations,
                               compositions, lemmas, near_misses, numeric_claims, open_obligations).
This is the OEPFP idea "slot filling instead of free prose": the reply is short, typed and checkable.
Binding (task id, stage, attempt, input digest) follows prepare_stage.build_packet.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .llm_common import canonical_json, sha256_bytes
from .memory import (HallucinationIndex, dag_neighbours, dag_node, format_negative, format_positive, index_path,
                     positive_entries)
from .verify import DeclIndex

LOADER = getattr(yaml, 'CSafeLoader', yaml.SafeLoader)

_S = {'type': 'string'}
_REF = {'type': 'object', 'additionalProperties': False, 'required': ['path', 'decl', 'status'],
        'properties': {'path': _S, 'decl': _S, 'status': {'type': 'string', 'enum': ['existing', 'proposed_new', 'none']}}}


def _obj(required, properties):
    return {'type': 'object', 'additionalProperties': False, 'required': required, 'properties': properties}


P0_SCHEMA = _obj(
    ['status', 'generators', 'relations', 'compositions', 'lemmas', 'near_misses', 'numeric_claims', 'open_obligations'],
    {
        'status': {'type': 'string', 'enum': ['incomplete', 'ready_for_host_review']},
        'generators': {'type': 'array', 'items': _obj(
            ['id', 'inputs', 'output', 'arity', 'carrier', 'ref'],
            {'id': _S, 'inputs': {'type': 'array', 'items': _S}, 'output': _S, 'arity': {'type': 'integer'},
             'carrier': _S, 'ref': _REF})},
        'relations': {'type': 'array', 'items': _obj(
            ['id', 'statement', 'hypotheses', 'ref'],
            {'id': _S, 'statement': _S, 'hypotheses': _S, 'ref': _REF})},
        'compositions': {'type': 'array', 'items': _obj(
            ['outer', 'slot', 'inner', 'licensing_relation'],
            {'outer': _S, 'slot': {'type': 'integer'}, 'inner': _S, 'licensing_relation': _S})},
        'lemmas': {'type': 'array', 'items': _obj(
            ['id', 'statement', 'relation_to_target', 'depends_on', 'lean_skeleton', 'claims_proved', 'ref'],
            {'id': _S, 'statement': _S,
             'relation_to_target': {'type': 'string', 'enum': ['restates', 'implies', 'auxiliary', 'strengthens', 'weakens']},
             'depends_on': {'type': 'array', 'items': _S}, 'lean_skeleton': _S, 'claims_proved': {'type': 'boolean'},
             'ref': _REF})},
        'near_misses': {'type': 'array', 'items': _obj(
            ['id', 'claim', 'rejecting_invariant'], {'id': _S, 'claim': _S, 'rejecting_invariant': _S})},
        'numeric_claims': {'type': 'array', 'items': _obj(
            ['id', 'expr', 'value'], {'id': _S, 'expr': _S, 'value': _S})},
        'open_obligations': {'type': 'array', 'items': _S},
    })

SYSTEM_P0 = (
    'You mine operad entries for ONE finite quantum mechanics target. Reply with ONE JSON object that matches '
    'the response schema. No prose, no code fences.\n'
    'Rules:\n'
    '- Cite a declaration with status "existing" ONLY if it is listed under @SRC or @KNOWN+. Otherwise use '
    'status "proposed_new" (or "none") and leave path empty. Never invent a file path or a declaration name.\n'
    '- The host greps every existing citation, recomputes every numeric_claim exactly, and elaborates every '
    'Lean skeleton. Each refused claim is recorded against your model name.\n'
    '- Declarations marked [test] are checkers, not operations: cite them only inside a relation or lemma, never as a generator.\n'
    '- generator: a typed operation. inputs = ordered colour names, output = one colour, arity = len(inputs).\n'
    '- composition: plug generator `inner` into input slot `slot` (0-based) of generator `outer`. The inner output '
    'colour must equal that input colour and a relation you listed must license the step.\n'
    '- lemma: relation_to_target is restates|implies|auxiliary|strengthens|weakens. Do not change a number of '
    'the target. The Lean skeleton may use sorry; set claims_proved true only for a sorry-free proof.\n'
    '- numeric_claims: exact rational arithmetic only, e.g. expr "11 - 2/3*5", value "23/3".\n'
    '- Prefer 2-6 well-grounded entries per array over many guesses. Empty arrays are allowed. '
    'List what you could not ground in open_obligations. AuthorityEffect: None.'
)


@dataclass
class CompiledPacket:
    node_id: str
    stage: str
    attempt_id: str
    system: str
    user: str
    schema: dict
    input_sha256: str
    meta: dict = field(default_factory=dict)
    target_statement: str = ''

    def estimated_tokens(self) -> int:
        return estimate_tokens(self.system + self.user + json.dumps(self.schema))

    def as_request_json(self) -> dict:
        return {'schema_id': 'omega.pfp.finite-qm.ladder-packet.v1', 'task_id': self.node_id, 'stage_id': 'P0_MINE_OPERAD',
                'attempt_id': self.attempt_id, 'input_sha256': self.input_sha256, 'authority_effect': 'None',
                'system_prompt': self.system, 'user_prompt': self.user, 'response_schema': self.schema,
                'meta': self.meta, 'dispatch_status': 'prepared_by_llm_ladder'}


def estimate_tokens(text: str) -> int:
    return int(len(text.encode('utf-8')) / 3.5) + 1


STOP = {'the', 'and', 'for', 'with', 'that', 'this', 'from', 'into', 'are', 'not', 'its', 'rat', 'one', 'two', 'all',
        'any', 'has', 'have', 'than', 'when', 'which', 'does', 'state', 'record', 'records', 'value', 'values', 'identity',
        'identities', 'finite', 'rational', 'exact', 'map', 'research', 'file', 'report', 'source', 'theorem', 'lemma',
        'def', 'nf', 'nc', 'at', 'of', 'in', 'to', 'by', 'is', 'as', 'on', 'or', 'an', 'no', 'it', 'be'}


def _tokens(text: str) -> set:
    parts = re.findall(r'[A-Za-z][a-z]+|[A-Z]+(?![a-z])|\d+', re.sub(r'([a-z])([A-Z])', r'\1 \2', text or ''))
    return {p.lower() for p in parts if len(p) > 2 and not p.isdigit() and p.lower() not in STOP}


def load_row(root, node_id):
    rows = json.loads((Path(root) / 'dag/operads/index.json').read_bytes().decode('utf-8'))['nodes']
    for position, row in enumerate(rows):
        if row['node_id'] == node_id:
            return position, row
    raise KeyError('node %s is not in dag/operads/index.json' % node_id)


def source_candidates(root, node_id, collection, index: DeclIndex, statement: str, limit: int):
    """[(score, path, decl dict)] best first: operad-record leads, names quoted in the statement, the node's own
    anchors, then declarations of source files whose file name shares words with the statement."""
    chosen: dict = {}

    def offer(score, path, decl):
        key = (path, decl['full'])
        if key not in chosen or chosen[key][0] < score:
            chosen[key] = (score, path, decl)

    for item in (collection.get('operation_candidates') or []) + (collection.get('relation_candidates') or []):
        path = item.get('source')
        entry = index.file_entry(path) if path else None
        if entry:
            for decl in index.match_in_table(entry['table'], item['name']):
                offer(100, path, decl)
    node = dag_node(root, node_id) or {}
    statement_tokens = _tokens(statement)
    for name in set(re.findall(r'[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+|[a-z]+[A-Z][A-Za-z0-9]*', statement)):
        for path, decl in index.find_anywhere(name):
            if decl['full'].split('.')[-1] == name:
                offer(90, path, decl)
    anchors = [a for a in (node.get('lean') or []) + (node.get('rust') or []) if a]
    for anchor in anchors:
        entry = index.file_entry(anchor)
        if entry:
            for decl in entry['table']:
                overlap = len(_tokens(decl['full']) & statement_tokens)
                if overlap >= 2:
                    offer(40 + overlap, anchor, decl)
    if len(chosen) < limit:
        by_file = []
        for path in index.source_paths():
            stem_tokens = _tokens(Path(path).stem)
            overlap = len(stem_tokens & statement_tokens)
            is_test = '/tests/' in path or Path(path).name.startswith('test_')
            if overlap >= (3 if is_test else 2) and path not in anchors:
                by_file.append((overlap - (1 if is_test else 0), path))
        for overlap, path in sorted(by_file, reverse=True)[:6]:
            entry = index.file_entry(path)
            for decl in (entry['table'] if entry else []):
                hit = len(_tokens(decl['full']) & statement_tokens)
                if hit >= 1:
                    offer(10 + overlap + hit, path, decl)
    ranked = sorted(chosen.values(), key=lambda row: (-row[0], row[1], row[2]['line']))
    return ranked[:limit]


def compile_p0(root, node_id, *, attempt_id, policy, index: DeclIndex | None = None, feedback=True,
               hallucinations: HallucinationIndex | None = None) -> CompiledPacket:
    root = Path(root)
    index = index or DeclIndex(root)
    position, row = load_row(root, node_id)
    collection = yaml.load((root / row['operad_collection']).read_bytes(), Loader=LOADER)
    target = collection['target']
    statement = target['source_statement']
    status = (dag_node(root, node_id) or {}).get('status', target.get('source_claim_label', '?'))
    assumptions = target.get('declared_assumptions') or []
    neighbours = dag_neighbours(root, node_id)
    related = [node_id] + neighbours
    candidates = source_candidates(root, node_id, collection, index, statement, policy['max_source_candidates'])
    hall = hallucinations or HallucinationIndex(index_path(root))
    negatives, positives = [], []
    if feedback:
        hints = {p + '::' + d['full'] for _, p, d in candidates} | {d['full'] for _, _, d in candidates}
        negatives = hall.relevant(related, hints, limit=policy['max_neg_lines'],
                                  still_absent=lambda key: not index.find_anywhere(key))
        positives = positive_entries(root, related, limit=policy['max_pos_lines'])
    lines = []
    src_lines = []
    for rank, (score, path, decl) in enumerate(candidates):
        is_test = '/tests/' in path or Path(path).name.startswith('test_') or decl['name'].startswith('test_')
        text = '%s | %s | %s%s' % (path, decl['full'], decl['kind'], ' [test]' if is_test else '')
        if rank < 8:
            signature = re.sub(r'\s+', ' ', index.statement(path, decl))[:150]
            text += ' | ' + signature
        src_lines.append(' ' + text)
    public = {'task_id': node_id, 'stage': 'P0', 'attempt_id': attempt_id, 'statement': statement,
              'bottleneck': target.get('source_bottleneck', ''), 'assumptions': assumptions,
              'src': [l.strip() for l in src_lines], 'known_neg': [format_negative(e) for e in negatives],
              'known_pos': [format_positive(r) for r in positives]}
    digest = sha256_bytes(canonical_json(public))
    lines.append('@PFP/1 task=%s stage=P0 attempt=%s in=%s guided=%s' % (node_id, attempt_id, digest[:8], 'yes' if feedback else 'no'))
    lines.append('@TARGET [%s] %s' % (status, re.sub(r'\s+', ' ', statement).strip()))
    if public['bottleneck']:
        lines.append('@BOTTLENECK ' + re.sub(r'\s+', ' ', public['bottleneck']).strip())
    lines.append('@ASSUME ' + ('; '.join(assumptions) if assumptions else 'none declared'))
    lines.append('@SRC path | decl | kind (copy path and decl into ref.path and ref.decl; cite as existing only from here)' if src_lines else '@SRC none found by the host; cite nothing as existing')
    lines += src_lines
    if public['known_pos']:
        lines.append('@KNOWN+ (host-verified earlier; reusable inside their scope)')
        lines += [' ' + x for x in public['known_pos']]
    if public['known_neg']:
        lines.append('@KNOWN- (host-refused earlier; do not repeat)')
        lines += [' ' + x for x in public['known_neg']]
    lines.append('@FILL generators relations compositions lemmas near_misses numeric_claims open_obligations status')
    meta = {'src_offered': len(src_lines), 'known_neg_injected': len(negatives), 'known_pos_injected': len(positives),
            'neighbours': neighbours[:12], 'feedback': feedback, 'index_position': position,
            'neg_entry_ids': [e['id'] for e in negatives]}
    return CompiledPacket(node_id, 'P0', attempt_id, SYSTEM_P0, '\n'.join(lines) + '\n', P0_SCHEMA, digest, meta, statement)


def staged_baseline_tokens(root, node_id) -> int | None:
    """Token estimate of the packet the file-only prepare_stage helper produces for the same node (for comparison)."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location('pfp_prepare_stage', Path(root) / 'dag/pfp/prepare_stage.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _, row = load_row(root, node_id)
        packet = module.build_packet(Path(root) / row['prompt'], 'P0_MINE_OPERAD', attempt_id='baseline')
        text = json.dumps({k: packet[k] for k in ('system_prompt', 'user_prompt', 'public_context', 'response_contract')})
        return estimate_tokens(text)
    except Exception:  # baseline is informational only
        return None
