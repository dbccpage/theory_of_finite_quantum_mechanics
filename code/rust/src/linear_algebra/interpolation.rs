
use super::rational_bareiss::{RationalBudget, RationalError};
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};

pub type RationalEndpoints = (BigRational, BigRational);

#[derive(Clone, Debug, PartialEq, Eq, thiserror::Error)]
pub enum NevilleError {
    #[error("interpolation needs a nonempty finite node family")]
    EmptyNodes,
    #[error("{actual} sample values for {expected} nodes")]
    SampleCount { expected: usize, actual: usize },
    #[error("nodes {first} and {second} coincide")]
    DuplicateNode { first: usize, second: usize },
    #[error("interval endpoints are inverted")]
    InvertedInterval,
    #[error("interval intersection is empty")]
    EmptyIntersection,
    #[error(transparent)]
    Arithmetic(#[from] RationalError),
}

fn storage<T>(
    count: usize,
    scalars_per_element: usize,
    fuel: &RationalBudget,
) -> Result<Vec<T>, NevilleError> {
    fuel.elements(count, scalars_per_element)?;
    let mut out = Vec::new();
    out.try_reserve_exact(count)
        .map_err(|_| RationalError::Allocation)?;
    Ok(out)
}

fn check_nodes(
    nodes: &[BigRational],
    values: usize,
    at: &BigRational,
    fuel: &mut RationalBudget,
) -> Result<(), NevilleError> {
    if nodes.is_empty() {
        return Err(NevilleError::EmptyNodes);
    }
    if nodes.len() != values {
        return Err(NevilleError::SampleCount {
            expected: nodes.len(),
            actual: values,
        });
    }
    fuel.elements(nodes.len(), 1)?;
    fuel.rational(at)?;
    for node in nodes {
        fuel.rational(node)?;
    }
    for (second, node) in nodes.iter().enumerate() {
        for (first, previous) in nodes[..second].iter().enumerate() {
            fuel.charge(1)?;
            if node == previous {
                return Err(NevilleError::DuplicateNode { first, second });
            }
        }
    }
    Ok(())
}

pub fn validate_interval(
    interval: &RationalEndpoints,
    fuel: &mut RationalBudget,
) -> Result<(), NevilleError> {
    fuel.rational(&interval.0)?;
    fuel.rational(&interval.1)?;
    fuel.charge(1)?;
    if interval.0 > interval.1 {
        return Err(NevilleError::InvertedInterval);
    }
    Ok(())
}

pub fn interval_add(
    a: &RationalEndpoints,
    b: &RationalEndpoints,
    fuel: &mut RationalBudget,
) -> Result<RationalEndpoints, NevilleError> {
    validate_interval(a, fuel)?;
    validate_interval(b, fuel)?;
    Ok((fuel.add(&a.0, &b.0)?, fuel.add(&a.1, &b.1)?))
}

pub fn interval_scale(
    a: &RationalEndpoints,
    k: &BigRational,
    fuel: &mut RationalBudget,
) -> Result<RationalEndpoints, NevilleError> {
    validate_interval(a, fuel)?;
    fuel.rational(k)?;
    fuel.charge(1)?;
    let (lo, hi) = if k.is_negative() {
        (&a.1, &a.0)
    } else {
        (&a.0, &a.1)
    };
    Ok((fuel.mul(lo, k)?, fuel.mul(hi, k)?))
}

pub fn interval_divide(
    a: &RationalEndpoints,
    k: &BigRational,
    fuel: &mut RationalBudget,
) -> Result<RationalEndpoints, NevilleError> {
    validate_interval(a, fuel)?;
    fuel.rational(k)?;
    fuel.charge(1)?;
    if k.is_zero() {
        return Err(RationalError::DivisionByZero.into());
    }
    let (lo, hi) = if k.is_negative() {
        (&a.1, &a.0)
    } else {
        (&a.0, &a.1)
    };
    Ok((fuel.div(lo, k)?, fuel.div(hi, k)?))
}

pub fn intersect(
    a: &RationalEndpoints,
    b: &RationalEndpoints,
    fuel: &mut RationalBudget,
) -> Result<RationalEndpoints, NevilleError> {
    validate_interval(a, fuel)?;
    validate_interval(b, fuel)?;
    fuel.charge(3)?;
    let lo = if a.0 >= b.0 { &a.0 } else { &b.0 };
    let hi = if a.1 <= b.1 { &a.1 } else { &b.1 };
    if lo > hi {
        return Err(NevilleError::EmptyIntersection);
    }
    Ok((lo.clone(), hi.clone()))
}

pub fn interpolate_prefixes(
    nodes: &[BigRational],
    values: &[BigRational],
    at: &BigRational,
    fuel: &mut RationalBudget,
) -> Result<Vec<BigRational>, NevilleError> {
    check_nodes(nodes, values.len(), at, fuel)?;
    for value in values {
        fuel.rational(value)?;
    }
    let mut work: Vec<BigRational> = storage(nodes.len(), 1, fuel)?;
    let mut prefixes = storage(nodes.len(), 1, fuel)?;
    for (j, value) in values.iter().enumerate() {
        work.push(value.clone());
        for i in (0..j).rev() {
            let a = fuel.sub(at, &nodes[i])?;
            let b = fuel.sub(&nodes[j], at)?;
            let denominator = fuel.sub(&nodes[j], &nodes[i])?;
            let left = fuel.mul(&a, &work[i + 1])?;
            let right = fuel.mul(&b, &work[i])?;
            let numerator = fuel.add(&left, &right)?;
            work[i] = fuel.div(&numerator, &denominator)?;
        }
        prefixes.push(work[0].clone());
    }
    Ok(prefixes)
}

pub fn interpolate_interval_prefixes(
    nodes: &[BigRational],
    samples: &[RationalEndpoints],
    at: &BigRational,
    fuel: &mut RationalBudget,
) -> Result<Vec<RationalEndpoints>, NevilleError> {
    check_nodes(nodes, samples.len(), at, fuel)?;
    fuel.elements(samples.len(), 2)?;
    for sample in samples {
        validate_interval(sample, fuel)?;
    }
    let mut work: Vec<RationalEndpoints> = storage(nodes.len(), 2, fuel)?;
    let mut prefixes = storage(nodes.len(), 2, fuel)?;
    for (j, sample) in samples.iter().enumerate() {
        work.push(sample.clone());
        for i in (0..j).rev() {
            let a = fuel.sub(at, &nodes[i])?;
            let b = fuel.sub(&nodes[j], at)?;
            let denominator = fuel.sub(&nodes[j], &nodes[i])?;
            let left = interval_scale(&work[i + 1], &a, fuel)?;
            let right = interval_scale(&work[i], &b, fuel)?;
            let numerator = interval_add(&left, &right, fuel)?;
            work[i] = interval_divide(&numerator, &denominator, fuel)?;
        }
        prefixes.push(work[0].clone());
    }
    Ok(prefixes)
}

pub fn lagrange_interval_prefixes(
    nodes: &[BigRational],
    samples: &[RationalEndpoints],
    at: &BigRational,
    fuel: &mut RationalBudget,
) -> Result<Vec<RationalEndpoints>, NevilleError> {
    check_nodes(nodes, samples.len(), at, fuel)?;
    fuel.elements(samples.len(), 2)?;
    for sample in samples {
        validate_interval(sample, fuel)?;
    }
    let mut weights: Vec<BigRational> = storage(nodes.len(), 1, fuel)?;
    let mut prefixes = storage(nodes.len(), 2, fuel)?;
    for j in 0..nodes.len() {
        let mut newest = BigRational::one();
        let numerator = fuel.sub(at, &nodes[j])?;
        for i in 0..j {
            let denominator = fuel.sub(&nodes[i], &nodes[j])?;
            let factor = fuel.div(&numerator, &denominator)?;
            weights[i] = fuel.mul(&weights[i], &factor)?;
            let new_numerator = fuel.sub(at, &nodes[i])?;
            let new_denominator = fuel.sub(&nodes[j], &nodes[i])?;
            let new_factor = fuel.div(&new_numerator, &new_denominator)?;
            newest = fuel.mul(&newest, &new_factor)?;
        }
        weights.push(newest);
        let mut sum = (BigRational::zero(), BigRational::zero());
        for i in 0..=j {
            let term = interval_scale(&samples[i], &weights[i], fuel)?;
            sum = interval_add(&sum, &term, fuel)?;
        }
        prefixes.push(sum);
    }
    Ok(prefixes)
}
