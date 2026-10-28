
use std::collections::{BTreeMap, BTreeSet};

use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use tfqm_holonomy::{ExactScalar, GaussianRational};
use serde::Serialize;

use crate::connection::U1Connection;
use crate::error::WdpError;
use crate::types::AuthorityEffect;

pub type Amplitude = GaussianRational<BigRational>;

pub const MAX_EXPONENT: i64 = 4096;

pub const MAX_VERTICES: usize = 100_000;

fn invalid(detail: String) -> WdpError {
    WdpError::InvalidInput { detail }
}

fn ratio(numerator: i64, denominator: i64) -> BigRational {
    BigRational::new(numerator.into(), denominator.into())
}

pub fn norm(z: &Amplitude) -> BigRational {
    z.norm_sq()
}

pub fn conj(z: &Amplitude) -> Amplitude {
    z.conjugate()
}

pub fn mul(a: &Amplitude, b: &Amplitude) -> Amplitude {
    a.clone() * b.clone()
}

pub fn unit_phase() -> Amplitude {
    GaussianRational::new(ratio(3, 5), ratio(4, 5)).expect("3/5 and 4/5 are reduced rationals")
}

pub fn u_pow(n: i64) -> Result<Amplitude, WdpError> {
    if n.unsigned_abs() > MAX_EXPONENT.unsigned_abs() {
        return Err(invalid(format!(
            "|n| = {} exceeds {MAX_EXPONENT}",
            n.unsigned_abs()
        )));
    }
    let mut result = Amplitude::one();
    let mut base = unit_phase();
    let mut exponent = n.unsigned_abs();
    while exponent > 0 {
        if exponent & 1 == 1 {
            result = mul(&result, &base);
        }
        base = mul(&base, &base);
        exponent >>= 1;
    }
    Ok(if n < 0 { conj(&result) } else { result })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OrientedGraph {
    vertices: usize,
    edges: Vec<(usize, usize)>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PathStep {
    pub edge: usize,
    pub forward: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EdgePath {
    pub start: usize,
    pub steps: Vec<PathStep>,
}

impl OrientedGraph {
    pub fn new(vertices: usize, edges: Vec<(usize, usize)>) -> Result<Self, WdpError> {
        if vertices == 0 {
            return Err(invalid("a graph needs at least one vertex".to_string()));
        }
        if vertices > MAX_VERTICES {
            return Err(invalid(format!(
                "{vertices} vertices exceed the cap {MAX_VERTICES}"
            )));
        }
        for (e, &(u, v)) in edges.iter().enumerate() {
            if u >= vertices || v >= vertices {
                return Err(invalid(format!(
                    "edge {e} = ({u}, {v}) leaves 0..{vertices}"
                )));
            }
            if u == v {
                return Err(invalid(format!("edge {e} is a self-loop at {u}")));
            }
        }
        Ok(Self { vertices, edges })
    }

    pub fn vertices(&self) -> usize {
        self.vertices
    }

    pub fn edges(&self) -> &[(usize, usize)] {
        &self.edges
    }

    fn check_cochain(&self, a: &[i64]) -> Result<(), WdpError> {
        if a.len() != self.edges.len() {
            return Err(invalid(format!(
                "cochain has {} values for {} edges",
                a.len(),
                self.edges.len()
            )));
        }
        Ok(())
    }

    pub fn path_end(&self, path: &EdgePath) -> Result<usize, WdpError> {
        if path.start >= self.vertices {
            return Err(invalid(format!(
                "path starts at vertex {} outside the graph",
                path.start
            )));
        }
        let mut here = path.start;
        for (k, step) in path.steps.iter().enumerate() {
            let &(tail, head) = self.edges.get(step.edge).ok_or_else(|| {
                invalid(format!(
                    "step {k} names edge {} outside the graph",
                    step.edge
                ))
            })?;
            let (from, to) = if step.forward {
                (tail, head)
            } else {
                (head, tail)
            };
            if from != here {
                return Err(invalid(format!(
                    "step {k} starts at {from} but the path is at {here}"
                )));
            }
            here = to;
        }
        Ok(here)
    }

    pub fn inverse_path(&self, path: &EdgePath) -> Result<EdgePath, WdpError> {
        let end = self.path_end(path)?;
        Ok(EdgePath {
            start: end,
            steps: path
                .steps
                .iter()
                .rev()
                .map(|s| PathStep {
                    edge: s.edge,
                    forward: !s.forward,
                })
                .collect(),
        })
    }

    pub fn concat_paths(&self, first: &EdgePath, second: &EdgePath) -> Result<EdgePath, WdpError> {
        let end = self.path_end(first)?;
        self.path_end(second)?;
        if second.start != end {
            return Err(invalid(format!(
                "cannot concatenate: first path ends at {end}, second starts at {}",
                second.start
            )));
        }
        Ok(EdgePath {
            start: first.start,
            steps: first.steps.iter().chain(&second.steps).copied().collect(),
        })
    }

    pub fn coboundary(&self, f: &[i64]) -> Result<Vec<i64>, WdpError> {
        if f.len() != self.vertices {
            return Err(invalid(format!(
                "0-cochain has {} values for {} vertices",
                f.len(),
                self.vertices
            )));
        }
        self.edges
            .iter()
            .map(|&(u, v)| {
                f[v].checked_sub(f[u])
                    .ok_or_else(|| invalid("coboundary overflows i64".to_string()))
            })
            .collect()
    }

    pub fn gauge_transform(&self, a: &[i64], f: &[i64]) -> Result<Vec<i64>, WdpError> {
        self.check_cochain(a)?;
        self.coboundary(f)?
            .into_iter()
            .zip(a)
            .map(|(d, &x)| {
                d.checked_add(x)
                    .ok_or_else(|| invalid("gauge transform overflows i64".to_string()))
            })
            .collect()
    }

    pub fn transport(&self, a: &[i64], edge: usize) -> Result<Amplitude, WdpError> {
        self.check_cochain(a)?;
        let value = a
            .get(edge)
            .ok_or_else(|| invalid(format!("edge {edge} outside the graph")))?;
        u_pow(*value)
    }

    pub fn gauge_conjugated_transport(
        &self,
        a: &[i64],
        f: &[i64],
        edge: usize,
    ) -> Result<Amplitude, WdpError> {
        self.check_cochain(a)?;
        if f.len() != self.vertices {
            return Err(invalid(format!(
                "0-cochain has {} values for {} vertices",
                f.len(),
                self.vertices
            )));
        }
        let &(tail, head) = self
            .edges
            .get(edge)
            .ok_or_else(|| invalid(format!("edge {edge} outside the graph")))?;
        let (g_head, g_tail) = (u_pow(f[head])?, u_pow(f[tail])?);
        Ok(mul(
            &mul(&g_head, &self.transport(a, edge)?),
            &conj(&g_tail),
        ))
    }

    pub fn pairing(&self, a: &[i64], path: &EdgePath) -> Result<i64, WdpError> {
        self.check_cochain(a)?;
        self.path_end(path)?;
        path.steps.iter().try_fold(0i64, |acc, step| {
            let value = if step.forward {
                Some(a[step.edge])
            } else {
                a[step.edge].checked_neg()
            };
            value
                .and_then(|v| acc.checked_add(v))
                .ok_or_else(|| invalid("pairing overflows i64".to_string()))
        })
    }

    pub fn path_amplitude(&self, a: &[i64], path: &EdgePath) -> Result<Amplitude, WdpError> {
        self.check_cochain(a)?;
        self.path_end(path)?;
        let mut amplitude = Amplitude::one();
        for step in &path.steps {
            let transport = self.transport(a, step.edge)?;
            amplitude = mul(
                &amplitude,
                &if step.forward {
                    transport
                } else {
                    conj(&transport)
                },
            );
        }
        Ok(amplitude)
    }

    pub fn holonomy(&self, a: &[i64], path: &EdgePath) -> Result<Amplitude, WdpError> {
        let end = self.path_end(path)?;
        if end != path.start {
            return Err(invalid(format!(
                "path from {} ends at {end}: not closed",
                path.start
            )));
        }
        self.path_amplitude(a, path)
    }

    pub fn path_vertex_names(&self, path: &EdgePath) -> Result<Vec<String>, WdpError> {
        self.path_end(path)?;
        let mut here = path.start;
        let mut names = vec![vertex_name(here)];
        for step in &path.steps {
            let (tail, head) = self.edges[step.edge];
            here = if step.forward { head } else { tail };
            names.push(vertex_name(here));
        }
        Ok(names)
    }

    pub fn u1_connection(&self, a: &[i64]) -> Result<U1Connection, WdpError> {
        self.check_cochain(a)?;
        let vertices: BTreeSet<String> = (0..self.vertices).map(vertex_name).collect();
        let mut phases = BTreeMap::new();
        for (e, &(u, v)) in self.edges.iter().enumerate() {
            let key = (vertex_name(u), vertex_name(v));
            if phases.insert(key, u_pow(a[e])?).is_some() {
                return Err(invalid(format!("edge {e} is parallel to an earlier edge")));
            }
        }
        U1Connection::new(vertices, phases)
    }
}

fn vertex_name(v: usize) -> String {
    format!("v{v}")
}

pub fn relative_phase(z1: &Amplitude, z2: &Amplitude) -> Option<Amplitude> {
    z2.exact_inv().ok().map(|inv| mul(z1, &inv))
}

pub fn same_up_to_common_phase(
    z: &(Amplitude, Amplitude),
    w: &(Amplitude, Amplitude),
) -> Option<Amplitude> {
    if norm(&z.0) != norm(&w.0) || norm(&z.1) != norm(&w.1) {
        return None;
    }
    if mul(&z.0, &conj(&z.1)) != mul(&w.0, &conj(&w.1)) {
        return None;
    }
    let g = if !z.0.is_zero() {
        mul(&w.0, &z.0.exact_inv().ok()?)
    } else if !z.1.is_zero() {
        mul(&w.1, &z.1.exact_inv().ok()?)
    } else {
        Amplitude::one()
    };
    let verified = norm(&g).is_one() && mul(&g, &z.0) == w.0 && mul(&g, &z.1) == w.1;
    verified.then_some(g)
}

pub fn readout_quadratic(z1: &Amplitude, z2: &Amplitude) -> BigRational {
    norm(&(z1.clone() + z2.clone()))
}

pub fn readout_quartic(z1: &Amplitude, z2: &Amplitude) -> BigRational {
    let quadratic = readout_quadratic(z1, z2);
    &quadratic * &quadratic
}

pub fn cross_term(z1: &Amplitude, z2: &Amplitude) -> BigRational {
    let product = mul(z1, &conj(z2));
    product.real() + product.real()
}

fn rational_sqrt(x: &BigRational) -> Option<BigRational> {
    if x.is_negative() {
        return None;
    }
    let root = |n: &num_bigint::BigInt| {
        let r = n.sqrt();
        (&r * &r == *n).then_some(r)
    };
    Some(BigRational::new(root(x.numer())?, root(x.denom())?))
}

pub fn unit_square_root(z: &Amplitude) -> Result<Option<Amplitude>, WdpError> {
    if !norm(z).is_one() {
        return Err(invalid(format!("{z} is not of norm one")));
    }
    let x_squared = (BigRational::one() + z.real()) / BigRational::from_integer(2.into());
    let Some(x) = rational_sqrt(&x_squared) else {
        return Ok(None);
    };
    let root = if x.is_zero() {
        Amplitude::i()
    } else {
        let y = z.imag() / (&x + &x);
        GaussianRational::new(x, y)?
    };
    Ok((mul(&root, &root) == *z).then_some(root))
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct HalfExponentObstruction {
    pub u: Amplitude,
    pub x_squared: BigRational,
    pub x_squared_is_rational_square: bool,
    pub u_has_square_root_in_q_i: bool,
    pub authority_effect: AuthorityEffect,
}

pub fn half_exponent_obstruction() -> Result<HalfExponentObstruction, WdpError> {
    let u = unit_phase();
    let x_squared = (BigRational::one() + u.real()) / BigRational::from_integer(2.into());
    Ok(HalfExponentObstruction {
        x_squared_is_rational_square: rational_sqrt(&x_squared).is_some(),
        u_has_square_root_in_q_i: unit_square_root(&u)?.is_some(),
        x_squared,
        u,
        authority_effect: AuthorityEffect::None,
    })
}

pub fn unit_phase_numerator_mod_five(n: u64) -> (u8, u8) {
    let mul = |(a, b): (u8, u8), (c, d): (u8, u8)| ((a * c + 4 * b * d) % 5, (a * d + b * c) % 5);
    let mut result = (1u8, 0u8);
    let mut base = (3u8, 4u8);
    let mut exponent = n;
    while exponent > 0 {
        if exponent & 1 == 1 {
            result = mul(result, base);
        }
        base = mul(base, base);
        exponent >>= 1;
    }
    result
}

pub fn u_power_is_never_one(n: i64) -> Result<bool, WdpError> {
    let exponent = u64::try_from(n)
        .ok()
        .filter(|&e| e >= 1)
        .ok_or_else(|| invalid(format!("n = {n} is not a positive exponent")))?;
    Ok(unit_phase_numerator_mod_five(exponent) != (0, 0))
}
