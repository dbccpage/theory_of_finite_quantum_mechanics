//! Checked simulations and conservative resource extensions of finite dynamics.
//! A successful exact check reflects availability. An extension preserves every
//! old defined step but may add availability, which is listed explicitly.
use crate::finite_continuation::PartialDynamics;
use std::collections::BTreeSet;
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SimulationMode {
    Exact,
    ResourceExtension,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SimulationError {
    InvalidMap,
    InvalidEncoding,
    WorkLimit,
    CertificateMismatch,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SimulationDecision {
    Checked {
        added_availability: Vec<(usize, usize)>,
    },
    ReportMismatch {
        state: usize,
        source_report: usize,
        target_report: usize,
    },
    StepMismatch {
        state: usize,
        input: usize,
        expected: Option<usize>,
        actual: Option<usize>,
    },
}
/// All maps and event macros are explicit. Readout labels must share one declared
/// interpretation; mere numerical equality does not supply a semantic dictionary.
pub fn check_simulation(
    source: &PartialDynamics,
    target: &PartialDynamics,
    map: &[usize],
    words: &[Vec<usize>],
    mode: SimulationMode,
    max_cells: usize,
) -> Result<SimulationDecision, SimulationError> {
    if map.len() != source.reports().len()
        || map.iter().any(|&t| t >= target.reports().len())
        || (mode == SimulationMode::ResourceExtension
            && map.iter().collect::<BTreeSet<_>>().len() != map.len())
    {
        return Err(SimulationError::InvalidMap);
    }
    if words.len() != source.transitions()[0].len()
        || words
            .iter()
            .flatten()
            .any(|&a| a >= target.transitions()[0].len())
    {
        return Err(SimulationError::InvalidEncoding);
    }
    let width = words
        .iter()
        .try_fold(1usize, |n, w| n.checked_add(w.len().checked_add(1)?));
    if width
        .and_then(|n| n.checked_mul(map.len()))
        .is_none_or(|n| n > max_cells)
    {
        return Err(SimulationError::WorkLimit);
    }
    let mut added = Vec::new();
    for (s, &t) in map.iter().enumerate() {
        if source.reports()[s] != target.reports()[t] {
            return Ok(SimulationDecision::ReportMismatch {
                state: s,
                source_report: source.reports()[s],
                target_report: target.reports()[t],
            });
        }
        for (a, w) in words.iter().enumerate() {
            let expected = source.transitions()[s][a].map(|s| map[s]);
            let actual = target
                .run(t, w)
                .map_err(|_| SimulationError::InvalidEncoding)?;
            if expected.is_none() && actual.is_some() && mode == SimulationMode::ResourceExtension {
                added.push((s, a));
            } else if expected != actual {
                return Ok(SimulationDecision::StepMismatch {
                    state: s,
                    input: a,
                    expected,
                    actual,
                });
            }
        }
    }
    Ok(SimulationDecision::Checked {
        added_availability: added,
    })
}
pub fn verify_simulation(
    source: &PartialDynamics,
    target: &PartialDynamics,
    map: &[usize],
    words: &[Vec<usize>],
    mode: SimulationMode,
    max_cells: usize,
    c: &SimulationDecision,
) -> Result<(), SimulationError> {
    if check_simulation(source, target, map, words, mode, max_cells)? == *c {
        Ok(())
    } else {
        Err(SimulationError::CertificateMismatch)
    }
}
