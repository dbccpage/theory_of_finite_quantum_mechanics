use std::collections::VecDeque;

pub const ORIGIN: &str =
    "Origin: code/rust/src/wdp/mod.rs @ 40de7d5cda1ff1f0db8305d0c1b2103646fab197";
pub const CLAIM: &str = "Claim: an integer 1-cochain on a finite directed graph is exact exactly when it is the coboundary of a 0-cochain, and the constant 3-cycle has L1 weight 3 and is not exact";
pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: u32 = 4;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CochainError {
    EmptyCarrier,
    EdgeOutOfRange { edge: usize, vertices: usize },
    VertexOutOfRange { vertex: usize, vertices: usize },
    Length { edges: usize, values: usize },
    PotentialLength { vertices: usize, values: usize },
    Overflow,
    BinaryFloatRefused,
    BooleanAsNumber,
    InexactToken,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DirectedCochain {
    vertices: usize,
    edges: Vec<(usize, usize)>,
    values: Vec<i64>,
}

pub fn admit_exact_integer(token: &str) -> Result<i64, CochainError> {
    if token == "true" || token == "false" {
        return Err(CochainError::BooleanAsNumber);
    }
    if token.bytes().any(|byte| matches!(byte, b'.' | b'e' | b'E')) {
        return Err(CochainError::BinaryFloatRefused);
    }
    parse_signed_digits(token)
}

fn parse_signed_digits(token: &str) -> Result<i64, CochainError> {
    let (negative, digits) = match token.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, token),
    };
    if digits.is_empty() || !digits.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err(CochainError::InexactToken);
    }
    let mut value = 0i64;
    for byte in digits.bytes() {
        let digit = i64::from(byte - b'0');
        value = value
            .checked_mul(10)
            .and_then(|place| place.checked_add(digit))
            .ok_or(CochainError::Overflow)?;
    }
    if negative {
        value = value.checked_neg().ok_or(CochainError::Overflow)?;
    }
    Ok(value)
}

fn read_potential(potential: &[Option<i64>], vertex: usize) -> Result<Option<i64>, CochainError> {
    potential
        .get(vertex)
        .copied()
        .ok_or(CochainError::VertexOutOfRange {
            vertex,
            vertices: potential.len(),
        })
}

fn write_potential(
    potential: &mut [Option<i64>],
    vertex: usize,
    value: i64,
) -> Result<(), CochainError> {
    let vertices = potential.len();
    let slot = potential
        .get_mut(vertex)
        .ok_or(CochainError::VertexOutOfRange { vertex, vertices })?;
    *slot = Some(value);
    Ok(())
}

fn head_from_tail(tail: i64, value: i64) -> Result<i64, CochainError> {
    tail.checked_add(value).ok_or(CochainError::Overflow)
}

fn tail_from_head(head: i64, value: i64) -> Result<i64, CochainError> {
    head.checked_sub(value).ok_or(CochainError::Overflow)
}

impl DirectedCochain {
    pub fn new(
        vertices: usize,
        edges: Vec<(usize, usize)>,
        values: Vec<i64>,
    ) -> Result<Self, CochainError> {
        if vertices == 0 {
            return Err(CochainError::EmptyCarrier);
        }
        if edges.len() != values.len() {
            return Err(CochainError::Length {
                edges: edges.len(),
                values: values.len(),
            });
        }
        for (index, &(tail, head)) in edges.iter().enumerate() {
            if tail >= vertices || head >= vertices {
                return Err(CochainError::EdgeOutOfRange {
                    edge: index,
                    vertices,
                });
            }
        }
        Ok(Self {
            vertices,
            edges,
            values,
        })
    }

    pub fn from_potential(
        vertices: usize,
        edges: Vec<(usize, usize)>,
        potential: &[i64],
    ) -> Result<Self, CochainError> {
        if potential.len() != vertices {
            return Err(CochainError::PotentialLength {
                vertices,
                values: potential.len(),
            });
        }
        let mut values = Vec::new();
        for &(tail, head) in &edges {
            let tail_value = *potential.get(tail).ok_or(CochainError::VertexOutOfRange {
                vertex: tail,
                vertices,
            })?;
            let head_value = *potential.get(head).ok_or(CochainError::VertexOutOfRange {
                vertex: head,
                vertices,
            })?;
            values.push(tail_from_head(head_value, tail_value)?);
        }
        Self::new(vertices, edges, values)
    }

