//! Native replay of the Lean-exported two-circulant quartet expressions.
//!
//! AuthorityEffect: None. Complete coefficient-table comparison and rational probes are
//! separate from analytic soundness and complete parameter/candidate coverage.
//! Inspection is a residual interval evaluation. The rectangular mode emits one
//! exact image and its complete input/Jacobian data; full-cover execution and
//! native-image kernel reflection remain separate.

use num_rational::BigRational;
use num_traits::{One, Zero};
use omega_kernel::exact::{parse_exact, to_canonical_string};
use omega_kernel::interval::Interval;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, BTreeSet};
use thiserror::Error;

const VARIABLES: usize = 440;
const EQUATIONS: usize = 618;
const GAUGED_EQUATIONS: usize = 666;
const MAX_BYTES: usize = 8_000_000;
const MAX_TERMS: usize = 5_000;
const MAX_DEPTH: usize = 64;

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Error)]
pub enum SystemError {
    #[error("system input exceeds the byte bound")]
    InputTooLarge,
    #[error("invalid system JSON: {0}")]
    Json(String),
    #[error("wrong system schema or dimensions")]
    Schema,
    #[error("missing or unordered {kind} index {index}")]
    Index { kind: String, index: usize },
    #[error("invalid canonical rational: {0}")]
    Rational(String),
    #[error("invalid full containing box at coordinate {0}")]
    ContainingBox(usize),
    #[error("expression variable {0} is out of bounds")]
    Variable(usize),
    #[error("expression exceeds the depth or term bound")]
    ExpressionBound,
    #[error("expression multiplication exceeds degree two")]
    Degree,
    #[error("point or interval box has dimension {found}, expected {expected}")]
    Dimension { expected: usize, found: usize },
    #[error("three complete rational parity probes are required")]
    Probes,
    #[error("native/Lean parity mismatch at probe {probe}, equation {equation}")]
    ProbeMismatch { probe: usize, equation: usize },
    #[error("native/Lean coefficient-table mismatch at equation {equation}")]
    CoefficientMismatch { equation: usize },
    #[error("invalid contractor box at coordinate {0}")]
    ContractorBox(usize),
    #[error("contractor center is outside coordinate {0}")]
    CenterOutsideBox(usize),
    #[error("invalid or unordered preconditioner entry at row {row}, equation {equation}")]
    Preconditioner { row: usize, equation: usize },
}

#[derive(Deserialize)]
#[serde(tag = "op", rename_all = "snake_case", deny_unknown_fields)]
enum ExprWire {
    Constant {
        value: String,
    },
    Variable {
        index: usize,
    },
    Add {
        left: Box<ExprWire>,
        right: Box<ExprWire>,
    },
    Mul {
        left: Box<ExprWire>,
        right: Box<ExprWire>,
    },
    Neg {
        argument: Box<ExprWire>,
    },
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct BoxWire {
    index: usize,
    lo: String,
    hi: String,
}
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct EquationWire {
    index: usize,
    expression: ExprWire,
}
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct ProbeWire {
    point: Vec<String>,
    expected: Vec<String>,
}
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct SystemWire {
    schema: String,
    variable_count: usize,
    equation_count: usize,
    r#box: Vec<BoxWire>,
    equations: Vec<EquationWire>,
    probes: Vec<ProbeWire>,
}

fn rational(text: &str) -> Result<BigRational, SystemError> {
    parse_exact(text).map_err(|_| SystemError::Rational(text.to_owned()))
}

/// Sorted variable-index factors; repetitions encode squares. All degrees <= 2.
#[derive(Clone, Debug)]
struct Polynomial {
    terms: BTreeMap<Vec<usize>, BigRational>,
}

impl Polynomial {
    fn constant(value: BigRational) -> Self {
        let terms = if value.is_zero() {
            BTreeMap::new()
        } else {
            BTreeMap::from([(Vec::new(), value)])
        };
        Self { terms }
    }

    fn combine(mut self, other: Self) -> Result<Self, SystemError> {
        for (monomial, coefficient) in other.terms {
            *self.terms.entry(monomial).or_default() += coefficient;
        }
        self.terms.retain(|_, c| !c.is_zero());
        if self.terms.len() > MAX_TERMS {
            return Err(SystemError::ExpressionBound);
        }
        Ok(self)
    }

    fn multiply(self, other: Self) -> Result<Self, SystemError> {
        let mut terms = BTreeMap::<Vec<usize>, BigRational>::new();
        for (a, ca) in &self.terms {
            for (b, cb) in &other.terms {
                if a.len() + b.len() > 2 {
                    return Err(SystemError::Degree);
                }
                let mut monomial: Vec<_> = a.iter().chain(b).copied().collect();
                monomial.sort_unstable();
                *terms.entry(monomial).or_default() += ca * cb;
                if terms.len() > MAX_TERMS {
                    return Err(SystemError::ExpressionBound);
                }
            }
        }
        terms.retain(|_, c| !c.is_zero());
        Ok(Self { terms })
    }

    fn compile(expression: ExprWire, depth: usize) -> Result<Self, SystemError> {
        if depth > MAX_DEPTH {
            return Err(SystemError::ExpressionBound);
        }
        match expression {
            ExprWire::Constant { value } => Ok(Self::constant(rational(&value)?)),
            ExprWire::Variable { index } => {
                if index >= VARIABLES {
                    return Err(SystemError::Variable(index));
                }
                Ok(Self {
                    terms: BTreeMap::from([(vec![index], BigRational::one())]),
                })
            }
            ExprWire::Add { left, right } => {
                Self::compile(*left, depth + 1)?.combine(Self::compile(*right, depth + 1)?)
            }
            ExprWire::Mul { left, right } => {
                Self::compile(*left, depth + 1)?.multiply(Self::compile(*right, depth + 1)?)
            }
            ExprWire::Neg { argument } => {
                let mut polynomial = Self::compile(*argument, depth + 1)?;
                for coefficient in polynomial.terms.values_mut() {
                    *coefficient = -coefficient.clone();
                }
                Ok(polynomial)
            }
        }
    }

