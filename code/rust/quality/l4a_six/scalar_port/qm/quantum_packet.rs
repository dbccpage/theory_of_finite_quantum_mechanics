use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::ordered;
use crate::linear_algebra::{involution as star, matrix as mx};
use ::linear_algebra::backend::basic_matrix::BasicMatrix as ProviderMatrix;
use num_traits::{One, Signed};
use engine_number_theory::cyclotomic::GaussianRat;
use engine_number_theory::rational::Rational;
use engine_quantum_physics::gauge_cochain_complex::{BornEntry, M2Packet, VerifiedM2Packet};

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum M2Refusal {
    #[error("matrix algebra refused: {0}")]
    Algebra(String),
    #[error("checked exact algebra: {0}")]
    ExactAlgebra(#[from] crate::linear_algebra::ExactFieldError),
    #[error("missing field: {0}")]
    MissingField(&'static str),
    #[error("gauge complex refused: {0}")]
    GaugeComplex(String),
    #[error("{field} {index} is {rows}x{cols}; the carrier is M_2")]
    UnsupportedCarrier {
        field: &'static str,
        index: usize,
        rows: usize,
        cols: usize,
    },
    #[error("state {0} is not Hermitian PSD with unit trace")]
    InvalidState(usize),
    #[error("effect {0} does not satisfy 0 <= E <= I")]
    InvalidEffect(usize),
    #[error("POVM context {0} does not sum to the identity")]
    InvalidPovm(usize),
    #[error("channel {0} is not trace preserving")]
    InvalidChannel(usize),
    #[error("Born entry {0} is malformed")]
    InconsistentBornEntry(usize),
}

fn identity2() -> BasicMatrix<GaussianRat> {
    mx::identity(2).expect("the declared M2 identity fits the carrier")
}

fn is_2x2(m: &ProviderMatrix<GaussianRat>) -> bool {
    m.shape() == (2, 2)
}

fn is_unit_trace_state(rho: &ProviderMatrix<GaussianRat>) -> Result<bool, M2Refusal> {
    let rho = BasicMatrix::try_from_provider(rho)?;
    Ok(
        ordered::hermitian_is_positive_semidefinite(&rho)?
            && mx::trace(&rho)? == GaussianRat::one(),
    )
}
fn is_effect(e: &ProviderMatrix<GaussianRat>) -> Result<bool, M2Refusal> {
    let e = BasicMatrix::try_from_provider(e)?;
    Ok(ordered::hermitian_is_positive_semidefinite(&e)?
        && ordered::hermitian_is_positive_semidefinite(&mx::sub(&identity2(), &e)?)?)
}

fn check_nonempty_fields(packet: &M2Packet) -> Result<(), M2Refusal> {
    if packet.states.is_empty() {
        return Err(M2Refusal::MissingField("states"));
    }
    if packet.effects.is_empty() {
        return Err(M2Refusal::MissingField("effects"));
    }
    if packet.born_table.is_empty() {
        return Err(M2Refusal::MissingField("born_table"));
    }
    Ok(())
}

fn check_matrix_list_2x2(
    field: &'static str,
    list: &[ProviderMatrix<GaussianRat>],
) -> Result<(), M2Refusal> {
    for (index, m) in list.iter().enumerate() {
        if !is_2x2(m) {
            return Err(M2Refusal::UnsupportedCarrier {
                field,
                index,
                rows: m.rows(),
                cols: m.cols(),
            });
        }
    }
    Ok(())
}

fn check_channels_2x2(channels: &[Vec<ProviderMatrix<GaussianRat>>]) -> Result<(), M2Refusal> {
    for (index, kraus) in channels.iter().enumerate() {
        for m in kraus {
            if !is_2x2(m) {
                return Err(M2Refusal::UnsupportedCarrier {
                    field: "kraus operator",
                    index,
                    rows: m.rows(),
                    cols: m.cols(),
                });
            }
        }
    }
    Ok(())
}

fn check_states_and_effects(packet: &M2Packet) -> Result<(), M2Refusal> {
    for (index, rho) in packet.states.iter().enumerate() {
        if !is_unit_trace_state(rho)? {
            return Err(M2Refusal::InvalidState(index));
        }
    }
    for (index, e) in packet.effects.iter().enumerate() {
        if !is_effect(e)? {
            return Err(M2Refusal::InvalidEffect(index));
        }
    }
    Ok(())
}

fn check_single_povm(
    index: usize,
    context: &[usize],
    effects: &[ProviderMatrix<GaussianRat>],
) -> Result<(), M2Refusal> {
    if context.is_empty() {
        return Err(M2Refusal::InvalidPovm(index));
    }
    let mut sum = mx::zeros(2, 2).map_err(|e| M2Refusal::Algebra(e.to_string()))?;
    for &k in context {
        let Some(effect) = effects.get(k) else {
            return Err(M2Refusal::InvalidPovm(index));
        };
        sum = mx::add(&sum, &BasicMatrix::try_from_provider(effect)?)
            .map_err(|e| M2Refusal::Algebra(e.to_string()))?;
    }
    if sum != identity2() {
        return Err(M2Refusal::InvalidPovm(index));
    }
    Ok(())
}

fn check_povms(packet: &M2Packet) -> Result<(), M2Refusal> {
    for (index, context) in packet.povms.iter().enumerate() {
        check_single_povm(index, context, &packet.effects)?;
    }
    Ok(())
}

fn check_single_channel(
    index: usize,
    kraus: &[ProviderMatrix<GaussianRat>],
) -> Result<(), M2Refusal> {
    let mut completeness = mx::zeros(2, 2).map_err(|e| M2Refusal::Algebra(e.to_string()))?;
    for raw in kraus {
        let k = BasicMatrix::try_from_provider(raw)?;
        let adjoint = star::adjoint(&k).map_err(|e| M2Refusal::Algebra(e.to_string()))?;
        let square = mx::multiply(&adjoint, &k).map_err(|e| M2Refusal::Algebra(e.to_string()))?;
        completeness =
            mx::add(&completeness, &square).map_err(|e| M2Refusal::Algebra(e.to_string()))?;
    }
    if kraus.is_empty() || completeness != identity2() {
        return Err(M2Refusal::InvalidChannel(index));
    }
    Ok(())
}

fn check_channels(channels: &[Vec<ProviderMatrix<GaussianRat>>]) -> Result<(), M2Refusal> {
    for (index, kraus) in channels.iter().enumerate() {
        check_single_channel(index, kraus)?;
    }
    Ok(())
}

fn check_born_table(packet: &M2Packet) -> Result<(), M2Refusal> {
    for (index, entry) in packet.born_table.iter().enumerate() {
        if entry.state >= packet.states.len()
            || entry.effect >= packet.effects.len()
            || entry.probability.is_negative()
            || entry.probability > Rational::one()
        {
            return Err(M2Refusal::InconsistentBornEntry(index));
        }
    }
    Ok(())
}

pub fn verify(packet: M2Packet) -> Result<VerifiedM2Packet, M2Refusal> {
    check_nonempty_fields(&packet)?;
    check_matrix_list_2x2("state", &packet.states)?;
    check_matrix_list_2x2("effect", &packet.effects)?;
    check_channels_2x2(&packet.channels)?;
    check_states_and_effects(&packet)?;
    check_povms(&packet)?;
    check_channels(&packet.channels)?;
    check_born_table(&packet)?;
    VerifiedM2Packet::from_declaration(packet).map_err(|e| M2Refusal::GaugeComplex(e.to_string()))
}

pub fn worked_example_packet(declared_probability: Rational) -> M2Packet {
    let half = GaussianRat::from_rational(Rational::new(1.into(), 2.into()));
    let rho =
        mx::diagonal(&[GaussianRat::one(), GaussianRat::zero()]).expect("declared qubit fixture");
    let plus = BasicMatrix::from_row_major(2, 2, vec![half; 4]).expect("declared qubit fixture");
    let minus = mx::sub(&identity2(), &plus).expect("declared qubit fixture");
    M2Packet {
        states: vec![rho.into_provider().expect("admitted qubit fixture")],
        effects: vec![
            plus.into_provider().expect("admitted qubit fixture"),
            minus.into_provider().expect("admitted qubit fixture"),
        ],
        povms: vec![vec![0, 1]],
        channels: vec![vec![identity2()
            .into_provider()
            .expect("admitted identity fixture")]],
        born_table: vec![BornEntry {
            state: 0,
            effect: 0,
            probability: declared_probability,
        }],
    }
}
