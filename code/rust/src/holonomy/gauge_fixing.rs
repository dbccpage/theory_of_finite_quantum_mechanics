
use crate::connection::DiscreteConnection;
use crate::error::HolonomyError;
use crate::graph::{CellComplex, OrientedStep};
use crate::matrix::{ExactMatrix, ExactScalar};
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::smith_normal_form::smith_normal_form_checked;
use num_bigint::{BigInt, BigUint};
use num_traits::{ToPrimitive, Zero};
use omega_kernel::resource_limits::check_and_reserve;
use std::collections::{BTreeMap, VecDeque};

fn edge_endpoints(complex: &CellComplex) -> Result<Vec<(usize, usize)>, HolonomyError> {
    let mut endpoints = Vec::new();
    check_and_reserve(
        &mut endpoints,
        complex.edges.len(),
        complex.limits.max_edges,
    )?;
    for edge in &complex.edges {
        let source =
            *complex
                .vertex_map
                .get(&edge.source)
                .ok_or_else(|| HolonomyError::VertexNotFound {
                    id: edge.source.clone(),
                })?;
        let target =
            *complex
                .vertex_map
                .get(&edge.target)
                .ok_or_else(|| HolonomyError::VertexNotFound {
                    id: edge.target.clone(),
                })?;
        endpoints.push((source, target));
    }
    Ok(endpoints)
}

fn check_edge(index: usize, edge_count: usize) -> Result<(), HolonomyError> {
    if index < edge_count {
        Ok(())
    } else {
        Err(HolonomyError::EdgeIndexOutOfRange { index, edge_count })
    }
}

