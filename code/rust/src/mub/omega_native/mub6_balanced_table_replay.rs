
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
pub const CORE_START: usize = 170;
pub const D_START: usize = 152;
pub const SCHEMA: &str = "mub6.balanced_quadratic.coefficients.v1";
pub const COEFFICIENT_SHA256: &str =
    "cb552359467ede318508279b62b7203e65b3c510abf77b5492d3d3f4a49c217d";
pub const CORE_RADIUS: (i64, i64) = (10035, 4096);

pub const MODULUS_START: usize = 0;
pub const GRAM_START: usize = 108;
pub const GRAPH_START: usize = 324;
pub const TRANSITION_MODULUS_START: usize = 540;

pub type Monomial = Vec<usize>;
pub type RationalPoly = BTreeMap<Monomial, BigRational>;
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

fn header_identity_and_counts_match(header: &Header) -> bool {
    let expected_vars: Vec<usize> = (0..VARIABLES).collect();
    let expected_eqs: Vec<usize> = (0..EQUATIONS).collect();
    header.kind == "header"
        && header.schema == SCHEMA
        && header.authority_effect == "None"
        && header.variable_count == VARIABLES
        && header.equation_count == EQUATIONS
        && header.coordinate_codes == expected_vars
        && header.equation_codes == expected_eqs
}

fn header_metadata_matches(header: &Header) -> bool {
    header.probe_count == PROBE_DEFINITIONS.len()
        && header.probe_definitions == PROBE_DEFINITIONS
        && header.semantics == SEMANTICS
        && header.determinant_inequality.is_null()
        && !header.kernel_reflected_file
        && !header.infeasibility_claimed
}

fn validate_coordinate_bounds(header: &Header) -> Result<(), BalancedReplayError> {
    if header.coordinate_bounds.len() != VARIABLES {
        return Err(shape("coordinate_bounds length"));
    }
    for (v, [low, high]) in header.coordinate_bounds.iter().enumerate() {
        let radius = coordinate_radius(v);
        if rational(low)? != -radius.clone() || rational(high)? != radius {
            return Err(shape(format!("coordinate bound {v}")));
        }
    }
    Ok(())
}

fn build_probe_points() -> Vec<Vec<BigRational>> {
    let mut points = Vec::with_capacity(PROBE_DEFINITIONS.len());
    for p in 0..PROBE_DEFINITIONS.len() {
        let mut pt = Vec::with_capacity(VARIABLES);
        for i in 0..VARIABLES {
            pt.push(probe(p, i));
        }
        points.push(pt);
    }
    points
}

fn factors_sorted_and_in_range(factors: &[usize]) -> bool {
    if factors.len() > 2 {
        return false;
    }
    for i in 0..factors.len() {
        if factors[i] >= VARIABLES || (i > 0 && factors[i - 1] > factors[i]) {
            return false;
        }
    }
    true
}

fn decode_row_poly(id: usize, row: &Row) -> Result<RationalPoly, BalancedReplayError> {
    let mut poly = RationalPoly::new();
    let mut previous: Option<&Vec<usize>> = None;
    for (coefficient, factors) in &row.terms {
        let q = rational(coefficient)?;
        let prev_bad = match previous {
            Some(p) => p >= factors,
            None => false,
        };
        if q.is_zero() || !factors_sorted_and_in_range(factors) || prev_bad {
            return Err(shape(format!("row {id} term order or range")));
        }
        previous = Some(factors);
        poly.insert(factors.clone(), q);
    }
    Ok(poly)
}

fn verify_row_probe_values(
    id: usize,
    poly: &RationalPoly,
    row: &Row,
    probe_points: &[Vec<BigRational>],
) -> Result<(), BalancedReplayError> {
    for (p, point) in probe_points.iter().enumerate() {
        let value = evaluate_rational(poly, point);
        if rational(&row.probe_values[p])? != value {
            return Err(shape(format!("row {id} probe {p}")));
        }
    }
    Ok(())
}

