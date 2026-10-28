
pub mod sparse;

use engine_homology::f2_cohomology::ComplexError;
use engine_homology::finite_poset::{FinitePoset, PosetError};
use engine_homology::integral_chain_complex::{IntegralChainComplex, SparseIntegerMatrix};
use engine_homology::integral_chain_equivalence::{
    verify_chain_equivalence, ChainEquivalenceCertificate, ChainEquivalenceError,
};
use engine_homology::permutohedral::{
    add_scaled, boundary, Cell, CellChain, ContractionLimits, LinearExtensionContraction,
    PermutohedralError,
};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use std::time::Instant;

pub const MAX_PAIRS: usize = 4;
pub const MAX_CERTIFICATE_BYTES: usize = 64 * 1024 * 1024;
pub const SCHEMA: &str = "omega.wdp.guarded-chain-transport.v1";
pub type CellLevels = Vec<Vec<Cell>>;
type CellIndex = Vec<BTreeMap<Cell, usize>>;
type CellImages = BTreeMap<Cell, CellChain>;
type OrderKey = Vec<(usize, usize)>;
type CarrierCache = BTreeMap<OrderKey, LinearExtensionContraction>;

#[derive(Debug, thiserror::Error)]
pub enum TransportError {
    #[error("pair count must be in 1..={MAX_PAIRS}, and capacity in 1..=pair count")]
    Parameters,
    #[error("invalid transport certificate: {0}")]
    Certificate(&'static str),
    #[error("required cell is absent from the declared complex")]
    MissingCell,
    #[error("integer overflow while {0}")]
    Overflow(&'static str),
    #[error(transparent)]
    Poset(#[from] PosetError),
    #[error(transparent)]
    Cellular(#[from] PermutohedralError),
    #[error(transparent)]
    Complex(#[from] ComplexError),
    #[error(transparent)]
    Equivalence(#[from] ChainEquivalenceError),
}
type Result<T> = std::result::Result<T, TransportError>;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct MatrixProposal {
    pub rows: usize,
    pub columns: Vec<Vec<(usize, i64)>>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct WitnessProposal {
    pub degree: usize,
    pub task_cycle: Vec<i64>,
    pub task_cocycle: Vec<i64>,
    pub event_cycle: Vec<i64>,
    pub event_cocycle: Vec<i64>,
    pub pairing: i64,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct TransportProposal {
    pub schema: String,
    pub pairs: usize,
    pub capacity: usize,
    pub event_cells: CellLevels,
    pub task_cells: CellLevels,
    pub projection: Vec<MatrixProposal>,
    pub inclusion: Vec<MatrixProposal>,
    pub source_homotopy: Vec<MatrixProposal>,
    pub target_homotopy: Vec<MatrixProposal>,
    pub witness: Option<WitnessProposal>,
}

#[derive(Debug, Clone, Serialize)]
pub struct ConstructionTimings {
    pub enumerate_microseconds: u128,
    pub maps_microseconds: u128,
    pub check_microseconds: u128,
    pub witness_microseconds: u128,
    pub task_carriers: usize,
    pub event_carriers: usize,
}

#[derive(Debug, Clone, Serialize)]
pub struct VerificationReport {
    pub status: &'static str,
    pub authority_effect: &'static str,
    pub pairs: usize,
    pub capacity: usize,
    pub event_f_vector: Vec<usize>,
    pub task_f_vector: Vec<usize>,
    pub checked_degrees: usize,
    pub checked_matrix_identities: usize,
    pub projection_inclusion_is_identity: bool,
    pub map_nonzero_entries: BTreeMap<&'static str, usize>,
    pub witness: Option<WitnessSummary>,
}

#[derive(Debug, Clone, Serialize)]
pub struct WitnessSummary {
    pub degree: usize,
    pub task_cycle_support: usize,
    pub task_cocycle_support: usize,
    pub event_cycle_support: usize,
    pub event_cocycle_support: usize,
    pub pairing: i64,
}

pub fn parameters(pairs: usize, capacity: usize) -> Result<()> {
    if !(1..=MAX_PAIRS).contains(&pairs) || capacity == 0 || capacity > pairs {
        return Err(TransportError::Parameters);
    }
    Ok(())
}

pub fn enumerate_event_cells(pairs: usize, capacity: usize) -> Result<CellLevels> {
    parameters(pairs, capacity)?;
    fn visit(states: &mut [u8], capacity: usize, blocks: &mut Cell, levels: &mut CellLevels) {
        if states.iter().all(|&s| s == 2) {
            levels[2 * states.len() - blocks.len()].push(blocks.clone());
            return;
        }
        let unstarted: Vec<_> = (0..states.len()).filter(|&i| states[i] == 0).collect();
        let active: Vec<_> = (0..states.len()).filter(|&i| states[i] == 1).collect();
        for start_mask in 0usize..(1 << unstarted.len()) {
            if active.len() + start_mask.count_ones() as usize > capacity {
                continue;
            }
            for finish_mask in 0usize..(1 << active.len()) {
                if start_mask == 0 && finish_mask == 0 {
                    continue;
                }
                let mut block = Vec::new();
                for (bit, &i) in unstarted.iter().enumerate() {
                    if start_mask & (1 << bit) != 0 {
                        states[i] = 1;
                        block.push(2 * i);
                    }
                }
                for (bit, &i) in active.iter().enumerate() {
                    if finish_mask & (1 << bit) != 0 {
                        states[i] = 2;
                        block.push(2 * i + 1);
                    }
                }
                block.sort_unstable();
                blocks.push(block);
                visit(states, capacity, blocks, levels);
                blocks.pop();
                for &i in &unstarted {
                    states[i] = 0;
                }
                for &i in &active {
                    states[i] = 1;
                }
            }
        }
    }
    let mut levels = vec![Vec::new(); 2 * pairs];
    visit(&mut vec![0; pairs], capacity, &mut Vec::new(), &mut levels);
    pack(&mut levels);
    Ok(levels)
}

pub fn enumerate_task_cells(pairs: usize, capacity: usize) -> Result<CellLevels> {
    parameters(pairs, capacity)?;
    fn visit(
        remaining: &[usize],
        capacity: usize,
        blocks: &mut Cell,
        levels: &mut CellLevels,
        pairs: usize,
    ) {
        if remaining.is_empty() {
            levels[pairs - blocks.len()].push(blocks.clone());
            return;
        }
        for mask in 1usize..(1 << remaining.len()) {
            if mask.count_ones() as usize > capacity {
                continue;
            }
            let block: Vec<_> = remaining
                .iter()
                .enumerate()
                .filter(|(j, _)| mask & (1 << j) != 0)
                .map(|(_, &i)| i)
                .collect();
            let next: Vec<_> = remaining
                .iter()
                .enumerate()
                .filter(|(j, _)| mask & (1 << j) == 0)
                .map(|(_, &i)| i)
                .collect();
            blocks.push(block);
            visit(&next, capacity, blocks, levels, pairs);
            blocks.pop();
        }
    }
    let mut levels = vec![Vec::new(); pairs];
    visit(
        &(0..pairs).collect::<Vec<_>>(),
        capacity,
        &mut Vec::new(),
        &mut levels,
        pairs,
    );
    pack(&mut levels);
    Ok(levels)
}

fn pack(levels: &mut CellLevels) {
    while levels.last().is_some_and(Vec::is_empty) {
        levels.pop();
    }
    for level in levels {
        level.sort();
    }
}

fn indices(levels: &CellLevels) -> CellIndex {
    levels
        .iter()
        .map(|cells| {
            cells
                .iter()
                .cloned()
                .enumerate()
                .map(|(i, cell)| (cell, i))
                .collect()
        })
        .collect()
}

fn sparse_column(chain: &CellChain, index: &BTreeMap<Cell, usize>) -> Result<Vec<(usize, i64)>> {
    let mut column = chain
        .iter()
        .map(|(cell, &value)| Ok((*index.get(cell).ok_or(TransportError::MissingCell)?, value)))
        .collect::<Result<Vec<_>>>()?;
    column.sort_unstable_by_key(|&(row, _)| row);
    Ok(column)
}

fn make_complex(
    levels: &CellLevels,
    index: &CellIndex,
    limits: ContractionLimits,
) -> Result<IntegralChainComplex> {
    let mut boundaries = Vec::new();
    for degree in 1..levels.len() {
        let columns = levels[degree]
            .iter()
            .map(|cell| sparse_column(&boundary(cell, limits)?, &index[degree - 1]))
            .collect::<Result<Vec<_>>>()?;
        boundaries.push(SparseIntegerMatrix::new(levels[degree - 1].len(), columns)?);
    }
    Ok(IntegralChainComplex::new(
        levels.iter().map(Vec::len).collect(),
        boundaries,
    )?)
}

fn event_task_order(cell: &Cell, pairs: usize) -> Result<FinitePoset> {
    let mut location = vec![0; 2 * pairs];
    for (block, labels) in cell.iter().enumerate() {
        for &label in labels {
            location[label] = block;
        }
    }
    let relations = (0..pairs)
        .flat_map(|i| (0..pairs).map(move |j| (i, j)))
        .filter(|&(i, j)| location[2 * i + 1] < location[2 * j]);
    Ok(FinitePoset::new(pairs, relations)?)
}

fn task_order(cell: &Cell, pairs: usize) -> Result<FinitePoset> {
    let mut location = vec![0; pairs];
    for (block, labels) in cell.iter().enumerate() {
        for &label in labels {
            location[label] = block;
        }
    }
    let relations = (0..pairs)
        .flat_map(|i| (0..pairs).map(move |j| (i, j)))
        .filter(|&(i, j)| location[i] < location[j]);
    Ok(FinitePoset::new(pairs, relations)?)
}

fn event_order(tasks: &FinitePoset) -> Result<FinitePoset> {
    let mut generators: Vec<_> = (0..tasks.size()).map(|i| (2 * i, 2 * i + 1)).collect();
    generators.extend(
        tasks
            .strict_relations()
            .into_iter()
            .map(|(i, j)| (2 * i + 1, 2 * j)),
    );
    Ok(FinitePoset::from_generating_relations(
        2 * tasks.size(),
        generators,
    )?)
}

fn carrier(
    cache: &mut CarrierCache,
    poset: FinitePoset,
    limits: ContractionLimits,
) -> Result<&mut LinearExtensionContraction> {
    let key = poset.strict_relations();
    if !cache.contains_key(&key) {
        cache.insert(key.clone(), LinearExtensionContraction::new(poset, limits)?);
    }
    cache.get_mut(&key).ok_or(TransportError::MissingCell)
}

fn map_chain(
    chain: &CellChain,
    images: &CellImages,
    limits: ContractionLimits,
) -> Result<CellChain> {
    let mut result = CellChain::new();
    for (cell, coefficient) in chain {
        add_scaled(
            &mut result,
            images.get(cell).ok_or(TransportError::MissingCell)?,
            *coefficient,
            limits,
        )?;
    }
    Ok(result)
}

fn maps_from_images(
    source: &CellLevels,
    target: &CellLevels,
    images: &CellImages,
    degree_shift: usize,
    degrees: usize,
) -> Result<Vec<SparseIntegerMatrix>> {
    let target_index = indices(target);
    let empty = BTreeMap::new();
    (0..degrees)
        .map(|degree| {
            let target_degree = degree + degree_shift;
            let index = target_index.get(target_degree).unwrap_or(&empty);
            let columns = source
                .get(degree)
                .into_iter()
                .flatten()
                .map(|cell| {
                    sparse_column(images.get(cell).ok_or(TransportError::MissingCell)?, index)
                })
                .collect::<Result<Vec<_>>>()?;
            Ok(SparseIntegerMatrix::new(index.len(), columns)?)
        })
        .collect()
}

fn wire_matrix(matrix: &SparseIntegerMatrix) -> MatrixProposal {
    MatrixProposal {
        rows: matrix.rows(),
        columns: (0..matrix.cols())
            .map(|j| matrix.column(j).expect("existing matrix column").to_vec())
            .collect(),
    }
}

fn decode_matrices(
    wire: &[MatrixProposal],
    row_counts: &[usize],
    column_counts: &[usize],
) -> Result<Vec<SparseIntegerMatrix>> {
    if wire.len() != row_counts.len() || wire.len() != column_counts.len() {
        return Err(TransportError::Certificate(
            "wrong number of degree matrices",
        ));
    }
    wire.iter()
        .enumerate()
        .map(|(degree, matrix)| {
            if matrix.rows != row_counts[degree] || matrix.columns.len() != column_counts[degree] {
                return Err(TransportError::Certificate("wrong matrix shape"));
            }
            for column in &matrix.columns {
                if column
                    .iter()
                    .any(|&(row, coefficient)| row >= matrix.rows || coefficient == 0)
                    || column.windows(2).any(|w| w[0].0 >= w[1].0)
                {
                    return Err(TransportError::Certificate(
                        "noncanonical sparse matrix column",
                    ));
                }
            }
            Ok(SparseIntegerMatrix::new(
                matrix.rows,
                matrix.columns.clone(),
            )?)
        })
        .collect()
}

pub fn propose_transport(
    pairs: usize,
    capacity: usize,
) -> Result<(TransportProposal, ConstructionTimings)> {
    parameters(pairs, capacity)?;
    let limits = ContractionLimits::default();
    let started = Instant::now();
    let event_cells = enumerate_event_cells(pairs, capacity)?;
    let task_cells = enumerate_task_cells(pairs, capacity)?;
    let event_index = indices(&event_cells);
    let task_index = indices(&task_cells);
    let source = make_complex(&event_cells, &event_index, limits)?;
    let target = make_complex(&task_cells, &task_index, limits)?;
    let enumerate_microseconds = started.elapsed().as_micros();
    let started = Instant::now();
    let mut task_carriers = CarrierCache::new();
    let mut event_carriers = CarrierCache::new();
    let mut projection = CellImages::new();
    let mut inclusion = CellImages::new();
    let mut source_homotopy = CellImages::new();
    for (degree, level) in event_cells.iter().enumerate() {
        for cell in level {
            let poset = event_task_order(cell, pairs)?;
            let image = if degree == 0 {
                BTreeMap::from([(
                    poset
                        .topological_order()
                        .into_iter()
                        .map(|i| vec![i])
                        .collect(),
                    1,
                )])
            } else {
                let boundary_image = map_chain(&boundary(cell, limits)?, &projection, limits)?;
                if boundary_image.is_empty() {
                    CellChain::new()
                } else {
                    carrier(&mut task_carriers, poset, limits)?
                        .fill_cycle(&boundary_image, degree - 1)?
                }
            };
            projection.insert(cell.clone(), image);
        }
    }
    for (degree, level) in task_cells.iter().enumerate() {
        for cell in level {
            let image = if degree == 0 {
                let events = cell
                    .iter()
                    .flatten()
                    .flat_map(|i| [vec![2 * i], vec![2 * i + 1]])
                    .collect();
                BTreeMap::from([(events, 1)])
            } else {
                let boundary_image = map_chain(&boundary(cell, limits)?, &inclusion, limits)?;
                let poset = event_order(&task_order(cell, pairs)?)?;
                if boundary_image.is_empty() {
                    CellChain::new()
                } else {
                    carrier(&mut event_carriers, poset, limits)?
                        .fill_cycle(&boundary_image, degree - 1)?
                }
            };
            inclusion.insert(cell.clone(), image);
        }
    }
    for (degree, level) in event_cells.iter().enumerate() {
        for cell in level {
            let projected = projection.get(cell).ok_or(TransportError::MissingCell)?;
            let mut residual = map_chain(projected, &inclusion, limits)?;
            add_scaled(
                &mut residual,
                &BTreeMap::from([(cell.clone(), 1)]),
                -1,
                limits,
            )?;
            if degree > 0 {
                let lower = map_chain(&boundary(cell, limits)?, &source_homotopy, limits)?;
                add_scaled(&mut residual, &lower, -1, limits)?;
            }
            let image = if residual.is_empty() {
                CellChain::new()
            } else {
                let poset = event_order(&event_task_order(cell, pairs)?)?;
                carrier(&mut event_carriers, poset, limits)?.fill_cycle(&residual, degree)?
            };
            source_homotopy.insert(cell.clone(), image);
        }
    }
    let degrees = source.top_dimension().max(target.top_dimension()) + 1;
    let certificate = ChainEquivalenceCertificate {
        projection: maps_from_images(&event_cells, &task_cells, &projection, 0, degrees)?,
        inclusion: maps_from_images(&task_cells, &event_cells, &inclusion, 0, degrees)?,
        source_homotopy: maps_from_images(
            &event_cells,
            &event_cells,
            &source_homotopy,
            1,
            degrees,
        )?,
        target_homotopy: (0..degrees)
            .map(|degree| {
                SparseIntegerMatrix::new(
                    target.cell_count(degree + 1),
                    vec![Vec::new(); target.cell_count(degree)],
                )
            })
            .collect::<std::result::Result<Vec<_>, _>>()?,
    };
    let maps_microseconds = started.elapsed().as_micros();
    let started = Instant::now();
    let checked = verify_chain_equivalence(&source, &target, &certificate)?;
    let check_microseconds = started.elapsed().as_micros();
    let started = Instant::now();
    let witness = if pairs >= 3 && capacity == pairs - 1 {
        let (cycle, cocycle) = sphere_witness(pairs, &task_cells)?;
        let transported = checked.transport_target_obstruction(pairs - 2, &cycle, &cocycle)?;
        Some(WitnessProposal {
            degree: pairs - 2,
            task_cycle: cycle,
            task_cocycle: cocycle,
            event_cycle: transported.source_cycle().to_vec(),
            event_cocycle: transported.source_cocycle().to_vec(),
            pairing: i64::try_from(transported.pairing())
                .map_err(|_| TransportError::Overflow("narrowing witness pairing"))?,
        })
    } else {
        None
    };
    let witness_microseconds = started.elapsed().as_micros();
    let proposal = TransportProposal {
        schema: SCHEMA.to_string(),
        pairs,
        capacity,
        event_cells,
        task_cells,
        projection: certificate.projection.iter().map(wire_matrix).collect(),
        inclusion: certificate.inclusion.iter().map(wire_matrix).collect(),
        source_homotopy: certificate
            .source_homotopy
            .iter()
            .map(wire_matrix)
            .collect(),
        target_homotopy: certificate
            .target_homotopy
            .iter()
            .map(wire_matrix)
            .collect(),
        witness,
    };
    Ok((
        proposal,
        ConstructionTimings {
            enumerate_microseconds,
            maps_microseconds,
            check_microseconds,
            witness_microseconds,
            task_carriers: task_carriers.len(),
            event_carriers: event_carriers.len(),
        },
    ))
}

fn sphere_witness(pairs: usize, levels: &CellLevels) -> Result<(Vec<i64>, Vec<i64>)> {
    let degree = pairs - 2;
    let index = indices(levels);
    let sphere = boundary(&vec![(0..pairs).collect()], ContractionLimits::default())?;
    let column = sparse_column(
        &sphere,
        index.get(degree).ok_or(TransportError::MissingCell)?,
    )?;
    let mut cycle = vec![0; levels[degree].len()];
    for (row, value) in column {
        cycle[row] = value;
    }
    let (facet, &sign) = cycle
        .iter()
        .enumerate()
        .find(|(_, value)| **value != 0)
        .ok_or(TransportError::Certificate("empty sphere boundary"))?;
    let mut cocycle = vec![0; cycle.len()];
    cocycle[facet] = sign;
    Ok((cycle, cocycle))
}

pub fn verify_transport(
    pairs: usize,
    capacity: usize,
    proposal: &TransportProposal,
) -> Result<VerificationReport> {
    parameters(pairs, capacity)?;
    if proposal.schema != SCHEMA || proposal.pairs != pairs || proposal.capacity != capacity {
        return Err(TransportError::Certificate(
            "schema or supplied problem mismatch",
        ));
    }
    let event_cells = enumerate_event_cells(pairs, capacity)?;
    let task_cells = enumerate_task_cells(pairs, capacity)?;
    if proposal.event_cells != event_cells || proposal.task_cells != task_cells {
        return Err(TransportError::Certificate(
            "supplied cells differ from the complete legal complexes",
        ));
    }
    let source = make_complex(
        &event_cells,
        &indices(&event_cells),
        ContractionLimits::default(),
    )?;
    let target = make_complex(
        &task_cells,
        &indices(&task_cells),
        ContractionLimits::default(),
    )?;
    let degrees = source.top_dimension().max(target.top_dimension()) + 1;
    let source_dims: Vec<_> = (0..degrees).map(|k| source.cell_count(k)).collect();
    let target_dims: Vec<_> = (0..degrees).map(|k| target.cell_count(k)).collect();
    let source_shift: Vec<_> = (0..degrees).map(|k| source.cell_count(k + 1)).collect();
    let target_shift: Vec<_> = (0..degrees).map(|k| target.cell_count(k + 1)).collect();
    let certificate = ChainEquivalenceCertificate {
        projection: decode_matrices(&proposal.projection, &target_dims, &source_dims)?,
        inclusion: decode_matrices(&proposal.inclusion, &source_dims, &target_dims)?,
        source_homotopy: decode_matrices(&proposal.source_homotopy, &source_shift, &source_dims)?,
        target_homotopy: decode_matrices(&proposal.target_homotopy, &target_shift, &target_dims)?,
    };
    let checked = verify_chain_equivalence(&source, &target, &certificate)?;
    if certificate
        .target_homotopy
        .iter()
        .any(|matrix| !matrix.is_zero())
    {
        return Err(TransportError::Certificate(
            "target homotopy must be zero for this strict retraction",
        ));
    }
    let witness = match (&proposal.witness, pairs >= 3 && capacity == pairs - 1) {
        (Some(witness), true) => {
            if witness.degree != pairs - 2 {
                return Err(TransportError::Certificate("wrong sphere witness degree"));
            }
            let (cycle, cocycle) = sphere_witness(pairs, &task_cells)?;
            if witness.task_cycle != cycle || witness.task_cocycle != cocycle {
                return Err(TransportError::Certificate(
                    "task witness differs from the oriented permutohedron boundary and facet",
                ));
            }
            let result = checked.transport_target_obstruction(
                witness.degree,
                &witness.task_cycle,
                &witness.task_cocycle,
            )?;
            if witness.event_cycle != result.source_cycle()
                || witness.event_cocycle != result.source_cocycle()
                || i128::from(witness.pairing) != result.pairing()
            {
                return Err(TransportError::Certificate(
                    "supplied transported witness mismatch",
                ));
            }
            Some(WitnessSummary {
                degree: witness.degree,
                task_cycle_support: witness.task_cycle.iter().filter(|&&v| v != 0).count(),
                task_cocycle_support: witness.task_cocycle.iter().filter(|&&v| v != 0).count(),
                event_cycle_support: witness.event_cycle.iter().filter(|&&v| v != 0).count(),
                event_cocycle_support: witness.event_cocycle.iter().filter(|&&v| v != 0).count(),
                pairing: witness.pairing,
            })
        }
        (None, false) => None,
        _ => {
            return Err(TransportError::Certificate(
                "sphere witness missing or supplied outside its declared family",
            ))
        }
    };
    let map_nonzero_entries = [
        ("projection", &proposal.projection),
        ("inclusion", &proposal.inclusion),
        ("source_homotopy", &proposal.source_homotopy),
        ("target_homotopy", &proposal.target_homotopy),
    ]
    .into_iter()
    .map(|(name, matrices)| {
        (
            name,
            matrices.iter().flat_map(|m| &m.columns).map(Vec::len).sum(),
        )
    })
    .collect();
    Ok(VerificationReport {
        status: "PASS",
        authority_effect: "None",
        pairs,
        capacity,
        event_f_vector: event_cells.iter().map(Vec::len).collect(),
        task_f_vector: task_cells.iter().map(Vec::len).collect(),
        checked_degrees: degrees,
        checked_matrix_identities: 4 * degrees,
        projection_inclusion_is_identity: true,
        map_nonzero_entries,
        witness,
    })
}