    // Indices and input dimensions are checked at the construction/API boundaries.
    fn eval(&self, point: &[BigRational]) -> BigRational {
        self.terms
            .iter()
            .map(|(monomial, coefficient)| {
                monomial
                    .iter()
                    .fold(coefficient.clone(), |value, &i| value * &point[i])
            })
            .sum()
    }

    fn range(&self, bounds: &[Interval]) -> Interval {
        self.terms
            .iter()
            .fold(Interval::point(BigRational::zero()), |sum, (m, c)| {
                let image = match m.as_slice() {
                    [] => Interval::point(BigRational::one()),
                    [i] => bounds[*i].clone(),
                    [i, j] if i == j => bounds[*i].sq(),
                    [i, j] => bounds[*i].mul(&bounds[*j]),
                    _ => m
                        .iter()
                        .fold(Interval::point(BigRational::one()), |image, &i| {
                            image.mul(&bounds[i])
                        }),
                };
                sum.add(&image.mul_scalar(c))
            })
    }

    fn derivative_range(&self, variable: usize, bounds: &[Interval]) -> Interval {
        let mut sum = Interval::point(BigRational::zero());
        for (m, c) in &self.terms {
            for (position, &index) in m.iter().enumerate() {
                if index != variable {
                    continue;
                }
                let mut image = Interval::point(c.clone());
                for (other, &factor) in m.iter().enumerate() {
                    if other != position {
                        image = image.mul(&bounds[factor]);
                    }
                }
                sum = sum.add(&image);
            }
        }
        sum
    }

    fn support(&self) -> BTreeSet<usize> {
        self.terms.keys().flat_map(|m| m.iter().copied()).collect()
    }
}

#[derive(Debug)]
pub struct ExecutableQuartetSystem {
    polynomials: Vec<Polynomial>,
    full_box: Vec<Interval>,
    input_sha256: String,
    probe_points: Vec<Vec<BigRational>>,
}

impl ExecutableQuartetSystem {
    pub fn from_bytes(bytes: &[u8]) -> Result<Self, SystemError> {
        if bytes.len() > MAX_BYTES {
            return Err(SystemError::InputTooLarge);
        }
        let wire: SystemWire =
            serde_json::from_slice(bytes).map_err(|e| SystemError::Json(e.to_string()))?;
        // The two admitted wire shapes have separately bound Lean exports.
        // A schema label alone does not establish the equations' semantics.
        let equation_count = match wire.schema.as_str() {
            "omega.mub6.szollosi-expressions.v1" => EQUATIONS,
            "omega.mub6.szollosi-gauged-expressions.v1" => GAUGED_EQUATIONS,
            _ => return Err(SystemError::Schema),
        };
        if wire.variable_count != VARIABLES
            || wire.equation_count != equation_count
            || wire.r#box.len() != VARIABLES
            || wire.equations.len() != equation_count
        {
            return Err(SystemError::Schema);
        }
        let mut full_box = Vec::with_capacity(VARIABLES);
        for (i, entry) in wire.r#box.into_iter().enumerate() {
            if entry.index != i {
                return Err(SystemError::Index {
                    kind: "coordinate".into(),
                    index: i,
                });
            }
            let lo = rational(&entry.lo)?;
            let hi = rational(&entry.hi)?;
            let radius = BigRational::from_integer(if i < 224 { 1.into() } else { 3.into() });
            if lo != -radius.clone() || hi != radius {
                return Err(SystemError::ContainingBox(i));
            }
            full_box.push(Interval::try_new(lo, hi).map_err(|_| SystemError::ContainingBox(i))?);
        }
        let mut polynomials = Vec::with_capacity(equation_count);
        for (i, entry) in wire.equations.into_iter().enumerate() {
            if entry.index != i {
                return Err(SystemError::Index {
                    kind: "equation".into(),
                    index: i,
                });
            }
            polynomials.push(Polynomial::compile(entry.expression, 0)?);
        }
        if wire.probes.len() != 3 {
            return Err(SystemError::Probes);
        }
        let mut probe_points = Vec::with_capacity(3);
        for (probe, entry) in wire.probes.into_iter().enumerate() {
            if entry.point.len() != VARIABLES || entry.expected.len() != equation_count {
                return Err(SystemError::Probes);
            }
            let point: Vec<_> = entry
                .point
                .iter()
                .map(|s| rational(s))
                .collect::<Result<_, _>>()?;
            for (equation, (polynomial, expected)) in
                polynomials.iter().zip(entry.expected).enumerate()
            {
                if polynomial.eval(&point) != rational(&expected)? {
                    return Err(SystemError::ProbeMismatch { probe, equation });
                }
            }
            probe_points.push(point);
        }
        Ok(Self {
            polynomials,
            full_box,
            input_sha256: format!("{:x}", Sha256::digest(bytes)),
            probe_points,
        })
    }

    pub fn eval(&self, point: &[BigRational]) -> Result<Vec<BigRational>, SystemError> {
        if point.len() != VARIABLES {
            return Err(SystemError::Dimension {
                expected: VARIABLES,
                found: point.len(),
            });
        }
        for value in point {
            if value.denom().is_zero() {
                return Err(SystemError::Rational("point has zero denominator".into()));
            }
            let reduced = value.reduced();
            if value.numer() != reduced.numer() || value.denom() != reduced.denom() {
                return Err(SystemError::Rational(
                    "point is not in canonical form".into(),
                ));
            }
        }
        Ok(self.polynomials.iter().map(|p| p.eval(point)).collect())
    }

    pub fn ranges(&self, bounds: &[Interval]) -> Result<Vec<Interval>, SystemError> {
        if bounds.len() != VARIABLES {
            return Err(SystemError::Dimension {
                expected: VARIABLES,
                found: bounds.len(),
            });
        }
        Ok(self.polynomials.iter().map(|p| p.range(bounds)).collect())
    }

