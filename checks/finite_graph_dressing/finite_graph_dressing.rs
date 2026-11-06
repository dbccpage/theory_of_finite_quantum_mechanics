//! Exact finite permutation witness for TFQ-0397/0398. AuthorityEffect: None.
//! Compile independently: rustc --edition=2021 --test finite_graph_dressing.rs.
//! The arbitrary-group theorem is in lean4/FiniteGraphDressing.lean.
use std::collections::VecDeque;

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Perm(Vec<usize>);

impl Perm {
    pub fn new(image: Vec<usize>) -> Result<Self, &'static str> {
        let mut sorted = image.clone();
        sorted.sort_unstable();
        if sorted != (0..image.len()).collect::<Vec<_>>() {
            return Err("not a permutation");
        }
        Ok(Self(image))
    }
    pub fn identity(degree: usize) -> Self { Self((0..degree).collect()) }
    pub fn compose(&self, other: &Self) -> Self {
        assert_eq!(self.0.len(), other.0.len(), "permutation degrees differ");
        Self(other.0.iter().map(|i| self.0[*i]).collect())
    }
    pub fn inverse(&self) -> Self {
        let mut out = vec![0; self.0.len()];
        for (i, j) in self.0.iter().enumerate() { out[*j] = i; }
        Self(out)
    }
}

#[derive(Clone)]
pub struct Edge { pub source: usize, pub target: usize, pub value: Perm }

pub struct Dressing {
    pub transports: Vec<Perm>,
    pub roots: Vec<usize>,
    pub tree_edges: Vec<usize>,
    pub residuals: Vec<Perm>,
}

impl Dressing {
    pub fn neutralizes(&self) -> bool {
        self.residuals.iter().all(|p| *p == Perm::identity(p.0.len()))
    }
}

pub fn forest_dressing(n: usize, degree: usize, edges: &[Edge], order: &[usize])
    -> Result<Dressing, &'static str>
{
    let mut sorted = order.to_vec();
    sorted.sort_unstable();
    if sorted != (0..edges.len()).collect::<Vec<_>>() { return Err("invalid edge order"); }
    let mut adjacent = vec![Vec::<(usize, usize, Perm)>::new(); n];
    for &i in order {
        let e = &edges[i];
        if e.source >= n || e.target >= n || e.value.0.len() != degree {
            return Err("edge outside declared graph or group");
        }
        adjacent[e.source].push((i, e.target, e.value.clone()));
        adjacent[e.target].push((i, e.source, e.value.inverse()));
    }
    let mut transports = vec![None::<Perm>; n];
    let mut roots = vec![0; n];
    let mut tree_edges = Vec::new();
    for root in 0..n {
        if transports[root].is_some() { continue; }
        transports[root] = Some(Perm::identity(degree));
        roots[root] = root;
        let mut queue = VecDeque::from([root]);
        while let Some(source) = queue.pop_front() {
            for (i, target, value) in &adjacent[source] {
                if transports[*target].is_none() {
                    transports[*target] = Some(value.compose(transports[source].as_ref().unwrap()));
                    roots[*target] = root;
                    tree_edges.push(*i);
                    queue.push_back(*target);
                }
            }
        }
    }
    let transports: Vec<_> = transports.into_iter().map(Option::unwrap).collect();
    let residuals = edges.iter().map(|e|
        transports[e.target].inverse().compose(&e.value).compose(&transports[e.source])
    ).collect();
    Ok(Dressing { transports, roots, tree_edges, residuals })
}

