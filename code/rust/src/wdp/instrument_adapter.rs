
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::{involution, matrix as mx};
use num_bigint::BigInt;
use num_traits::{Signed, ToPrimitive, Zero};
use tfqm_number_theory::cyclotomic::GaussianRat;
use tfqm_number_theory::rational::{ri, Rational};
use omega_quantum_physics::exact_channel::ExactKrausChannel;
use omega_quantum_physics::exact_hermitian::hermitian_trace;
use serde::Serialize;

use crate::empirical_adapter::{adapt_exact, EmpiricalModel, MeasurementCover, RunTable, Section};
use crate::error::WdpError;
use crate::types::{blake3_digest, AuthorityEffect};

pub const MAX_RUNS: usize = 1_000_000;

fn invalid(detail: String) -> WdpError {
    WdpError::InvalidInput { detail }
}

pub fn qubit_matrix(rows: [[GaussianRat; 2]; 2]) -> BasicMatrix<GaussianRat> {
    BasicMatrix::<GaussianRat>::from_row_major(2, 2, rows.into_iter().flatten().collect())
        .expect("two declared rows of two entries")
}

fn norm_of(v: &[GaussianRat]) -> Rational {
    v.iter().fold(Rational::zero(), |acc, x| acc + x.norm_sq())
}

#[derive(Debug, Clone)]
pub struct QubitState {
    components: Vec<(Rational, [GaussianRat; 2])>,
}

impl QubitState {
    pub fn new(components: Vec<(Rational, [GaussianRat; 2])>) -> Result<Self, WdpError> {
        if components.is_empty() {
            return Err(invalid("a state needs at least one component".to_string()));
        }
        if let Some(j) = components.iter().position(|(w, _)| w.is_negative()) {
            return Err(invalid(format!("mixture weight {j} is negative")));
        }
        let trace = components
            .iter()
            .fold(Rational::zero(), |acc, (w, v)| acc + w * norm_of(v));
        if trace != ri(1) {
            return Err(invalid(format!("mixture has trace {trace}, not 1")));
        }
        Ok(Self { components })
    }

    pub fn pure(v: [GaussianRat; 2]) -> Result<Self, WdpError> {
        Self::new(vec![(ri(1), v)])
    }

    pub fn components(&self) -> &[(Rational, [GaussianRat; 2])] {
        &self.components
    }

    pub fn density_matrix(&self) -> Result<BasicMatrix<GaussianRat>, WdpError> {
        self.components
            .iter()
            .try_fold(mx::zeros(2, 2)?, |acc, (w, v)| {
                Ok(mx::add(
                    &acc,
                    &mx::scale(
                        &involution::outer_product(v, v)?,
                        &GaussianRat::from_rational(w.clone()),
                    )?,
                )?)
            })
    }

    pub fn trace(&self) -> Result<Rational, WdpError> {
        Ok(hermitian_trace(&self.density_matrix()?)?)
    }

    pub fn same_density(&self, other: &QubitState) -> Result<bool, WdpError> {
        Ok(self.density_matrix()? == other.density_matrix()?)
    }