    pub fn l1_weight(&self) -> Result<i64, CochainError> {
        let mut total = 0i64;
        for value in &self.values {
            let magnitude = value.checked_abs().ok_or(CochainError::Overflow)?;
            total = total.checked_add(magnitude).ok_or(CochainError::Overflow)?;
        }
        Ok(total)
    }

    pub fn authority_effect(&self) -> &'static str {
        AUTHORITY_EFFECT
    }

    pub fn is_exact(&self) -> Result<bool, CochainError> {
        let mut potential = vec![None; self.vertices];
        for root in 0..self.vertices {
            if read_potential(&potential, root)?.is_some() {
                continue;
            }
            write_potential(&mut potential, root, 0)?;
            if !self.component_consistent(root, &mut potential)? {
                return Ok(false);
            }
        }
        Ok(true)
    }

    fn component_consistent(
        &self,
        root: usize,
        potential: &mut [Option<i64>],
    ) -> Result<bool, CochainError> {
        let mut queue = VecDeque::new();
        queue.push_back(root);
        while queue.pop_front().is_some() {
            if !self.scan_edges(potential, &mut queue)? {
                return Ok(false);
            }
        }
        Ok(true)
    }

    fn scan_edges(
        &self,
        potential: &mut [Option<i64>],
        queue: &mut VecDeque<usize>,
    ) -> Result<bool, CochainError> {
        for index in 0..self.edges.len() {
            if !self.propagate(index, potential, queue)? {
                return Ok(false);
            }
        }
        Ok(true)
    }

    fn propagate(
        &self,
        index: usize,
        potential: &mut [Option<i64>],
        queue: &mut VecDeque<usize>,
    ) -> Result<bool, CochainError> {
        let (tail, head) = match self.edges.get(index) {
            Some(edge) => *edge,
            None => {
                return Err(CochainError::EdgeOutOfRange {
                    edge: index,
                    vertices: self.vertices,
                })
            }
        };
        let value = match self.values.get(index) {
            Some(value) => *value,
            None => {
                return Err(CochainError::Length {
                    edges: self.edges.len(),
                    values: self.values.len(),
                })
            }
        };
        let tail_p = read_potential(potential, tail)?;
        let head_p = read_potential(potential, head)?;
        self.apply_edge(tail, head, tail_p, head_p, value, potential, queue)
    }

    fn apply_known_tail(
        &self,
        head: usize,
        tail_value: i64,
        head_value: Option<i64>,
        value: i64,
        potential: &mut [Option<i64>],
        queue: &mut VecDeque<usize>,
    ) -> Result<bool, CochainError> {
        let expected = head_from_tail(tail_value, value)?;
        if let Some(found) = head_value {
            return Ok(found == expected);
        }
        write_potential(potential, head, expected)?;
        queue.push_back(head);
        Ok(true)
    }

    fn apply_known_head(
        &self,
        tail: usize,
        head_value: i64,
        value: i64,
        potential: &mut [Option<i64>],
        queue: &mut VecDeque<usize>,
    ) -> Result<bool, CochainError> {
        let expected = tail_from_head(head_value, value)?;
        write_potential(potential, tail, expected)?;
        queue.push_back(tail);
        Ok(true)
    }

    fn apply_edge(
        &self,
        tail: usize,
        head: usize,
        tail_p: Option<i64>,
        head_p: Option<i64>,
        value: i64,
        potential: &mut [Option<i64>],
        queue: &mut VecDeque<usize>,
    ) -> Result<bool, CochainError> {
        match (tail_p, head_p) {
            (Some(tail_value), head_value) => {
                self.apply_known_tail(head, tail_value, head_value, value, potential, queue)
            }
            (None, Some(head_value)) => {
                self.apply_known_head(tail, head_value, value, potential, queue)
            }
            (None, None) => Ok(true),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn need(cond: bool, message: &str) -> Result<(), String> {
        if cond {
            Ok(())
        } else {
            Err(message.to_string())
        }
    }

    fn triangle(values: Vec<i64>) -> Result<DirectedCochain, CochainError> {
        DirectedCochain::new(3, vec![(0, 1), (1, 2), (2, 0)], values)
    }

    fn show(error: impl std::fmt::Debug) -> String {
        format!("{error:?}")
    }

    #[test]
    fn unit_constant_triangle_is_not_exact_and_weighs_three() -> Result<(), String> {
        triangle(vec![1, 1, 1]).map_err(show).and_then(unit_cycle)
    }

    fn unit_cycle(cycle: DirectedCochain) -> Result<(), String> {
        let weight = cycle.l1_weight().map_err(show)?;
        let exact = cycle.is_exact().map_err(show)?;
        unit_cycle_claims(weight, exact, cycle.authority_effect())
    }

    fn unit_cycle_claims(weight: i64, exact: bool, effect: &str) -> Result<(), String> {
        need(weight == 3, "l1")?;
        need(!exact, "obstruction")?;
        need(effect == AUTHORITY_EFFECT, "authority")
    }

    #[test]
    fn integration_potential_coboundary_is_exact() -> Result<(), String> {
        DirectedCochain::from_potential(3, vec![(0, 1), (1, 2), (2, 0)], &[0, 1, -1])
            .map_err(show)
            .and_then(integration_coboundary)
    }

    fn integration_coboundary(cochain: DirectedCochain) -> Result<(), String> {
        let exact = cochain.is_exact().map_err(show)?;
        let weight = cochain.l1_weight().map_err(show)?;
        integration_values(exact, weight)
    }

    fn integration_values(exact: bool, weight: i64) -> Result<(), String> {
        need(exact, "coboundary")?;
        need(weight == 4, "differences")
    }

    #[test]
    fn e2e_balanced_triangle_closes_and_constant_cycle_does_not() -> Result<(), String> {
        e2e_pair().and_then(|(balanced, obstructed)| e2e_exactness(balanced, obstructed))
    }

    fn e2e_pair() -> Result<(DirectedCochain, DirectedCochain), String> {
        let balanced = triangle(vec![1, 1, -2]).map_err(show)?;
        let obstructed = triangle(vec![1, 1, 1]).map_err(show)?;
        Ok((balanced, obstructed))
    }

    fn e2e_exactness(balanced: DirectedCochain, obstructed: DirectedCochain) -> Result<(), String> {
        let balanced_exact = balanced.is_exact().map_err(show)?;
        let obstructed_exact = obstructed.is_exact().map_err(show)?;
        e2e_claims(balanced_exact, obstructed_exact)
    }

    fn e2e_claims(balanced_exact: bool, obstructed_exact: bool) -> Result<(), String> {
        need(balanced_exact, "balanced")?;
        need(!obstructed_exact, "constant")?;
        e2e_text()
    }

    fn e2e_text() -> Result<(), String> {
        need(ORIGIN.contains("code/rust/src/wdp/mod.rs"), "origin")?;
        need(CLAIM.contains("L1 weight 3"), "claim")
    }

    #[test]
    fn negative_refuses_empty_carrier_range_length_overflow_and_inexact_tokens() -> Result<(), String>
    {
        negative_shape().and_then(|_| negative_tokens())
    }

    fn negative_shape() -> Result<(), String> {
        need(DirectedCochain::new(0, vec![], vec![]).is_err(), "empty carrier")?;
        need(
            matches!(
                DirectedCochain::new(1, vec![(0, 2)], vec![1]),
                Err(CochainError::EdgeOutOfRange { .. })
            ),
            "edge range",
        )?;
        need(
            matches!(
                DirectedCochain::new(2, vec![(0, 1)], vec![]),
                Err(CochainError::Length { .. })
            ),
            "length",
        )
    }

    fn negative_tokens() -> Result<(), String> {
        need(
            matches!(
                DirectedCochain::from_potential(2, vec![(0, 1)], &[i64::MAX, i64::MIN]),
                Err(CochainError::Overflow)
            ),
            "overflow",
        )?;
        need(
            admit_exact_integer("1.5") == Err(CochainError::BinaryFloatRefused),
            "float",
        )?;
        negative_integer()
    }

    fn negative_integer() -> Result<(), String> {
        need(
            admit_exact_integer("true") == Err(CochainError::BooleanAsNumber),
            "bool",
        )?;
        need(admit_exact_integer("-4") == Ok(-4), "integer")
    }
}