#[cfg(test)]
mod tests {
    use super::*;
    fn s3() -> Vec<Perm> {
        vec![[0,1,2], [0,2,1], [1,0,2], [1,2,0], [2,0,1], [2,1,0]]
            .into_iter().map(|p| Perm::new(p.to_vec()).unwrap()).collect()
    }
    fn edge(s: usize, t: usize, p: &Perm) -> Edge {
        Edge { source: s, target: t, value: p.clone() }
    }
    #[test]
    fn all_216_s3_triangles_match_loop_and_exhaustive_gauge_search() {
        let group = s3();
        let one = Perm::identity(3);
        for a in &group { for b in &group { for c in &group {
            let edges = [edge(0,1,a), edge(1,2,b), edge(2,0,c)];
            let result = forest_dressing(3,3,&edges,&[0,1,2]).unwrap();
            let exists = group.iter().any(|x| group.iter().any(|y| {
                let g = [&one,x,y];
                edges.iter().all(|e| e.value == g[e.target].inverse().compose(g[e.source]))
            }));
            assert_eq!(result.neutralizes(), c.compose(b).compose(a) == one);
            assert_eq!(result.neutralizes(), exists);
            assert!(result.tree_edges.iter().all(|i| result.residuals[*i] == one));
        }}}
    }
    #[test]
    fn tree_change_and_noncommutative_gauge_covariance() {
        let group = s3();
        let a = &group[1]; let b = &group[2]; let one = Perm::identity(3);
        assert_ne!(a.compose(b), b.compose(a));
        let edges = [edge(0,1,a),edge(1,2,b),edge(2,0,&one),edge(0,2,a)];
        let first = forest_dressing(3,3,&edges,&[0,1,2,3]).unwrap();
        let second = forest_dressing(3,3,&edges,&[3,2,1,0]).unwrap();
        assert_ne!(first.tree_edges, second.tree_edges);
        let change: Vec<_> = second.transports.iter().zip(&first.transports)
            .map(|(y,x)| y.inverse().compose(x)).collect();
        for (i,e) in edges.iter().enumerate() {
            assert_eq!(second.residuals[i], change[e.target].compose(&first.residuals[i])
                .compose(&change[e.source].inverse()));
        }
        for x in &group { for y in &group { for z in &group {
            let g = [x,y,z];
            let transformed: Vec<_> = edges.iter().map(|e| edge(e.source,e.target,
                &g[e.target].compose(&e.value).compose(&g[e.source].inverse()))).collect();
            let result = forest_dressing(3,3,&transformed,&[0,1,2,3]).unwrap();
            for (i,r) in first.residuals.iter().enumerate() {
                assert_eq!(result.residuals[i], x.compose(r).compose(&x.inverse()));
            }
        }}}
    }
    #[test]
    fn disconnected_loops_parallel_edges_and_empty_graph() {
        let a = &s3()[1]; let one = Perm::identity(3);
        let edges = [edge(1,0,a),edge(1,0,a),edge(2,2,&one)];
        let r = forest_dressing(4,3,&edges,&[0,1,2]).unwrap();
        assert!(r.neutralizes()); assert_eq!(r.roots, vec![0,0,2,3]);
        assert_eq!(r.tree_edges.len(), 1);
        assert!(!forest_dressing(1,3,&[edge(0,0,a)],&[0]).unwrap().neutralizes());
        assert!(!forest_dressing(2,3,&[edge(0,1,a),edge(0,1,&one)],&[0,1]).unwrap().neutralizes());
        assert!(forest_dressing(0,3,&[],&[]).unwrap().neutralizes());
    }
    #[test]
    fn local_face_flatness_does_not_eliminate_a_second_cycle() {
        let one = Perm::identity(3); let a = &s3()[1];
        let edges = [edge(0,1,&one),edge(1,2,&one),edge(2,0,&one),edge(2,3,&one),edge(3,0,a)];
        assert!(!forest_dressing(4,3,&edges,&[0,1,2,3,4]).unwrap().neutralizes());
    }
    #[test]
    fn malformed_inputs_are_refused() {
        assert!(Perm::new(vec![0,0]).is_err());
        let e = [edge(0,1,&Perm::identity(3))];
        assert!(forest_dressing(1,3,&e,&[0]).is_err());
        assert!(forest_dressing(2,2,&e,&[0]).is_err());
        assert!(forest_dressing(2,3,&e,&[]).is_err());
        assert!(forest_dressing(2,3,&e,&[0,0]).is_err());
    }
}