    pub fn canonical_string(&self) -> Result<String, WdpError> {
        let rho = self.density_matrix()?;
        let entries: Vec<String> = rho
            .as_slice()
            .iter()
            .enumerate()
            .map(|(i, x)| format!("({},{})={}+{}i", i / 2, i % 2, x.re, x.im))
            .collect();
        Ok(format!("qubit-density-2x2;{}", entries.join(";")))
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct InstrumentReceipt {
    pub outcome: usize,
    pub probability: Rational,
    pub post_state_digest: Option<String>,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OutcomeRunTable {
    pub cover: MeasurementCover,
    pub table: RunTable,
    pub runs: usize,
}

#[derive(Debug, Clone)]
pub struct QubitInstrument {
    channel: ExactKrausChannel,
}

impl QubitInstrument {
    pub fn new(operators: Vec<BasicMatrix<GaussianRat>>, label: &str) -> Result<Self, WdpError> {
        let channel = ExactKrausChannel::try_new(2, 2, operators, label)?;
        Ok(Self { channel })
    }

    pub fn outcomes(&self) -> usize {
        self.channel.operators().len()
    }

    pub fn operators(&self) -> &[BasicMatrix<GaussianRat>] {
        self.channel.operators()
    }

    pub fn channel(&self) -> &ExactKrausChannel {
        &self.channel
    }

    pub fn povm_effects(&self) -> Result<Vec<BasicMatrix<GaussianRat>>, WdpError> {
        self.operators()
            .iter()
            .map(|k| Ok(mx::multiply(&involution::adjoint(k)?, k)?))
            .collect()
    }

    fn operator(&self, outcome: usize) -> Result<&BasicMatrix<GaussianRat>, WdpError> {
        self.operators()
            .get(outcome)
            .ok_or_else(|| invalid(format!("outcome {outcome} outside 0..{}", self.outcomes())))
    }

    pub fn outcome_probability(
        &self,
        outcome: usize,
        state: &QubitState,
    ) -> Result<Rational, WdpError> {
        let k = self.operator(outcome)?;
        state
            .components()
            .iter()
            .try_fold(Rational::zero(), |acc, (w, v)| {
                let image = mx::multiply_vector(k, v)?;
                Ok(acc + w * norm_of(&image))
            })
    }

    pub fn outcome_probability_trace_formula(
        &self,
        outcome: usize,
        state: &QubitState,
    ) -> Result<Rational, WdpError> {
        let k = self.operator(outcome)?;
        let effect = mx::multiply(&involution::adjoint(k)?, k)?;
        let trace = mx::trace(&mx::multiply(&effect, &state.density_matrix()?)?)?;
        if !trace.im.is_zero() {
            return Err(invalid(format!(
                "tr(E rho) = {}+{}i is not real",
                trace.re, trace.im
            )));
        }
        Ok(trace.re)
    }

    pub fn outcome_probabilities(&self, state: &QubitState) -> Result<Vec<Rational>, WdpError> {
        (0..self.outcomes())
            .map(|o| self.outcome_probability(o, state))
            .collect()
    }

    pub fn post_state(
        &self,
        outcome: usize,
        state: &QubitState,
    ) -> Result<Option<QubitState>, WdpError> {
        let p = self.outcome_probability(outcome, state)?;
        if p.is_zero() {
            return Ok(None);
        }
        let k = self.operator(outcome)?;
        let components = state
            .components()
            .iter()
            .map(|(w, v)| {
                let image = mx::multiply_vector(k, v)?;
                let vector: [GaussianRat; 2] = image
                    .try_into()
                    .map_err(|_| invalid("Kraus image is not a qubit vector".to_string()))?;
                Ok::<_, WdpError>((w / &p, vector))
            })
            .collect::<Result<Vec<_>, WdpError>>()?;
        QubitState::new(components).map(Some)
    }

    pub fn average_post_density(
        &self,
        state: &QubitState,
    ) -> Result<BasicMatrix<GaussianRat>, WdpError> {
        Ok(self.channel.apply(&state.density_matrix()?)?)
    }

    pub fn receipt(
        &self,
        outcome: usize,
        state: &QubitState,
    ) -> Result<InstrumentReceipt, WdpError> {
        let probability = self.outcome_probability(outcome, state)?;
        let post_state_digest = self
            .post_state(outcome, state)?
            .map(|post| post.canonical_string().map(|s| blake3_digest(s.as_bytes())))
            .transpose()?;
        Ok(InstrumentReceipt {
            outcome,
            probability,
            post_state_digest,
            authority_effect: AuthorityEffect::None,
        })
    }

    pub fn receipts(&self, state: &QubitState) -> Result<Vec<InstrumentReceipt>, WdpError> {
        (0..self.outcomes())
            .map(|o| self.receipt(o, state))
            .collect()
    }

    pub fn outcome_run_table(&self, state: &QubitState) -> Result<OutcomeRunTable, WdpError> {
        self.outcome_run_table_with_limit(state, MAX_RUNS)
    }

    pub fn outcome_run_table_with_limit(
        &self,
        state: &QubitState,
        max_runs: usize,
    ) -> Result<OutcomeRunTable, WdpError> {
        let probabilities = self.outcome_probabilities(state)?;
        let mut runs = BigInt::from(1);
        for p in &probabilities {
            let d = p.denom().clone();
            let (mut a, mut b) = (runs.clone(), d.clone());
            while !b.is_zero() {
                let r = &a % &b;
                a = b;
                b = r;
            }
            runs = &runs / &a * &d;
        }
        let n = runs
            .to_usize()
            .filter(|&n| n <= max_runs)
            .ok_or_else(|| invalid(format!("{runs} runs exceed the cap {max_runs}")))?;
        let mut outcome_runs: Vec<Section> = Vec::new();
        for (o, p) in probabilities.iter().enumerate() {
            let count = (p * Rational::from_integer(runs.clone()))
                .to_integer()
                .to_usize()
                .ok_or_else(|| invalid("run count does not fit in usize".to_string()))?;
            outcome_runs.extend(std::iter::repeat_n(vec![o], count));
        }
        let cover = MeasurementCover::new(1, self.outcomes(), vec![vec![0]])?;
        let table = RunTable::new(&cover, vec![outcome_runs])?;
        Ok(OutcomeRunTable {
            cover,
            table,
            runs: n,
        })
    }

    pub fn outcome_model(&self, state: &QubitState) -> Result<EmpiricalModel, WdpError> {
        let runs = self.outcome_run_table(state)?;
        Ok(adapt_exact(&runs.cover, &runs.table)?)
    }
}

pub fn luders_instrument() -> Result<QubitInstrument, WdpError> {
    let (zero, one) = (GaussianRat::zero(), GaussianRat::one());
    QubitInstrument::new(
        vec![
            qubit_matrix([[one.clone(), zero.clone()], [zero.clone(), zero.clone()]]),
            qubit_matrix([[zero.clone(), zero.clone()], [zero, one]]),
        ],
        "luders",
    )
}

pub fn non_projective_instrument() -> Result<QubitInstrument, WdpError> {
    non_projective_with_phase(GaussianRat::one(), "non_projective")
}

pub fn complex_phase_instrument() -> Result<QubitInstrument, WdpError> {
    non_projective_with_phase(GaussianRat::i(), "complex_phase")
}

fn non_projective_with_phase(phase: GaussianRat, label: &str) -> Result<QubitInstrument, WdpError> {
    let zero = GaussianRat::zero();
    let real = |n: i64, d: i64| GaussianRat::from_rational(Rational::new(n.into(), d.into()));
    QubitInstrument::new(
        vec![
            qubit_matrix([
                [GaussianRat::one(), zero.clone()],
                [zero.clone(), real(3, 5)],
            ]),
            qubit_matrix([[zero.clone(), zero.clone()], [zero, real(4, 5).mul(&phase)]]),
        ],
        label,
    )
}

pub fn measure_and_prepare_instrument(w: [GaussianRat; 2]) -> Result<QubitInstrument, WdpError> {
    if norm_of(&w) != ri(1) {
        return Err(invalid(format!(
            "the prepared vector has norm {}, not 1",
            norm_of(&w)
        )));
    }
    let zero = GaussianRat::zero();
    let [w0, w1] = w;
    QubitInstrument::new(
        vec![
            qubit_matrix([[w0.clone(), zero.clone()], [w1.clone(), zero.clone()]]),
            qubit_matrix([[zero.clone(), w0], [zero, w1]]),
        ],
        "measure_and_prepare",
    )
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct FiniteInstrumentReceipt {
    pub instrument_digest: String,
    pub input_state_digest: String,
    pub outcome: usize,
    pub probability: Rational,
    pub post_state_digest: Option<String>,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone)]
pub struct FiniteQuantumInstrument {
    instrument: omega_quantum_physics::exact_instrument::ExactFiniteInstrument,
}

fn finite_matrix_digest(matrix: &BasicMatrix<GaussianRat>) -> String {
    let mut encoding = format!("wdp-qi-matrix-v1;{}x{};", matrix.rows(), matrix.cols());
    for entry in matrix.as_slice() {
        encoding.push_str(&format!("{}+{}i;", entry.re, entry.im));
    }
    blake3_digest(encoding.as_bytes())
}

impl FiniteQuantumInstrument {
    pub fn new(
        dim_in: usize,
        dim_out: usize,
        groups: Vec<Vec<BasicMatrix<GaussianRat>>>,
        label: &str,
    ) -> Result<Self, omega_quantum_physics::exact_instrument::ExactInstrumentError> {
        Ok(Self {
            instrument: omega_quantum_physics::exact_instrument::ExactFiniteInstrument::try_new(
                dim_in, dim_out, groups, label,
            )?,
        })
    }

    pub fn instrument(&self) -> &omega_quantum_physics::exact_instrument::ExactFiniteInstrument {
        &self.instrument
    }

    pub fn canonical_digest(&self) -> String {
        let channel = self.instrument.channel();
        let mut encoding = format!(
            "wdp-finite-instrument-v1;{}x{};outcomes={};",
            channel.dim_out(),
            channel.dim_in(),
            self.instrument.outcomes(),
        );
        for outcome in 0..self.instrument.outcomes() {
            let operators = self
                .instrument
                .operators_for_outcome(outcome)
                .expect("validated outcome index");
            encoding.push_str(&format!("o={outcome};terms={};", operators.len()));
            for operator in operators {
                encoding.push_str(&finite_matrix_digest(operator));
                encoding.push(';');
            }
        }
        blake3_digest(encoding.as_bytes())
    }

    pub fn receipt(
        &self,
        outcome: usize,
        state: &omega_quantum_physics::exact_instrument::ExactDensityState,
    ) -> Result<
        FiniteInstrumentReceipt,
        omega_quantum_physics::exact_instrument::ExactInstrumentError,
    > {
        let probability = self.instrument.probability(outcome, state)?;
        let post_state_digest = self
            .instrument
            .post_state(outcome, state)?
            .map(|post| finite_matrix_digest(post.matrix()));
        Ok(FiniteInstrumentReceipt {
            instrument_digest: self.canonical_digest(),
            input_state_digest: finite_matrix_digest(state.matrix()),
            outcome,
            probability,
            post_state_digest,
            authority_effect: AuthorityEffect::None,
        })
    }

    pub fn verify_receipt(
        &self,
        state: &omega_quantum_physics::exact_instrument::ExactDensityState,
        receipt: &FiniteInstrumentReceipt,
    ) -> Result<bool, omega_quantum_physics::exact_instrument::ExactInstrumentError> {
        Ok(self.receipt(receipt.outcome, state)? == *receipt)
    }
}
