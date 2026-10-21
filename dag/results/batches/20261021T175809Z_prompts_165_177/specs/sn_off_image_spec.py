"""Build specs/PG-SN-OFF-IMAGE-REFUSAL.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_sn_off_image.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-SN-OFF-IMAGE-REFUSAL'
H = 'A section s : S -> Y and a retraction r : Y -> S + {refusal} with r(s x) = inl x (old-image law) and soundness (r y = inl x implies s x = y); or the pinned S(n) model with its five base shapes over an abstract glyph alphabet.'
OFF = 'omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean'
SC = 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnCarrier.lean'
DW = 'omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs'


def spec():
    boundary = {
        'supports': ('Kernel-checked, for every glyph alphabet and every stage: in the transcription of the pinned SnCarrier definitions (glyph alphabet abstracted, one-field wrappers flattened; restated, not imported) every accepted outcome of r_n is a section image with the base presentation as payload (accepted_only_from_section, accepted_iff), r_n refuses exactly the presentations that are no section image at that stage (nonDescent_iff_off_image), a section image at another stage is refused (retraction_stage_strict), sectionLift is injective (sectionLift_injective), and the image test is decided by the outcome (inImage_iff); the restated pair (sectionLift n, retrB n), with the outcome read as Base + Unit, is a SectionRetraction of the abstract part (sn_is_section_retraction), so refusal is exactly the absence of a base presentation lifting to p (sn_refused_iff_off_image); in the abstract setting of a section s and a retraction r with the old-image law and soundness, r refuses exactly off the image of s, the round trip s(r y) = y fails exactly off the image (refused_iff_off_image, roundtrip_fails_off_image), and the soundness hypothesis cannot be dropped (abstract instance on Fin 1 -> Fin 2; for S(n), laxRetr obeys the law and never refuses for every alphabet, and lax_breaks_refusal_characterisation is an instance on Bool glyphs at stage 0). refuseOffImage constructs a sound refusing retraction by testing the round trip (refuseOffImage_isSectionRetraction, toy_refused_iff_odd), so refusal-iff-off-image is circular by construction there and is not evidence for the S(n) statement. All S(n) re-proofs report propext only. '
                     'Native: on eight explicit universes of presentations (up to 866 elements) the pinned lift and retraction are executed: refusal equals off-image with zero violations, payloads are correct, the round trip holds on exactly the image and fails on exactly the refused points, other-stage lifts and over-long bodies are refused, and the lax retraction recovers every base presentation (lax_law_holds) while refusing nothing (lax_refused = 0; both columns are by-construction consequences, the Lean file carries the statement); plus five toy sections x -> c x with exact on-image and refused counts.'),
        'does_not_support': ('The claim that this closes the domain-restriction half of ledger row WDP-P001-019 (a ledger interpretation, not examined); the external prompt file fable_theorems_2026-10-17/05_sn_off_image_refusal.md named in the DAG source list, which was not read; off-image refusal for sections other than the five base shapes (nested lift, retraction or refusal terms as base members are outside the model); any cardinality claim about Carrier n or the declared table (node PG-SN-CARRIER); unrestricted old-image recovery (ledger row WDP-P001-019 stays a negative boundary for the unrestricted interface); the 36-glyph source alphabet beyond the generic statement, and alphabets above three glyphs in the native universes; wire parsing of the source grammar; decidability beyond this syntactic model (the source itself says the image condition is not a general computability theorem); the circular reading in which off-image is defined as failure of the round trip; any physical interpretation.'),
        'narrowest_claim': 'For a restatement over an arbitrary glyph alphabet of the pinned S(n) section and retraction (five base shapes at a given stage), the retraction refuses exactly the presentations that are not section images at that stage, and the restated pair is a section/retraction pair (law and soundness) in the abstract sense, where refusal is the failure of the round trip s(r(p)) = p; this rests on the soundness of the specific retraction (accepted_only_from_section), because the old-image law alone is satisfied by a retraction that refuses nothing.',
        'next_test': 'With the bridge sn_is_section_retraction proved, extend the refusal characterisation to a grammar that admits nested lift, retraction and refusal terms as base members: add them to Base, restate sectionLift and retr on the enlarged type, and decide whether accepted_only_from_section and sectionLift injectivity still hold or whether a new off-image class appears.'}
    generators = [
        {'id': 'section_lift', 'source_declarations': [SC + '::sectionLift (line 70), a definition (restricted to BasePresentation); ' + OFF + ' uses it throughout'],
         'ordered_inputs': ['Stage', 'BasePresentation'], 'output': 'Presentation', 'semantic_predicate': 'u_N on the five base shapes.', 'hypotheses': [H]},
        {'id': 'retraction_down_map', 'source_declarations': [SC + '::retractionDownMap (line 90), RetractOutcome (line 84)'],
         'ordered_inputs': ['Stage', 'Presentation'], 'output': 'RetractOutcome', 'semantic_predicate': 'r_N: accept a stage-N lift of one of the five shapes, otherwise NON_DESCENT.', 'hypotheses': [H]},
        {'id': 'image_test', 'source_declarations': [OFF + '::inImage (line 186) and inImage_iff (line 191): a Bool test read off the outcome, proved equivalent to membership in the section image'],
         'ordered_inputs': ['Stage', 'Presentation'], 'output': 'Bool', 'semantic_predicate': 'true iff the retraction accepts.', 'hypotheses': [H]},
        {'id': 'roundtrip_refusal', 'source_declarations': [DW + '::verify_sn_off_image_refusal_witness (line 64): a toy section 2x with r(y) = y / 2 on {0..5}, where off-image is DEFINED as failure of s(r(y)) = y'],
         'ordered_inputs': ['Point'], 'output': 'AcceptedOrRefused', 'semantic_predicate': 'inl(r0 y) when s(r0 y) = y, else refusal; sound by construction.', 'hypotheses': [H]}]
    relations = [
        {'id': 'accepted_only_from_section', 'source_declarations': [OFF + '::accepted_only_from_section (line 75): general over p, q and every stage for the pinned 36-glyph model'],
         'equation_or_predicate': 'retr_n(p) = accepted q implies p = sectionLift_n(b) and q = b for some base b', 'typing_conditions': 'Stage x Presentation',
         'evidence_status': 'Kernel theorems accepted_only_from_section, accepted_iff for every alphabet; native accepted = image with correct payload', 'scope': 'Every alphabet and stage'},
        {'id': 'nonDescent_iff_off_image', 'source_declarations': [OFF + '::nonDescent_iff_off_image (line 127): general for the pinned model'],
         'equation_or_predicate': 'retr_n(p) = NON_DESCENT iff p is no section image at stage n', 'typing_conditions': 'Stage x Presentation',
         'evidence_status': 'Kernel theorem nonDescent_iff_off_image for every alphabet; native iff_violations = 0 on eight universes', 'scope': 'Every alphabet and stage'},
        {'id': 'stage_strictness', 'source_declarations': [OFF + '::retraction_stage_strict (line 174)'],
         'equation_or_predicate': 'a section image at stage m is refused by r_n for m different from n', 'typing_conditions': 'Stage x Stage x BasePresentation',
         'evidence_status': 'Kernel theorem retraction_stage_strict; native stage_mismatch_refused = (S-1)|Base|', 'scope': 'Every alphabet'},
        {'id': 'sn_section_retraction_bridge', 'source_declarations': ['no source declaration; connects the abstract part to the restated SnOffImage.nonDescent_iff_off_image (line 127)'],
         'equation_or_predicate': '(sectionLift n, retrB n) is a SectionRetraction (law and soundness); hence retrB n p = refusal iff no base presentation lifts to p', 'typing_conditions': 'Stage x Presentation over an arbitrary alphabet',
         'evidence_status': 'Kernel theorems sn_is_section_retraction, sn_refused_iff_off_image, sectionLift_injective; native lift_collisions = 0', 'scope': 'Every alphabet and stage'},
        {'id': 'abstract_refusal', 'source_declarations': ['no source declaration; the abstract form of the roundtrip refusal named in the DAG statement (the source witness in ' + DW + ' is a fixed toy)'],
         'equation_or_predicate': 'law and soundness imply r y = refusal iff y is off the image and s(r y) = y fails exactly there', 'typing_conditions': 'Section and retraction on arbitrary types',
         'evidence_status': 'Kernel theorems refused_iff_off_image, roundtrip_fails_off_image, roundtrip_iff_in_image, SectionRetraction.injective; native toy counts', 'scope': 'All types'},
        {'id': 'soundness_necessity', 'source_declarations': ['no source declaration; the old-image law (Paper001 old_image_injective) is silent off the image'],
         'equation_or_predicate': 'a lax retraction accepting every refused point as the ground presentation obeys the old-image law and refuses nothing', 'typing_conditions': 'S(n) model and Fin 1 -> Fin 2 instance',
         'evidence_status': 'Kernel theorems lax_obeys_law, lax_never_refuses, lax_breaks_refusal_characterisation, lax_retraction_obeys_law_but_accepts_off_image; native lax_iff_violations = refused', 'scope': 'S(n) over Bool glyphs (instance) and the lax construction for every alphabet'},
        {'id': 'roundtrip_construction', 'source_declarations': [DW + '::verify_sn_off_image_refusal_witness (line 64): a fixed toy instance'],
         'equation_or_predicate': 'any total left inverse r0 gives a sound refusing retraction y -> (inl r0 y if s(r0 y) = y else refusal)', 'typing_conditions': 'DecidableEq target',
         'evidence_status': 'Kernel theorems refuseOffImage_isSectionRetraction, toy_refused_iff_odd; native toy records. Circular by construction (refusal is the round-trip test), so not evidence for the S(n) statement', 'scope': 'All types with decidable equality'}]
    compositions = [
        {'outer_operation': 'image_test', 'input_slot': 1, 'inner_operation': 'section_lift', 'colour_match': 'Presentation', 'hypothesis_match': H + ' Same stage in both.',
         'licensing_relations': ['nonDescent_iff_off_image'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'retraction_down_map', 'input_slot': 1, 'inner_operation': 'section_lift', 'colour_match': 'Presentation', 'hypothesis_match': H,
         'licensing_relations': ['accepted_only_from_section'], 'evidence_status': 'Kernel and native'}]
    failed = [
        {'composition': 'retraction_down_map(m, section_lift(n, b)) with m different from n', 'reason': 'Refused: the stage test is exact (retraction_stage_strict); the composite is the refusal, not a recovery.'},
        {'composition': 'section_lift composed with the retraction as a map on all presentations', 'reason': 'Not a map: the refusal summand has no image under the section; it is defined only where r accepts, and then it is the identity (roundtrip_iff_in_image).'},
        {'composition': 'refusal read off the old-image law alone', 'reason': 'The lax retraction obeys the law and refuses nothing (lax_never_refuses); soundness of the specific retraction is what refuses.'}]
    counterexamples = [
        {'id': 'lax_retraction', 'statement': 'r(y) = inl 0 for all y on Fin 1 -> Fin 2 obeys the law but accepts the off-image point 1; the S(n) version accepts every refused point as the ground presentation.', 'scope': 'Instance and construction; kernel lax_retraction_obeys_law_but_accepts_off_image, lax_breaks_refusal_characterisation.'},
        {'id': 'three_glyph_body', 'statement': 'lift at stage 2 with the three-glyph body (true, false, true) is refused by r_2 although it has the right stage and the lift head.', 'scope': 'Instance over Bool glyphs; kernel instance_refusals.'},
        {'id': 'circular_toy', 'statement': 'in the source toy witness off-image is defined as failure of s(r y) = y, so refusal by the round trip is true by definition there.', 'scope': 'Reading of the fixed witness in derivation_dag_witnesses.rs; the non-circular statement is nonDescent_iff_off_image.'}]
    return build_spec(
        node=NODE, short='sn_off_image', lean='SnOffImageRefusal',
        anchors=['SnOffImageRefusal.SectionRetraction.injective', 'SnOffImageRefusal.sn_is_section_retraction', 'SnOffImageRefusal.sn_refused_iff_off_image', 'SnOffImageRefusal.sectionLift_injective', 'SnOffImageRefusal.refused_iff_off_image', 'SnOffImageRefusal.roundtrip_iff_in_image',
                 'SnOffImageRefusal.roundtrip_fails_off_image', 'SnOffImageRefusal.refuseOffImage_isSectionRetraction', 'SnOffImageRefusal.toy_refused_iff_odd',
                 'SnOffImageRefusal.lax_retraction_obeys_law_but_accepts_off_image', 'SnOffImageRefusal.old_image_base', 'SnOffImageRefusal.accepted_only_from_section',
                 'SnOffImageRefusal.accepted_iff', 'SnOffImageRefusal.nonDescent_iff_off_image', 'SnOffImageRefusal.retraction_stage_strict',
                 'SnOffImageRefusal.inImage_iff', 'SnOffImageRefusal.lax_breaks_refusal_characterisation', 'SnOffImageRefusal.instance_refusals'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('No operation candidate was recovered, so the declarations were mined by hand from SnOffImage.lean (sha256 746372dc..., matches the pin) and SnCarrier.lean: accepted_only_from_section (line 75), nonDescent_iff_off_image (line 127), sectionLift_injective (line 151), retraction_stage_strict (line 174), inImage_iff (line 191). They are general theorems for the pinned 36-glyph model, not vacuous; the compiled file reports propext and Quot.sound for several of them although its docstring says "stays within propext" (a minor docstring overclaim; this node re-proves them for every alphabet with propext only). '
                      'The external prompt file named in the collection (prompts/fable_theorems_2026-10-17/05_sn_off_image_refusal.md) is not present in the checked-out source repository and was not read. The Rust witness verify_sn_off_image_refusal_witness is a fixed toy (section 2x, retraction y / 2 on {0..5}) that defines off-image as failure of the round trip; it does not exercise the S(n) syntax, so it gives refusal by definition. '
                      'This node proves the non-circular statement (refusal iff no section image, using the soundness of the specific retraction), shows that the old-image law alone does not give refusal, and executes the pinned functions on explicit universes.'),
        predicates=['Presentations as wire strings and the retraction as a regular-expression parser; the round trip tested literally by re-lifting the parsed result and comparing strings.',
                    'Image set built independently from the base wires; refusal/off-image disagreement counted over the whole universe of lifts and retractions with glyph-word, arrow and pair bodies (not all presentations); payload compared with the base wire; lift collisions recounted.',
                    'Toy sections by direct divisibility (refused iff c does not divide y) with law and soundness failures recomputed through divmod, not through the producer round trip. The lax columns (lax_law_holds, lax_refused) are by-construction consequences recomputed by running the lax parser.',
                    'Theorem-level consistency: no violations, accepted = image = round trips, round trips fail exactly on refused points, lax recovers every base presentation and refuses nothing, no lift collisions.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['Nested lift, retraction and refusal terms as base members.', 'A corrected cardinality theorem for the carriers (PG-SN-CARRIER).', 'Wire parser correspondence for the source grammar.',
                          'A general decidability statement for the image condition beyond this syntactic model.'],
        colour_meanings={'Stage': 'Natural-number stage index', 'BasePresentation': 'One of the five base shapes', 'Presentation': 'Element of the full presentation grammar',
                         'RetractOutcome': 'accepted presentation or NON_DESCENT', 'Bool': 'Image test result', 'Point': 'Point of the target set of a section', 'AcceptedOrRefused': 'Element of S + {refusal}'},
        depends_on_result=True,
        qualification='Off-image refusal holds for the pinned retraction because of its soundness (accepted only from section images), not because of the old-image law; the source Rust witness defines off-image by the round trip and so does not support the statement by itself.',
        challenge_plan='Coordinate mutants of every certificate leaf plus thirteen semantic near misses: law implies refusal, an exception to the characterisation, wrong-stage lift accepted, long body accepted, round trip everywhere, single-stage universe, lax retraction breaking the law, wrong payload, accepted beyond the image, non-injective section lift, zero-multiplier toy, toy retraction accepting everything, identity section with off-image points.',
        composition_tree=['image_test(n, section_lift(n, b))', 'retraction_down_map(n, section_lift(n, b))'],
        construction='Explicit universes of presentations with the pinned lift and retraction executed, plus toy sections; Lean proves the characterisation for every alphabet and in the abstract.',
        relation_evidence={'nonDescent_iff_off_image': 'Kernel theorem; native zero violations on eight universes.', 'soundness_necessity': 'Kernel lax theorems; native lax_iff_violations equals the refused count.',
                           'roundtrip_construction': 'Kernel refuseOffImage_isSectionRetraction; native toy counts k and (c-1)k.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
