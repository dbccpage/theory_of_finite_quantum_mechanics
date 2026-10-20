

use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::{involution as iv, matrix as mx, ExactFieldError};
use num_traits::Zero;
use omega_number_theory::cyclotomic::Cyc12;
use omega_number_theory::cyclotomic_integer::{CyclotomicInteger as C, CyclotomicIntegerError};
use omega_number_theory::quadratic::Quadratic;
use omega_number_theory::rational::{ri, Rational};

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum SpinFoamModelError {
    #[error(transparent)]
    Matrix(#[from] ExactFieldError),
    #[error(transparent)]
    Ring(#[from] CyclotomicIntegerError),
    #[error("invalid declared model input: {0}")]
    Input(String),
}
impl From<String> for SpinFoamModelError {
    fn from(s: String) -> Self {
        Self::Input(s)
    }
}
impl From<&str> for SpinFoamModelError {
    fn from(s: &str) -> Self {
        Self::Input(s.into())
    }
}
const TET: [[usize; 3]; 4] = [[0, 3, 1], [1, 4, 2], [2, 5, 0], [3, 4, 5]];
const SIMPLEX: [[usize; 4]; 5] = [
    [6, 7, 8, 9],
    [3, 4, 5, 9],
    [1, 2, 5, 8],
    [0, 2, 4, 7],
    [0, 1, 3, 6],
];

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum ModelVersion {
    Published,
    Corrected,
}

pub const ADMISSIBLE_BASIS: [[u32; 4]; 8] = [
    [0, 0, 0, 0],
    [1, 1, 0, 0],
    [1, 0, 1, 0],
    [1, 0, 0, 1],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 1, 1],
    [1, 1, 1, 1],
];

pub fn quantum_integer(n: usize) -> C {
    let value = omega_number_theory::cyclotomic_field::quantum_integer(12, n as i64)
        .expect("fixed q-number budget");
    C::new(12, value.coefficients().to_vec())
        .expect("q-integer has integral cyclotomic coordinates")
}
fn amplitude<const N: usize>(s: &[u32], faces: &[[usize; N]]) -> C {
    let mut a = C::scalar(12, 1).expect("fixed valid conductor");
    let z = C::zeta(12).unwrap();
    for f in faces {
        let sum: u64 = f.iter().map(|&i| u64::from(s[i])).sum();
        if sum % 2 != 0 {
            return C::scalar(12, 0).expect("fixed valid conductor");
        }
        a = a.mul(&z.pow(((sum * 3) % 12) as usize)).unwrap();
    }
    a
}
pub fn tetrahedron(s: &[u32; 6]) -> C {
    amplitude(s, &TET)
}
pub fn simplex4(s: &[u32; 10]) -> C {
    amplitude(s, &SIMPLEX)
}
pub fn admissible(s: &[u32]) -> bool {
    s.iter().fold(0u32, |parity, s| parity ^ (s & 1)) == 0
}

pub fn adjoint_bulk(bulk: &[u32; 10]) -> [u32; 10] {
    [
        bulk[0], bulk[1], bulk[2], bulk[6], bulk[7], bulk[8], bulk[3], bulk[4], bulk[5], bulk[9],
    ]
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryState {
    pub spins: [u32; 4],
    pub amplitude: C,
}
impl BoundaryState {
    pub fn inner_product(&self, b: &Self) -> Result<C, SpinFoamModelError> {
        if self.spins == b.spins && admissible(&self.spins) {
            Ok(self.amplitude.conj().mul(&b.amplitude)?)
        } else {
            Ok(C::scalar(12, 0).expect("fixed valid conductor"))
        }
    }
    pub fn master(&self) -> Self {
        Self {
            spins: self.spins,
            amplitude: if admissible(&self.spins) {
                C::scalar(12, 0).expect("fixed valid conductor")
            } else {
                self.amplitude.clone()
            },
        }
    }
    pub fn projector(&self) -> Self {
        Self {
            spins: self.spins,
            amplitude: if admissible(&self.spins) {
                self.amplitude.clone()
            } else {
                C::scalar(12, 0).expect("fixed valid conductor")
            },
        }
    }
    pub fn evolve(&self, bulk: &[u32; 10]) -> Result<Self, SpinFoamModelError> {
        Ok(Self {
            spins: self.spins,
            amplitude: transition(ModelVersion::Published, &self.spins, &self.spins, bulk)
                .mul(&self.amplitude)?,
        })
    }
}

fn connected(version: ModelVersion, input: &[u32; 4], output: &[u32; 4]) -> bool {
    match version {
        ModelVersion::Published => admissible(input) && admissible(output),
        ModelVersion::Corrected => input == output && admissible(input),
    }
}

pub fn transition(
    version: ModelVersion,
    input: &[u32; 4],
    output: &[u32; 4],
    bulk: &[u32; 10],
) -> C {
    if connected(version, input, output) {
        simplex4(bulk)
    } else {
        C::scalar(12, 0).expect("fixed valid conductor")
    }
}

pub fn transition_matrix(version: ModelVersion, bulk: &[u32; 10]) -> BasicMatrix<Cyc12> {
    let amplitude = simplex4(bulk);
    let a = Cyc12 {
        a: std::array::from_fn(|i| {
            amplitude
                .coefficient_values()
                .get(i)
                .cloned()
                .unwrap_or_else(Rational::zero)
        }),
    };
    mx::from_fn(8, 8, |r, c| {
        if connected(version, &ADMISSIBLE_BASIS[c], &ADMISSIBLE_BASIS[r]) {
            a.clone()
        } else {
            Cyc12::zero()
        }
    })
    .expect("fixed eight-boundary carrier")
}

pub fn real_value(z: &C) -> Result<Option<Quadratic<3>>, SpinFoamModelError> {
    if z.conductor() != 12 {
        return Err("CONDUCTOR_12_REQUIRED".into());
    }
    let mut c = z.coefficient_values().to_vec();
    c.resize(4, Rational::zero());
    if !c[2].is_zero() || c[1] != -(&c[3] * ri(2)) {
        return Ok(None);
    }
    Ok(Some(Quadratic::<3>::new(c[0].clone(), &c[1] / ri(2))))
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PachnerState {
    pub external: [u32; 6],
    pub internal: Vec<u32>,
    pub amplitude: C,
}
impl PachnerState {
    pub fn projector(&self) -> Self {
        let mut r = self.clone();
        if !admissible(&r.external) {
            r.amplitude = C::scalar(12, 0).expect("fixed valid conductor")
        }
        r
    }
    pub fn two_to_three(&self) -> Result<Self, SpinFoamModelError> {
        if self.internal.len() != 1 {
            return Err("PACHNER_REQUIRES_TWO_TETRAHEDRA".into());
        }
        Ok(Self {
            external: self.external,
            internal: vec![self.internal[0], 0, 0],
            amplitude: self.amplitude.clone(),
        })
    }
    pub fn partition(&self, version: ModelVersion) -> Result<C, SpinFoamModelError> {
        let projected = self.projector().amplitude;
        Ok(match version {
            ModelVersion::Published => self.amplitude.mul(&projected)?,
            ModelVersion::Corrected => self.amplitude.conj().mul(&projected)?,
        })
    }
}
fn combinations(n: usize, k: usize) -> Vec<Vec<usize>> {
    omega_combinatorics::enumeration::combinations(n, k, 64).expect("fixed simplex face budget")
}
pub fn sphere_partition(spins: &[u32; 20]) -> C {
    let faces = combinations(6, 3);
    let cells = combinations(6, 5);
    cells.iter().fold(
        C::scalar(12, 1).expect("fixed valid conductor"),
        |a, cell| {
            let triples = combinations(5, 3);
            let mut s = [0; 10];
            for (i, t) in triples.iter().enumerate() {
                let f: Vec<_> = t.iter().map(|&j| cell[j]).collect();
                s[i] = spins[faces.iter().position(|v| *v == f).unwrap()];
            }
            a.mul(&simplex4(&s)).unwrap()
        },
    )
}

pub fn sphere_euler() -> i64 {
    (1..=5)
        .map(|k| {
            let count = combinations(6, k).len() as i64;
            if k % 2 == 1 {
                count
            } else {
                -count
            }
        })
        .sum()
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct SpinFoamCensus {
    pub level: usize,
    pub tetrahedra_checked: usize,
    pub simplices_checked: usize,
    pub admissible_tetrahedra: usize,
    pub admissible_simplices: usize,
    pub sphere_euler: i64,
    pub q2_square_three: bool,
    pub q6_zero: bool,
    pub tetra_orientation: bool,
    pub simplex_symmetries: bool,
    pub boundary_projector: bool,
    pub master_self_adjoint_on_basis: bool,
    pub diagonal_evolution_projector: bool,
    pub pachner_intertwining: bool,
    pub sphere_euler_two: bool,
    pub sphere_vacuum_partition: bool,
    pub corrected_vacuum_transition_unitary: bool,
    pub corrected_partition_unit_norm_and_pachner_invariance: bool,
}

impl SpinFoamCensus {
    fn local_checks_hold(&self) -> bool {
        self.q2_square_three
            && self.q6_zero
            && self.tetra_orientation
            && self.simplex_symmetries
            && self.boundary_projector
            && self.master_self_adjoint_on_basis
    }

    fn global_checks_hold(&self) -> bool {
        self.diagonal_evolution_projector
            && self.pachner_intertwining
            && self.sphere_euler_two
            && self.sphere_vacuum_partition
            && self.corrected_vacuum_transition_unitary
            && self.corrected_partition_unit_norm_and_pachner_invariance
    }

    pub fn checks_hold(&self) -> bool {
        self.local_checks_hold() && self.global_checks_hold()
    }
}

fn decode_spins<const N: usize>(mut code: usize, level: usize) -> [u32; N] {
    let mut s = [0; N];
    for x in &mut s {
        *x = (code % level) as u32;
        code /= level;
    }
    s
}

fn census_tetrahedra(level: usize) -> (bool, usize) {
    let zero = C::scalar(12, 0).expect("fixed valid conductor");
    let mut tetra_sym = true;
    let mut admissible_tets = 0;
    for code in 0..level.pow(6) {
        let s = decode_spins::<6>(code, level);
        let a = tetrahedron(&s);
        let r = [s[1], s[0], s[2], s[3], s[5], s[4]];
        tetra_sym &= tetrahedron(&r) == a.conj();
        admissible_tets += usize::from(a != zero);
    }
    (tetra_sym, admissible_tets)
}

fn census_simplices(level: usize) -> (bool, usize) {
    let zero = C::scalar(12, 0).expect("fixed valid conductor");
    let mut simplex_sym = true;
    let mut admissible_cells = 0;
    for code in 0..level.pow(10) {
        let s = decode_spins::<10>(code, level);
        let a = simplex4(&s);
        let c = [s[6], s[7], s[0], s[8], s[1], s[2], s[9], s[3], s[4], s[5]];
        simplex_sym &= simplex4(&adjoint_bulk(&s)) == a.conj() && simplex4(&c) == a;
        admissible_cells += usize::from(a != zero);
    }
    (simplex_sym, admissible_cells)
}

fn census_boundary_states(z: &C) -> Result<(bool, bool, bool), SpinFoamModelError> {
    let mut projector = true;
    let mut adjoint = true;
    let mut duality = true;
    for code in 0..16 {
        let spins = std::array::from_fn(|i| ((code >> i) & 1) as u32);
        let b = BoundaryState {
            spins,
            amplitude: z.pow(code),
        };
        projector &= b.projector().projector() == b.projector();
        duality &= b.evolve(&[0; 10])? == b.projector();
        adjoint &= b.inner_product(&b.master())? == b.master().inner_product(&b)?;
    }
    Ok((projector, adjoint, duality))
}

fn census_pachner_states(z: &C) -> Result<(bool, bool), SpinFoamModelError> {
    let mut pachner = true;
    let mut corrected_pachner = true;
    for code in 0..64 {
        let b = PachnerState {
            external: std::array::from_fn(|i| ((code >> i) & 1) as u32),
            internal: vec![1],
            amplitude: z.pow(code),
        };
        let b23 = b.two_to_three()?;
        pachner &= b23.projector() == b.projector().two_to_three()?
            && b.partition(ModelVersion::Published)? == b23.partition(ModelVersion::Published)?;
        let norm = b.partition(ModelVersion::Corrected)?;
        let expected_norm =
            C::scalar(12, i64::from(admissible(&b.external))).expect("fixed valid conductor");
        corrected_pachner &=
            norm == expected_norm && b23.partition(ModelVersion::Corrected)? == norm;
    }
    Ok((pachner, corrected_pachner))
}

pub fn census(level: usize) -> Result<SpinFoamCensus, SpinFoamModelError> {
    if level == 0 || level > 3 {
        return Err("INVALID_SPIN_LEVEL".into());
    }
    let (tetra_sym, admissible_tets) = census_tetrahedra(level);
    let (simplex_sym, admissible_cells) = census_simplices(level);
    let z = C::zeta(12)?;
    let (projector, adjoint, duality) = census_boundary_states(&z)?;
    let (pachner, corrected_pachner) = census_pachner_states(&z)?;
    let vacuum_unitary = iv::is_unitary(&transition_matrix(ModelVersion::Corrected, &[0; 10]))?;
    let euler = sphere_euler();
    Ok(SpinFoamCensus {
        level,
        tetrahedra_checked: level.pow(6),
        simplices_checked: level.pow(10),
        admissible_tetrahedra: admissible_tets,
        admissible_simplices: admissible_cells,
        sphere_euler: euler,
        q2_square_three: quantum_integer(2).mul(&quantum_integer(2))?
            == C::scalar(12, 3).expect("fixed valid conductor"),
        q6_zero: quantum_integer(6) == C::scalar(12, 0).expect("fixed valid conductor"),
        tetra_orientation: tetra_sym,
        simplex_symmetries: simplex_sym,
        boundary_projector: projector,
        master_self_adjoint_on_basis: adjoint,
        diagonal_evolution_projector: duality,
        pachner_intertwining: pachner,
        sphere_euler_two: euler == 2,
        sphere_vacuum_partition: sphere_partition(&[0; 20])
            == C::scalar(12, 1).expect("fixed valid conductor"),
        corrected_vacuum_transition_unitary: vacuum_unitary,
        corrected_partition_unit_norm_and_pachner_invariance: corrected_pachner,
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn finite_lean_models() {
        let r = census(2).unwrap();
        assert!(r.checks_hold());
        assert_eq!(r.admissible_tetrahedra, 8);
        assert_eq!(r.admissible_simplices, 64);
        assert!(census(0).is_err());
    }
    #[test]
    fn nonclaims_have_counterexamples() {
        let off_diagonal = |version| transition(version, &[0; 4], &[1, 1, 0, 0], &[0; 10]);
        assert_eq!(
            off_diagonal(ModelVersion::Published),
            C::scalar(12, 1).expect("fixed valid conductor")
        );
        assert_eq!(
            off_diagonal(ModelVersion::Corrected),
            C::scalar(12, 0).expect("fixed valid conductor")
        );
        let s = PachnerState {
            external: [0; 6],
            internal: vec![0],
            amplitude: C::zeta(12).unwrap().pow(3),
        };
        assert_eq!(
            s.partition(ModelVersion::Published).unwrap(),
            C::scalar(12, -1).expect("fixed valid conductor")
        );
        assert_eq!(
            s.partition(ModelVersion::Corrected).unwrap(),
            C::scalar(12, 1).expect("fixed valid conductor")
        );
    }
    #[test]
    fn real_values_of_q_zeta_12_are_read_exactly() {
        let z = C::zeta(12).unwrap();
        let one_plus = C::scalar(12, 1)
            .expect("fixed valid conductor")
            .add(&z)
            .unwrap();
        let norm = one_plus.conj().mul(&one_plus).unwrap();
        assert_eq!(
            real_value(&norm).unwrap(),
            Some(Quadratic::<3>::new(ri(2), ri(1)))
        );
        assert_eq!(real_value(&z).unwrap(), None);
        assert!(Quadratic::<3>::new(ri(2), ri(-1)).is_nonnegative());
        assert!(!Quadratic::<3>::new(ri(1), ri(-1)).is_nonnegative());
        assert!(Quadratic::<3>::new(ri(-1), ri(1)).is_nonnegative());
        assert!(!Quadratic::<3>::new(ri(-2), ri(1)).is_nonnegative());
        assert_eq!(
            real_value(&C::scalar(8, 1).expect("fixed valid conductor")),
            Err("CONDUCTOR_12_REQUIRED".into())
        );
    }
}
