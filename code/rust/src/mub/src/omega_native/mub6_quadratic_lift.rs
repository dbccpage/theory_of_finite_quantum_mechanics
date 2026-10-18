
use num_rational::BigRational;
use num_traits::{One, Zero};
use omega_kernel::exact::{parse_exact, to_canonical_string};
use omega_kernel::interval::Interval;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;

pub const VARIABLES: usize = 386;
pub const EQUATIONS: usize = 648;
pub const COEFFICIENT_SHA256: &str =
    "a8b2dbcbc44d0618bbf0bf36fd2b252d7cc8a03a1168ebf98ecc28010dceed03";

#[derive(Debug, Error)]
pub enum LiftError {
    #[error("coefficient input digest does not match the checked table")]
    InputHash,
    #[error("invalid JSON: {0}")]
    Json(#[from] serde_json::Error),
    #[error("invalid coefficient table: {0}")]
    Shape(&'static str),
    #[error("invalid reduced numerator/denominator rational: {0}")]
    Rational(String),
    #[error("box must have 386 coordinates and be contained in the original box")]
    Box,
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
struct Complete {
    kind: String,
    equations: usize,
    total_terms: usize,
    maximum_terms: usize,
}

type Term = (BigRational, Vec<usize>);
type Polynomial = Vec<Term>;

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct BoxRequest {
    schema: String,
    input_sha256: String,
    bounds: Vec<[String; 2]>,
}

fn rational(text: &str) -> Result<BigRational, LiftError> {
    let raw = text.strip_suffix("/1").unwrap_or(text);
    let q = parse_exact(raw).map_err(|_| LiftError::Rational(text.to_owned()))?;
    if format!("{}/{}", q.numer(), q.denom()) != text {
        return Err(LiftError::Rational(text.to_owned()));
    }
    Ok(q)
}

fn probe(p: usize, i: usize) -> BigRational {
    let (n, d) = match p {
        0 => (0, 1),
        1 => ((i % 17) as i64 - 7, 13),
        2 => (if i % 2 == 0 { 1 } else { -1 }, 1),
        _ => (((7 * i + 3) % 19) as i64 - 8, 11),
    };
    BigRational::new(n.into(), d.into())
}

fn term_range(term: &Term, bounds: &[Interval]) -> Interval {
    let (coefficient, factors) = term;
    let product = match factors.as_slice() {
        [i, j] if i == j => bounds[*i].sq(),
        _ => factors
            .iter()
            .fold(Interval::point(BigRational::one()), |v, i| {
                v.mul(&bounds[*i])
            }),
    };
    product.mul_scalar(coefficient)
}

fn range(poly: &Polynomial, bounds: &[Interval], omit: Option<usize>) -> Interval {
    poly.iter()
        .enumerate()
        .filter(|(k, _)| Some(*k) != omit)
        .fold(Interval::point(BigRational::zero()), |v, (_, term)| {
            v.add(&term_range(term, bounds))
        })
}

fn pair(bound: &Interval) -> [String; 2] {
    [
        to_canonical_string(bound.lo()),
        to_canonical_string(bound.hi()),
    ]
}

#[derive(Debug)]
pub struct QuadraticLift {
    polynomials: Vec<Polynomial>,
    full_box: Vec<Interval>,
}

#[derive(Debug, Serialize)]
pub struct Tightening {
    equation: usize,
    variable: usize,
    isolated_power: usize,
    before: [String; 2],
    target_power_range: [String; 2],
    after: [String; 2],
}

#[derive(Debug, Serialize)]
pub struct Inspection {
    schema: &'static str,
    authority_effect: &'static str,
    input_sha256: &'static str,
    status: &'static str,
    variable_count: usize,
    equation_count: usize,
    term_count: usize,
    probe_comparisons: usize,
    algorithm: &'static str,
    square_bisections: usize,
    input_box: Vec<[String; 2]>,
    retained_box: Vec<[String; 2]>,
    equation_ranges: Vec<[String; 2]>,
    excluded_equation: Option<usize>,
    separation_exclusion: Option<SeparationExclusion>,
    request_sha256: Option<String>,
    tightenings: Vec<Tightening>,
    contracted_coordinates: Vec<usize>,
    root_existence_claimed: bool,
    kernel_reflected_runtime: bool,
    global_nonexistence_claimed: bool,
}

#[derive(Debug, Serialize)]
pub struct SeparationExclusion {
    first_transition: usize,
    second_transition: usize,
    first_column: usize,
    second_column: usize,
    component_square_upper_bounds: Vec<[String; 2]>,
    distance_upper_bound: String,
    distance_lower_bound: String,
    soundness_endpoint: &'static str,
}

fn separation_exclusion(bounds: &[Interval], lower: &BigRational) -> Option<SeparationExclusion> {
    for i in 0..6 {
        for j in 0..6 {
            let mut upper = BigRational::zero();
            let mut components = Vec::with_capacity(6);
            for k in 0..6 {
                let real = bounds[170 + 2 * (6 * k + i)]
                    .sub(&bounds[170 + 2 * (36 + 6 * k + j)])
                    .sq();
                let imag = bounds[171 + 2 * (6 * k + i)]
                    .sub(&bounds[171 + 2 * (36 + 6 * k + j)])
                    .sq();
                upper += real.hi() + imag.hi();
                components.push([
                    to_canonical_string(real.hi()),
                    to_canonical_string(imag.hi()),
                ]);
            }
            if upper < *lower {
                return Some(SeparationExclusion {
                    first_transition: 0,
                    second_transition: 1,
                    first_column: i,
                    second_column: j,
                    component_square_upper_bounds: components,
                    distance_upper_bound: to_canonical_string(&upper),
                    distance_lower_bound: to_canonical_string(lower),
                    soundness_endpoint: "MUB.QuadraticTransitionSeparation.component_box_exclusion",
                });
            }
        }
    }
    None
}

impl QuadraticLift {
    pub fn from_bytes(bytes: &[u8]) -> Result<Self, LiftError> {
        if format!("{:x}", Sha256::digest(bytes)) != COEFFICIENT_SHA256 {
            return Err(LiftError::InputHash);
        }
        Self::decode(bytes)
    }

    fn decode(bytes: &[u8]) -> Result<Self, LiftError> {
        let text = std::str::from_utf8(bytes).map_err(|_| LiftError::Shape("UTF-8"))?;
        let lines: Vec<_> = text.lines().collect();
        if lines.len() != EQUATIONS + 2 {
            return Err(LiftError::Shape("line count"));
        }
        let h: Header = serde_json::from_str(lines[0])?;
        if h.kind != "header" || h.schema != "mub6.quadratic_lift.coefficients.v1"
            || h.authority_effect != "None" || h.variable_count != VARIABLES
            || h.equation_count != EQUATIONS || h.coordinate_codes != (0..VARIABLES).collect::<Vec<_>>()
            || h.equation_codes != (0..EQUATIONS).collect::<Vec<_>>()
            || h.coordinate_bounds.len() != VARIABLES || h.probe_count != 4
            || h.probe_definitions != ["0", "(i mod 17 - 7)/13", "1 if i even else -1", "((7*i+3) mod 19 - 8)/11"]
            || h.semantics != "Sum coefficient times product of factor coordinates; every equation equals zero."
            || !h.determinant_inequality.is_null() || h.kernel_reflected_file || h.infeasibility_claimed
        {
            return Err(LiftError::Shape("header"));
        }
        let mut full_box = Vec::with_capacity(VARIABLES);
        for (i, b) in h.coordinate_bounds.iter().enumerate() {
            let radius = BigRational::from_integer((if i < 170 { 1 } else { 3 }).into());
            if rational(&b[0])? != -&radius || rational(&b[1])? != radius {
                return Err(LiftError::Shape("coordinate bounds"));
            }
            full_box.push(Interval::new(-&radius, radius));
        }
        let mut polynomials = Vec::with_capacity(EQUATIONS);
        for (id, line) in lines[1..=EQUATIONS].iter().enumerate() {
            let row: Row = serde_json::from_str(line)?;
            if row.kind != "equation"
                || row.id != id
                || row.degree_bound != 2
                || row.term_count != row.terms.len()
                || row.probe_values.len() != 4
                || row.terms.windows(2).any(|w| w[0].1 >= w[1].1)
            {
                return Err(LiftError::Shape("equation row"));
            }
            let mut polynomial = Vec::with_capacity(row.terms.len());
            for (c, factors) in row.terms {
                let c = rational(&c)?;
                if c.is_zero()
                    || factors.len() > 2
                    || factors.iter().any(|&i| i >= VARIABLES)
                    || factors.windows(2).any(|w| w[0] > w[1])
                {
                    return Err(LiftError::Shape("monomial"));
                }
                polynomial.push((c, factors));
            }
            for p in 0..4 {
                let value: BigRational = polynomial
                    .iter()
                    .map(|(c, f)| f.iter().fold(c.clone(), |v, &i| v * probe(p, i)))
                    .sum();
                if value != rational(&row.probe_values[p])? {
                    return Err(LiftError::Shape("probe value"));
                }
            }
            polynomials.push(polynomial);
        }
        let tail: Complete = serde_json::from_str(lines[EQUATIONS + 1])?;
        if tail.kind != "complete"
            || tail.equations != EQUATIONS
            || tail.total_terms != 4920
            || tail.maximum_terms != 12
            || polynomials.iter().map(Vec::len).sum::<usize>() != tail.total_terms
            || polynomials.iter().map(Vec::len).max() != Some(tail.maximum_terms)
        {
            return Err(LiftError::Shape("completion record"));
        }
        Ok(Self {
            polynomials,
            full_box,
        })
    }

    pub fn inspect_full_box(&self) -> Result<Inspection, LiftError> {
        self.inspect_box(&self.full_box)
    }

    pub fn inspect_box_bytes(&self, bytes: &[u8]) -> Result<Inspection, LiftError> {
        let request: BoxRequest = serde_json::from_slice(bytes)?;
        if request.schema != "mub6.quadratic_lift.box.v1"
            || request.input_sha256 != COEFFICIENT_SHA256
            || request.bounds.len() != VARIABLES
        {
            return Err(LiftError::Box);
        }
        let mut bounds = Vec::with_capacity(VARIABLES);
        for [lo, hi] in request.bounds {
            let lo = parse_exact(&lo).map_err(|_| LiftError::Rational(lo))?;
            let hi = parse_exact(&hi).map_err(|_| LiftError::Rational(hi))?;
            bounds.push(Interval::try_new(lo, hi).map_err(|_| LiftError::Box)?);
        }
        let mut result = self.inspect_box(&bounds)?;
        result.request_sha256 = Some(format!("{:x}", Sha256::digest(bytes)));
        Ok(result)
    }

    pub fn inspect_box(&self, input: &[Interval]) -> Result<Inspection, LiftError> {
        if input.len() != VARIABLES
            || input
                .iter()
                .zip(&self.full_box)
                .any(|(b, full)| b.lo() < full.lo() || b.hi() > full.hi())
        {
            return Err(LiftError::Box);
        }
        let (bounds, tightenings, excluded) = contract(&self.polynomials, input);
        let ranges: Vec<_> = self
            .polynomials
            .iter()
            .map(|p| range(p, &bounds, None))
            .collect();
        let excluded = excluded.or_else(|| {
            ranges
                .iter()
                .position(|r| !r.contains(&BigRational::zero()))
        });
        let contracted: Vec<_> = input
            .iter()
            .zip(&bounds)
            .enumerate()
            .filter_map(|(i, (a, b))| (a != b).then_some(i))
            .collect();
        let separation = if excluded.is_none() {
            separation_exclusion(&bounds, &BigRational::new(43623.into(), 1024.into()))
        } else {
            None
        };
        Ok(Inspection {
            schema: "mub6.quadratic_lift.interval_inspection.v2",
            authority_effect: "None",
            input_sha256: COEFFICIENT_SHA256,
            status: if excluded.is_some() || separation.is_some() {
                "EXCLUDED_BOX"
            } else if contracted.is_empty() {
                "UNRESOLVED_BOX"
            } else {
                "CONTRACTED_UNRESOLVED_BOX"
            },
            variable_count: VARIABLES,
            equation_count: EQUATIONS,
            term_count: 4920,
            probe_comparisons: EQUATIONS * 4,
            algorithm: "One ordered sweep; isolated linear and square terms; closed intersections; transition-column separation",
            square_bisections: 12,
            input_box: input.iter().map(pair).collect(),
            retained_box: bounds.iter().map(pair).collect(),
            equation_ranges: ranges.iter().map(pair).collect(),
            excluded_equation: excluded,
            separation_exclusion: separation,
            request_sha256: None,
            tightenings,
            contracted_coordinates: contracted,
            root_existence_claimed: false,
            kernel_reflected_runtime: false,
            global_nonexistence_claimed: false,
        })
    }
}

fn contract(
    polynomials: &[Polynomial],
    input: &[Interval],
) -> (Vec<Interval>, Vec<Tightening>, Option<usize>) {
    let mut bounds = input.to_vec();
    let mut changes = Vec::new();
    for (e, poly) in polynomials.iter().enumerate() {
        if !range(poly, &bounds, None).contains(&BigRational::zero()) {
            return (bounds, changes, Some(e));
        }
        for (k, (coefficient, factors)) in poly.iter().enumerate() {
            let (i, power) = match factors.as_slice() {
                [i] => (*i, 1),
                [i, j] if i == j => (*i, 2),
                _ => continue,
            };
            if poly
                .iter()
                .enumerate()
                .any(|(j, (_, f))| j != k && f.contains(&i))
            {
                continue;
            }
            let target = range(poly, &bounds, Some(k)).mul_scalar(&(-coefficient.recip()));
            let image = if power == 1 {
                target.clone()
            } else {
                if target.hi() < &BigRational::zero() {
                    return (bounds, changes, Some(e));
                }
                let mut hi = (-bounds[i].lo()).max(bounds[i].hi().clone());
                if &hi * &hi > *target.hi() {
                    let mut lo = BigRational::zero();
                    for _ in 0..12 {
                        let mid = (&lo + &hi) / BigRational::from_integer(2.into());
                        if &mid * &mid >= *target.hi() {
                            hi = mid;
                        } else {
                            lo = mid;
                        }
                    }
                }
                Interval::new(-&hi, hi)
            };
            let lo = bounds[i].lo().max(image.lo()).clone();
            let hi = bounds[i].hi().min(image.hi()).clone();
            if lo > hi {
                return (bounds, changes, Some(e));
            }
            let after = Interval::new(lo, hi);
            if after != bounds[i] {
                changes.push(Tightening {
                    equation: e,
                    variable: i,
                    isolated_power: power,
                    before: pair(&bounds[i]),
                    target_power_range: pair(&target),
                    after: pair(&after),
                });
                bounds[i] = after;
            }
        }
    }
    (bounds, changes, None)
}

#[cfg(test)]
mod tests {
    use super::*;
    const TABLE: &[u8] = include_bytes!("../../../../../papers/derivations/mub6/artifacts/quadratic_lift_coefficients_20261011.jsonl");
    fn q(n: i64) -> BigRational {
        BigRational::from_integer(n.into())
    }
    fn b(lo: i64, hi: i64) -> Interval {
        Interval::new(q(lo), q(hi))
    }

    #[test]
    fn full_table_contracts_only_transition_coordinates_and_remains_unresolved() {
        let system = QuadraticLift::from_bytes(TABLE).unwrap();
        let result = system.inspect_full_box().unwrap();
        assert_eq!(result.status, "CONTRACTED_UNRESOLVED_BOX");
        assert_eq!(
            result.contracted_coordinates,
            (170..386).collect::<Vec<_>>()
        );
        assert_eq!(result.excluded_equation, None);
        assert!(result.separation_exclusion.is_none());
        assert_eq!(result.tightenings.len(), 216);
        assert!(result.retained_box[170..]
            .iter()
            .all(|v| v == &["-10035/4096", "10035/4096"]));
        let zero = vec![Interval::point(q(0)); VARIABLES];
        let excluded = system.inspect_box(&zero).unwrap();
        assert_eq!(excluded.status, "EXCLUDED_BOX");
        assert_eq!(excluded.excluded_equation, Some(7));
        assert!(system.inspect_box(&[]).is_err());
        assert!(system.inspect_box(&vec![b(-4, 4); VARIABLES]).is_err());
    }

    #[test]
    fn digest_and_structural_mutations_are_rejected() {
        let mut changed = TABLE.to_vec();
        changed.push(b'\n');
        assert!(matches!(
            QuadraticLift::from_bytes(&changed),
            Err(LiftError::InputHash)
        ));
        let original: Vec<serde_json::Value> = std::str::from_utf8(TABLE)
            .unwrap()
            .lines()
            .map(|l| serde_json::from_str(l).unwrap())
            .collect();
        for case in 0..9 {
            let mut rows = original.clone();
            match case {
                0 => rows[0]["variable_count"] = 385.into(),
                1 => rows[0]["coordinate_bounds"][170][1] = "4/1".into(),
                2 => rows[8]["id"] = 8.into(),
                3 => rows[8]["probe_values"][0] = "0/1".into(),
                4 => rows[8]["terms"][0][0] = "-2/2".into(),
                5 => rows[8]["terms"][1][1] = serde_json::json!([386, 386]),
                6 => rows[8]["terms"][1] = rows[8]["terms"][0].clone(),
                7 => rows[649]["total_terms"] = 4919.into(),
                _ => rows[0]["infeasibility_claimed"] = true.into(),
            }
            let bytes = rows
                .iter()
                .map(|v| serde_json::to_string(v).unwrap())
                .collect::<Vec<_>>()
                .join("\n");
            assert!(
                QuadraticLift::decode(bytes.as_bytes()).is_err(),
                "mutation {case}"
            );
        }
        for bad in ["1", "1.0", "0/0", "2/2", "1/-2", "01/1"] {
            assert!(rational(bad).is_err(), "{bad}");
        }
    }

    #[test]
    fn square_enclosure_and_isolation_retain_known_roots_and_closed_contacts() {
        let circle = vec![(q(-25), vec![]), (q(1), vec![0, 0]), (q(1), vec![1, 1])];
        let (bounds, _, excluded) = contract(&[circle], &[b(-6, 6), b(-6, 6)]);
        assert_eq!(excluded, None);
        for (x, y) in [(3, 4), (-3, 4), (0, -5), (5, 0)] {
            assert!(bounds[0].contains(&q(x)) && bounds[1].contains(&q(y)));
        }
        assert_eq!(term_range(&(q(1), vec![0, 0]), &[b(-3, 3)]), b(0, 9));
        let linear = vec![(q(2), vec![]), (q(-1), vec![0])];
        assert_eq!(contract(&[linear.clone()], &[b(0, 2)]).0, vec![b(2, 2)]);
        assert_eq!(contract(&[linear], &[b(0, 1)]).2, Some(0));
        let coupled = vec![(q(-2), vec![]), (q(1), vec![0]), (q(1), vec![0, 0])];
        let (bounds, changes, excluded) = contract(&[coupled], &[b(-3, 3)]);
        assert!(changes.is_empty());
        assert_eq!(excluded, None);
        assert_eq!(bounds, vec![b(-3, 3)]);
    }

    #[test]
    fn separation_excludes_a_box_not_excluded_by_the_original_sweep() {
        let system = QuadraticLift::from_bytes(TABLE).unwrap();
        let mut bounds = system.full_box.clone();
        for a in 0..2 {
            for k in 0..6 {
                bounds[170 + 2 * (36 * a + 6 * k)] = Interval::new(
                    BigRational::new(9.into(), 10.into()),
                    BigRational::new(11.into(), 10.into()),
                );
                bounds[171 + 2 * (36 * a + 6 * k)] = Interval::new(
                    BigRational::new(11.into(), 5.into()),
                    BigRational::new(23.into(), 10.into()),
                );
                if k % 2 == 1 {
                    bounds[171 + 2 * (36 * a + 6 * k)] =
                        bounds[171 + 2 * (36 * a + 6 * k)].mul_scalar(&q(-1));
                }
            }
        }
        assert!(bounds.iter().all(|v| v.lo() < v.hi()));
        let (old_bounds, _, old_excluded) = contract(&system.polynomials, &bounds);
        assert_eq!(old_excluded, None);
        assert!(system
            .polynomials
            .iter()
            .all(|p| range(p, &old_bounds, None).contains(&q(0))));
        let request = serde_json::json!({
            "schema": "mub6.quadratic_lift.box.v1",
            "input_sha256": COEFFICIENT_SHA256,
            "bounds": bounds.iter().map(pair).collect::<Vec<_>>()
        });
        let bytes = serde_json::to_vec(&request).unwrap();
        let result = system.inspect_box_bytes(&bytes).unwrap();
        assert_eq!(result.status, "EXCLUDED_BOX");
        assert_eq!(result.excluded_equation, None);
        assert_eq!(
            result.request_sha256,
            Some(format!("{:x}", Sha256::digest(&bytes)))
        );
        let witness = result.separation_exclusion.unwrap();
        assert_eq!((witness.first_column, witness.second_column), (0, 0));
        assert_eq!(witness.distance_lower_bound, "43623/1024");
        assert!(parse_exact(&witness.distance_upper_bound).unwrap() < q(1));
        for case in 0..5 {
            let mut mutated = request.clone();
            match case {
                0 => mutated["bounds"][0] = serde_json::json!(["1", "-1"]),
                1 => mutated["bounds"][0][0] = "-2".into(),
                2 => mutated["bounds"][0][0] = serde_json::json!(false),
                3 => mutated["input_sha256"] = "wrong".into(),
                _ => mutated["bounds"] = serde_json::json!([]),
            }
            assert!(system
                .inspect_box_bytes(&serde_json::to_vec(&mutated).unwrap())
                .is_err());
        }
    }

    #[test]
    fn separation_requires_strict_distance_inequality() {
        let mut bounds = vec![b(0, 0); VARIABLES];
        for k in 0..6 {
            for j in 0..6 {
                bounds[170 + 2 * (36 + 6 * k + j)] = b(1, 1);
            }
        }
        assert!(separation_exclusion(&bounds, &q(6)).is_none());
        assert!(separation_exclusion(&bounds, &q(5)).is_none());
        let witness = separation_exclusion(&bounds, &q(7)).unwrap();
        assert_eq!(witness.distance_upper_bound, "6");
    }
}
