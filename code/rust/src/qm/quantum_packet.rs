use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::{involution as star, matrix as mx};
use num_traits::{One, Signed};
use omega_number_theory::cyclotomic::GaussianRat;
use omega_number_theory::rational::Rational;
use omega_quantum_physics::exact_hermitian;
use omega_quantum_physics::gauge_cochain_complex::{BornEntry, M2Packet, VerifiedM2Packet};

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum M2Refusal {
    #[error("matrix algebra refused: {0}")]
    Algebra(String),
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

fn is_2x2(m: &BasicMatrix<GaussianRat>) -> bool {
    m.shape() == (2, 2)
}

fn is_unit_trace_state(rho: &BasicMatrix<GaussianRat>) -> bool {
    exact_hermitian::is_positive_semidefinite(rho)
        && mx::trace(rho).is_ok_and(|trace| trace == GaussianRat::one())
}

fn is_effect(e: &BasicMatrix<GaussianRat>) -> bool {
    exact_hermitian::is_positive_semidefinite(e)
        && mx::sub(&identity2(), e)
            .is_ok_and(|complement| exact_hermitian::is_positive_semidefinite(&complement))
}

pub fn verify(packet: M2Packet) -> Result<VerifiedM2Packet, M2Refusal> {
    if packet.states.is_empty() {
        return Err(M2Refusal::MissingField("states"));
    }
    if packet.effects.is_empty() {
        return Err(M2Refusal::MissingField("effects"));
    }
    if packet.born_table.is_empty() {
        return Err(M2Refusal::MissingField("born_table"));
    }
    let shaped: [(&'static str, &Vec<BasicMatrix<GaussianRat>>); 2] =
        [("state", &packet.states), ("effect", &packet.effects)];
    for (field, list) in shaped {
        if let Some((index, m)) = list.iter().enumerate().find(|(_, m)| !is_2x2(m)) {
            return Err(M2Refusal::UnsupportedCarrier {
                field,
                index,
                rows: m.rows(),
                cols: m.cols(),
            });
        }
    }
    for (index, kraus) in packet.channels.iter().enumerate() {
        if let Some(m) = kraus.iter().find(|m| !is_2x2(m)) {
            return Err(M2Refusal::UnsupportedCarrier {
                field: "kraus operator",
                index,
                rows: m.rows(),
                cols: m.cols(),
            });
        }
    }
    if let Some(index) = packet
        .states
        .iter()
        .position(|rho| !is_unit_trace_state(rho))
    {
        return Err(M2Refusal::InvalidState(index));
    }
    if let Some(index) = packet.effects.iter().position(|e| !is_effect(e)) {
        return Err(M2Refusal::InvalidEffect(index));
    }
    for (index, context) in packet.povms.iter().enumerate() {
        if context.is_empty() || context.iter().any(|&k| k >= packet.effects.len()) {
            return Err(M2Refusal::InvalidPovm(index));
        }
        let mut sum = mx::zeros(2, 2).map_err(|e| M2Refusal::Algebra(e.to_string()))?;
        for &k in context {
            sum =
                mx::add(&sum, &packet.effects[k]).map_err(|e| M2Refusal::Algebra(e.to_string()))?;
        }
        if sum != identity2() {
            return Err(M2Refusal::InvalidPovm(index));
        }
    }
    for (index, kraus) in packet.channels.iter().enumerate() {
        let mut completeness = mx::zeros(2, 2).map_err(|e| M2Refusal::Algebra(e.to_string()))?;
        for k in kraus {
            let adjoint = star::adjoint(k).map_err(|e| M2Refusal::Algebra(e.to_string()))?;
            let square =
                mx::multiply(&adjoint, k).map_err(|e| M2Refusal::Algebra(e.to_string()))?;
            completeness =
                mx::add(&completeness, &square).map_err(|e| M2Refusal::Algebra(e.to_string()))?;
        }
        if kraus.is_empty() || completeness != identity2() {
            return Err(M2Refusal::InvalidChannel(index));
        }
    }
    for (index, entry) in packet.born_table.iter().enumerate() {
        if entry.state >= packet.states.len()
            || entry.effect >= packet.effects.len()
            || entry.probability.is_negative()
            || entry.probability > Rational::one()
        {
            return Err(M2Refusal::InconsistentBornEntry(index));
        }
    }
    VerifiedM2Packet::from_declaration(packet).map_err(|e| M2Refusal::GaugeComplex(e.to_string()))
}

pub fn worked_example_packet(declared_probability: Rational) -> M2Packet {
    let half = GaussianRat::from_rational(Rational::new(1.into(), 2.into()));
    let rho =
        mx::diagonal(&[GaussianRat::one(), GaussianRat::zero()]).expect("declared qubit fixture");
    let plus = BasicMatrix::from_row_major(2, 2, vec![half; 4]).expect("declared qubit fixture");
    let minus = mx::sub(&identity2(), &plus).expect("declared qubit fixture");
    M2Packet {
        states: vec![rho],
        effects: vec![plus, minus],
        povms: vec![vec![0, 1]],
        channels: vec![vec![identity2()]],
        born_table: vec![BornEntry {
            state: 0,
            effect: 0,
            probability: declared_probability,
        }],
    }
}