fn decode_and_verify_equation_row(
    id: usize,
    line: &str,
    probe_points: &[Vec<BigRational>],
) -> Result<RationalPoly, BalancedReplayError> {
    let row: Row = serde_json::from_str(line)?;
    if row.kind != "equation" || row.id != id || row.degree_bound != 2 {
        return Err(shape(format!("row {id} header fields")));
    }
    if row.term_count != row.terms.len() || row.probe_values.len() != PROBE_DEFINITIONS.len() {
        return Err(shape(format!("row {id} counts")));
    }
    let poly = decode_row_poly(id, &row)?;
    verify_row_probe_values(id, &poly, &row, probe_points)?;
    Ok(poly)
}

fn decode_all_equation_rows(
    lines: &[&str],
    probe_points: &[Vec<BigRational>],
) -> Result<(Vec<RationalPoly>, usize, usize), BalancedReplayError> {
    let mut rows = Vec::with_capacity(EQUATIONS);
    let mut total_terms = 0;
    let mut maximum_terms = 0;
    for (id, line) in lines[1..=EQUATIONS].iter().enumerate() {
        let poly = decode_and_verify_equation_row(id, line, probe_points)?;
        total_terms += poly.len();
        maximum_terms = maximum_terms.max(poly.len());
        rows.push(poly);
    }
    Ok((rows, total_terms, maximum_terms))
}

fn validate_table_tail(
    tail: &Tail,
    total_terms: usize,
    maximum_terms: usize,
) -> Result<(), BalancedReplayError> {
    if tail.kind != "complete"
        || tail.equations != EQUATIONS
        || tail.total_terms != total_terms
        || tail.maximum_terms != maximum_terms
    {
        return Err(shape("tail totals"));
    }
    Ok(())
}

impl BalancedTable {
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
            return Err(shape(format!(
                "expected {} lines, found {}",
                EQUATIONS + 2,
                lines.len()
            )));
        }
        let header: Header = serde_json::from_str(lines[0])?;
        if !header_identity_and_counts_match(&header) || !header_metadata_matches(&header) {
            return Err(shape("header fields differ from the balanced schema"));
        }
        validate_coordinate_bounds(&header)?;
        let probe_points = build_probe_points();
        let (rows, total_terms, maximum_terms) = decode_all_equation_rows(&lines, &probe_points)?;
        let tail: Tail = serde_json::from_str(lines[EQUATIONS + 1])?;
        validate_table_tail(&tail, total_terms, maximum_terms)?;
        Ok(Self {
            rows,
            total_terms,
            maximum_terms,
        })
    }
}

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