    /// Sparse interval Jacobian, retaining one row for every equation.
    pub fn jacobian_ranges(
        &self,
        bounds: &[Interval],
    ) -> Result<Vec<BTreeMap<usize, Interval>>, SystemError> {
        if bounds.len() != VARIABLES {
            return Err(SystemError::Dimension {
                expected: VARIABLES,
                found: bounds.len(),
            });
        }
        Ok(self
            .polynomials
            .iter()
            .map(|p| {
                p.support()
                    .into_iter()
                    .map(|i| (i, p.derivative_range(i, bounds)))
                    .collect()
            })
            .collect())
    }

    fn coefficient_table(&self) -> Vec<CoefficientRow> {
        self.polynomials
            .iter()
            .enumerate()
            .map(|(index, polynomial)| CoefficientRow {
                index,
                terms: polynomial
                    .terms
                    .iter()
                    .map(|(factors, coefficient)| CoefficientTerm {
                        coefficient: to_canonical_string(coefficient),
                        factors: factors.clone(),
                    })
                    .collect(),
            })
            .collect()
    }

    /// Compare every compiled coefficient with the independent Lean-normalized table.
    /// The reference hash binds these bytes; analytic cover closure remains separate.
    pub fn inspect_full_box(&self, reference_bytes: &[u8]) -> Result<ReplayReceipt, SystemError> {
        if reference_bytes.len() > MAX_BYTES {
            return Err(SystemError::InputTooLarge);
        }
        let reference: Vec<CoefficientRow> = serde_json::from_slice(reference_bytes)
            .map_err(|e| SystemError::Json(e.to_string()))?;
        if reference.len() != self.polynomials.len() {
            return Err(SystemError::Schema);
        }
        let coefficients = self.coefficient_table();
        for (equation, (actual, expected)) in coefficients.iter().zip(&reference).enumerate() {
            if actual != expected {
                return Err(SystemError::CoefficientMismatch { equation });
            }
        }
        let ranges: Vec<_> = self
            .polynomials
            .iter()
            .map(|p| p.range(&self.full_box))
            .collect();
        let excluded_equation = ranges
            .iter()
            .position(|r| !r.contains(&BigRational::zero()));
        Ok(ReplayReceipt {
            schema: "omega.mub6.szollosi-native-replay.v1",
            status: if excluded_equation.is_some() {
                "FULL_BOX_RESIDUAL_EXCLUSION"
            } else {
                "UNRESOLVED_FULL_BOX"
            },
            input_sha256: self.input_sha256.clone(),
            coefficient_reference_sha256: format!("{:x}", Sha256::digest(reference_bytes)),
            checked_coefficient_rows: coefficients.len(),
            coefficients,
            variable_count: VARIABLES,
            equation_count: self.polynomials.len(),
            sparse_terms: self.polynomials.iter().map(|p| p.terms.len()).sum(),
            maximum_degree: self
                .polynomials
                .iter()
                .flat_map(|p| p.terms.keys().map(Vec::len))
                .max()
                .unwrap_or(0),
            parity_probes: self.probe_points.len(),
            parity_scalar_comparisons: self.probe_points.len() * self.polynomials.len(),
            excluded_equation,
            full_56_cell_and_cusp_calculation_complete: false,
            krawczyk_run: false,
            kernel_reflection_complete: false,
            intervals: ranges
                .iter()
                .enumerate()
                .map(|(index, r)| RangeReceipt {
                    index,
                    lo: to_canonical_string(r.lo()),
                    hi: to_canonical_string(r.hi()),
                })
                .collect(),
        })
    }
    /// Exact rectangular image for the complete system; this is a single box,
    /// without a cover, root-existence claim or native-data kernel reflection.
    pub fn contract_from_bytes(
        &self,
        reference_bytes: &[u8],
        request_bytes: &[u8],
    ) -> Result<RectangularReceipt, SystemError> {
        if request_bytes.len() > MAX_BYTES {
            return Err(SystemError::InputTooLarge);
        }
        let request: RectangularRequest =
            serde_json::from_slice(request_bytes).map_err(|e| SystemError::Json(e.to_string()))?;
        if request.schema != "omega.mub6.rectangular-request.v1"
            || request.variable_count != VARIABLES
            || request.equation_count != self.polynomials.len()
            || request.bounds.len() != VARIABLES
            || request.center.len() != VARIABLES
            || request.preconditioner.len() != VARIABLES
        {
            return Err(SystemError::Schema);
        }
        let reference = self.inspect_full_box(reference_bytes)?;
        let mut bounds = Vec::with_capacity(VARIABLES);
        let mut center = Vec::with_capacity(VARIABLES);
        let mut weights = Vec::with_capacity(VARIABLES);
        for (i, entry) in request.bounds.iter().enumerate() {
            if entry.index != i {
                return Err(SystemError::Index {
                    kind: "contractor coordinate".into(),
                    index: i,
                });
            }
            let lo = rational(&entry.lo)?;
            let hi = rational(&entry.hi)?;
            if lo < *self.full_box[i].lo() || hi > *self.full_box[i].hi() {
                return Err(SystemError::ContractorBox(i));
            }
            let interval = Interval::try_new(lo, hi).map_err(|_| SystemError::ContractorBox(i))?;
            let value = rational(&request.center[i])?;
            if !interval.contains(&value) {
                return Err(SystemError::CenterOutsideBox(i));
            }
            bounds.push(interval);
            center.push(value);
            let row = &request.preconditioner[i];
            if row.index != i {
                return Err(SystemError::Index {
                    kind: "preconditioner row".into(),
                    index: i,
                });
            }
            let mut entries = BTreeMap::new();
            let mut previous = None;
            for entry in &row.entries {
                let equation = entry.equation;
                let value = rational(&entry.coefficient)?;
                if equation >= self.polynomials.len()
                    || previous.is_some_and(|p| p >= equation)
                    || value.is_zero()
                {
                    return Err(SystemError::Preconditioner { row: i, equation });
                }
                previous = Some(equation);
                entries.insert(equation, value);
            }
            weights.push(entries);
        }
        let values = self.eval(&center)?;
        let jacobian = self.jacobian_ranges(&bounds)?;
        let images = rectangular_image(&center, &bounds, &values, &jacobian, &weights)?;
        let mut excluded_coordinate = None;
        let mut contracted_coordinates = Vec::new();
        let mut intersections = Vec::with_capacity(VARIABLES);
        for (i, (image, bound)) in images.iter().zip(&bounds).enumerate() {
            if image.hi() < bound.lo() || bound.hi() < image.lo() {
                if excluded_coordinate.is_none() {
                    excluded_coordinate = Some(i);
                }
                intersections.push(None);
            } else {
                let lo = image.lo().max(bound.lo()).clone();
                let hi = image.hi().min(bound.hi()).clone();
                let retained =
                    Interval::try_new(lo, hi).map_err(|_| SystemError::ContractorBox(i))?;
                if &retained != bound {
                    contracted_coordinates.push(i);
                }
                intersections.push(Some(range_receipt(i, &retained)));
            }
        }
        Ok(RectangularReceipt {
            schema: "omega.mub6.rectangular-replay.v1",
            status: if excluded_coordinate.is_some() {
                "EXCLUDED_BOX"
            } else if contracted_coordinates.is_empty() {
                "UNRESOLVED_BOX"
            } else {
                "CONTRACTED_UNRESOLVED_BOX"
            },
            input_sha256: self.input_sha256.clone(),
            coefficient_reference_sha256: reference.coefficient_reference_sha256,
            request_sha256: format!("{:x}", Sha256::digest(request_bytes)),
            checked_coefficient_rows: self.polynomials.len(),
            nonzero_preconditioner_entries: weights.iter().map(BTreeMap::len).sum(),
            request,
            center_residuals: values.iter().map(to_canonical_string).collect(),
            jacobian: jacobian
                .iter()
                .enumerate()
                .map(|(index, row)| JacobianRow {
                    index,
                    entries: row
                        .iter()
                        .map(|(&k, interval)| range_receipt(k, interval))
                        .collect(),
                })
                .collect(),
            images: images
                .iter()
                .enumerate()
                .map(|(i, interval)| range_receipt(i, interval))
                .collect(),
            intersections,
            excluded_coordinate,
            contracted_coordinates,
            root_existence_claimed: false,
            full_56_cell_and_cusp_calculation_complete: false,
            kernel_reflection_complete: false,
        })
    }

