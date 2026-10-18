//! MUB(6) balanced lift: independent replay of the pinned 648-equation, 320-coordinate table.
//!
//! The table `balanced_quadratic_coefficients_20261011.jsonl` (010_mub6 artifacts) is parsed
//! with its SHA-256 digest pinned. Every row is then regenerated here from the definitions in
//! `MubBalancedQuadraticPolynomials.lean` and `MubQuadraticLiftPolynomials.lean`: the raw
//! Hadamards `H = fromBlocks E B C D`, `U`, `V` in the gauge with first rows (and the first
//! column of `H`) equal to one, the three transition cores `W_a` completed by the sum-six
//! rule, and the four equation blocks
//!
//! * codes `36a+6i+j`: `|A_ij|^2 - 1` for `A in (H, U, V)`;
//! * codes `108 + 2(36a+6i+j) + b`: component `b` of `(A^H A - 6 I)_ij`;
//! * codes `324 + 2(36a+6i+j) + b`: component `b` of `(W_a - T_a)_ij` with
//!   `T = (H^H U, H^H V, U^H V)`;
//! * codes `540 + 36a+6i+j`: `|W_a,ij|^2 - 6`.
//!
//! The regenerated rows are compared with the table term by term over the rationals.
//! Evaluation at a point uses exact arithmetic in Q(zeta_24).
//!
//! Checked here: the rows equal the regenerated polynomials; which rows are empty and why;
//! the Hermitian-duplicate and diagonal-sum identities among the Gram rows; the value of every
//! row at the point encoded from an exact triple `(H, U, V)`; and box membership of that point.
//! Not checked here: the Lean theorem `exists_quartet_iff_balanced_polynomials` (a Lean kernel
//! run), or the existence or non-existence of a fourth mutually unbiased basis.
//!
//! AuthorityEffect: None
//! Firewall Line: NOT MUB(6)=3, NOT MUB(6)<=3; stated region only; mints no authority

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use omega_number_theory::cyclotomic::Cyc24;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::btree_map::Entry;
use std::collections::{BTreeMap, BTreeSet};
use thiserror::Error;

pub const VARIABLES: usize = 320;
pub const EQUATIONS: usize = 648;
/// First coordinate index of the transition cores `W_a[i][j]`, `a < 3`, `i, j < 5`.
pub const CORE_START: usize = 170;
/// First coordinate index of the `D` block of `H` (rows 3..5, columns 3..5).
pub const D_START: usize = 152;
pub const SCHEMA: &str = "mub6.balanced_quadratic.coefficients.v1";
pub const COEFFICIENT_SHA256: &str =
    "cb552359467ede318508279b62b7203e65b3c510abf77b5492d3d3f4a49c217d";
/// Half-width of the box on a transition-core coordinate (above `sqrt 6`).
pub const CORE_RADIUS: (i64, i64) = (10035, 4096);

pub const MODULUS_START: usize = 0;
pub const GRAM_START: usize = 108;
pub const GRAPH_START: usize = 324;
pub const TRANSITION_MODULUS_START: usize = 540;

/// A monomial: the sorted list of coordinate indices it multiplies, with repetition.
pub type Monomial = Vec<usize>;
/// A sparse polynomial with rational coefficients. Zero coefficients are never stored.
pub type RationalPoly = BTreeMap<Monomial, BigRational>;
/// A 6 x 6 matrix over Q(zeta_24), row-major.
pub type ExactMatrix = Vec<Vec<Cyc24>>;

