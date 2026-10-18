use omega_number_theory::quadratic::Quadratic;
pub type IsingScalar = Quadratic<2>;
pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; exact finite recoupling; no continuum admission.";
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum SpinFoamError {
    #[error("SU(2)_2 label must be in 0..=2")]
    Label,
    #[error("admissible recoupling coefficient did not lie in Q(sqrt(2))")]
    Field,
    #[error("finite state sum exceeds its operation budget")]
    Budget,
}
pub fn ising_admissible(a: u8, b: u8, c: u8) -> bool {
    a <= 2
        && b <= 2
        && c <= 2
        && a + b >= c
        && a + c >= b
        && b + c >= a
        && (a + b + c) % 2 == 0
        && a + b + c <= 4
}
pub fn quantum_dimension(label: u8) -> Result<IsingScalar, SpinFoamError> {
    match label {
        0 | 2 => Ok(IsingScalar::one()),
        1 => Ok(IsingScalar::sqrt_d()),
        _ => Err(SpinFoamError::Label),
    }
}
fn qfactorial(n: u8) -> IsingScalar {
    let mut previous = IsingScalar::zero();
    let mut current = IsingScalar::one();
    let mut result = IsingScalar::one();
    for _ in 1..=n {
        result = result.mul(&current);
        let next = IsingScalar::sqrt_d().mul(&current).sub(&previous);
        previous = current;
        current = next;
    }
    result
}
fn delta_squared(a: u8, b: u8, c: u8) -> IsingScalar {
    qfactorial((a + b - c) / 2)
        .mul(&qfactorial((a + c - b) / 2))
        .mul(&qfactorial((b + c - a) / 2))
        .checked_div(&qfactorial((a + b + c) / 2 + 1))
        .expect("admissibility keeps denominator nonzero")
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RacahCoefficient {
    factor: IsingScalar,
    squared_prefactor: IsingScalar,
}
impl RacahCoefficient {
    pub fn factor(&self) -> &IsingScalar {
        &self.factor
    }
    pub fn squared_prefactor(&self) -> &IsingScalar {
        &self.squared_prefactor
    }
    pub fn squared_value(&self) -> IsingScalar {
        self.factor.mul(&self.factor).mul(&self.squared_prefactor)
    }
    pub fn quadratic_value(&self) -> Result<IsingScalar, SpinFoamError> {
        if self.factor == IsingScalar::zero() {
            return Ok(IsingScalar::zero());
        }
        Ok(self
            .factor
            .mul(&self.squared_prefactor.sqrt().ok_or(SpinFoamError::Field)?))
    }
}
pub fn ising_six_j_radical(labels: [u8; 6]) -> Result<RacahCoefficient, SpinFoamError> {
    let [a, b, c, d, e, f] = labels;
    if labels.iter().any(|&v| v > 2) {
        return Err(SpinFoamError::Label);
    }
    let triangles = [(a, b, c), (a, e, f), (d, b, f), (d, e, c)];
    if triangles
        .iter()
        .any(|&(u, v, w)| !ising_admissible(u, v, w))
    {
        return Ok(RacahCoefficient {
            factor: IsingScalar::zero(),
            squared_prefactor: IsingScalar::one(),
        });
    }
    let squared_prefactor = triangles.iter().fold(IsingScalar::one(), |x, &(u, v, w)| {
        x.mul(&delta_squared(u, v, w))
    });
    let t = [
        (a + b + c) / 2,
        (a + e + f) / 2,
        (d + b + f) / 2,
        (d + e + c) / 2,
    ];
    let u = [
        (a + b + d + e) / 2,
        (a + c + d + f) / 2,
        (b + c + e + f) / 2,
    ];
    let lower = *t.iter().max().expect("four faces");
    let upper = *u.iter().min().expect("three sums");
    let mut sum = IsingScalar::zero();
    for z in lower..=upper {
        let denominator = t
            .iter()
            .fold(IsingScalar::one(), |x, &v| x.mul(&qfactorial(z - v)));
        let denominator = u
            .iter()
            .fold(denominator, |x, &v| x.mul(&qfactorial(v - z)));
        let term = qfactorial(z + 1)
            .checked_div(&denominator)
            .ok_or(SpinFoamError::Field)?;
        sum = if z % 2 == 0 {
            sum.add(&term)
        } else {
            sum.sub(&term)
        };
    }
    Ok(RacahCoefficient {
        factor: sum,
        squared_prefactor,
    })
}
pub fn ising_six_j(labels: [u8; 6]) -> Result<IsingScalar, SpinFoamError> {
    ising_six_j_radical(labels)?.quadratic_value()
}
pub fn ising_f(a: u8, b: u8, c: u8, d: u8, e: u8, f: u8) -> Result<IsingScalar, SpinFoamError> {
    if [a, b, c, d, e, f].iter().any(|&v| v > 2) {
        return Err(SpinFoamError::Label);
    }
    if !ising_admissible(a, b, e)
        || !ising_admissible(e, c, d)
        || !ising_admissible(b, c, f)
        || !ising_admissible(a, f, d)
    {
        return Ok(IsingScalar::zero());
    }
    let racah = ising_six_j_radical([a, b, e, c, d, f])?;
    let root = quantum_dimension(e)?
        .mul(&quantum_dimension(f)?)
        .mul(racah.squared_prefactor())
        .sqrt()
        .ok_or(SpinFoamError::Field)?;
    let value = root.mul(racah.factor());
    Ok(if ((a + b + c + d) / 2) % 2 == 0 {
        value
    } else {
        value.neg()
    })
}
#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct SpinFoam {
    pub degree: usize,
    pub label: String,
    pub tetrahedral_labels: Vec<[u8; 6]>,
}
impl SpinFoam {
    pub fn new(degree: usize, label: impl Into<String>) -> Self {
        Self {
            degree,
            label: label.into(),
            tetrahedral_labels: Vec::new(),
        }
    }
    pub fn from_tetrahedra(
        labels: Vec<[u8; 6]>,
        label: impl Into<String>,
    ) -> Result<Self, SpinFoamError> {
        if labels.len() > 4096 {
            return Err(SpinFoamError::Budget);
        }
        for &cell in &labels {
            ising_six_j_radical(cell)?;
        }
        Ok(Self {
            degree: labels.len(),
            label: label.into(),
            tetrahedral_labels: labels,
        })
    }
    pub fn tetrahedral_amplitude(&self) -> Result<RacahCoefficient, SpinFoamError> {
        if self.tetrahedral_labels.len() > 4096 {
            return Err(SpinFoamError::Budget);
        }
        self.tetrahedral_labels.iter().try_fold(
            RacahCoefficient {
                factor: IsingScalar::one(),
                squared_prefactor: IsingScalar::one(),
            },
            |product, &labels| {
                let cell = ising_six_j_radical(labels)?;
                Ok(RacahCoefficient {
                    factor: product.factor.mul(&cell.factor),
                    squared_prefactor: product.squared_prefactor.mul(&cell.squared_prefactor),
                })
            },
        )
    }
    pub fn authority_fence() -> &'static str {
        AUTHORITY_FENCE
    }
}