fn entry_base_a0(i: usize, j: usize) -> Option<usize> {
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

pub fn entry_base(a: usize, i: usize, j: usize) -> Option<usize> {
    match a {
        0 => entry_base_a0(i, j),
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

pub fn core_base(a: usize, i: usize, j: usize) -> usize {
    CORE_START + 2 * (25 * a + 5 * i + j)
}

fn symbolic_basis_entry(a: usize, i: usize, j: usize) -> ComplexPoly {
    match entry_base(a, i, j) {
        Some(base) => ComplexPoly::coordinate(base),
        None => ComplexPoly::constant(1),
    }
}

fn symbolic_basis_matrix(a: usize) -> SymbolicMatrix {
    let mut mat = Vec::with_capacity(6);
    for i in 0..6 {
        let mut row = Vec::with_capacity(6);
        for j in 0..6 {
            row.push(symbolic_basis_entry(a, i, j));
        }
        mat.push(row);
    }
    mat
}

fn symbolic_bases() -> [SymbolicMatrix; 3] {
    [
        symbolic_basis_matrix(0),
        symbolic_basis_matrix(1),
        symbolic_basis_matrix(2),
    ]
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

pub fn modulus_code(a: usize, i: usize, j: usize) -> usize {
    MODULUS_START + 36 * a + 6 * i + j
}
pub fn gram_code(a: usize, i: usize, j: usize, b: usize) -> usize {
    GRAM_START + 2 * (36 * a + 6 * i + j) + b
}
pub fn graph_code(a: usize, i: usize, j: usize, b: usize) -> usize {
    GRAPH_START + 2 * (36 * a + 6 * i + j) + b
}
pub fn transition_modulus_code(a: usize, i: usize, j: usize) -> usize {
    TRANSITION_MODULUS_START + 36 * a + 6 * i + j
}

fn populate_cell_equations(
    equations: &mut [RationalPoly],
    bases: &[SymbolicMatrix; 3],
    grams: &[SymbolicMatrix],
    cores: &[SymbolicMatrix],
    transitions: &[SymbolicMatrix],
    a: usize,
    i: usize,
    j: usize,
) {
    equations[modulus_code(a, i, j)] = poly_add(&bases[a][i][j].norm(), &poly_const(1), -1);
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
                populate_cell_equations(
                    &mut equations,
                    &bases,
                    &grams,
                    &cores,
                    &transitions,
                    a,
                    i,
                    j,
                );
            }
        }
    }
    equations
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct TableInventory {
    pub table_sha256: String,
    pub rows: usize,
    pub variables: usize,
    pub total_terms: usize,
    pub maximum_terms: usize,
    pub mismatched_rows: Vec<usize>,
    pub empty_rows: Vec<usize>,
    pub empty_gauge_modulus_rows: usize,
    pub nonempty_modulus_rows: usize,
    pub empty_gram_rows: usize,
    pub gram_hermitian_duplicate_pairs: usize,
    pub gram_diagonal_real_equal_modulus_sum: usize,
    pub gram_upper_rows: usize,
    pub graph_rows: usize,
    pub transition_modulus_rows: usize,
}

fn is_gauge(a: usize, i: usize, j: usize) -> bool {
    entry_base(a, i, j).is_none()
}

#[derive(Default)]
struct InventoryCounters {
    empty_gauge_modulus_rows: usize,
    nonempty_modulus_rows: usize,
    empty_gram_rows: usize,
    gram_hermitian_duplicate_pairs: usize,
    gram_diagonal_real_equal_modulus_sum: usize,
    gram_upper_rows: usize,
}

fn is_hermitian_duplicate_pair(rows: &[RationalPoly], a: usize, i: usize, j: usize) -> bool {
    let re_equal = rows[gram_code(a, i, j, 0)] == rows[gram_code(a, j, i, 0)];
    let im_opposite = rows[gram_code(a, i, j, 1)]
        == poly_add(&RationalPoly::new(), &rows[gram_code(a, j, i, 1)], -1);
    re_equal && im_opposite
}

fn accumulate_cell_inventory(
    rows: &[RationalPoly],
    a: usize,
    i: usize,
    j: usize,
    counters: &mut InventoryCounters,
) {
    let modulus = &rows[modulus_code(a, i, j)];
    let gauge = is_gauge(a, i, j);
    if modulus.is_empty() && gauge {
        counters.empty_gauge_modulus_rows += 1;
    } else if !modulus.is_empty() && !gauge {
        counters.nonempty_modulus_rows += 1;
    }
    for b in 0..2 {
        if rows[gram_code(a, i, j, b)].is_empty() {
            counters.empty_gram_rows += 1;
        }
    }
    if i < j {
        counters.gram_upper_rows += 2;
    } else if i > j && is_hermitian_duplicate_pair(rows, a, i, j) {
        counters.gram_hermitian_duplicate_pairs += 1;
    }
}

fn check_column_sum_inventory(rows: &[RationalPoly], a: usize, i: usize) -> bool {
    let mut column_sum = RationalPoly::new();
    for k in 0..6 {
        column_sum = poly_add(&column_sum, &rows[modulus_code(a, k, i)], 1);
    }
    rows[gram_code(a, i, i, 0)] == column_sum
}

pub fn inventory(table: &BalancedTable) -> TableInventory {
    let regenerated = regenerate_equations();
    let rows = &table.rows;
    let mut mismatched_rows = Vec::new();
    let mut empty_rows = Vec::new();
    for c in 0..EQUATIONS {
        if rows[c] != regenerated[c] {
            mismatched_rows.push(c);
        }
        if rows[c].is_empty() {
            empty_rows.push(c);
        }
    }
    let mut counters = InventoryCounters::default();
    for a in 0..3 {
        for i in 0..6 {
            for j in 0..6 {
                accumulate_cell_inventory(rows, a, i, j, &mut counters);
            }
            if check_column_sum_inventory(rows, a, i) {
                counters.gram_diagonal_real_equal_modulus_sum += 1;
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
        empty_gauge_modulus_rows: counters.empty_gauge_modulus_rows,
        nonempty_modulus_rows: counters.nonempty_modulus_rows,
        empty_gram_rows: counters.empty_gram_rows,
        gram_hermitian_duplicate_pairs: counters.gram_hermitian_duplicate_pairs,
        gram_diagonal_real_equal_modulus_sum: counters.gram_diagonal_real_equal_modulus_sum,
        gram_upper_rows: counters.gram_upper_rows,
        graph_rows: TRANSITION_MODULUS_START - GRAPH_START,
        transition_modulus_rows: EQUATIONS - TRANSITION_MODULUS_START,
    }
}

pub fn real_part(z: &Cyc24) -> Cyc24 {
    z.add(&z.conj()).scale_rat(&BigRational::new(1.into(), 2.into()))
}

pub fn imag_part(z: &Cyc24) -> Cyc24 {
    z.sub(&z.conj())
        .mul(&Cyc24::i())
        .scale_rat(&BigRational::new((-1).into(), 2.into()))
}

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

fn validate_single_basis_gauge(a: usize, m: &ExactMatrix) -> Result<(), BalancedReplayError> {
    let one = Cyc24::one();
    for i in 0..6 {
        for j in 0..6 {
            if is_gauge(a, i, j) && m[i][j] != one {
                return Err(BalancedReplayError::Matrix(format!(
                    "basis {a} entry ({i},{j}) is outside the gauge"
                )));
            }
        }
    }
    Ok(())
}

fn encode_single_basis_entries(a: usize, m: &ExactMatrix, point: &mut [Cyc24]) {
    for i in 0..6 {
        for j in 0..6 {
            if let Some(base) = entry_base(a, i, j) {
                point[base] = real_part(&m[i][j]);
                point[base + 1] = imag_part(&m[i][j]);
            }
        }
    }
}

fn encode_single_transition_core(a: usize, t: &ExactMatrix, point: &mut [Cyc24]) {
    for (i, row) in t.iter().enumerate().take(5) {
        for (j, z) in row.iter().enumerate().take(5) {
            let base = core_base(a, i, j);
            point[base] = real_part(z);
            point[base + 1] = imag_part(z);
        }
    }
}

pub fn encode_triple(
    h: &ExactMatrix,
    u: &ExactMatrix,
    v: &ExactMatrix,
) -> Result<Vec<Cyc24>, BalancedReplayError> {
    let bases = [h, u, v];
    for (name, m) in ["H", "U", "V"].iter().zip(bases) {
        check_square(name, m)?;
    }
    for (a, m) in bases.iter().enumerate() {
        validate_single_basis_gauge(a, m)?;
    }
    let mut point = vec![Cyc24::zero(); VARIABLES];
    for (a, m) in bases.iter().enumerate() {
        encode_single_basis_entries(a, m, &mut point);
    }
    let transitions = [
        exact_conj_transpose_mul(h, u),
        exact_conj_transpose_mul(h, v),
        exact_conj_transpose_mul(u, v),
    ];
    for (a, t) in transitions.iter().enumerate() {
        encode_single_transition_core(a, t, &mut point);
    }
    Ok(point)
}

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

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct PointEvaluation {
    pub nonzero_rows: Vec<usize>,
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

pub fn block_of(code: usize) -> &'static str {
    match code {
        c if c < GRAM_START => "modulus",
        c if c < GRAPH_START => "gram",
        c if c < TRANSITION_MODULUS_START => "graph",
        _ => "transition_modulus",
    }
}

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