#[derive(Debug, Error)]
pub enum BalancedReplayError {
    #[error("coefficient table digest {0} does not match the pinned digest")]
    InputHash(String),
    #[error("json: {0}")]
    Json(#[from] serde_json::Error),
    #[error("table shape: {0}")]
    Shape(String),
    #[error("rational literal is not canonical p/q: {0}")]
    Rational(String),
    #[error("matrix input: {0}")]
    Matrix(String),
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Header {
    kind: String,
    schema: String,
    authority_effect: String,
    variable_count: usize,
    equation_count: usize,
    coordinate_codes: Vec<usize>,
    equation_codes: Vec<usize>,
    coordinate_bounds: Vec<[String; 2]>,
    probe_count: usize,
    probe_definitions: Vec<String>,
    semantics: String,
    determinant_inequality: serde_json::Value,
    kernel_reflected_file: bool,
    infeasibility_claimed: bool,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Row {
    kind: String,
    id: usize,
    degree_bound: usize,
    term_count: usize,
    terms: Vec<(String, Vec<usize>)>,
    probe_values: Vec<String>,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Tail {
    kind: String,
    equations: usize,
    total_terms: usize,
    maximum_terms: usize,
}

const PROBE_DEFINITIONS: [&str; 4] = [
    "0",
    "(i mod 17 - 7)/13",
    "1 if i even else -1",
    "((7*i+3) mod 19 - 8)/11",
];
const SEMANTICS: &str = "Sum coefficient times product of factor coordinates; every equation equals zero.";

/// The pinned table, parsed and checked for shape, canonical rationals and probe values.
#[derive(Debug, Clone)]
pub struct BalancedTable {
    pub rows: Vec<RationalPoly>,
    pub total_terms: usize,
    pub maximum_terms: usize,
}

fn rational(text: &str) -> Result<BigRational, BalancedReplayError> {
    let bad = || BalancedReplayError::Rational(text.to_string());
    let (n, d) = text.split_once('/').ok_or_else(bad)?;
    let n: BigInt = n.parse().map_err(|_| bad())?;
    let d: BigInt = d.parse().map_err(|_| bad())?;
    if !d.is_positive() {
        return Err(bad());
    }
    let q = BigRational::new(n, d);
    if format!("{}/{}", q.numer(), q.denom()) != text {
        return Err(bad());
    }
    Ok(q)
}

fn canonical(q: &BigRational) -> String {
    format!("{}/{}", q.numer(), q.denom())
}

fn probe(p: usize, i: usize) -> BigRational {
    let r = |n: i64, d: i64| BigRational::new(n.into(), d.into());
    let i = i as i64;
    match p {
        0 => BigRational::zero(),
        1 => r(i % 17 - 7, 13),
        2 => r(if i % 2 == 0 { 1 } else { -1 }, 1),
        _ => r((7 * i + 3) % 19 - 8, 11),
    }
}

/// Upper end of the box on coordinate `v` (the lower end is its negative).
pub fn coordinate_radius(v: usize) -> BigRational {
    if v < CORE_START {
        BigRational::one()
    } else {
        BigRational::new(CORE_RADIUS.0.into(), CORE_RADIUS.1.into())
    }
}

fn shape(message: impl Into<String>) -> BalancedReplayError {
    BalancedReplayError::Shape(message.into())
}

impl BalancedTable {
    /// Parses the pinned table. Any digest, shape, literal or probe mismatch is an error.
    pub fn from_bytes(bytes: &[u8]) -> Result<Self, BalancedReplayError> {
        let digest = format!("{:x}", Sha256::digest(bytes));
        if digest != COEFFICIENT_SHA256 {
            return Err(BalancedReplayError::InputHash(digest));
        }
        Self::decode(bytes)
    }

    fn decode(bytes: &[u8]) -> Result<Self, BalancedReplayError> {
        let text = std::str::from_utf8(bytes).map_err(|_| shape("table is not UTF-8"))?;
        let lines: Vec<&str> = text.lines().collect();
        if lines.len() != EQUATIONS + 2 {
            return Err(shape(format!("expected {} lines, found {}", EQUATIONS + 2, lines.len())));
        }
        let header: Header = serde_json::from_str(lines[0])?;
        let expected_codes = |n: usize| (0..n).collect::<Vec<_>>();
        if header.kind != "header"
            || header.schema != SCHEMA
            || header.authority_effect != "None"
            || header.variable_count != VARIABLES
            || header.equation_count != EQUATIONS
            || header.coordinate_codes != expected_codes(VARIABLES)
            || header.equation_codes != expected_codes(EQUATIONS)
            || header.probe_count != PROBE_DEFINITIONS.len()
            || header.probe_definitions != PROBE_DEFINITIONS
            || header.semantics != SEMANTICS
            || !header.determinant_inequality.is_null()
            || header.kernel_reflected_file
            || header.infeasibility_claimed
        {
            return Err(shape("header fields differ from the balanced schema"));
        }
        if header.coordinate_bounds.len() != VARIABLES {
            return Err(shape("coordinate_bounds length"));
        }
        for (v, [low, high]) in header.coordinate_bounds.iter().enumerate() {
            let radius = coordinate_radius(v);
            if rational(low)? != -radius.clone() || rational(high)? != radius {
                return Err(shape(format!("coordinate bound {v}")));
            }
        }
        let probe_points: Vec<Vec<BigRational>> = (0..PROBE_DEFINITIONS.len())
            .map(|p| (0..VARIABLES).map(|i| probe(p, i)).collect())
            .collect();
        let mut rows = Vec::with_capacity(EQUATIONS);
        let mut total_terms = 0;
        let mut maximum_terms = 0;
        for (id, line) in lines[1..=EQUATIONS].iter().enumerate() {
            let row: Row = serde_json::from_str(line)?;
            if row.kind != "equation" || row.id != id || row.degree_bound != 2 {
                return Err(shape(format!("row {id} header fields")));
            }
            if row.term_count != row.terms.len() || row.probe_values.len() != PROBE_DEFINITIONS.len()
            {
                return Err(shape(format!("row {id} counts")));
            }
            let mut poly = RationalPoly::new();
            let mut previous: Option<&Vec<usize>> = None;
            for (coefficient, factors) in &row.terms {
                let q = rational(coefficient)?;
                if q.is_zero()
                    || factors.len() > 2
                    || factors.windows(2).any(|w| w[0] > w[1])
                    || factors.iter().any(|&v| v >= VARIABLES)
                    || previous.is_some_and(|p| p >= factors)
                {
                    return Err(shape(format!("row {id} term order or range")));
                }
                previous = Some(factors);
                poly.insert(factors.clone(), q);
            }
            for (p, point) in probe_points.iter().enumerate() {
                let value = evaluate_rational(&poly, point);
                if rational(&row.probe_values[p])? != value {
                    return Err(shape(format!("row {id} probe {p}")));
                }
            }
            total_terms += poly.len();
            maximum_terms = maximum_terms.max(poly.len());
            rows.push(poly);
        }
        let tail: Tail = serde_json::from_str(lines[EQUATIONS + 1])?;
        if tail.kind != "complete"
            || tail.equations != EQUATIONS
            || tail.total_terms != total_terms
            || tail.maximum_terms != maximum_terms
        {
            return Err(shape("tail totals"));
        }
        Ok(Self {
            rows,
            total_terms,
            maximum_terms,
        })
    }
}

/// Evaluates a rational polynomial at a rational point.
pub fn evaluate_rational(poly: &RationalPoly, point: &[BigRational]) -> BigRational {
    let mut sum = BigRational::zero();
    for (factors, coefficient) in poly {
        let mut term = coefficient.clone();
        for &v in factors {
            term *= &point[v];
        }
        sum += term;
    }
    sum
}

/// Evaluates a rational polynomial at a point of Q(zeta_24).
pub fn evaluate_exact(poly: &RationalPoly, point: &[Cyc24]) -> Cyc24 {
    let mut sum = Cyc24::zero();
    for (factors, coefficient) in poly {
        let mut term = Cyc24::rat(coefficient.clone());
        for &v in factors {
            term = term.mul(&point[v]);
        }
        sum = sum.add(&term);
    }
    sum
}

fn accumulate(acc: &mut RationalPoly, monomial: Monomial, coefficient: BigRational) {
    if coefficient.is_zero() {
        return;
    }
    match acc.entry(monomial) {
        Entry::Vacant(slot) => {
            slot.insert(coefficient);
        }
        Entry::Occupied(mut slot) => {
            *slot.get_mut() += coefficient;
            if slot.get().is_zero() {
                slot.remove();
            }
        }
    }
}

fn poly_add(p: &RationalPoly, q: &RationalPoly, sign: i64) -> RationalPoly {
    let mut out = p.clone();
    let s = BigRational::from_integer(sign.into());
    for (m, c) in q {
        accumulate(&mut out, m.clone(), c * &s);
    }
    out
}

fn poly_mul(p: &RationalPoly, q: &RationalPoly) -> RationalPoly {
    let mut out = RationalPoly::new();
    for (m1, c1) in p {
        for (m2, c2) in q {
            let mut m = m1.clone();
            m.extend_from_slice(m2);
            m.sort_unstable();
            accumulate(&mut out, m, c1 * c2);
        }
    }
    out
}

fn poly_const(n: i64) -> RationalPoly {
    let mut out = RationalPoly::new();
    accumulate(&mut out, Vec::new(), BigRational::from_integer(n.into()));
    out
}

fn poly_var(v: usize) -> RationalPoly {
    let mut out = RationalPoly::new();
    out.insert(vec![v], BigRational::one());
    out
}

/// A complex-valued polynomial `re + i im` in the 320 real coordinates.
#[derive(Clone, Debug, PartialEq)]
struct ComplexPoly {
    re: RationalPoly,
    im: RationalPoly,
}

impl ComplexPoly {
    fn constant(n: i64) -> Self {
        Self {
            re: poly_const(n),
            im: RationalPoly::new(),
        }
    }
    fn coordinate(base: usize) -> Self {
        Self {
            re: poly_var(base),
            im: poly_var(base + 1),
        }
    }
    fn add(&self, o: &Self, sign: i64) -> Self {
        Self {
            re: poly_add(&self.re, &o.re, sign),
            im: poly_add(&self.im, &o.im, sign),
        }
    }
    fn mul(&self, o: &Self) -> Self {
        Self {
            re: poly_add(&poly_mul(&self.re, &o.re), &poly_mul(&self.im, &o.im), -1),
            im: poly_add(&poly_mul(&self.re, &o.im), &poly_mul(&self.im, &o.re), 1),
        }
    }
    fn conj(&self) -> Self {
        Self {
            re: self.re.clone(),
            im: poly_add(&RationalPoly::new(), &self.im, -1),
        }
    }
    fn norm(&self) -> RationalPoly {
        poly_add(&poly_mul(&self.re, &self.re), &poly_mul(&self.im, &self.im), 1)
    }
    fn component(&self, b: usize) -> RationalPoly {
        if b == 0 {
            self.re.clone()
        } else {
            self.im.clone()
        }
    }
}

type SymbolicMatrix = Vec<Vec<ComplexPoly>>;

/// Coordinate base (real part) of each gauge-free entry, following `MubBoundedExportIndices`
/// and `MubBalancedIndices`: `None` marks a gauge entry fixed to one.
pub fn entry_base(a: usize, i: usize, j: usize) -> Option<usize> {
    match a {
        0 => {
            if i == 0 || j == 0 {
                None
            } else if i < 3 && j < 3 {
                Some(2 * (2 * (i - 1) + (j - 1)))
            } else if i < 3 {
                Some(2 * (4 + 3 * (i - 1) + (j - 3)))
            } else if j < 3 {
                Some(2 * (10 + 2 * (i - 3) + (j - 1)))
            } else {
                Some(D_START + 2 * (3 * (i - 3) + (j - 3)))
            }
        }
        1 | 2 => {
            if i == 0 {
                None
            } else {
                let start = if a == 1 { 16 } else { 46 };
                Some(2 * (start + 6 * (i - 1) + j))
            }
        }
        _ => None,
    }
}

/// Coordinate base (real part) of transition core `W_a[i][j]`, `i, j < 5`.
pub fn core_base(a: usize, i: usize, j: usize) -> usize {
    CORE_START + 2 * (25 * a + 5 * i + j)
}

fn symbolic_bases() -> [SymbolicMatrix; 3] {
    std::array::from_fn(|a| {
        (0..6)
            .map(|i| {
                (0..6)
                    .map(|j| match entry_base(a, i, j) {
                        Some(base) => ComplexPoly::coordinate(base),
                        None => ComplexPoly::constant(1),
                    })
                    .collect()
            })
            .collect()
    })
}

fn symbolic_transition(a: usize) -> SymbolicMatrix {
    let core = |i: usize, j: usize| ComplexPoly::coordinate(core_base(a, i, j));
    let mut w: SymbolicMatrix = vec![vec![ComplexPoly::constant(0); 6]; 6];
    for (i, row) in w.iter_mut().enumerate().take(5) {
        for (j, entry) in row.iter_mut().enumerate().take(5) {
            *entry = core(i, j);
        }
    }
    for (i, row) in w.iter_mut().enumerate().take(5) {
        let mut s = ComplexPoly::constant(6);
        for j in 0..5 {
            s = s.add(&core(i, j), -1);
        }
        row[5] = s;
    }
    for (j, entry) in w[5].iter_mut().enumerate().take(5) {
        let mut s = ComplexPoly::constant(6);
        for i in 0..5 {
            s = s.add(&core(i, j), -1);
        }
        *entry = s;
    }
    let mut corner = ComplexPoly::constant(-24);
    for i in 0..5 {
        for j in 0..5 {
            corner = corner.add(&core(i, j), 1);
        }
    }
    w[5][5] = corner;
    w
}

fn symbolic_conj_transpose_mul(x: &SymbolicMatrix, y: &SymbolicMatrix) -> SymbolicMatrix {
    (0..6)
        .map(|i| {
            (0..6)
                .map(|j| {
                    (0..6).fold(ComplexPoly::constant(0), |acc, k| {
                        acc.add(&x[k][i].conj().mul(&y[k][j]), 1)
                    })
                })
                .collect()
        })
        .collect()
}

/// Row code of `|A_ij|^2 - 1`.
pub fn modulus_code(a: usize, i: usize, j: usize) -> usize {
    MODULUS_START + 36 * a + 6 * i + j
}
/// Row code of component `b` of `(A^H A - 6 I)_ij`.
pub fn gram_code(a: usize, i: usize, j: usize, b: usize) -> usize {
    GRAM_START + 2 * (36 * a + 6 * i + j) + b
}
/// Row code of component `b` of `(W_a - T_a)_ij`.
pub fn graph_code(a: usize, i: usize, j: usize, b: usize) -> usize {
    GRAPH_START + 2 * (36 * a + 6 * i + j) + b
}
/// Row code of `|W_a,ij|^2 - 6`.
pub fn transition_modulus_code(a: usize, i: usize, j: usize) -> usize {
    TRANSITION_MODULUS_START + 36 * a + 6 * i + j
}

/// Regenerates the 648 balanced equations from their definitions, indexed by row code.
pub fn regenerate_equations() -> Vec<RationalPoly> {
    let bases = symbolic_bases();
    let pairs = [(0, 1), (0, 2), (1, 2)];
    let transitions: Vec<SymbolicMatrix> = pairs
        .iter()
        .map(|&(x, y)| symbolic_conj_transpose_mul(&bases[x], &bases[y]))
        .collect();
    let grams: Vec<SymbolicMatrix> = bases
        .iter()
        .map(|m| symbolic_conj_transpose_mul(m, m))
        .collect();
    let cores: Vec<SymbolicMatrix> = (0..3).map(symbolic_transition).collect();
    let mut equations = vec![RationalPoly::new(); EQUATIONS];
    for a in 0..3 {
        for i in 0..6 {
            for j in 0..6 {
                equations[modulus_code(a, i, j)] =
                    poly_add(&bases[a][i][j].norm(), &poly_const(1), -1);
                let diagonal = if i == j { 6 } else { 0 };
                let gram = grams[a][i][j].add(&ComplexPoly::constant(diagonal), -1);
                let graph = cores[a][i][j].add(&transitions[a][i][j], -1);
                for b in 0..2 {
                    equations[gram_code(a, i, j, b)] = gram.component(b);
                    equations[graph_code(a, i, j, b)] = graph.component(b);
                }
                equations[transition_modulus_code(a, i, j)] =
                    poly_add(&cores[a][i][j].norm(), &poly_const(6), -1);
            }
        }
    }
    equations
}

/// Row-by-row accounting of the pinned table against its definitions.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct TableInventory {
    pub table_sha256: String,
    pub rows: usize,
    pub variables: usize,
    pub total_terms: usize,
    pub maximum_terms: usize,
    /// Rows whose terms differ from the regenerated polynomial (expected empty).
    pub mismatched_rows: Vec<usize>,
    pub empty_rows: Vec<usize>,
    /// `|A_ij|^2 - 1` rows for gauge entries fixed to one (constant zero).
    pub empty_gauge_modulus_rows: usize,
    pub nonempty_modulus_rows: usize,
    /// Gram rows that are constant zero: every diagonal imaginary part, and the real
    /// diagonal entry of column 0 of `H`, whose column is fixed to ones.
    pub empty_gram_rows: usize,
    /// Pairs `i > j` with real rows equal and imaginary rows opposite to `(j, i)`.
    pub gram_hermitian_duplicate_pairs: usize,
    /// Diagonal real Gram rows equal to the sum of the modulus rows of that column.
    pub gram_diagonal_real_equal_modulus_sum: usize,
    /// Gram rows `i < j` (real and imaginary), the ones not implied by other rows.
    pub gram_upper_rows: usize,
    pub graph_rows: usize,
    pub transition_modulus_rows: usize,
}

fn is_gauge(a: usize, i: usize, j: usize) -> bool {
    entry_base(a, i, j).is_none()
}

/// Compares the table with the regenerated equations and accounts for every row.
pub fn inventory(table: &BalancedTable) -> TableInventory {
    let regenerated = regenerate_equations();
    let mismatched_rows: Vec<usize> = (0..EQUATIONS)
        .filter(|&c| table.rows[c] != regenerated[c])
        .collect();
    let rows = &table.rows;
    let empty_rows: Vec<usize> = (0..EQUATIONS).filter(|&c| rows[c].is_empty()).collect();
    let mut empty_gauge_modulus_rows = 0;
    let mut nonempty_modulus_rows = 0;
    let mut empty_gram_rows = 0;
    let mut gram_hermitian_duplicate_pairs = 0;
    let mut gram_diagonal_real_equal_modulus_sum = 0;
    let mut gram_upper_rows = 0;
    for a in 0..3 {
        for i in 0..6 {
            for j in 0..6 {
                let modulus = &rows[modulus_code(a, i, j)];
                if modulus.is_empty() && is_gauge(a, i, j) {
                    empty_gauge_modulus_rows += 1;
                } else if !modulus.is_empty() && !is_gauge(a, i, j) {
                    nonempty_modulus_rows += 1;
                }
                for b in 0..2 {
                    if rows[gram_code(a, i, j, b)].is_empty() {
                        empty_gram_rows += 1;
                    }
                }
                if i < j {
                    gram_upper_rows += 2;
                }
                if i > j {
                    let re_equal = rows[gram_code(a, i, j, 0)] == rows[gram_code(a, j, i, 0)];
                    let im_opposite = rows[gram_code(a, i, j, 1)]
                        == poly_add(&RationalPoly::new(), &rows[gram_code(a, j, i, 1)], -1);
                    if re_equal && im_opposite {
                        gram_hermitian_duplicate_pairs += 1;
                    }
                }
            }
            let column_sum = (0..6).fold(RationalPoly::new(), |acc, k| {
                poly_add(&acc, &rows[modulus_code(a, k, i)], 1)
            });
            if rows[gram_code(a, i, i, 0)] == column_sum {
                gram_diagonal_real_equal_modulus_sum += 1;
            }
        }
    }
    TableInventory {
        table_sha256: COEFFICIENT_SHA256.to_string(),
        rows: rows.len(),
        variables: VARIABLES,
        total_terms: table.total_terms,
        maximum_terms: table.maximum_terms,
        mismatched_rows,
        empty_rows,
        empty_gauge_modulus_rows,
        nonempty_modulus_rows,
        empty_gram_rows,
        gram_hermitian_duplicate_pairs,
        gram_diagonal_real_equal_modulus_sum,
        gram_upper_rows,
        graph_rows: TRANSITION_MODULUS_START - GRAPH_START,
        transition_modulus_rows: EQUATIONS - TRANSITION_MODULUS_START,
    }
}

/// `(z + conj z) / 2`.
pub fn real_part(z: &Cyc24) -> Cyc24 {
    z.add(&z.conj()).scale_rat(&BigRational::new(1.into(), 2.into()))
}

/// `(z - conj z) / (2 i)`.
pub fn imag_part(z: &Cyc24) -> Cyc24 {
    z.sub(&z.conj())
        .mul(&Cyc24::i())
        .scale_rat(&BigRational::new((-1).into(), 2.into()))
}

/// `(X^H Y)_ij = sum_k conj(X_ki) Y_kj` over Q(zeta_24).
pub fn exact_conj_transpose_mul(x: &ExactMatrix, y: &ExactMatrix) -> ExactMatrix {
    let n = x.len();
    (0..n)
        .map(|i| {
            (0..n)
                .map(|j| {
                    (0..n).fold(Cyc24::zero(), |acc, k| acc.add(&x[k][i].conj().mul(&y[k][j])))
                })
                .collect()
        })
        .collect()
}

fn check_square(name: &str, m: &ExactMatrix) -> Result<(), BalancedReplayError> {
    if m.len() != 6 || m.iter().any(|row| row.len() != 6) {
        return Err(BalancedReplayError::Matrix(format!("{name} is not 6 x 6")));
    }
    Ok(())
}

/// Encodes raw Hadamards `(H, U, V)` in the table's gauge as its 320 coordinates. The cores
/// are the 5 x 5 corners of `H^H U`, `H^H V`, `U^H V`. A matrix outside the gauge (a first
/// row, or the first column of `H`, not all ones) is refused.
pub fn encode_triple(
    h: &ExactMatrix,
    u: &ExactMatrix,
    v: &ExactMatrix,
) -> Result<Vec<Cyc24>, BalancedReplayError> {
    let bases = [h, u, v];
    for (name, m) in ["H", "U", "V"].iter().zip(bases) {
        check_square(name, m)?;
    }
    let one = Cyc24::one();
    for (a, m) in bases.iter().enumerate() {
        for i in 0..6 {
            for j in 0..6 {
                if is_gauge(a, i, j) && m[i][j] != one {
                    return Err(BalancedReplayError::Matrix(format!(
                        "basis {a} entry ({i},{j}) is outside the gauge"
                    )));
                }
            }
        }
    }
    let mut point = vec![Cyc24::zero(); VARIABLES];
    for (a, m) in bases.iter().enumerate() {
        for i in 0..6 {
            for j in 0..6 {
                if let Some(base) = entry_base(a, i, j) {
                    point[base] = real_part(&m[i][j]);
                    point[base + 1] = imag_part(&m[i][j]);
                }
            }
        }
    }
    let transitions = [
        exact_conj_transpose_mul(h, u),
        exact_conj_transpose_mul(h, v),
        exact_conj_transpose_mul(u, v),
    ];
    for (a, t) in transitions.iter().enumerate() {
        for (i, row) in t.iter().enumerate().take(5) {
            for (j, z) in row.iter().enumerate().take(5) {
                let base = core_base(a, i, j);
                point[base] = real_part(z);
                point[base + 1] = imag_part(z);
            }
        }
    }
    Ok(point)
}

/// Box membership of an exact point, decided coordinate pair by coordinate pair. A pair
/// `(x, y)` with rational `x^2 + y^2 <= r^2` lies in the box; a rational coordinate is
/// compared directly; anything else is reported undecided rather than guessed.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct BoxMembership {
    pub inside: usize,
    pub outside: Vec<usize>,
    pub undecided: Vec<usize>,
}

pub fn box_membership(point: &[Cyc24]) -> BoxMembership {
    let mut inside = 0;
    let mut outside = Vec::new();
    let mut undecided = Vec::new();
    for pair in 0..VARIABLES / 2 {
        let (x, y) = (&point[2 * pair], &point[2 * pair + 1]);
        let radius = coordinate_radius(2 * pair);
        let square = radius.clone() * radius.clone();
        let modulus = x.mul(x).add(&y.mul(y)).as_rational();
        if modulus.is_some_and(|m| m <= square) {
            inside += 2;
            continue;
        }
        for (offset, c) in [x, y].iter().enumerate() {
            match c.as_rational() {
                Some(q) if q.abs() <= radius => inside += 1,
                Some(_) => outside.push(2 * pair + offset),
                None => undecided.push(2 * pair + offset),
            }
        }
    }
    BoxMembership {
        inside,
        outside,
        undecided,
    }
}

/// Every row's value at an exact point: which rows do not vanish, and their distinct values.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct PointEvaluation {
    pub nonzero_rows: Vec<usize>,
    /// Distinct nonzero values as canonical `p/q`, or `irrational` when not in Q.
    pub nonzero_values: BTreeSet<String>,
    pub box_membership: BoxMembership,
}

pub fn evaluate_point(table: &BalancedTable, point: &[Cyc24]) -> PointEvaluation {
    let mut nonzero_rows = Vec::new();
    let mut nonzero_values = BTreeSet::new();
    for (code, row) in table.rows.iter().enumerate() {
        let value = evaluate_exact(row, point);
        if !value.is_zero() {
            nonzero_rows.push(code);
            nonzero_values.insert(match value.as_rational() {
                Some(q) => canonical(&q),
                None => "irrational".to_string(),
            });
        }
    }
    PointEvaluation {
        nonzero_rows,
        nonzero_values,
        box_membership: box_membership(point),
    }
}

/// Builds an index from row code to equation block name, for reports.
pub fn block_of(code: usize) -> &'static str {
    match code {
        c if c < GRAM_START => "modulus",
        c if c < GRAPH_START => "gram",
        c if c < TRANSITION_MODULUS_START => "graph",
        _ => "transition_modulus",
    }
}

/// Counts rows per block, keyed by block name.
pub fn rows_per_block(codes: &[usize]) -> BTreeMap<&'static str, usize> {
    let mut out = BTreeMap::new();
    for &c in codes {
        *out.entry(block_of(c)).or_insert(0) += 1;
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rational_literals_are_canonical_only() {
        assert!(rational("3/4").is_ok());
        assert!(rational("6/8").is_err());
        assert!(rational("3").is_err());
        assert!(rational("3/-4").is_err());
        assert!(rational("+3/4").is_err());
    }

    #[test]
    fn regeneration_has_forty_two_constant_rows() {
        let equations = regenerate_equations();
        let empty = equations.iter().filter(|p| p.is_empty()).count();
        assert_eq!(empty, 42);
    }

    #[test]
    fn real_and_imaginary_parts_recombine() {
        let z = Cyc24::zeta24(5).add(&Cyc24::from_int(3));
        let back = real_part(&z).add(&imag_part(&z).mul(&Cyc24::i()));
        assert_eq!(back, z);
        assert_eq!(real_part(&z).conj(), real_part(&z));
        assert_eq!(imag_part(&z).conj(), imag_part(&z));
    }
}
