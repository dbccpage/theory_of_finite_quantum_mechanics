use crate::finite_category::{DeclaredFiniteCategory, ValidatedFiniteCategory};
use std::collections::{BTreeMap, BTreeSet};

pub const MAX_PATHS: usize = 64;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct PathEdge {
    pub source: usize,
    pub target: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PathError {
    EmptyGraph,
    GraphBudget,
    InvalidVertex,
    Cycle,
    PathBudget,
    UnknownPath,
    MissingComposite,
    CategoryValidation,
}
impl std::fmt::Display for PathError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "finite path category refused: {self:?}")
    }
}
impl std::error::Error for PathError {}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct FinitePath {
    source: usize,
    target: usize,
    edges: Vec<usize>,
}
impl FinitePath {
    pub fn source(&self) -> usize {
        self.source
    }
    pub fn target(&self) -> usize {
        self.target
    }
    pub fn edges(&self) -> &[usize] {
        &self.edges
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FinitePathCategory {
    vertices: usize,
    edges: Vec<PathEdge>,
    paths: Vec<FinitePath>,
    composition: Vec<Vec<Option<usize>>>,
    category: ValidatedFiniteCategory,
}
impl FinitePathCategory {
    pub fn new(vertices: usize, edges: Vec<PathEdge>, max_paths: usize) -> Result<Self, PathError> {
        if vertices == 0 {
            return Err(PathError::EmptyGraph);
        }
        if vertices > MAX_PATHS || edges.len() > MAX_PATHS {
            return Err(PathError::GraphBudget);
        }
        if edges
            .iter()
            .any(|e| e.source >= vertices || e.target >= vertices)
        {
            return Err(PathError::InvalidVertex);
        }
        let mut outgoing = vec![Vec::new(); vertices];
        let mut indegree = vec![0usize; vertices];
        for (i, e) in edges.iter().enumerate() {
            outgoing[e.source].push(i);
            indegree[e.target] += 1;
        }
        let mut ready: BTreeSet<_> = (0..vertices).filter(|&v| indegree[v] == 0).collect();
        let mut visited = 0;
        while let Some(v) = ready.pop_first() {
            visited += 1;
            for &i in &outgoing[v] {
                let target = edges[i].target;
                indegree[target] -= 1;
                if indegree[target] == 0 {
                    ready.insert(target);
                }
            }
        }
        if visited != vertices {
            return Err(PathError::Cycle);
        }
        let budget = max_paths.min(MAX_PATHS);
        if vertices > budget {
            return Err(PathError::PathBudget);
        }
        let mut paths: Vec<_> = (0..vertices)
            .map(|v| FinitePath {
                source: v,
                target: v,
                edges: vec![],
            })
            .collect();
        let mut cursor = 0;
        while cursor < paths.len() {
            for &edge in &outgoing[paths[cursor].target] {
                if paths.len() == budget {
                    return Err(PathError::PathBudget);
                }
                let mut word = paths[cursor].edges.clone();
                word.push(edge);
                paths.push(FinitePath {
                    source: paths[cursor].source,
                    target: edges[edge].target,
                    edges: word,
                });
            }
            cursor += 1;
        }
        let indices: BTreeMap<_, _> = paths
            .iter()
            .enumerate()
            .map(|(i, p)| ((p.source, p.edges.clone()), i))
            .collect();
        let mut category =
            DeclaredFiniteCategory::new("complete finite acyclic free path category");
        for v in 0..vertices {
            category.add_identity(&format!("v{v}"), &format!("p{v}"));
        }
        for (i, p) in paths.iter().enumerate().skip(vertices) {
            category.add_morphism(
                &format!("p{i}"),
                &format!("v{}", p.source),
                &format!("v{}", p.target),
            );
        }
        let mut composition = vec![vec![None; paths.len()]; paths.len()];
        for (i, p) in paths.iter().enumerate() {
            for (j, q) in paths.iter().enumerate() {
                if p.target != q.source {
                    continue;
                }
                let mut word = p.edges.clone();
                word.extend_from_slice(&q.edges);
                let k = *indices
                    .get(&(p.source, word))
                    .ok_or(PathError::MissingComposite)?;
                composition[i][j] = Some(k);
                category.set_composition(&format!("p{i}"), &format!("p{j}"), &format!("p{k}"));
            }
        }
        let category = ValidatedFiniteCategory::try_new(category)
            .map_err(|_| PathError::CategoryValidation)?;
        Ok(Self {
            vertices,
            edges,
            paths,
            composition,
            category,
        })
    }
    pub fn vertices(&self) -> usize {
        self.vertices
    }
    pub fn edges(&self) -> &[PathEdge] {
        &self.edges
    }
    pub fn paths(&self) -> &[FinitePath] {
        &self.paths
    }
    pub fn category(&self) -> &ValidatedFiniteCategory {
        &self.category
    }
    pub fn path(&self, index: usize) -> Result<&FinitePath, PathError> {
        self.paths.get(index).ok_or(PathError::UnknownPath)
    }
    pub fn compose(&self, first: usize, second: usize) -> Result<Option<usize>, PathError> {
        self.composition
            .get(first)
            .and_then(|row| row.get(second))
            .copied()
            .ok_or(PathError::UnknownPath)
    }
    pub fn edge_path(&self, edge: usize) -> Result<usize, PathError> {
        if edge >= self.edges.len() {
            return Err(PathError::UnknownPath);
        }
        self.paths
            .iter()
            .position(|p| p.edges == [edge])
            .ok_or(PathError::MissingComposite)
    }
    pub fn origin_path_counts(&self) -> Vec<usize> {
        let mut counts = vec![0; self.vertices];
        for p in &self.paths {
            counts[p.source] += 1;
        }
        counts
    }
}