fn check_vertex(index: usize, vertex_count: usize) -> Result<(), HolonomyError> {
    if index < vertex_count {
        Ok(())
    } else {
        Err(HolonomyError::VertexIndexOutOfRange {
            index,
            vertex_count,
        })
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct Link {
    edge: usize,
    direction_from_parent: i8,
    parent: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct Forest {
    tree_edge: Vec<bool>,
    parent: Vec<Option<Link>>,
    root: Vec<usize>,
    discovery: Vec<usize>,
}

fn spanning_forest(vertex_count: usize, endpoints: &[(usize, usize)]) -> Forest {
    let mut adjacency: Vec<Vec<(usize, usize, i8)>> = vec![Vec::new(); vertex_count];
    for (edge, &(source, target)) in endpoints.iter().enumerate() {
        adjacency[source].push((target, edge, 1));
        adjacency[target].push((source, edge, -1));
    }
    let mut tree_edge = vec![false; endpoints.len()];
    let mut parent: Vec<Option<Link>> = vec![None; vertex_count];
    let mut root: Vec<usize> = (0..vertex_count).collect();
    let mut visited = vec![false; vertex_count];
    let mut discovery = Vec::with_capacity(vertex_count);
    for start in 0..vertex_count {
        if visited[start] {
            continue;
        }
        visited[start] = true;
        discovery.push(start);
        let mut queue = VecDeque::from([start]);
        while let Some(u) = queue.pop_front() {
            for &(v, edge, direction) in &adjacency[u] {
                if visited[v] {
                    continue;
                }
                visited[v] = true;
                tree_edge[edge] = true;
                parent[v] = Some(Link {
                    edge,
                    direction_from_parent: direction,
                    parent: u,
                });
                root[v] = start;
                discovery.push(v);
                queue.push_back(v);
            }
        }
    }
    Forest {
        tree_edge,
        parent,
        root,
        discovery,
    }
}

pub fn cycle_rank(complex: &CellComplex) -> Result<usize, HolonomyError> {
    let endpoints = edge_endpoints(complex)?;
    let forest = spanning_forest(complex.vertices.len(), &endpoints);
    Ok(forest.tree_edge.iter().filter(|&&on_tree| !on_tree).count())
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EdgeConnection<T: ExactScalar> {
    dim: usize,
    values: Vec<ExactMatrix<T>>,
    inverses: Vec<ExactMatrix<T>>,
}

impl<T: ExactScalar> EdgeConnection<T> {
    pub fn new(
        complex: &CellComplex,
        dim: usize,
        values: Vec<ExactMatrix<T>>,
    ) -> Result<Self, HolonomyError> {
        if dim == 0 {
            return Err(HolonomyError::DimensionMismatch {
                expected: 1,
                actual: 0,
            });
        }
        if dim > complex.limits.max_dimension {
            return Err(HolonomyError::AllocationFailure {
                requested: dim,
                detail: format!(
                    "Requested dimension {dim} > max_dimension {}",
                    complex.limits.max_dimension
                ),
            });
        }
        if values.len() != complex.edges.len() {
            return Err(HolonomyError::EdgeValueCount {
                expected: complex.edges.len(),
                actual: values.len(),
            });
        }
        let mut inverses = Vec::new();
        check_and_reserve(&mut inverses, values.len(), complex.limits.max_edges)?;
        for (value, edge) in values.iter().zip(&complex.edges) {
            if value.rows != dim || value.cols != dim {
                return Err(HolonomyError::DimensionMismatch {
                    expected: dim,
                    actual: value.rows.max(value.cols),
                });
            }
            inverses.push(value.inverse().map_err(|e| match e {
                HolonomyError::SingularMatrix { detail } => HolonomyError::SingularConnection {
                    src: edge.source.clone(),
                    tgt: edge.target.clone(),
                    detail,
                },
                other => other,
            })?);
        }
        Ok(Self {
            dim,
            values,
            inverses,
        })
    }

    pub fn from_scalars(complex: &CellComplex, scalars: Vec<T>) -> Result<Self, HolonomyError> {
        let values = scalars
            .into_iter()
            .map(|s| ExactMatrix::try_new(1, 1, vec![s]))
            .collect::<Result<Vec<_>, _>>()?;
        Self::new(complex, 1, values)
    }

    pub fn trivial(complex: &CellComplex, dim: usize) -> Result<Self, HolonomyError> {
        let values = (0..complex.edges.len())
            .map(|_| ExactMatrix::try_identity(dim))
            .collect::<Result<Vec<_>, _>>()?;
        Self::new(complex, dim, values)
    }

    pub fn pure_gauge(
        complex: &CellComplex,
        potentials: &[ExactMatrix<T>],
    ) -> Result<Self, HolonomyError> {
        let dim = potentials.first().map_or(1, |h| h.rows);
        Self::trivial(complex, dim)?.gauge_transform(complex, potentials)
    }

    pub fn from_discrete_connection(
        complex: &CellComplex,
        connection: &DiscreteConnection<T>,
    ) -> Result<Self, HolonomyError> {
        refuse_antiparallel_edges(complex)?;
        let values = complex
            .edges
            .iter()
            .map(|edge| connection.get_step(&edge.source, &edge.target).cloned())
            .collect::<Result<Vec<_>, _>>()?;
        Self::new(complex, connection.dim, values)
    }

    pub fn to_discrete_connection(
        &self,
        complex: &CellComplex,
    ) -> Result<DiscreteConnection<T>, HolonomyError> {
        self.check_complex(complex)?;
        refuse_antiparallel_edges(complex)?;
        let mut connection = DiscreteConnection::new(self.dim, complex.limits);
        for (edge, value) in complex.edges.iter().zip(&self.values) {
            connection.set_connection(edge.source.clone(), edge.target.clone(), value.clone())?;
        }
        Ok(connection)
    }

    pub fn dim(&self) -> usize {
        self.dim
    }

    pub fn edge_count(&self) -> usize {
        self.values.len()
    }

    fn check_complex(&self, complex: &CellComplex) -> Result<(), HolonomyError> {
        if self.values.len() == complex.edges.len() {
            Ok(())
        } else {
            Err(HolonomyError::EdgeValueCount {
                expected: complex.edges.len(),
                actual: self.values.len(),
            })
        }
    }

    pub fn value(&self, edge: usize) -> Result<&ExactMatrix<T>, HolonomyError> {
        check_edge(edge, self.values.len())?;
        Ok(&self.values[edge])
    }

    pub fn step(&self, step: OrientedStep) -> Result<&ExactMatrix<T>, HolonomyError> {
        check_edge(step.edge_index, self.values.len())?;
        match step.direction {
            1 => Ok(&self.values[step.edge_index]),
            -1 => Ok(&self.inverses[step.edge_index]),
            direction => Err(HolonomyError::InvalidStepDirection { step: 0, direction }),
        }
    }

    pub fn walk(
        &self,
        complex: &CellComplex,
        start: usize,
        steps: &[OrientedStep],
    ) -> Result<(ExactMatrix<T>, usize), HolonomyError> {
        self.check_complex(complex)?;
        let endpoints = edge_endpoints(complex)?;
        self.walk_with_endpoints(complex, &endpoints, start, steps)
    }

    fn walk_with_endpoints(
        &self,
        complex: &CellComplex,
        endpoints: &[(usize, usize)],
        start: usize,
        steps: &[OrientedStep],
    ) -> Result<(ExactMatrix<T>, usize), HolonomyError> {
        check_vertex(start, complex.vertices.len())?;
        if steps.len() > complex.limits.max_path_length {
            return Err(HolonomyError::PathLengthExceeded {
                length: steps.len(),
                limit: complex.limits.max_path_length,
            });
        }
        let mut transport = ExactMatrix::try_identity(self.dim)?;
        let mut here = start;
        for (index, step) in steps.iter().enumerate() {
            check_edge(step.edge_index, endpoints.len())?;
            let (source, target) = endpoints[step.edge_index];
            let (from, to) = match step.direction {
                1 => (source, target),
                -1 => (target, source),
                direction => {
                    return Err(HolonomyError::InvalidStepDirection {
                        step: index,
                        direction,
                    })
                }
            };
            if from != here {
                return Err(HolonomyError::BrokenWalk {
                    step: index,
                    detail: format!(
                        "step {index} leaves vertex {from} but the walk is at vertex {here}"
                    ),
                });
            }
            transport = self.step(*step)?.matmul(&transport)?;
            here = to;
        }
        Ok((transport, here))
    }

    pub fn loop_holonomy(
        &self,
        complex: &CellComplex,
        start: usize,
        steps: &[OrientedStep],
    ) -> Result<ExactMatrix<T>, HolonomyError> {
        let (transport, end) = self.walk(complex, start, steps)?;
        if end != start {
            return Err(HolonomyError::OpenLoop {
                start: complex.vertices[start].id.clone(),
                end: complex.vertices[end].id.clone(),
            });
        }
        Ok(transport)
    }

    pub fn gauge_transform(
        &self,
        complex: &CellComplex,
        gauge: &[ExactMatrix<T>],
    ) -> Result<Self, HolonomyError> {
        self.check_complex(complex)?;
        if gauge.len() != complex.vertices.len() {
            return Err(HolonomyError::VertexValueCount {
                expected: complex.vertices.len(),
                actual: gauge.len(),
            });
        }
        for g in gauge {
            if g.rows != self.dim || g.cols != self.dim {
                return Err(HolonomyError::DimensionMismatch {
                    expected: self.dim,
                    actual: g.rows.max(g.cols),
                });
            }
        }
        let gauge_inverses = gauge
            .iter()
            .map(ExactMatrix::inverse)
            .collect::<Result<Vec<_>, _>>()?;
        let endpoints = edge_endpoints(complex)?;
        let mut values = Vec::new();
        let mut inverses = Vec::new();
        check_and_reserve(&mut values, endpoints.len(), complex.limits.max_edges)?;
        check_and_reserve(&mut inverses, endpoints.len(), complex.limits.max_edges)?;
        for (edge, &(s, t)) in endpoints.iter().enumerate() {
            values.push(
                gauge[t]
                    .matmul(&self.values[edge])?
                    .matmul(&gauge_inverses[s])?,
            );
            inverses.push(
                gauge[s]
                    .matmul(&self.inverses[edge])?
                    .matmul(&gauge_inverses[t])?,
            );
        }
        Ok(Self {
            dim: self.dim,
            values,
            inverses,
        })
    }

    pub fn covariant_difference_matrix(
        &self,
        complex: &CellComplex,
    ) -> Result<ExactMatrix<T>, HolonomyError> {
        self.check_complex(complex)?;
        let endpoints = edge_endpoints(complex)?;
        let rows = endpoints.len().checked_mul(self.dim).ok_or_else(|| {
            HolonomyError::AllocationFailure {
                requested: usize::MAX,
                detail: "incidence dimension overflow".into(),
            }
        })?;
        let cols = complex
            .vertices
            .len()
            .checked_mul(self.dim)
            .ok_or_else(|| HolonomyError::AllocationFailure {
                requested: usize::MAX,
                detail: "incidence dimension overflow".into(),
            })?;
        let entries = rows
            .checked_mul(cols)
            .ok_or_else(|| HolonomyError::AllocationFailure {
                requested: usize::MAX,
                detail: "incidence buffer overflow".into(),
            })?;
        if entries > complex.limits.max_operations {
            return Err(HolonomyError::AllocationFailure {
                requested: entries,
                detail: "incidence operation budget".into(),
            });
        }
        let mut out = ExactMatrix::try_zero(rows, cols)?;
        for (edge, &(s, t)) in endpoints.iter().enumerate() {
            for i in 0..self.dim {
                for j in 0..self.dim {
                    let index = (edge * self.dim + i) * cols + s * self.dim + j;
                    out.data[index] -= self.values[edge].get(i, j).clone();
                }
                let index = (edge * self.dim + i) * cols + t * self.dim + i;
                out.data[index] += T::one();
            }
        }
        Ok(out)
    }

    pub fn connection_laplacian(
        &self,
        complex: &CellComplex,
        weights: &[T],
    ) -> Result<ExactMatrix<T>, HolonomyError> {
        if weights.len() != complex.edges.len() {
            return Err(HolonomyError::EdgeValueCount {
                expected: complex.edges.len(),
                actual: weights.len(),
            });
        }
        let d = self.covariant_difference_matrix(complex)?;
        let n = d.cols;
        let work = n
            .checked_mul(n)
            .and_then(|k| k.checked_mul(d.rows))
            .ok_or_else(|| HolonomyError::AllocationFailure {
                requested: usize::MAX,
                detail: "Laplacian work overflow".into(),
            })?;
        if work > complex.limits.max_operations {
            return Err(HolonomyError::AllocationFailure {
                requested: work,
                detail: "Laplacian operation budget".into(),
            });
        }
        let mut out = ExactMatrix::try_zero(n, n)?;
        for i in 0..n {
            for j in 0..n {
                let mut value = T::zero();
                for row in 0..d.rows {
                    value += d.get(row, i).conjugate()
                        * weights[row / self.dim].clone()
                        * d.get(row, j).clone();
                }
                out.data[i * n + j] = value;
            }
        }
        Ok(out)
    }

    pub fn face_holonomy(
        &self,
        complex: &CellComplex,
        face: usize,
    ) -> Result<ExactMatrix<T>, HolonomyError> {
        self.check_complex(complex)?;
        let endpoints = edge_endpoints(complex)?;
        self.face_holonomy_with_endpoints(complex, &endpoints, face)
    }

    fn face_holonomy_with_endpoints(
        &self,
        complex: &CellComplex,
        endpoints: &[(usize, usize)],
        face: usize,
    ) -> Result<ExactMatrix<T>, HolonomyError> {
        let declared = complex
            .faces
            .get(face)
            .ok_or_else(|| HolonomyError::FaceNotFound {
                id: face.to_string(),
            })?;
        let start_id = declared.boundary_vertices.first().ok_or_else(|| {
            HolonomyError::BoundaryCycleMismatch {
                face: declared.id.clone(),
                detail: "the face lists no boundary vertices".into(),
            }
        })?;
        let start =
            *complex
                .vertex_map
                .get(start_id)
                .ok_or_else(|| HolonomyError::VertexNotFound {
                    id: start_id.clone(),
                })?;
        let (transport, end) =
            self.walk_with_endpoints(complex, endpoints, start, &declared.boundary_edges)?;
        if end != start {
            return Err(HolonomyError::BoundaryCycleMismatch {
                face: declared.id.clone(),
                detail: "the boundary steps do not return to the first boundary vertex".into(),
            });
        }
        Ok(transport)
    }
}

fn refuse_antiparallel_edges(complex: &CellComplex) -> Result<(), HolonomyError> {
    for (first, edge) in complex.edges.iter().enumerate() {
        if edge.source == edge.target {
            continue;
        }
        if let Some(&second) = complex
            .edge_map
            .get(&(edge.target.clone(), edge.source.clone()))
        {
            return Err(HolonomyError::AntiparallelEdges {
                first: first.min(second),
                second: first.max(second),
            });
        }
    }
    Ok(())
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FundamentalCycle {
    pub edge: usize,
    pub base: String,
    pub vertices: Vec<String>,
    pub steps: Vec<OrientedStep>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct HolonomyWitness<T: ExactScalar> {
    pub edge: usize,
    pub cycle: FundamentalCycle,
    pub holonomy: ExactMatrix<T>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PureGaugeVerdict<T: ExactScalar> {
    PureGauge { potentials: Vec<ExactMatrix<T>> },
    NotPureGauge { witness: Box<HolonomyWitness<T>> },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TreeGauge<T: ExactScalar> {
    dim: usize,
    vertex_ids: Vec<String>,
    endpoints: Vec<(usize, usize)>,
    forest: Forest,
    gauge: Vec<ExactMatrix<T>>,
    transport_from_root: Vec<ExactMatrix<T>>,
    residual: EdgeConnection<T>,
}

impl<T: ExactScalar> TreeGauge<T> {
    pub fn dim(&self) -> usize {
        self.dim
    }

    pub fn gauge(&self) -> &[ExactMatrix<T>] {
        &self.gauge
    }

    pub fn gauge_map(&self) -> BTreeMap<String, ExactMatrix<T>> {
        self.vertex_ids
            .iter()
            .cloned()
            .zip(self.gauge.iter().cloned())
            .collect()
    }

    pub fn transport_from_root(&self, vertex: usize) -> Result<&ExactMatrix<T>, HolonomyError> {
        check_vertex(vertex, self.vertex_ids.len())?;
        Ok(&self.transport_from_root[vertex])
    }

    pub fn residual(&self) -> &EdgeConnection<T> {
        &self.residual
    }

    pub fn residual_value(&self, edge: usize) -> Result<&ExactMatrix<T>, HolonomyError> {
        self.residual.value(edge)
    }

    pub fn is_tree_edge(&self, edge: usize) -> Result<bool, HolonomyError> {
        check_edge(edge, self.forest.tree_edge.len())?;
        Ok(self.forest.tree_edge[edge])
    }

    pub fn tree_edges(&self) -> Vec<usize> {
        (0..self.forest.tree_edge.len())
            .filter(|&e| self.forest.tree_edge[e])
            .collect()
    }

    pub fn root_of(&self, vertex: usize) -> Result<usize, HolonomyError> {
        check_vertex(vertex, self.vertex_ids.len())?;
        Ok(self.forest.root[vertex])
    }

    pub fn cycle_holonomies(&self) -> Vec<(usize, ExactMatrix<T>)> {
        (0..self.forest.tree_edge.len())
            .filter(|&e| !self.forest.tree_edge[e])
            .map(|e| (e, self.residual.values[e].clone()))
            .collect()
    }

    pub fn is_gauge_trivial(&self) -> bool {
        match ExactMatrix::<T>::try_identity(self.dim) {
            Ok(identity) => self.residual.values.iter().all(|value| *value == identity),
            Err(_) => false,
        }
    }

    fn steps_down_to(&self, vertex: usize) -> Vec<OrientedStep> {
        let mut steps = Vec::new();
        let mut here = vertex;
        while let Some(link) = self.forest.parent[here] {
            steps.push(OrientedStep {
                edge_index: link.edge,
                direction: link.direction_from_parent,
            });
            here = link.parent;
        }
        steps.reverse();
        steps
    }

    pub fn fundamental_cycle(&self, edge: usize) -> Result<FundamentalCycle, HolonomyError> {
        check_edge(edge, self.endpoints.len())?;
        let (source, target) = self.endpoints[edge];
        let root = self.forest.root[source];
        let mut steps = self.steps_down_to(source);
        steps.push(OrientedStep {
            edge_index: edge,
            direction: 1,
        });
        let up: Vec<OrientedStep> = self
            .steps_down_to(target)
            .into_iter()
            .rev()
            .map(|step| OrientedStep {
                edge_index: step.edge_index,
                direction: -step.direction,
            })
            .collect();
        steps.extend(up);

        let mut vertices = vec![root];
        for step in &steps {
            let (s, t) = self.endpoints[step.edge_index];
            vertices.push(if step.direction == 1 { t } else { s });
        }
        Ok(FundamentalCycle {
            edge,
            base: self.vertex_ids[root].clone(),
            vertices: vertices
                .into_iter()
                .map(|v| self.vertex_ids[v].clone())
                .collect(),
            steps,
        })
    }

    pub fn pure_gauge_verdict(&self) -> Result<PureGaugeVerdict<T>, HolonomyError> {
        let identity = ExactMatrix::<T>::try_identity(self.dim)?;
        for (edge, value) in self.cycle_holonomies() {
            if value != identity {
                return Ok(PureGaugeVerdict::NotPureGauge {
                    witness: Box::new(HolonomyWitness {
                        edge,
                        cycle: self.fundamental_cycle(edge)?,
                        holonomy: value,
                    }),
                });
            }
        }
        Ok(PureGaugeVerdict::PureGauge {
            potentials: self.transport_from_root.clone(),
        })
    }
}

pub fn tree_gauge<T: ExactScalar>(
    complex: &CellComplex,
    connection: &DiscreteConnection<T>,
) -> Result<TreeGauge<T>, HolonomyError> {
    tree_gauge_indexed(
        complex,
        &EdgeConnection::from_discrete_connection(complex, connection)?,
    )
}

pub fn tree_gauge_indexed<T: ExactScalar>(
    complex: &CellComplex,
    connection: &EdgeConnection<T>,
) -> Result<TreeGauge<T>, HolonomyError> {
    connection.check_complex(complex)?;
    let dim = connection.dim;
    let vertex_count = complex.vertices.len();
    let endpoints = edge_endpoints(complex)?;
    let forest = spanning_forest(vertex_count, &endpoints);

    let identity = ExactMatrix::<T>::try_identity(dim)?;
    let mut gauge = Vec::new();
    let mut transport_from_root = Vec::new();
    check_and_reserve(&mut gauge, vertex_count, complex.limits.max_vertices)?;
    check_and_reserve(
        &mut transport_from_root,
        vertex_count,
        complex.limits.max_vertices,
    )?;
    for _ in 0..vertex_count {
        gauge.push(identity.clone());
        transport_from_root.push(identity.clone());
    }
    for &vertex in &forest.discovery {
        if let Some(link) = forest.parent[vertex] {
            let forward = OrientedStep {
                edge_index: link.edge,
                direction: link.direction_from_parent,
            };
            let backward = OrientedStep {
                edge_index: link.edge,
                direction: -link.direction_from_parent,
            };
            transport_from_root[vertex] = connection
                .step(forward)?
                .matmul(&transport_from_root[link.parent])?;
            gauge[vertex] = gauge[link.parent].matmul(connection.step(backward)?)?;
        }
    }

    let mut values = Vec::new();
    let mut inverses = Vec::new();
    check_and_reserve(&mut values, endpoints.len(), complex.limits.max_edges)?;
    check_and_reserve(&mut inverses, endpoints.len(), complex.limits.max_edges)?;
    for (edge, &(s, t)) in endpoints.iter().enumerate() {
        values.push(
            gauge[t]
                .matmul(&connection.values[edge])?
                .matmul(&transport_from_root[s])?,
        );
        inverses.push(
            gauge[s]
                .matmul(&connection.inverses[edge])?
                .matmul(&transport_from_root[t])?,
        );
    }
    Ok(TreeGauge {
        dim,
        vertex_ids: complex.vertices.iter().map(|v| v.id.clone()).collect(),
        endpoints,
        forest,
        gauge,
        transport_from_root,
        residual: EdgeConnection {
            dim,
            values,
            inverses,
        },
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum GaugeEquivalence<T: ExactScalar> {
    Equivalent { gauge: Vec<ExactMatrix<T>> },
    Inequivalent { edge: usize },
    Undetermined { edge: usize },
}

pub fn gauge_equivalence<T: ExactScalar>(
    complex: &CellComplex,
    a: &EdgeConnection<T>,
    b: &EdgeConnection<T>,
) -> Result<GaugeEquivalence<T>, HolonomyError> {
    if a.dim != b.dim {
        return Err(HolonomyError::DimensionMismatch {
            expected: a.dim,
            actual: b.dim,
        });
    }
    let fixed_a = tree_gauge_indexed(complex, a)?;
    let fixed_b = tree_gauge_indexed(complex, b)?;
    let mut first_difference = None;
    for (edge, residual_a) in fixed_a.cycle_holonomies() {
        let residual_b = fixed_b.residual_value(edge)?;
        if residual_a == *residual_b {
            continue;
        }
        if residual_a.trace()? != residual_b.trace()?
            || residual_a.determinant()? != residual_b.determinant()?
        {
            return Ok(GaugeEquivalence::Inequivalent { edge });
        }
        first_difference.get_or_insert(edge);
    }
    if let Some(edge) = first_difference {
        return Ok(GaugeEquivalence::Undetermined { edge });
    }
    let gauge = fixed_b
        .transport_from_root
        .iter()
        .zip(&fixed_a.gauge)
        .map(|(t_b, g_a)| t_b.matmul(g_a))
        .collect::<Result<Vec<_>, _>>()?;
    Ok(GaugeEquivalence::Equivalent { gauge })
}

pub fn face_holonomies<T: ExactScalar>(
    complex: &CellComplex,
    connection: &EdgeConnection<T>,
) -> Result<Vec<ExactMatrix<T>>, HolonomyError> {
    connection.check_complex(complex)?;
    let endpoints = edge_endpoints(complex)?;
    (0..complex.faces.len())
        .map(|face| connection.face_holonomy_with_endpoints(complex, &endpoints, face))
        .collect()
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum HolonomyVerdict<T: ExactScalar> {
    Curved {
        face_holonomies: Vec<ExactMatrix<T>>,
        first_curved_face: usize,
    },
    FlatNontrivial {
        cycle_holonomies: Vec<(usize, ExactMatrix<T>)>,
    },
    GaugeTrivial,
}

pub fn holonomy_verdict<T: ExactScalar>(
    complex: &CellComplex,
    connection: &EdgeConnection<T>,
) -> Result<HolonomyVerdict<T>, HolonomyError> {
    let holonomies = face_holonomies(complex, connection)?;
    let identity = ExactMatrix::<T>::try_identity(connection.dim)?;
    if let Some(first_curved_face) = holonomies.iter().position(|h| *h != identity) {
        return Ok(HolonomyVerdict::Curved {
            face_holonomies: holonomies,
            first_curved_face,
        });
    }
    let fixed = tree_gauge_indexed(complex, connection)?;
    if fixed.is_gauge_trivial() {
        Ok(HolonomyVerdict::GaugeTrivial)
    } else {
        Ok(HolonomyVerdict::FlatNontrivial {
            cycle_holonomies: fixed.cycle_holonomies(),
        })
    }
}

fn gcd(mut a: u64, mut b: u64) -> u64 {
    while b != 0 {
        (a, b) = (b, a % b);
    }
    a
}

pub fn flat_cyclic_gauge_classes(
    complex: &CellComplex,
    order: u64,
) -> Result<BigUint, HolonomyError> {
    if order == 0 {
        return Err(HolonomyError::InvalidGroupOrder { order });
    }
    let endpoints = edge_endpoints(complex)?;
    let forest = spanning_forest(complex.vertices.len(), &endpoints);
    let off_tree: Vec<usize> = (0..endpoints.len())
        .filter(|&e| !forest.tree_edge[e])
        .collect();
    let z = off_tree.len();
    let column_of: BTreeMap<usize, usize> = off_tree
        .iter()
        .enumerate()
        .map(|(column, &edge)| (edge, column))
        .collect();

    let faces = complex.faces.len();
    let mut data = vec![BigInt::zero(); faces * z];
    for (face_index, face) in complex.faces.iter().enumerate() {
        let start_id =
            face.boundary_vertices
                .first()
                .ok_or_else(|| HolonomyError::BoundaryCycleMismatch {
                    face: face.id.clone(),
                    detail: "the face lists no boundary vertices".into(),
                })?;
        let start =
            *complex
                .vertex_map
                .get(start_id)
                .ok_or_else(|| HolonomyError::VertexNotFound {
                    id: start_id.clone(),
                })?;
        let mut here = start;
        for (index, step) in face.boundary_edges.iter().enumerate() {
            check_edge(step.edge_index, endpoints.len())?;
            let (source, target) = endpoints[step.edge_index];
            let (from, to) = match step.direction {
                1 => (source, target),
                -1 => (target, source),
                direction => {
                    return Err(HolonomyError::InvalidStepDirection {
                        step: index,
                        direction,
                    })
                }
            };
            if from != here {
                return Err(HolonomyError::BrokenWalk {
                    step: index,
                    detail: format!(
                        "step {index} of face '{}' leaves vertex {from} but the boundary is at \
                         vertex {here}",
                        face.id
                    ),
                });
            }
            here = to;
            if let Some(&column) = column_of.get(&step.edge_index) {
                data[face_index * z + column] += BigInt::from(step.direction);
            }
        }
        if here != start {
            return Err(HolonomyError::BoundaryCycleMismatch {
                face: face.id.clone(),
                detail: "the boundary steps do not return to the first boundary vertex".into(),
            });
        }
    }

    let power = |exponent: usize| -> Result<BigUint, HolonomyError> {
        let exponent = u32::try_from(exponent).map_err(|_| HolonomyError::AllocationFailure {
            requested: exponent,
            detail: "the exponent of the class count does not fit in u32".into(),
        })?;
        Ok(num_traits::pow::Pow::pow(BigUint::from(order), exponent))
    };
    if faces == 0 || z == 0 || data.iter().all(Zero::is_zero) {
        return power(z);
    }
    let matrix = BasicMatrix::from_row_major(faces, z, data).map_err(|e| {
        HolonomyError::IntegerEliminationFailed {
            detail: e.to_string(),
        }
    })?;
    let normal_form = smith_normal_form_checked(&matrix).map_err(|e| {
        HolonomyError::IntegerEliminationFailed {
            detail: e.to_string(),
        }
    })?;
    let invariants = normal_form.diagonal().invariants();
    let modulus = BigInt::from(order);
    let mut count = power(z - invariants.len())?;
    for invariant in invariants {
        let residue = (invariant % &modulus).to_u64().ok_or_else(|| {
            HolonomyError::IntegerEliminationFailed {
                detail: "an invariant factor reduced modulo the group order does not fit in u64"
                    .into(),
            }
        })?;
        count *= BigUint::from(gcd(residue, order));
    }
    Ok(count)
}