    /// Deterministic first linear pivots; this is not a Jacobian inverse.
    pub fn contract_full_box_linear(
        &self,
        reference_bytes: &[u8],
    ) -> Result<RectangularReceipt, SystemError> {
        let mut rows: Vec<_> = (0..VARIABLES)
            .map(|index| PreconditionerRow {
                index,
                entries: Vec::new(),
            })
            .collect();
        for (equation, polynomial) in self.polynomials.iter().enumerate() {
            if polynomial.terms.keys().any(|m| m.len() > 1) {
                continue;
            }
            if let Some((factor, coefficient)) = polynomial.terms.iter().find(|(m, _)| m.len() == 1)
            {
                let i = factor[0];
                if rows[i].entries.is_empty() {
                    rows[i].entries.push(PreconditionerEntry {
                        equation,
                        coefficient: to_canonical_string(&(BigRational::one() / coefficient)),
                    });
                }
            }
        }
        let request = RectangularRequest {
            schema: "omega.mub6.rectangular-request.v1".into(),
            variable_count: VARIABLES,
            equation_count: self.polynomials.len(),
            bounds: self
                .full_box
                .iter()
                .enumerate()
                .map(|(i, b)| range_receipt(i, b))
                .collect(),
            center: self
                .full_box
                .iter()
                .map(|b| to_canonical_string(&b.mid()))
                .collect(),
            preconditioner: rows,
        };
        let bytes = serde_json::to_vec(&request).map_err(|e| SystemError::Json(e.to_string()))?;
        self.contract_from_bytes(reference_bytes, &bytes)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct CoefficientTerm {
    pub coefficient: String,
    pub factors: Vec<usize>,
}
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct CoefficientRow {
    pub index: usize,
    pub terms: Vec<CoefficientTerm>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct RangeReceipt {
    pub index: usize,
    pub lo: String,
    pub hi: String,
}
#[derive(Debug, Serialize)]
pub struct ReplayReceipt {
    pub schema: &'static str,
    pub status: &'static str,
    pub input_sha256: String,
    pub coefficient_reference_sha256: String,
    pub checked_coefficient_rows: usize,
    pub coefficients: Vec<CoefficientRow>,
    pub variable_count: usize,
    pub equation_count: usize,
    pub sparse_terms: usize,
    pub maximum_degree: usize,
    pub parity_probes: usize,
    pub parity_scalar_comparisons: usize,
    pub excluded_equation: Option<usize>,
    pub full_56_cell_and_cusp_calculation_complete: bool,
    pub krawczyk_run: bool,
    pub kernel_reflection_complete: bool,
    pub intervals: Vec<RangeReceipt>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct PreconditionerEntry {
    pub equation: usize,
    pub coefficient: String,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct PreconditionerRow {
    pub index: usize,
    pub entries: Vec<PreconditionerEntry>,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RectangularRequest {
    pub schema: String,
    pub variable_count: usize,
    pub equation_count: usize,
    pub bounds: Vec<RangeReceipt>,
    pub center: Vec<String>,
    pub preconditioner: Vec<PreconditionerRow>,
}
#[derive(Debug, Serialize)]
pub struct JacobianRow {
    pub index: usize,
    pub entries: Vec<RangeReceipt>,
}
#[derive(Debug, Serialize)]
pub struct RectangularReceipt {
    pub schema: &'static str,
    pub status: &'static str,
    pub input_sha256: String,
    pub coefficient_reference_sha256: String,
    pub request_sha256: String,
    pub checked_coefficient_rows: usize,
    pub nonzero_preconditioner_entries: usize,
    pub request: RectangularRequest,
    pub center_residuals: Vec<String>,
    pub jacobian: Vec<JacobianRow>,
    pub images: Vec<RangeReceipt>,
    pub intersections: Vec<Option<RangeReceipt>>,
    pub excluded_coordinate: Option<usize>,
    pub contracted_coordinates: Vec<usize>,
    pub root_existence_claimed: bool,
    pub full_56_cell_and_cusp_calculation_complete: bool,
    pub kernel_reflection_complete: bool,
}

fn range_receipt(index: usize, interval: &Interval) -> RangeReceipt {
    RangeReceipt {
        index,
        lo: to_canonical_string(interval.lo()),
        hi: to_canonical_string(interval.hi()),
    }
}

/// Sparse evaluation of c-Cf(c)+(I-CJ(X))(X-c), preserving cancellations.
/// Dimensions, coordinate indices and equation indices are checked before access.
fn rectangular_image(
    center: &[BigRational],
    bounds: &[Interval],
    values: &[BigRational],
    jacobian: &[BTreeMap<usize, Interval>],
    weights: &[BTreeMap<usize, BigRational>],
) -> Result<Vec<Interval>, SystemError> {
    let n = bounds.len();
    let m = values.len();
    for found in [center.len(), weights.len()] {
        if found != n {
            return Err(SystemError::Dimension { expected: n, found });
        }
    }
    if jacobian.len() != m {
        return Err(SystemError::Dimension {
            expected: m,
            found: jacobian.len(),
        });
    }
    for row in jacobian {
        if let Some(&i) = row.keys().find(|&&i| i >= n) {
            return Err(SystemError::Variable(i));
        }
    }
    for (i, row) in weights.iter().enumerate() {
        if let Some(&e) = row.keys().find(|&&e| e >= m) {
            return Err(SystemError::Preconditioner {
                row: i,
                equation: e,
            });
        }
    }
    let mut images = Vec::with_capacity(n);
    for (i, row) in weights.iter().enumerate() {
        if !bounds[i].contains(&center[i]) {
            return Err(SystemError::CenterOutsideBox(i));
        }
        let mut offset = center[i].clone();
        let mut matrix = BTreeMap::from([(i, Interval::point(BigRational::one()))]);
        for (&e, coefficient) in row {
            offset -= coefficient * &values[e];
            for (&k, derivative) in &jacobian[e] {
                let current = matrix
                    .entry(k)
                    .or_insert_with(|| Interval::point(BigRational::zero()));
                *current = current.sub(&derivative.mul_scalar(coefficient));
            }
        }
        let mut image = Interval::point(offset);
        for (k, value) in matrix {
            if value.lo().is_zero() && value.hi().is_zero() {
                continue;
            }
            image = image.add(&value.mul(&bounds[k].sub(&Interval::point(center[k].clone()))));
        }
        images.push(image);
    }
    Ok(images)
}

#[cfg(test)]
mod tests {
    use super::*;
    const SYSTEM: &[u8] = include_bytes!(
        "../../../../../papers/derivations/mub6/artifacts/mub_szollosi_executable_system.json"
    );

    const COEFFICIENTS: &[u8] = include_bytes!(
        "../../../../../papers/derivations/mub6/artifacts/mub_szollosi_lean_coefficients.json"
    );

    const GAUGED_SYSTEM: &[u8] = include_bytes!(
        "../../../../../papers/derivations/mub6/artifacts/mub_szollosi_gauged_executable_system.json"
    );
    const GAUGED_COEFFICIENTS: &[u8] = include_bytes!(
        "../../../../../papers/derivations/mub6/artifacts/mub_szollosi_gauged_lean_coefficients.json"
    );

    #[test]
    fn gauged_export_retains_every_original_coefficient_and_probe() {
        let base = ExecutableQuartetSystem::from_bytes(SYSTEM).unwrap();
        let gauged = ExecutableQuartetSystem::from_bytes(GAUGED_SYSTEM).unwrap();
        let receipt = gauged.inspect_full_box(GAUGED_COEFFICIENTS).unwrap();
        assert_eq!(&receipt.coefficients[..EQUATIONS], base.coefficient_table());
        assert_eq!(receipt.equation_count, GAUGED_EQUATIONS);
        assert_eq!(receipt.checked_coefficient_rows, GAUGED_EQUATIONS);
        assert_eq!(receipt.parity_scalar_comparisons, 1998);
        assert_eq!(receipt.sparse_terms, 5320);
        assert_eq!(receipt.maximum_degree, 2);
        assert_eq!(receipt.status, "UNRESOLVED_FULL_BOX");
        assert!(!receipt.kernel_reflection_complete);
    }

    #[test]
    fn gauged_shape_requires_its_exact_schema_and_equation_count() {
        for (schema, count) in [
            ("omega.mub6.szollosi-expressions.v1", 666),
            ("omega.mub6.szollosi-gauged-expressions.v1", 618),
            ("omega.mub6.szollosi-gauged-expressions.v1", 667),
            ("omega.mub6.unspecified.v1", 666),
        ] {
            let mut wire: serde_json::Value = serde_json::from_slice(GAUGED_SYSTEM).unwrap();
            wire["schema"] = schema.into();
            wire["equation_count"] = count.into();
            assert!(matches!(
                ExecutableQuartetSystem::from_bytes(&serde_json::to_vec(&wire).unwrap()),
                Err(SystemError::Schema)
            ));
        }
    }

    #[test]
    fn gauged_reference_rejects_missing_or_changed_balance_rows() {
        let gauged = ExecutableQuartetSystem::from_bytes(GAUGED_SYSTEM).unwrap();
        assert!(matches!(
            gauged.inspect_full_box(COEFFICIENTS),
            Err(SystemError::Schema)
        ));
        let mut reference: serde_json::Value = serde_json::from_slice(GAUGED_COEFFICIENTS).unwrap();
        reference[642]["terms"][0]["coefficient"] = "-5".into();
        assert!(matches!(
            gauged.inspect_full_box(&serde_json::to_vec(&reference).unwrap()),
            Err(SystemError::CoefficientMismatch { equation: 642 })
        ));
    }

    #[test]
    fn gauged_request_cannot_use_the_base_equation_count_or_out_of_range_weights() {
        let gauged = ExecutableQuartetSystem::from_bytes(GAUGED_SYSTEM).unwrap();
        let parent = gauged
            .contract_full_box_linear(GAUGED_COEFFICIENTS)
            .unwrap();
        let mut request = parent.request;
        request.equation_count = EQUATIONS;
        assert!(matches!(
            gauged.contract_from_bytes(GAUGED_COEFFICIENTS, &serde_json::to_vec(&request).unwrap()),
            Err(SystemError::Schema)
        ));
        request.equation_count = GAUGED_EQUATIONS;
        request.preconditioner[0].entries = vec![PreconditionerEntry {
            equation: GAUGED_EQUATIONS,
            coefficient: "1".into(),
        }];
        assert!(matches!(
            gauged.contract_from_bytes(GAUGED_COEFFICIENTS, &serde_json::to_vec(&request).unwrap()),
            Err(SystemError::Preconditioner {
                row: 0,
                equation: GAUGED_EQUATIONS
            })
        ));
    }

    #[test]
    fn balance_excludes_a_transition_row_whose_real_entries_are_at_most_one_half() {
        let gauged = ExecutableQuartetSystem::from_bytes(GAUGED_SYSTEM).unwrap();
        let parent = gauged
            .contract_full_box_linear(GAUGED_COEFFICIENTS)
            .unwrap();
        assert_eq!(parent.nonzero_preconditioner_entries, 74);
        assert_eq!(parent.contracted_coordinates.len(), 48);
        let mut request = parent.request;
        request.bounds = parent
            .intersections
            .into_iter()
            .map(Option::unwrap)
            .collect();
        for (i, b) in request.bounds.iter().enumerate() {
            request.center[i] = if b.lo == b.hi {
                b.lo.clone()
            } else {
                "0".into()
            };
        }
        for j in 0..6 {
            request.bounds[368 + 2 * j].lo = "-1/2".into();
            request.bounds[368 + 2 * j].hi = "1/2".into();
        }
        let receipt = gauged
            .contract_from_bytes(GAUGED_COEFFICIENTS, &serde_json::to_vec(&request).unwrap())
            .unwrap();
        assert_eq!(receipt.status, "EXCLUDED_BOX");
        assert_eq!(receipt.excluded_coordinate, Some(368));
        assert_eq!(receipt.images[368].lo, "7/2");
        assert_eq!(receipt.images[368].hi, "17/2");
        assert!(receipt.intersections[368].is_none());
        assert!(!receipt.root_existence_claimed);
        assert!(!receipt.full_56_cell_and_cusp_calculation_complete);
        assert!(!receipt.kernel_reflection_complete);
    }

    #[test]
    fn full_export_replays_all_lean_probe_values() {
        let system = ExecutableQuartetSystem::from_bytes(SYSTEM).unwrap();
        let receipt = system.inspect_full_box(COEFFICIENTS).unwrap();
        assert_eq!(receipt.parity_scalar_comparisons, 1854);
        assert_eq!(receipt.checked_coefficient_rows, EQUATIONS);
        assert_eq!(
            receipt
                .coefficients
                .iter()
                .map(|row| row.terms.len())
                .sum::<usize>(),
            5128
        );
        assert_eq!(receipt.maximum_degree, 2);
        assert_eq!(receipt.status, "UNRESOLVED_FULL_BOX");
        assert_eq!(receipt.intervals.len(), EQUATIONS);
        assert!(!receipt.full_56_cell_and_cusp_calculation_complete);
        assert!(!receipt.kernel_reflection_complete);
    }

    #[test]
    fn complete_coefficients_detect_a_change_invisible_to_all_three_probes() {
        let mut wire: serde_json::Value = serde_json::from_slice(SYSTEM).unwrap();
        let delta = serde_json::json!({"op":"mul",
            "left":{"op":"add","left":{"op":"variable","index":0},"right":{"op":"variable","index":1}},
            "right":{"op":"add","left":{"op":"add","left":{"op":"variable","index":0},"right":{"op":"neg","argument":{"op":"variable","index":2}}},"right":{"op":"constant","value":"2/7"}}});
        let original = wire["equations"][0]["expression"].clone();
        wire["equations"][0]["expression"] =
            serde_json::json!({"op":"add","left":original,"right":delta});
        // (x0+x1)(x0-x2+2/7) vanishes at every stored probe, yet changes the polynomial.
        let changed =
            ExecutableQuartetSystem::from_bytes(&serde_json::to_vec(&wire).unwrap()).unwrap();
        assert!(matches!(
            changed.inspect_full_box(COEFFICIENTS),
            Err(SystemError::CoefficientMismatch { equation: 0 })
        ));
        let baseline = ExecutableQuartetSystem::from_bytes(SYSTEM).unwrap();
        let mut point = vec![BigRational::zero(); VARIABLES];
        point[0] = BigRational::one();
        assert_ne!(
            changed.eval(&point).unwrap()[0],
            baseline.eval(&point).unwrap()[0]
        );
        let mut reference: serde_json::Value = serde_json::from_slice(COEFFICIENTS).unwrap();
        reference[0]["terms"][0]["coefficient"] = "99".into();
        assert!(matches!(
            baseline.inspect_full_box(&serde_json::to_vec(&reference).unwrap()),
            Err(SystemError::CoefficientMismatch { equation: 0 })
        ));
        reference.as_array_mut().unwrap().pop();
        assert!(matches!(
            baseline.inspect_full_box(&serde_json::to_vec(&reference).unwrap()),
            Err(SystemError::Schema)
        ));
    }

    #[test]
    fn wrong_raw_overlap_target_is_rejected_by_lean_parity() {
        let mut wire: serde_json::Value = serde_json::from_slice(SYSTEM).unwrap();
        wire["equations"][510]["expression"]["right"]["argument"]["value"] = "5".into();
        assert!(matches!(
            ExecutableQuartetSystem::from_bytes(&serde_json::to_vec(&wire).unwrap()),
            Err(SystemError::ProbeMismatch {
                probe: 0,
                equation: 510
            })
        ));
    }

    #[test]
    fn missing_equations_bad_indices_and_restricted_box_are_refused() {
        let wire: serde_json::Value = serde_json::from_slice(SYSTEM).unwrap();
        let mut missing = wire.clone();
        missing["equations"].as_array_mut().unwrap().pop();
        assert!(matches!(
            ExecutableQuartetSystem::from_bytes(&serde_json::to_vec(&missing).unwrap()),
            Err(SystemError::Schema)
        ));
        let mut duplicate = wire.clone();
        duplicate["equations"][1]["index"] = 0.into();
        assert!(matches!(
            ExecutableQuartetSystem::from_bytes(&serde_json::to_vec(&duplicate).unwrap()),
            Err(SystemError::Index { .. })
        ));
        let mut restricted = wire;
        restricted["box"][0]["lo"] = "0".into();
        assert!(matches!(
            ExecutableQuartetSystem::from_bytes(&serde_json::to_vec(&restricted).unwrap()),
            Err(SystemError::ContainingBox(0))
        ));
    }

    #[test]
    fn malformed_expression_and_rational_inputs_return_errors() {
        let wire: serde_json::Value = serde_json::from_slice(SYSTEM).unwrap();
        let mut invalid = wire.clone();
        invalid["equations"][0]["expression"] = serde_json::json!({"op":"variable","index":440});
        assert!(matches!(
            ExecutableQuartetSystem::from_bytes(&serde_json::to_vec(&invalid).unwrap()),
            Err(SystemError::Variable(440))
        ));
        for text in ["1/1", "0.5", "1/0"] {
            let mut invalid = wire.clone();
            invalid["box"][0]["lo"] = text.into();
            assert!(matches!(
                ExecutableQuartetSystem::from_bytes(&serde_json::to_vec(&invalid).unwrap()),
                Err(SystemError::Rational(_))
            ));
        }
        let mut cubic = wire;
        cubic["equations"][0]["expression"] = serde_json::json!({"op":"mul","left":{"op":"variable","index":0},"right":{"op":"mul","left":{"op":"variable","index":1},"right":{"op":"variable","index":2}}});
        assert!(matches!(
            ExecutableQuartetSystem::from_bytes(&serde_json::to_vec(&cubic).unwrap()),
            Err(SystemError::Degree)
        ));
    }

    #[test]
    fn interval_images_contain_rational_points_and_derivatives_match_secants() {
        let system = ExecutableQuartetSystem::from_bytes(SYSTEM).unwrap();
        let ranges = system.ranges(&system.full_box).unwrap();
        for point in &system.probe_points {
            for (range, value) in ranges.iter().zip(system.eval(point).unwrap()) {
                assert!(range.contains(&value));
            }
        }
        let point = &system.probe_points[1];
        let point_box: Vec<_> = point.iter().cloned().map(Interval::point).collect();
        let jacobian = system.jacobian_ranges(&point_box).unwrap();
        for equation in [0, 4, 6, 78, 222, 294, 510, 617] {
            for (&variable, derivative) in &jacobian[equation] {
                let mut plus = point.clone();
                plus[variable] += BigRational::one();
                let mut minus = point.clone();
                minus[variable] -= BigRational::one();
                let secant = (system.polynomials[equation].eval(&plus)
                    - system.polynomials[equation].eval(&minus))
                    / BigRational::from_integer(2.into());
                assert_eq!(derivative.lo(), &secant);
                assert_eq!(derivative.hi(), &secant);
            }
        }
        assert!(matches!(
            system.eval(&[]),
            Err(SystemError::Dimension { .. })
        ));
        let invalid_point = vec![BigRational::new_raw(1.into(), 0.into()); VARIABLES];
        assert!(matches!(
            system.eval(&invalid_point),
            Err(SystemError::Rational(_))
        ));
        let unreduced_point = vec![BigRational::new_raw(2.into(), 2.into()); VARIABLES];
        assert!(matches!(
            system.eval(&unreduced_point),
            Err(SystemError::Rational(_))
        ));
        assert!(matches!(
            system.ranges(&[]),
            Err(SystemError::Dimension { .. })
        ));
    }
    fn q(n: i64, d: i64) -> BigRational {
        BigRational::new(n.into(), d.into())
    }

    #[test]
    fn rectangular_image_matches_checked_separation_and_contact_examples() {
        let center = vec![q(3, 2), q(0, 1)];
        let bounds = vec![
            Interval::new(q(1, 1), q(2, 1)),
            Interval::new(q(-2, 1), q(2, 1)),
        ];
        let values = vec![q(3, 2), q(3, 2), q(0, 1)];
        let jac = vec![
            BTreeMap::from([(0, Interval::point(q(1, 1))), (1, Interval::point(q(1, 1)))]),
            BTreeMap::from([
                (0, Interval::point(q(1, 1))),
                (1, Interval::point(q(-1, 1))),
            ]),
            BTreeMap::from([(0, bounds[1].clone()), (1, bounds[0].clone())]),
        ];
        let weights = vec![
            BTreeMap::from([(0, q(1, 2)), (1, q(1, 2))]),
            BTreeMap::from([(0, q(1, 2)), (1, q(-1, 2))]),
        ];
        let images = rectangular_image(&center, &bounds, &values, &jac, &weights).unwrap();
        assert_eq!(images, vec![Interval::point(q(0, 1)); 2]);
        assert!(images[0].hi() < bounds[0].lo());
        let touching = vec![
            Interval::new(q(0, 1), q(1, 1)),
            Interval::new(q(-1, 1), q(1, 1)),
        ];
        let images = rectangular_image(
            &[q(0, 1), q(0, 1)],
            &touching,
            &[q(0, 1), q(0, 1), q(0, 1)],
            &jac,
            &weights,
        )
        .unwrap();
        assert!(touching[0].contains(images[0].lo()));
        assert_eq!(images[0].hi(), touching[0].lo());
    }

    #[test]
    fn overdetermined_strict_inclusion_does_not_supply_a_common_root() {
        // f=(x,1), C=(1,0): K={0} lies strictly inside [-1,1], while f1 is always one.
        let images = rectangular_image(
            &[q(0, 1)],
            &[Interval::new(q(-1, 1), q(1, 1))],
            &[q(0, 1), q(1, 1)],
            &[
                BTreeMap::from([(0, Interval::point(q(1, 1)))]),
                BTreeMap::new(),
            ],
            &[BTreeMap::from([(0, q(1, 1))])],
        )
        .unwrap();
        assert_eq!(images[0], Interval::point(q(0, 1)));
        assert_ne!(q(1, 1), q(0, 1));
    }

    #[test]
    fn quadratic_image_keeps_a_known_root_and_exact_endpoints() {
        // f=x^2-9/4, center=3/2, J([1,2])=[2,4], C=1/3.
        let images = rectangular_image(
            &[q(3, 2)],
            &[Interval::new(q(1, 1), q(2, 1))],
            &[q(0, 1)],
            &[BTreeMap::from([(0, Interval::new(q(2, 1), q(4, 1)))])],
            &[BTreeMap::from([(0, q(1, 3))])],
        )
        .unwrap();
        assert_eq!(images[0], Interval::new(q(4, 3), q(5, 3)));
        assert!(images[0].contains(&q(3, 2)));
    }

    #[test]
    fn rectangular_dimensions_and_out_of_range_indices_are_refused() {
        let bounds = [Interval::new(q(-1, 1), q(1, 1))];
        assert!(matches!(
            rectangular_image(
                &[],
                &bounds,
                &[q(0, 1)],
                &[BTreeMap::new()],
                &[BTreeMap::new()]
            ),
            Err(SystemError::Dimension { .. })
        ));
        assert!(matches!(
            rectangular_image(
                &[q(0, 1)],
                &bounds,
                &[q(0, 1)],
                &[BTreeMap::from([(1, Interval::point(q(1, 1)))])],
                &[BTreeMap::new()]
            ),
            Err(SystemError::Variable(1))
        ));
        assert!(matches!(
            rectangular_image(
                &[q(0, 1)],
                &bounds,
                &[q(0, 1)],
                &[BTreeMap::new()],
                &[BTreeMap::from([(1, q(1, 1))])]
            ),
            Err(SystemError::Preconditioner { .. })
        ));
        assert!(matches!(
            rectangular_image(
                &[q(2, 1)],
                &bounds,
                &[q(0, 1)],
                &[BTreeMap::new()],
                &[BTreeMap::new()]
            ),
            Err(SystemError::CenterOutsideBox(0))
        ));
    }

    #[test]
    fn complete_native_rectangular_box_is_deterministic_and_scoped() {
        let system = ExecutableQuartetSystem::from_bytes(SYSTEM).unwrap();
        let a = system.contract_full_box_linear(COEFFICIENTS).unwrap();
        let b = system.contract_full_box_linear(COEFFICIENTS).unwrap();
        assert_eq!(
            serde_json::to_vec(&a).unwrap(),
            serde_json::to_vec(&b).unwrap()
        );
        assert_eq!(a.checked_coefficient_rows, 618);
        assert_eq!(a.jacobian.len(), 618);
        assert_eq!(a.images.len(), 440);
        assert_eq!(a.intersections.len(), 440);
        assert!(a.nonzero_preconditioner_entries > 0);
        assert!(!a.root_existence_claimed);
        assert!(!a.full_56_cell_and_cusp_calculation_complete);
        assert!(!a.kernel_reflection_complete);
    }

    #[test]
    fn contractor_wire_refuses_bad_centers_boxes_and_weights() {
        let system = ExecutableQuartetSystem::from_bytes(SYSTEM).unwrap();
        let receipt = system.contract_full_box_linear(COEFFICIENTS).unwrap();
        let wire = serde_json::to_value(&receipt.request).unwrap();
        let mut bad = wire.clone();
        bad["center"][0] = "99".into();
        assert!(matches!(
            system.contract_from_bytes(COEFFICIENTS, &serde_json::to_vec(&bad).unwrap()),
            Err(SystemError::CenterOutsideBox(0))
        ));
        let mut bad = wire.clone();
        bad["bounds"][0]["lo"] = "1".into();
        bad["bounds"][0]["hi"] = "0".into();
        assert!(matches!(
            system.contract_from_bytes(COEFFICIENTS, &serde_json::to_vec(&bad).unwrap()),
            Err(SystemError::ContractorBox(0))
        ));
        let mut bad = wire.clone();
        bad["bounds"][0]["lo"] = "-2".into();
        assert!(matches!(
            system.contract_from_bytes(COEFFICIENTS, &serde_json::to_vec(&bad).unwrap()),
            Err(SystemError::ContractorBox(0))
        ));
        for entries in [
            serde_json::json!([{"equation":618,"coefficient":"1"}]),
            serde_json::json!([{"equation":0,"coefficient":"1"},{"equation":0,"coefficient":"1"}]),
            serde_json::json!([{"equation":0,"coefficient":"0"}]),
        ] {
            let mut bad = wire.clone();
            bad["preconditioner"][0]["entries"] = entries;
            assert!(matches!(
                system.contract_from_bytes(COEFFICIENTS, &serde_json::to_vec(&bad).unwrap()),
                Err(SystemError::Preconditioner { .. })
            ));
        }
        let mut bad = wire.clone();
        bad["center"][0] = "1/1".into();
        assert!(matches!(
            system.contract_from_bytes(COEFFICIENTS, &serde_json::to_vec(&bad).unwrap()),
            Err(SystemError::Rational(_))
        ));
        let mut bad = wire.clone();
        bad["preconditioner"][1]["index"] = 0.into();
        assert!(matches!(
            system.contract_from_bytes(COEFFICIENTS, &serde_json::to_vec(&bad).unwrap()),
            Err(SystemError::Index { .. })
        ));
        let mut bad = wire.clone();
        bad["center"].as_array_mut().unwrap().pop();
        assert!(matches!(
            system.contract_from_bytes(COEFFICIENTS, &serde_json::to_vec(&bad).unwrap()),
            Err(SystemError::Schema)
        ));
        let mut bad = wire.clone();
        bad["variable_count"] = true.into();
        assert!(matches!(
            system.contract_from_bytes(COEFFICIENTS, &serde_json::to_vec(&bad).unwrap()),
            Err(SystemError::Json(_))
        ));
    }
}
