"""Build specs/L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_phase_blind_fiber.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE'
H = 'Amplitudes are Gaussian integers; the mix is the unnormalized two-sector Hadamard (a+b, a-b); unit phases are the declared assumption.'


def spec():
    boundary = {
        'supports': 'For Gaussian-integer sector amplitudes a, b, both nonzero, the phase-blind weights (|a|^2, |b|^2) do not determine the unnormalized Hadamard readout (|a+b|^2, |a-b|^2) (kernel-checked for every such pair, not only for the (1,1)/(1,-1) witnesses); mixing always doubles the total weight; the readout difference is 4 Re(a conj b); a zero first sector (a = 0, by w_eq_zero the fiber of weight 0 is the single point 0) or a zero second sector forces the readout to depend on the other weight only, so it descends (descends_when_zero_sector, descends_when_second_zero). Exact fiber and readout tables for ten weight pairs, including the unrealizable weight 3 (for which descends=true is vacuous: both fibers empty).',
        'does_not_support': 'Complex-Hilbert amplitudes beyond Z[i]; normalized or projective states; more than two sectors; mixes other than the unnormalized 2x2 Hadamard; the embedding of Z[i] into C (non-descent on the Gaussian-lattice fibers gives non-descent on the full complex phase fibers only after that embedding is formalised); the identification of the module readout with the source declarations phaseBlind/mix/readout over Vec GaussInt Bool (H008/H010), which is a modelling identification, not a checked one; any measurement, branch or physical interpretation of the phase fiber.',
        'narrowest_claim': 'Over Z[i] with the unnormalized two-sector Hadamard readout: both sector amplitudes nonzero implies the weight pair does not determine the readout; a zero first or zero second sector implies it does.',
        'next_test': 'Decide non-descent of the normalized projective readout w(a+b)/(2(w(a)+w(b))) for n>=3 complex sectors under a unitary mix other than the 2x2 Hadamard, by exhibiting a fiber pair with different readouts or a descending fiber.'}
    generators = [
        {'id': 'phase_blind_weight', 'source_declarations': ['lean4/H008PhaseBlindPresentation.lean::phaseBlind (line 18), weight_nonneg (line 23)'], 'ordered_inputs': ['GaussianAmplitude'], 'output': 'Weight', 'semantic_predicate': 'w(z)=re^2+im^2; invariant under multiplication by the units {1,i,-1,-i}.', 'hypotheses': [H]},
        {'id': 'phase_fiber', 'source_declarations': ['lean4/H008PhaseBlindPresentation.lean::psi1, psi2 (lines 37-40) are two points of one fiber; the general fiber is not declared in the source'], 'ordered_inputs': ['Weight'], 'output': 'GaussianAmplitudeSet', 'semantic_predicate': 'All Gaussian integers of a given weight (the phase fiber); empty when the weight is not a sum of two squares, a single point at weight 0.', 'hypotheses': [H]},
        {'id': 'hadamard_readout', 'source_declarations': ['lean4/H010InterferenceNonDescent.lean::mix (line 20), readout (line 25)'], 'ordered_inputs': ['GaussianAmplitude', 'GaussianAmplitude'], 'output': 'ReadoutPair', 'semantic_predicate': 'Unnormalized mix readout (w(a+b), w(a-b)).', 'hypotheses': [H]},
        {'id': 'readout_total', 'source_declarations': ['lean4/H008PhaseBlindPresentation.lean::totalWeight (line 21)'], 'ordered_inputs': ['ReadoutPair'], 'output': 'Weight', 'semantic_predicate': 'Sum of the two readout components.', 'hypotheses': [H]}]
    relations = [
        {'id': 'weight_unit_invariance', 'source_declarations': ['lean4/H008PhaseBlindPresentation.lean::global_phase_blind (source is general over Vec; this node proves the pair case again for the Z[i] pair carrier)'], 'equation_or_predicate': 'w(i*z)=w(z)=w(-z)', 'typing_conditions': 'GaussianAmplitude', 'evidence_status': 'Kernel theorem w_I_mul, w_neg', 'scope': 'All Gaussian integers'},
        {'id': 'readout_total_doubling', 'source_declarations': ['lean4/H010InterferenceNonDescent.lean::mix_doubles_total (fixed witnesses psi1, psi2 only)'], 'equation_or_predicate': 'sum(readout(a,b)) = 2(w(a)+w(b))', 'typing_conditions': 'GaussianAmplitude x GaussianAmplitude', 'evidence_status': 'Kernel theorem readout_total; native table', 'scope': 'All Gaussian integers'},
        {'id': 'interference_term', 'source_declarations': ['no source declaration; new general identity'], 'equation_or_predicate': 'readout(a,b).1 - readout(a,b).2 = 4 Re(a conj b)', 'typing_conditions': 'GaussianAmplitude x GaussianAmplitude', 'evidence_status': 'Kernel theorem readout_interference; native table', 'scope': 'All Gaussian integers'},
        {'id': 'nonzero_sectors_nondescent', 'source_declarations': ['lean4/H010InterferenceNonDescent.lean::no_descent_through_fiber (fixed witnesses psi1, psi2: an instance, not the general statement)'], 'equation_or_predicate': 'a!=0 and b!=0 imply no f with readout(x,y)=f(w x,w y) on fiber(w a) x fiber(w b)', 'typing_conditions': 'Weight x Weight with realizable fibers', 'evidence_status': 'Kernel theorem no_descent via fiber_changes_readout; native table', 'scope': 'All nonzero Gaussian pairs'},
        {'id': 'zero_sector_descent', 'source_declarations': ['no source declaration; new boundary theorem'], 'equation_or_predicate': 'w(a)=0 implies the readout is a function of the weights', 'typing_conditions': 'Weight 0 fiber is {0}', 'evidence_status': 'Kernel theorem descends_when_zero_sector; native table', 'scope': 'All Gaussian b'}]
    compositions = [
        {'outer_operation': 'readout_total', 'input_slot': 0, 'inner_operation': 'hadamard_readout', 'colour_match': 'ReadoutPair', 'hypothesis_match': H,
         'licensing_relations': ['readout_total_doubling'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'hadamard_readout', 'input_slot': 0, 'inner_operation': 'phase_fiber', 'colour_match': 'GaussianAmplitudeSet element -> GaussianAmplitude',
         'hypothesis_match': 'Fiber element chosen explicitly; selection is not an operation of the quotient.', 'licensing_relations': ['nonzero_sectors_nondescent'], 'evidence_status': 'Kernel and native'}]
    failed = [{'composition': 'hadamard_readout factored through (phase_blind_weight, phase_blind_weight)', 'reason': 'No such factorization exists when both sectors are nonzero (kernel no_descent); it exists when a sector is zero.'}]
    counterexamples = [{'id': 'psi1_psi2_witness', 'statement': 'amplitudes (1,1) and (1,-1) share weights (1,1) but read out (4,0) and (0,4).', 'scope': 'Instance of no_descent with a=b=1.'}]
    return build_spec(
        node=NODE, short='phase_blind_fiber', lean='PhaseBlindFiber',
        anchors=['PhaseBlindFiber.w_I_mul', 'PhaseBlindFiber.readout_total', 'PhaseBlindFiber.readout_interference',
                 'PhaseBlindFiber.fiber_changes_readout', 'PhaseBlindFiber.w_eq_zero', 'PhaseBlindFiber.descends_when_second_zero', 'PhaseBlindFiber.no_descent', 'PhaseBlindFiber.descends_when_zero_sector',
                 'PhaseBlindFiber.witness_readouts', 'PhaseBlindFiber.phase_blind_fiber_interference'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('The source declares only two witnesses (psi1, psi2) and a Bool-indexed readout; the claim "the phase fiber over a weight vector is nontrivial" and "mixing separates fibers" is general. '
                      'Mine the actual declarations phaseBlind, mix, readout, no_descent_through_fiber, then prove the general Z[i] statements and compute fibers by exact enumeration. '
                      'The weight vector must have both entries positive and realizable (sum of two squares) for the fiber to be nontrivial; the zero-weight sector is the exact boundary where descent holds.'),
        predicates=['Independent brute-force Gaussian fiber enumeration over the integer box.',
                    'Closed-form readout (W+2c, W-2c) with c=Re(a conj b), not the literal addition used by the producer.',
                    'Descent flag equals (distinct readouts <= 1), and every realizable pair with both weights positive is flagged non-descending.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['Normalized and projective readouts on complex amplitudes.', 'More than two sectors and mixes other than the 2x2 Hadamard.',
                          'Any physical or branch interpretation of the phase fiber.'],
        colour_meanings={'GaussianAmplitude': 'Gaussian integer amplitude (re, im)', 'Weight': 'Nonnegative integer phase-blind weight',
                         'GaussianAmplitudeSet': 'Finite phase fiber of one weight', 'ReadoutPair': 'Pair (w(a+b), w(a-b))'},
        depends_on_result=True,
        qualification='Scope is the Z[i] two-sector unnormalized Hadamard readout; the source witnesses are instances, and the normalized/projective and complex-Hilbert versions are not established.',
        challenge_plan='Coordinate mutants of every certificate leaf plus seven semantic near misses: real-sign fiber, unit-orbit fiber (with its true readouts), zero first or second sector treated as generic, unrealizable weight accepted, total not doubled, equal weights imply equal readout.',
        composition_tree=['readout_total(hadamard_readout(a,b))', 'hadamard_readout(phase_fiber(w0)[i], phase_fiber(w1)[j])'],
        construction='Exact integer fibers and readouts for ten weight pairs; Lean proves the general Z[i] statements.',
        relation_evidence={'weight_unit_invariance': 'Kernel theorem; native fibers closed under units.', 'nonzero_sectors_nondescent': 'Kernel theorem for every nonzero pair; native tables for 7 realizable pairs.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
